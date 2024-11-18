from flask import Flask, request, jsonify
import PyPDF2
import google.generativeai as genai
import os
from dotenv import load_dotenv
from flask_cors import CORS

# Load environment variables
load_dotenv()

# Configure Gemini AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = Flask(__name__)
# Enable CORS for all routes
CORS(app)

# Function to get a response from Gemini AI
def get_gemini_response(input_text, pdf_text, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash-001')
    response = model.generate_content([input_text, pdf_text, prompt])
    return response.text

# Endpoint to process resume and job description
@app.route('/process', methods=['POST'])
def process_resume():
    try:
        # Get the job description and uploaded file from the request
        job_description = request.form.get('jobDescription')
        prompt_type = request.form.get('action')  # Reason, improve, or keywords

        # Uploaded PDF file
        uploaded_file = request.files['resume']

        # Extract text from the uploaded PDF
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        pdf_text = ""
        for page in pdf_reader.pages:
            pdf_text += page.extract_text()

        # Define prompts based on the action
        prompts = {
            "reason": "Your reason-based prompt goes here...",
            "improve": "Your improvement-based prompt goes here...",
            "keywords": "Your keyword-based prompt goes here...",
        }
        prompt = prompts.get(prompt_type, "")

        # Get the Gemini AI response
        gemini_response = get_gemini_response(job_description, pdf_text, prompt)

        # Return the response
        return jsonify({"message": gemini_response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
