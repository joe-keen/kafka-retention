#!/bin/bash

function decrease_retention() {
    /opt/kafka/bin/kafka-topics.sh --zookeeper localhost:2181 --alter \
        --topic $1 --config retention.ms=60
}

function reset_retention() {
    /opt/kafka/bin/kafka-topics.sh --zookeeper localhost:2181 --alter \
        --topic $1 --deleteConfig retention.ms
}

kafka_dir='/var/kafka'

if [ ! -d "$kafka_dir" ]; then
    echo "No /var/kafka directory found.  Unable to do anything."
    exit 0
fi

size=`df -kh | grep $kafka_dir$ | awk '{print $5}' | awk -F% '{print $1}'`

if [ "$size" -gt "50" ]; then
    echo "$kafka_dir > 75% usage.  Reducing kafka retention to 1 hour."
    decrease_retention metrics
    decrease_retention logs
fi

if [ "$size" -lt "25" ]; then
    echo "$kafka_dir < 25% usage.  Resetting retention to default."
    reset_retention metrics
    reset_retention logs
fi
