# Transform Airflow

## Install:
```bash
pip install transform-airflow
```

## Available Operators:
- MaterializeOperator
  - materialization_name: str
  - start_time: Optional[str]
  - end_time: Optional[str]
  - model_key_id: Optional[int]=None
  - output_table: Optional[str]=None
  - force: bool=False


## Creating DAG:
```python
from transform_airflow.operators import MaterializeOperator

# Init DAG
my_dag = DAG("my_dag_name")


# Associate task with DAG
op = MaterializeOperator(
  task_id=task_id,
  materialization_name="test",
  start_time="2021-01-01",
  end_time="2021-01-10",
)

# Perform any dependency structuring on tasks
```