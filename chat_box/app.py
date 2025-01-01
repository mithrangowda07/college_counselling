from flask import Flask, render_template, request, jsonify
from groq import Groq
from fpdf import FPDF
import os

app = Flask(__name__)

# Set up Groq API key
GROQ_API_KEY = "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"
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

# Initialize Groq client
try:
    client = Groq(api_key=os.environ["GROQ_API_KEY"])
except Exception as e:
    print(f"Failed to initialize Groq client: {e}")

# Function to validate prompts
def is_valid_prompt(prompt):
    keywords = ["college", "placement", "fee", "ranking", "infrastructure", "course", "admission"]
    return any(keyword in prompt.lower() for keyword in keywords)

# Function to create a PDF from content
def create_pdf(content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    encoded_content = content.encode("latin-1", "replace").decode("latin-1")  # Handle special characters
    pdf.multi_cell(0, 10, encoded_content)
    return pdf.output(dest="S").encode("latin-1")

# Route for the chatbot UI
@app.route("/")
def index():
    return render_template("index.html")

# Route to handle chat messages
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        user_prompt = data.get("prompt", "")

        if not is_valid_prompt(user_prompt):
            return jsonify({"response": "Please ask questions related to colleges, such as placements, fees, infrastructure, or rankings."})

        # Prepare messages for Groq API
        messages = [
            {"role": "system", "content": "You are a chatbot that provides accurate and concise information about colleges in India, including placements, fees, infrastructure, rankings, and related topics. You must not respond to queries unrelated to these topics."},
            {"role": "user", "content": user_prompt}
        ]

        # Get response from Groq
        response = client.chat.completions.create(model="llama3-8b-8192", messages=messages)
        assistant_response = response.choices[0].message.content
        return jsonify({"response": assistant_response})

    except Exception as e:
        return jsonify({"error": str(e)})

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
