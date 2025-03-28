from flask import Flask, render_template, request, jsonify
import openai
import json

app = Flask(__name__)

openai.api_key = "API_KEY"

# AI study plan generator
def generate_study_plan(syllabus, deadlines, study_time, user_input):
    if not syllabus or not deadlines or not study_time:
        return "Please enter all details for an accurate study plan."

    # AI-assisted response
    messages = [
        {"role": "system", "content": "You are an AI study planner."},
        {"role": "user", "content": f"Syllabus: {syllabus}, Deadlines: {deadlines}, Study time: {study_time} hours/day. {user_input}"}
    ]
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=500
    )
    
    return response["choices"][0]["message"]["content"]

# AI Chatbot
def chatbot_response(user_message):
    messages = [
        {"role": "system", "content": "You are a helpful chatbot for students."},
        {"role": "user", "content": user_message}
    ]
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=150
    )
    
    return response["choices"][0]["message"]["content"]

# Routes
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/generate_plan', methods=['POST'])
def generate_plan():
    data = request.json
    study_plan = generate_study_plan(data['syllabus'], data['deadlines'], data['study_time'], data['user_input'])
    return jsonify({"study_plan": study_plan})

@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.json
    reply = chatbot_response(data['message'])
    return jsonify({"reply": reply})

if __name__ == '__main__':
    app.run(debug=True, port=7860)
