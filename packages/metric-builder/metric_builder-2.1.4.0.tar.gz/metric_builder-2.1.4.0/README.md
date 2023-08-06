# Metric Builder

Utility for building templated metric extraction queries that can be traversed through time.

## Prerequisites

You will need the following to run this code:
  * Python 3
  
## Installation

To be determined...

## Usage

In order to extract a given metric, a `Metric` object needs to be instantiated:

```python
metric = Metric(
    query="""
        SELECT count(*) AS total
        FROM `project.dataset.table`
        WHERE DATETIME_TRUNC(created_datetime, DAY) = '{{ reference_time | format_date('%Y-%m-%d') }}'
    """,
    reader = BigQueryReader(json_credentials_path='/path/to/creds.json')
)
```

The `query` parameter is a templated query where you can format the `reference_time` `datetime` object to the required format using template filters.

The `reader` parameter is the object that is actually going to connect to the desired database and perform the queries.

The `metric` object can now be used to fetch metrics for a given point in time as follows:

```python
result = metric.fetch(reference_time=datetime.date(2019, 10, 21))
```

The result is returned as a list of dictionaries.

### Template filters

[Jinja2](https://jinja.palletsprojects.com/en/2.10.x/) is used as the templating engine. All built in Jinja filters are thus available. Relevant custom template filters have been added though for convenience:

#### format_date

Specify format of datetime:

```
'{{ reference_time | format_date('%Y-%m-%d') }}'
```

#### day_delta

Change a given datetime object by a specified number of days:

```
'{{ reference_time | day_delta(-7) | format_date('%Y-%m-%d') }}'
```

### Readers

Any reader will implement the following method that is used to execute queries:

```python
def execute(self, query) -> List[Dict[str, Any]]:
    ...
```

#### BigQueryReader

The underlying client is required to be authenticated with the necessary priviledges to read from the requested BigQuery tables.

If you authenticate with:

```bash
gcloud auth login
```

or

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/keyfile.json"
```

then you can just instantiate your `Reader` like this:

```python
reader = BigQueryReader()
```

The other option is to explicitly authenticate with a service account key file:

```python
reader = BigQueryReader(json_credentials_path='/path/to/creds.json')
```

#### HiveReader

Coming soon...