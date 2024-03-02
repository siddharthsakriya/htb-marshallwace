# Description: This file contains the tasks for the stream processor.
from Kafka import Data_source

# ===== KAFKA STREAM PROCESSOR TASKS =====
def data_source_task():
    """
    Data source task:

    This task takes data from the data source and ingests it into the system. 
    Currently we are using Apache Kafka.
    """
    return data_process_task()


# ===== FLINK STREAM PROCESSOR TASKS =====
def data_process_task(data):
    """
    Data processing task:

    This task takes data from the data source and processes it.
    Currently we are using Apache Flink/storm.
    """
    return state_management_task(data)


def state_management_task(data):
    """
    State management task:

    This task manages the state of the system.
    Currently we are not doing anything here.
    """
    return data_windowing_task(data)


def data_windowing_task(data):
    """
    Data windowing task:

    This task takes data from the data source and windows it and performs time series analysis.
    Currently this is done using numpy and pandas.
    """
    return data_sink_task(data)



def data_sink_task(data):
    """
    Data sink task:

    This task takes data from the data source and outputs it to the data sink.
    Currently we are sending data to a webapp (maybe a database with data lake architecture in the future?)
    """
    pass
