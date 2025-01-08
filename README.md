# Network Intrusion Detection System

## How to run

To configure Kafka so that two brokers on different machines share the same topic, you need to set up a **Kafka cluster**, follow this instruction

---

### Steps to Configure Kafka Cluster

1. **Install Kafka on Both Machines**  
   Ensure Kafka is installed and running on both machines. You will need the Kafka broker's configuration file (commonly named `server.properties`) on both systems.

---

2. **Configure `server.properties` on Each Machine**  
   Each Kafka broker requires a unique **broker ID**, and all brokers in the cluster need to share the same **Zookeeper ensemble** or **KRaft (Kafka Raft)** configuration.

   Update the following in `server.properties` for each broker:

   - **Broker ID**:  
     This must be unique for each broker in the cluster.  
     ```
     broker.id=1   # Set 1 for the first machine
     ```
     On the second machine:
     ```
     broker.id=2   # Set 2 for the second machine
     ```

   - **Advertised Listeners**:  
     Configure `advertised.listeners` to let other brokers and clients connect. Use the machine's hostname or IP.  
     ```
     advertised.listeners=PLAINTEXT://<IP>:9092
     ```
     Example for the first machine:
     ```
     advertised.listeners=PLAINTEXT://192.168.1.101:9092
     ```
     Example for the second machine:
     ```
     advertised.listeners=PLAINTEXT://192.168.1.102:9092
     ```

   - **Log Directory**:  
     Ensure the `log.dirs` path is valid and unique for each machine:
     ```
     log.dirs=/tmp/kafka-logs
     ```

   - **Zookeeper Connection (Optional if Using Zookeeper)**:  
     Specify the Zookeeper ensemble's connection string, listing all Zookeeper servers:  
     ```
     zookeeper.connect=192.168.1.100:2181,192.168.1.101:2181,192.168.1.102:2181
     ```
     If you are not using Zookeeper (e.g., using KRaft), ensure KRaft configurations are consistent across brokers.

---

3. **Set Up Zookeeper (Optional)**  
   If you're using Zookeeper as the Kafka metadata manager, you need to set up Zookeeper on one or more machines and configure the `zookeeper.connect` property in `server.properties` as shown above.

   For simplicity, you can run Zookeeper on one of the machines and specify its IP in `zookeeper.connect`.

   Alternatively, for a production-ready cluster, deploy a Zookeeper ensemble on three or more machines.

---

4. **Start Kafka Brokers**  
   Start the Kafka brokers on both machines using their respective configuration files. Ensure the two brokers are aware of each other through the Zookeeper or KRaft configuration.

---

5. **Create a Shared Topic**  
   Once both brokers are running, use the Kafka CLI to create a topic that will be shared between the brokers.

   Example:
   ```bash
   bin/kafka-topics.sh --create \
   --topic shared-topic \
   --partitions 3 \
   --replication-factor 2 \
   --bootstrap-server 192.168.1.101:9092,192.168.1.102:9092
   ```

   - `--partitions`: Number of partitions for the topic.
   - `--replication-factor`: Set this to the number of brokers in your cluster (or less if desired).

   This ensures that the topic is replicated across both brokers.

---

6. **Verify the Cluster**  
   You can verify that the topic is shared between brokers by describing the topic:

   ```bash
   bin/kafka-topics.sh --describe \
   --topic shared-topic \
   --bootstrap-server 192.168.1.101:9092
   ```

   You should see details about the topic partitions and their replication across brokers.

---

### Key Points
- **Replication**: Kafka automatically replicates topic partitions across brokers based on the `replication-factor`.
- **Leader Election**: Each partition of a topic has a "leader" broker that handles writes and reads. Other brokers act as followers for that partition.
- **High Availability**: If one broker goes down, Kafka ensures the topic is still available via the other broker.

---

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
