# velib-prj
School project about Paris Velib's data.

## Run the project : 
### Requirements :
- Java JDK 11
- [Kafka & Zookeeper](https://kafka.apache.org/downloads)
- MongoDB
- Python 3.X
- Pip 21.X or greater

Or
- Docker compose 2.X
- Python 3.X
- pip 21.X or greater

## Docker procedure
1. Start kafka, zookeeper and a MongoDB server:
> `docker-compose up -d`

2. Install python packages:
> `pip install -r ./requirements.txt`

3. Start Spark Structured Streaming app: 
> `cd 'spark struct str'/`
> `python main.py`

4. Start kafka consumer:
> `cd kafka/`
> `python consumer.py` 

5. Start kafka producer:
> `cd kafka/`
> `python producer.py` 

By default, the docker compose creates a MongoDB server which is exposed on port 27017, you can change this in `docker-compose.yml`. Don't forget to modify the MongoDB connection string in `kafka/utils/envs.py`.

## Standalone procedure
1. In two separate terminals, launch Zookeeper :
> `kafka_2.13-3.0.0/bin/zookeeper-server-start.sh kafka_2.13-3.0.0/config/zookeeper.properties`

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;and launch Kafka :
> `kafka_2.13-3.0.0/bin/kafka-server-start.sh kafka_2.13-3.0.0/config/server.properties`

2. Add following line to ~/.zshrc :
>`export PATH="$PATH:/Users/nicolas/Downloads/kafka_2.13-3.3.2/bin/"`

3. Create a new Kafka topic:
> `kafka-topics.sh --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1 --create --topic test1`

4. Start a MongoDB server. Don't forget to modify the MongoDB connection string in `kafka/utils/envs.py`

5. Install python packages:
> `pip install -r ./requirements.txt`

6. Start Spark Structured Streaming app: 
> `cd 'spark struct str'/`
> `python main.py`

7. Start kafka app:
> `cd kafka/`
> `python producer.py`

## Docs
In the doc/ folder, an XML explains the architecture of the app, from getting data to ML predictions and data researching.<br>
In the doc/notebooks, [Jupyter notebooks](https://jupyter.org) will explain certain of our researchs.
