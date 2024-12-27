import json
import yaml
import torch
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import MapType, StringType
from model.Classifier import Classifier
from server.utillities import parse_json, load_config, transform_data, output_results


def preprocess(batch_data) -> list[torch.Tensor, list]:
    '''
    Preprocess raw data received from Kafka
    ---

    Data flow:
    > Kafka (key, value) pairs  -->  CICFlowmeter table  -->  torch.Tensor batch AND key mapping for data

    batch: torch.Tensor of shape [batch_size, feature_dim]
    mapping example:
    mapping = ['192.168.1.2', '192.168.2.1','192.168.1.2',...,'192.168.1.220] (len(mapping) = batch_size)
    '''
    batch = []
    mapping = []
    for row in batch_data:
        # Convert the parsed data to a suitable format for the CICFlowmeter

        # YOUR CODE HERE!

    return batch, mapping


def process_batch(model: Classifier, batch_df, batch_id):
    '''
    Pipeline
    '''
    batch_data = batch_df.collect()
    attack_prop = model(batch_data)
    prediction = model.get_class(attack_prop)
    output_results(prediction)


if __name__ == '__main__':
    config = load_config('configs.json')
    with open('server/model/model_configs.yaml', 'rb') as file:
        model_config = yaml.safe_load(file)

    # Kafka Configuration
    kafka_config = config["kafka"]
    spark_config = config['spark']

    # Create Spark Session
    spark_session = SparkSession.builder \
        .appName("KafkaTorchExample") \
        .config('spark.jars.packages', 'org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1') \
        .master(f"spark://{spark_config['master']}") \
        .getOrCreate()

    # Load the PyTorch model
    model = Classifier(
        model_config['input_dim'], model_config['output_dim'], model_config['mapper'])
    model.load_state_dict(torch.load("model/model.pth"))
    model.eval()  # Set model to evaluation mode

    # Read the Kafka stream
    df = spark_session.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", kafka_config['bootstrap_servers']) \
        .option("subscribe", kafka_config['topic']) \
        .load()

    decoded_data = df.selectExpr(
        "CAST(key AS STRING)", "CAST(value AS STRING)")
    transformed_data = transform_data(decoded_data)

    # Execute streaming query
    query = transformed_data.writeStream \
        .foreachBatch(process_batch) \
        .start()

    # Wait for the streaming to finish
    query.awaitTermination()
