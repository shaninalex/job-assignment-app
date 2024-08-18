#!/bin/bash

# NOTE:
# rabbitmq:3-management-alpine image has python on board out of the box.
# So more complicated setup can be done with python.

# Function to wait for RabbitMQ to start
wait_for_rabbitmq() {
    until rabbitmqctl node_health_check &> /dev/null; do
        echo "RabbitMQ not ready, waiting..."
        sleep 1
    done
    echo "RabbitMQ is ready"
}

# Wait for RabbitMQ to start
wait_for_rabbitmq

# Declare exchanges
rabbitmqadmin declare exchange name=ex.admin_events type=fanout durable=true
rabbitmqadmin declare exchange name=ex.email type=fanout durable=true

# Declare queues
rabbitmqadmin declare queue name=q.admin_events durable=true
rabbitmqadmin declare queue name=q.email durable=true

# Bind queues
rabbitmqadmin declare binding source=ex.admin_events destination=q.admin_events routing_key=""
rabbitmqadmin declare binding source=ex.email destination=q.email routing_key=""

# This is bad, but it's not for production any way.
while true; do
    sleep 3600
done
