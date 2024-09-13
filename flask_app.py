from flask import Flask, request, jsonify
import spacy

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")

@app.route('/', methods=['GET'])
def home():
    return "Hello, World! The Flask app is running."

@app.route('/ask', methods=['POST'])
def ask_bot():
    user_query = request.json.get('query')
    if not user_query:
        return jsonify({'error': 'No query provided'}), 400
    
    response = generate_sql(user_query)
    return jsonify({'response': response})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
