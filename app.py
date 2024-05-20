from flask import Flask, render_template, request
from azure.cosmos import CosmosClient
import uuid
from azure.servicebus.aio import ServiceBusClient
from azure.servicebus import ServiceBusMessage
from azure.cosmos import CosmosClient
from azure.messaging.webpubsubservice import WebPubSubServiceClient

app = Flask(__name__)

DATABASE_NAME = "ToDoList"
CONTAINER_NAME = "Items"

part1 = "AccountEndpoint=https://azurecosmosemails"
part2 = "erver.documents.azure.com:443/;AccountKey=RI8PZOR8rROhmucmF"
part3 = "k0N4ABgpE7tjqBcFIKfPpGKPxeD3b76wYK6uRjBKZl6fhm56xxrZHhXU3euACDbNi5oDg==;"

client = CosmosClient.from_connection_string(part1 + part2 + part3)

database = client.get_database_client(DATABASE_NAME)

container = database.get_container_client(CONTAINER_NAME)

part1 = "Endpoint=sb://emailspam.servicebus.windows.net/;SharedAccess"
part2 = "KeyName=RootManageSharedAccessKey;SharedAccessKey=mvfrWyMCwI+kAN"
part3 = "MMKe9eQhaC/47foWkC4+ASbMInOqE="

NAMESPACE_CONNECTION_STRING = part1 + part2 + part3
QUEUE_NAME = "bprocessing"


@app.route('/')
def index():
    return render_template('index.html')


async def send_message(sender, message):
    single_message = ServiceBusMessage(str(message))
    await sender.send_messages(single_message)


@app.route('/check_spam', methods=['POST'])
def check_spam():
    email_text = request.form['email_text']
    data = {}
    data["id"] = str(uuid.uuid4())
    data["email"] = email_text
    container.create_item(data)
    client = ServiceBusClient.from_connection_string(NAMESPACE_CONNECTION_STRING)
    sender = client.get_queue_sender(QUEUE_NAME)
    send_message(sender, data)
    # Dummy spam check logic
    if "spam" in email_text.lower():
        result = "This is spam."
    else:
        result = "This is not spam."
    return render_template('index.html', result=result)


if __name__ == '__main__':
    app.run(debug=True)
