FROM python:3.8-slim
# Install aws cli
RUN apt-get update
RUN apt-get install curl unzip less -y
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
RUN unzip awscliv2.zip
RUN ./aws/install

# Run the remaining app setup
ENV PYTHONUNBUFFERED 1
WORKDIR /code

# Install the dependencies
COPY requirements /code/requirements
RUN pip install -r requirements/local.txt

# Create the user for the app
RUN groupadd -g 777 appuser && \
    useradd -r -u 777 -g appuser appuser

# Copy the dynamodb initialization script
COPY ./scripts/init-dynamodb.sh /init-dynamodb.sh

# Replace the line endings
RUN sed -i 's/\r$//g' /init-dynamodb.sh

# Make the script executable
RUN chmod +x /init-dynamodb.sh

USER appuser

COPY . /code/
