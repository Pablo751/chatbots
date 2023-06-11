from flask import Flask, jsonify, request
import openai
import os
from dotenv import load_dotenv

app = Flask(__name__)

# load values from the .env file if it exists
load_dotenv()

# configure OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

class Chatbot:
    def __init__(self, id, name, description):
        self.id = id
        self.name = name
        self.description = description

chatbots = [
    Chatbot(1, "Website Expert", "This chatbot can provide information about articles on your website and help sell products."),
    Chatbot(2, "Writing Assistant", "This chatbot can help with writing tasks."),
    Chatbot(3, "Pet Advisor", "This chatbot can provide non-professional veterinary advice based on user input about their pet."),
]

@app.route('/chatbots', methods=['GET'])
def get_chatbots():
    return jsonify([chatbot.__dict__ for chatbot in chatbots])

@app.route('/chatbots/<int:chatbot_id>', methods=['GET'])
def get_chatbot(chatbot_id):
    chatbot = next((c for c in chatbots if c.id == chatbot_id), None)
    if chatbot is None:
        return jsonify({"error": "Chatbot not found"}), 404
    return jsonify(chatbot.__dict__)

@app.route('/chatbots/<int:chatbot_id>/interact', methods=['POST'])
def interact_with_chatbot(chatbot_id):
    chatbot = next((c for c in chatbots if c.id == chatbot_id), None)
    if chatbot is None:
        return jsonify({"error": "Chatbot not found"}), 404
    message = request.json.get('message')
    if message is None:
        return jsonify({"error": "No message provided"}), 400
    # Call the OpenAI API to generate a response based on the message.
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": message},
        ]
    )
    return jsonify({"response": response.choices[0].message['content']})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

