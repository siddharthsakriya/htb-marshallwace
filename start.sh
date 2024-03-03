#!/bin/bash

# Start of the docker-compose.yml file
echo "version: '3'
services:" > docker-compose.yml

# Configuration file containing your JSON
CONFIG_FILE="kafka-server/scalability.conf"

# Counter for service names
COUNTER=1

# install jq using apt get on linux or brew on mac (silent install)
if [ "$(uname)" == "Darwin" ]; then
    brew install jq > /dev/null
else
    sudo apt-get install jq -y > /dev/null
fi

echo """
# ==== Kafka Services ====
  zookeeper:
    restart: always
    image: docker.io/bitnami/zookeeper:3.8
    ports:
      - "2181:2181"
    volumes:
      - "zookeeper-volume:/bitnami"
    environment:
      - ALLOW_ANONYMOUS_LOGIN=yes
    networks:
      - pipeline-network

  kafka:
    container_name: kafka
    restart: always
    image: docker.io/bitnami/kafka:3.3
    ports:
      - "9093:9093"
    volumes:
      - "kafka-volume:/bitnami"
    environment:
      - KAFKA_BROKER_ID=1
      - KAFKA_CFG_ZOOKEEPER_CONNECT=zookeeper:2181
      - ALLOW_PLAINTEXT_LISTENER=yes
      - KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP=CLIENT:PLAINTEXT,EXTERNAL:PLAINTEXT
      - KAFKA_CFG_LISTENERS=CLIENT://:9092,EXTERNAL://:9093
      - KAFKA_CFG_ADVERTISED_LISTENERS=CLIENT://kafka:9092,EXTERNAL://localhost:9093
      - KAFKA_CFG_INTER_BROKER_LISTENER_NAME=CLIENT
      - KAFKA_CFG_MESSAGE_MAX_BYTES=20000000
    networks:
      - pipeline-network
    depends_on:
      - zookeeper

  kafka-ui:
    restart: always
    image: provectuslabs/kafka-ui:latest
    ports:
      - "8083:8080"
    environment:
      - DYNAMIC_CONFIG_ENABLED=true
      - KAFKA_CLUSTERS_0_NAME=pipeline_pundits
      - KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS=kafka:9092
    networks:
      - pipeline-network
    depends_on:
      - kafka
  
  # ==== ticker Services ====
""" >> docker-compose.yml


# Read tickers array from the config file using jq
TICKERS=$(jq -r '.tickers[]' "$CONFIG_FILE")

for line in $TICKERS
do
    # Append a service entry for each ticker
    echo "  ticker_$COUNTER:
    build: kafka-server
    container_name: ticker_$COUNTER
    networks:
      - pipeline-network
    command: sh -c \"python3 kafka_launcher.py\"
    environment:
      - KAFKA_BROKER_SERVER=kafka:9092
      - TICKER=$line" >> docker-compose.yml
    ((COUNTER++))
done

# add the rest of the docker-compose.yml file
echo '''


  # ==== Backend Services ====
  backend:
    container_name: back-end
    build: server
    command: sh -c "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"
    ports:
      - "8000:8000"
    networks:
      - pipeline-network

  # ==== Frontend Services ====
  client:
    container_name: webapp
    build: webapp
    ports:
      - "8080:80"
    depends_on:
      - backend
    networks:
      - pipeline-network

volumes:
  kafka-volume:
  zookeeper-volume:

networks:
  pipeline-network: {}''' >> docker-compose.yml

echo "Generated docker-compose.yml with $((COUNTER - 1)) tickers."

sudo docker-compose up --build