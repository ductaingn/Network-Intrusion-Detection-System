from pyspark.sql import SparkSession
import pyspark as spark

# Kafka Configuration
KAFKA_HOST = 'localhost'
KAFKA_BROKER1_PORT = '9092'
KAFKA_TOPIC = 'quickstart-events'

# Create Spark Session
spark = SparkSession.builder \
    .appName("KafkaStreamExample") \
    .config('spark.jars.packages', 'org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1') \
    .master("spark://nguyen-Lenovo-ThinkBook-14p-Gen-2:7077") \
    .getOrCreate()

# Read the Kafka stream
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", f"{KAFKA_HOST}:{KAFKA_BROKER1_PORT}") \
    .option("subscribe", KAFKA_TOPIC) \
    .load()

# Select the key and value (in Kafka, they are stored as binary, so cast to string)
kafka_data = df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

# Output the stream to the console for debugging
query = kafka_data.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

# Wait for the streaming to finish
query.awaitTermination()
