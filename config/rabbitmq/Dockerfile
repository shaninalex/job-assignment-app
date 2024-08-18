FROM rabbitmq:3-management-alpine

# Copy the setup script into the container
COPY setup_rabbitmq.sh /usr/local/bin/setup_rabbitmq.sh

# Make the setup script executable
RUN chmod +x /usr/local/bin/setup_rabbitmq.sh

# Specify the command to run when the container starts
CMD ["bash", "-c", "rabbitmq-server & /usr/local/bin/setup_rabbitmq.sh"]
