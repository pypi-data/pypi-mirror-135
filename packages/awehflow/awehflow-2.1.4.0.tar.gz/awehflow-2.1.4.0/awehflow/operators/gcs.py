from typing import Iterable
from airflow.contrib.hooks.gcs_hook import GoogleCloudStorageHook as GCSHook
from airflow.providers.google.cloud.hooks.bigquery import BigQueryHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from pathlib import Path
from datetime import datetime as dt
from random import randint


class BigQueryCSVExtractAndComposeOperator(BaseOperator):
    """
    Uses Google Cloud Storage compose to extract a BigQuery table to a single CSV single file
    """

    template_fields = (
        'source_project',
        'source_dataset',
        'source_table',
        'destination_object_name',
        'temp_bucket_name', 
        'temp_dataset_name', )

    @apply_defaults
    def __init__(self,
                 source_project: str,
                 source_dataset: str,
                 source_table: str,
                 destination_object_name: str,
                 temp_bucket_name: str,
                 temp_dataset_name: str,
                 print_header: bool = True,
                 field_delimiter: str = ',',
                 bigquery_conn_id: str = 'bigquery_default',
                 gcp_conn_id: str = 'gcp_conn_id',
                 location=None,
                 *args, **kwargs) -> None:
        """
        Create an instance of the BigQueryCSVExtractAndComposeOperator
        :param source_dataset_table: The source BigQuery table to extract, including the data set and table name ie. dev_temp.some_table_to_extract
        :param destination_object_name: The destination filename as a bucket URI ie gs://dev_extract_data/some_sub_folder/my_extract.csv
        :param temp_bucket_name: The temporary bucket area where files can be extracted and composed
        :param temp_dataset_name: A temp dataset where temporary tables can be created and saved, while processing
        :param print_header: Whether or not the extracted data should contain a header or not
        :param field_delimiter: What kind of field delimiter to use. Default: ,
        :param bigquery_conn_id: The name of the google_cloud_platform connection to use for queries.  The user should have R/W permission to the temp dataset
        :param gcp_conn_id: The name of the google_cloud_platform connection to use for GCS jobs.  The connection should have R/W permission to the destination bucket and temp bucket
        :param args:
        :param kwargs:
        """
        super().__init__(*args, **kwargs)

        self.source_project = source_project
        self.source_dataset = source_dataset
        self.source_table = source_table
        self.destination_object_name = destination_object_name
        self.temp_bucket_name = temp_bucket_name.strip('/')
        self.temp_dataset_name = temp_dataset_name
        self.print_header = print_header
        self.field_delimiter = field_delimiter
        self.bigquery_conn_id = bigquery_conn_id
        self.gcp_conn_id = gcp_conn_id
        self.location = location

        # place holders for execute method
        self.gcs_hook = None
        self.bq_hook = None

    def execute(self, context):
        """
        Execute the BigQueryCSVExtractAndComposeOperator to extract a biq query table to a bucket and then compose the parts into a single CSV file
        :param context: The airflow context to execute on
        :return:
        """

        if self.gcs_hook is None:
            self.log.info('Creating GCSHook')
            self.gcs_hook = GCSHook(gcp_conn_id=self.gcp_conn_id)

        if self.bq_hook is None:
            self.log.info('Creating BigQueryHook')
            client = BigQueryHook(gcp_conn_id=self.bigquery_conn_id, location=self.location)
            self.bq_hook = client

        compose_bucket_name, compose_filename = self.get_bucket_and_filename(object_name=self.destination_object_name)
        self.log.info('Calculated final compose_bucket_name [{}] and compose_filename [{}]'.format(compose_bucket_name, compose_filename))

        working_bucket_name, junk_data = self.get_bucket_and_filename(object_name=self.temp_bucket_name + '/junk.dat')
        self.log.info('Calculated working_bucket_name: {}'.format(working_bucket_name))

        tmp_file_uniq = 'data_extract_tmp_' + dt.now().strftime('%Y%m%H%M%S') + '_' + str(randint(1, 100))
        tmp_parts_name = tmp_file_uniq + '_*.csv'
        tmp_compose_file = 'composed_data_' + tmp_file_uniq + '.csv'

        try:
            if self.print_header:
                self.log.info('Header requested so generating header tbl and file')

                tmp_header_filename = self.temp_bucket_name + '/_header_' + tmp_file_uniq + '_*.csv'
                tmp_header_table_name = '{}.{}_header_data'.format(self.temp_dataset_name, tmp_file_uniq)

                self.log.info('Defined tmp_header_filename [{}] and tmp_header_table_name [{}]'.format(tmp_header_filename, tmp_header_table_name))
                self.log.info('Creating empty header table [{}]'.format(tmp_header_table_name))

                header_table_created = False

                try:
                    self.bq_hook.run_query(
                        sql=f'SELECT * FROM `{self.source_project}.{self.source_dataset}.{self.source_table}` WHERE 1=0 LIMIT 1',
                        destination_dataset_table=tmp_header_table_name,
                        write_disposition='WRITE_TRUNCATE',
                        use_legacy_sql=False,
                        location=self.location
                    )

                    header_table_created = True

                    self.log.info('Exporting header table [{}] to file [{}]'.format(tmp_header_table_name, tmp_header_filename))

                    self.bq_hook.run_extract(
                        source_project_dataset_table=tmp_header_table_name,
                        destination_cloud_storage_uris='gs://{bucket}/{header}'.format(bucket=working_bucket_name, header=tmp_header_filename),
                        print_header=True,
                        field_delimiter=self.field_delimiter)
                    self.log.info('Completed export of header table data')
                finally:
                    if header_table_created:
                        self.bq_hook.delete_table(table_id=f'{self.source_project}.{tmp_header_table_name}', not_found_ok=True)

            self.log.info("Extracting table data to tmp_parts_name [{}]".format(tmp_parts_name))
            self.bq_hook.run_extract(
                source_project_dataset_table=f'{self.source_project}:{self.source_dataset}.{self.source_table}',
                destination_cloud_storage_uris='gs://{bucket}/{data}'.format(bucket=working_bucket_name, data=tmp_parts_name),
                print_header=False,
                field_delimiter=self.field_delimiter
            )

            self.log.info('Completed extraction of primary table')
            self.log.info('Listing file parts matching [{}] to compose'.format(tmp_file_uniq))

            source_list = self.list_extract_files(working_bucket_name, tmp_file_uniq)
            self.log.info('Composing tmp_compose_file from source_list')
            self.log.info('source_list: {}'.format(source_list))
            self.log.info('-->')
            self.log.info('tmp_compose_file: {}'.format(tmp_compose_file))

            self.gcs_hook.compose(working_bucket_name,
                         source_objects=source_list,
                         destination_object=tmp_compose_file
                )

            self.log.info('Copying tmp_compose_file [{}/{}] to final compose_filename [{}/{}]'.format(
                self.temp_bucket_name,
                tmp_compose_file,
                compose_bucket_name,
                compose_filename
            ))

            self.gcs_hook.copy(source_bucket=working_bucket_name, source_object=tmp_compose_file,
                               destination_bucket=compose_bucket_name,
                               destination_object=compose_filename)

            self.log.info('Completed header-less extract & compose')
        finally:
            self.log.info('Deleting temp files created in [{}] during export process'.format(working_bucket_name))
            source_list = self.list_extract_files(bucket_name=working_bucket_name, file_pattern=tmp_file_uniq)
            for src in source_list:
                self.log.info('Deleting file [{}]'.format(src))
                self.gcs_hook.delete(working_bucket_name, src) # pragma: no cover

    def get_bucket_and_filename(self, object_name):
        """
        Split the gs:// URI for the destination object to a bucket_name and file_name
        :param object_name: The cloud storage URI
        :return: a tuple containing two variables, the bucket_name and the file_name component
        """
        bucket_path = Path(object_name.replace('gs:/', ''))
        bucket_name = str(bucket_path.parent).split('/')[1]
        dest_filename = object_name.replace('gs://' + bucket_name + '/', '')
        return bucket_name, dest_filename

    def list_extract_files(self, bucket_name, file_pattern):
        source_list = []

        file_list = self.gcs_hook.list(bucket_name)
        for filename in file_list:

            if file_pattern in str(filename):
                self.log.info('Found tmp file [{}], adding to source list'.format(filename))
                source_list.append(filename)

        return source_list

