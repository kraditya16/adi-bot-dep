# Initialize Flask app

import os
from flask import Flask, render_template, request, jsonify
from openai import AzureOpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
app = Flask(__name__)

# Initialize Azure OpenAI client
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-12-01-preview",  # Set appropriate API version
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")  # Azure endpoint
)

# Environment variables for deployment
DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT")

@app.route("/")
def home():
    # Render the HTML template for the chatbot UI
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    # Get user message from the frontend
    user_message = request.json.get("message")

    # Call Azure OpenAI API for the response
    response = client.chat.completions.create(
        model=DEPLOYMENT_NAME,
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": user_message}
        ]
    )

    # Extract reply from the response object
    reply = response.choices[0].message.content

    # Return the response to the frontend as JSON
    return jsonify({"reply": reply})

if __name__ == "__main__":
    # Start Flask app on port 8000 (dynamic port for Azure)
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)


