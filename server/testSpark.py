import json
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType
from model.Classifier import Classifier
import torch
import pandas as pd
import os
import utillities as utillities
import sys
import yaml
sys.path.append("/home/nguyen/Projects/Big Data Storage and Processing/Source Code/server/utillities.py")

try:
    from pyspark import SparkContext
    from pyspark import SparkConf

    print ("success")

except ImportError as e:
    print ("error importing spark modules", e)
    sys.exit(1)
# Set Hadoop user name
os.environ['HADOOP_USER_NAME'] = 'hadoop'

def process(batch_df, batch_id, model):
    '''
    Function to process each micro-batch
    '''
    if batch_df.isEmpty():
        print(f"Batch {batch_id} is empty.")
        return
    
    # Convert Spark DataFrame to pandas DataFrame
    pandas_df:pd.DataFrame = batch_df.toPandas()
    pandas_df = pandas_df.drop(['key'],axis=1)

    # Function to remove brackets and convert to integer
    pandas_df.to_csv('df.csv')
    def clean_value(value):
        if value is not None: # cwe_flag_count column
            return float(value.strip('[""]'))
        else:
            return 0 # cwe_flag_count isn't produced by your Producer or PacketAnalyzer

    # Apply the function to all columns
    pandas_df = pandas_df.map(clean_value)
    # pandas_df.to_csv('df.csv')

    x = torch.tensor(pandas_df.astype(float).values, dtype=torch.float32).view(-1, 52)
    out = model(x)
    return out

# Function to load configuration from a file
def load_config(config_file):
    with open(config_file, 'r') as file:
        if config_file.split('.')[-1] == 'json':
            return json.load(file)
        else:
            return yaml.safe_load(file)

# Main execution
if __name__ == '__main__':
    config = load_config('configs.json')

    # Kafka and Spark Configuration
    kafka_config = config["kafka"]
    spark_config = config['spark']
    hadoop_config = config['hadoop']

    # Classifier Configuration
    model_config = load_config('model/model_configs.yaml')
    attributes = model_config['attributes']
    
    # Define the schema of the JSON data
    schema = StructType([StructField(attr, StringType(), True) for attr in attributes])

    # Create a SparkSession
    spark_session = SparkSession.builder \
        .appName("KafkaStreamExample") \
        .config('spark.jars.packages', 'org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1') \
        .master(f"spark://{spark_config['master']}") \
        .getOrCreate()
    # spark_session.sparkContext.addPyFile("idspython.py")

    # Read the Kafka stream
    df = spark_session.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", kafka_config['bootstrap_servers']) \
        .option("subscribe", kafka_config['topic']) \
        .load()

    # Parse the value column as JSON
    kafka_data = df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)") \
                   .withColumn("json_data", from_json(col("value"), schema)) \
                   .select("key", "json_data.*")

    # Define a PyTorch model
    model = Classifier(
        model_config['architecture']['input_dim'], model_config['architecture']['output_dim'], model_config['mapper'],
        model_config['learning_rate'])
    model.load_state_dict(torch.load("model/model.pth")['model_state_dict'])
    model.eval() 

    # Write the stream using foreachBatch
    query = kafka_data.writeStream \
        .outputMode("append") \
        .format("console") \
        .foreachBatch(lambda batch_df, batch_id: process(batch_df, batch_id, model)) \
        .start()

    # Await termination of the stream
    query.awaitTermination()


    # Write to HDFS
    # query = kafka_data.writeStream \
    #     .outputMode("append") \
    #     .format("csv")  \
    #     .option("path", f'hdfs://{hadoop_config['hdfs_server']}/{hadoop_config['write_location']}') \
    #     .option("checkpointLocation", f'hdfs://{hadoop_config['hdfs_server']}/{hadoop_config['checkpoint_location']}') \
    #     .start()

    query.awaitTermination()
