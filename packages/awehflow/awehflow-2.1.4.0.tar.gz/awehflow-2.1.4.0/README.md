# Awehflow

![coverage report](https://gitlab.com/spatialedge/awehflow/badges/master/coverage.svg)
![pipeline status](https://gitlab.com/spatialedge/awehflow/badges/master/pipeline.svg)

Configuration based Airflow pipelines with metric logging and alerting out the box.

## Prerequisites

You will need the following to run this code:
  * Python 3

## Installation

```
pip install awehflow[default]
```

If you are installing on Google Cloud Composer with Airflow 1.10.2:

```
pip install awehflow[composer]
```

## Usage

Usage of `awehflow` can be broken up into two parts: bootstrapping and configuration of pipelines

### Bootstrap

In order to expose the generated pipelines (`airflow` _DAGs_) for `airflow` to pick up when scanning for _DAGs_, one has to create a `DagLoader` that points to a folder where the pipeline configuration files will be located:

```python
import os

from awehflow.alerts.slack import SlackAlerter
from awehflow.core import DagLoader
from awehflow.events.postgres import PostgresMetricsEventHandler

"""airflow doesn't pick up DAGs in files unless 
the words 'airflow' and 'DAG' features"""

configs_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'configs')

metrics_handler = PostgresMetricsEventHandler(jobs_table='jobs', task_metrics_table='task_metrics')

slack_alerter = SlackAlerter(channel='#airflow')

loader = DagLoader(
    project="awehflow-demo",
    configs_path=configs_path,
    event_handlers=[metrics_handler],
    alerters=[slack_alerter]
)

dags = loader.load(global_symbol_table=globals())
```

As seen in the code snippet, one can also pass in _"event handlers"_ and _"alerters"_ to perform actions on certain pipeline events and potentially alert the user of certain events on a given channel. See the sections below for more detail.
The global symbol table needs to be passed to the `loader` since `airflow` scans it for objects of type `DAG`, and then synchronises the state with its own internal state store.

\*_caveat_: `airflow` ignores `python` files that don't contain the words _"airflow"_ and _"DAG"_. It is thus advised to put those words in a comment to ensure the generated _DAGs_ get picked up when the `DagBag` is getting filled.

#### Event Handlers

As a pipeline generated using `awehflow` is running, certain events get emitted. An event handler gives the user the option of running code when these events occur.

The following events are (potentially) potentially emitted as a pipeline runs:

* `start`
* `success`
* `failure`
* `task_metric`

Existing event handlers include:

* `PostgresMetricsEventHandler`: persists pipeline metrics to a Postgres database
* `PublishToGooglePubSubEventHandler`: events get passed straight to a Google Pub/Sub topic

An `AlertsEventHandler` gets automatically added to a pipeline. Events get passed along to registered alerters.

#### Alerters

An `Alerter` is merely a class that implements an `alert` method. The following alerters are currently available:

* `SlackAlerter`

###

## Running the tests

Tests may be run with
```bash
python -m unittest discover tests
```

or to run code coverage too:

```bash
coverage run -m unittest discover tests && coverage html
```

