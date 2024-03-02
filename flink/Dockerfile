# Start with the official Flink image
FROM flink:latest

# Set environment variables if necessary
ENV FLINK_HOME=/opt/flink
ENV PATH=$FLINK_HOME/bin:$PATH

# Copy custom configuration files into the container
# Make sure to have these files in your Docker context
COPY flink-conf.yaml $FLINK_HOME/conf/
COPY log4j.properties $FLINK_HOME/conf/

# Add any additional dependencies, plugins, or custom user code
COPY --chown=flink:flink my-custom-connector.jar $FLINK_HOME/lib/
