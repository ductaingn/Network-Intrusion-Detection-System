# Network Intrusion Detection System

## How to run

1. Change configs in
```
\client\configs.json
\server\configs.json
```

2. Start your Kafka server and create 2 brokers, one for sending network data and one for classified data (e.g: "test" and "testOutput")
```
cd ~/kafka/kafka_2.13-3.9.0/
bin/zookeeper-server-start.sh config/zookeeper.properties
bin/kafka-server-start.sh config/server.properties
bin/kafka-topics.sh --create --topic test --bootstrap-server <<YOUR IP ADDRESS>>:9092 
bin/kafka-topics.sh --create --topic testOutput --bootstrap-server <<YOUR IP ADDRESS>>:9092 
```

3. Start your Spark master and add a worker
```
cd ~/spark/spark-3.5.3-bin-hadoop3/sbin
start-master.sh --host <<YOUR IP ADDRESS>> --port 7077
start-worker.sh spark://<<YOUR IP ADDRESS>>:7077 
```
4. Run 
```
cd server/
python testSpark.py
cd client/
python main.py
```
