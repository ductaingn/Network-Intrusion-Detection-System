import json
from pyspark.sql.functions import udf
from pyspark.sql.types import MapType, StringType


def parse_json(value):
    '''
    Define a UDF to parse JSON
    '''
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return {}


def load_config(config_file):
    '''
    Load configurations
    '''
    with open(config_file, 'r') as file:
        return json.load(file)


def transform_data(decoded_data):
    parse_json_udf = udf(parse_json, MapType(StringType(), StringType()))
    return decoded_data.withColumn("parsed_value", parse_json_udf(decoded_data["value"]))


def output_results(processed_results):
    for key, output in processed_results:
        print(f"Key: {key}, Model Output: {output}")
