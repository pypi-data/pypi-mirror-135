# badook tests python SDK

## Setup

### Prerequisites

Current version supports Python 3.7 only

### Installation
To install badook from pip use:

```
python -m pip install badook-tests
```

## Running the example localy

To run using a local server first set the local address correctly in the `config\badook.yaml` file under the `data_cluster_url` entry.
Next run the example using the following command:

```{python}
python examples/test_dsl_example.py
```
