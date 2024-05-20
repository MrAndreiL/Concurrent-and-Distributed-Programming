from flask import Flask, render_template, request
from azure.cosmos import CosmosClient
import uuid

app = Flask(__name__)

DATABASE_NAME = "ToDoList"
CONTAINER_NAME = "Items"

part1 = "AccountEndpoint=https://azurecosmosemails"
part2 = "erver.documents.azure.com:443/;AccountKey=RI8PZOR8rROhmucmF"
part3 = "k0N4ABgpE7tjqBcFIKfPpGKPxeD3b76wYK6uRjBKZl6fhm56xxrZHhXU3euACDbNi5oDg==;"

client = CosmosClient.from_connection_string(part1 + part2 + part3)

database = client.get_database_client(DATABASE_NAME)

container = database.get_container_client(CONTAINER_NAME)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/check_spam', methods=['POST'])
def check_spam():
    email_text = request.form['email_text']
    data = {}
    data["id"] = str(uuid.uuid4())
    data["email"] = email_text
    container.create_item(data)
    # Dummy spam check logic
    if "spam" in email_text.lower():
        result = "This is spam."
    else:
        result = "This is not spam."
    return render_template('index.html', result=result)


if __name__ == '__main__':
    app.run(debug=True)
