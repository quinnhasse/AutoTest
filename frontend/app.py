from flask import Flask, render_template, request
from backend.agent import AIAgent
import os

app = Flask(__name__)

from config import GITHUB_TOKEN,REPO_NAME

# Initialize the AI Agent
ai_agent = AIAgent(GITHUB_TOKEN)
# Clone the repository
ai_agent.github_manager.clone_repository(REPO_NAME)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            user_input = request.form['user_input']
            response = ai_agent.process_request(user_input)
            return render_template('index.html', response=response)
        except Exception as e:
            print(f"Error processing request: {e}")
            return render_template('index.html', error=str(e))
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)