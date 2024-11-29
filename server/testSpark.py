import json
from pyspark.sql import SparkSession
import torch
import pyspark as spark


def load_config(config_file):
    with open(config_file, 'r') as file:
        return json.load(file)


if __name__ == '__main__':
    config = load_config('configs.json')

    # Kafka Configuration
    kafka_config = config["kafka"]
    spark_config = config['spark']

    # Create Spark Session
    spark_session = SparkSession.builder \
        .appName("KafkaStreamExample") \
        .config('spark.jars.packages', 'org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1') \
        .master(f"spark://{spark_config['master']}") \
        .getOrCreate()

    # Read the Kafka stream
    df = spark_session.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", kafka_config['bootstrap_servers']) \
        .option("subscribe", kafka_config['topic']) \
        .load()

    # Select the key and value (in Kafka, they are stored as binary, so cast to string)
    kafka_data = df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

    # Output the stream to the console for debugging
    query = kafka_data.writeStream \
        .outputMode("append") \
        .format("console") \
        .start()
    model = torch.nn.Linear(1, 2)
    output = model(kafka_data)
    # Wait for the streaming to finish
    query.awaitTermination()
