# stream_processor/tasks.py

from celery import shared_task

"""
EXAMPLE FOR DEVS:

@periodic_task(run_every=timedelta(seconds=10))
def foo():
    print('Hello, world!')

# This will print 'Hello, world!' every 10 seconds.

@shared_task
def add(x, y):
    return x + y

# This will return the sum of x and y.

"""

@shared_task
def data_ingestion_task(data):
    """
    Data ingestion task:

    This task takes data from the data source and ingests it into the system. 
    Currently we are using Apache Kafka.
    """
    return data_process_task(data)

@shared_task
def data_process_task(data):
    """
    Data processing task:

    This task takes data from the data source and processes it.
    Currently we are using Apache Flink/storm.
    """
    return state_management_task(data)

@shared_task
def state_management_task(data):
    """
    State management task:

    This task manages the state of the system.
    Currently we are not doing anything here.
    """
    return data_windowing_task(data)

@shared_task
def data_windowing_task(data):
    """
    Data windowing task:

    This task takes data from the data source and windows it and performs time series analysis.
    Currently this is done using numpy and pandas.
    """
    return data_output_task(data)

@shared_task
def data_output_task(data):
    """
    Data output task:

    This task takes data from the data source and outputs it to the data sink.
    Currently we are sending data to a webapp (maybe a database with data lake architecture in the future?)
    """
    pass
