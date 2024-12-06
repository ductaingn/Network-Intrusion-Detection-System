from hdfs import InsecureClient

client = InsecureClient('http://192.168.90.20:50070', user='hadoop')

hdfs_file = '/user/hadoop/test/testing.csv'
local_path = '/home/nguyen/Downloads/testing.csv'

client.download(hdfs_path=hdfs_file, local_path=local_path)
