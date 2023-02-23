# velib-prj
School project about Paris Velib's data.

## Run the project : 
### Requirements :
- Install Java JDK 11
- Download [Kafka & Zookeeper](https://kafka.apache.org/downloads)

Or
- Download docker

## Procedure docker
1. Start kafka and zookeeper./:
> `docker-compose up -d`

2. Start Spark Structured Streaming app: 
> `cd 'spark struct str'/`
> `python main.py`

3. Start kafka app:
> `cd kafka/`
> `python consumer.py` 

and

> `python producer.py` 

## Procedure standalone
1. In two separate terminals, launch Zookeeper :
> `kafka_2.13-3.0.0/bin/zookeeper-server-start.sh kafka_2.13-3.0.0/config/zookeeper.properties`

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;and launch Kafka :

> `kafka_2.13-3.0.0/bin/kafka-server-start.sh kafka_2.13-3.0.0/config/server.properties`

2. Add following line to ~/.zshrc :

>`export PATH="$PATH:/Users/nicolas/Downloads/kafka_2.13-3.3.2/bin/"`

3. Create a new Kafka topic:

> `kafka-topics.sh --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1 --create --topic test1`

4. Start Spark Structured Streaming app: 
> `cd 'spark struct str'/`
> `python main.py`

5. Start kafka app:
> `cd kafka/`
> `python producer.py`

## Docs
In the doc/ folder, an XML explains the architecture of the app, from getting data to ML predictions and data researching.<br>
In the doc/notebooks, [Jupyter notebooks](https://jupyter.org) will explain certain of our researchs.
