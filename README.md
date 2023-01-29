# velib-prj
School project about Paris Velib's data.

## Run the project : 
### Requirements :
- Install Java JDK 11
- Download [Kafka & Zookeeper](https://kafka.apache.org/downloads)

## Procedure
1. In two separate terminals, launch Zookeeper :
> `kafka_2.13-3.0.0/bin/zookeeper-server-start.sh kafka_2.13-3.0.0/config/zookeeper.properties`

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;and launch Kafka :

> `kafka_2.13-3.0.0/bin/kafka-server-start.sh kafka_2.13-3.0.0/config/server.properties`

2. Add following line to ~/.zshrc :

>`export PATH="$PATH:/Users/nicolas/Downloads/kafka_2.13-3.3.2/bin/"`

3. Create a new Kafka topic:

> `kafka-topics.sh --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1 --create --topic test1`

4. In two separate terminals, launch Kafka consumer :
> `python3 kafka/consumer.py`

5. and launch Kafka producer :
> `python3 kafka/producer.py`

## Docs
In the doc/ folder, an XML explains the possible architecture for the app, from getting data to ML predictions.
