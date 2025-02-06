import os
import openai
from backend.github_utils import GitHubManager
from backend.exa_research import ResearchAgent
import logging

logger = logging.getLogger(__name__)

class AIAgent:
    def __init__(self, github_token):
        self.github_manager = GitHubManager(github_token)
        self.research_agent = ResearchAgent()
        self.project_context = {}
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        openai.api_key = self.openai_api_key

    def process_request(self, user_input):
        # Analyze the user input
        if user_input.lower().startswith("git@github.com"):
            # Handle Git operations
            response = self.github_manager.add_submodule(user_input)
            return response
        else:
            # General request processing
            code_files, assistant_reply = self.generate_code(user_input)
            # Push code to GitHub
            if code_files:
                commit_message = f"Auto-generated code for: {user_input}"
                self.github_manager.commit_and_push_changes(code_files, commit_message)
            return assistant_reply

    def generate_code(self, prompt):
        # Perform research using the ResearchAgent
        research_summary = self.research_agent.perform_research(prompt)

        # Prepare messages for OpenAI
        messages = [
        {"role": "system", "content": "You are an AI developer assistant."},
        {"role": "user", "content": f"{prompt}\n\nPlease provide the code enclosed in triple backticks with the filename specified after the opening backticks, like ```python filename.py"}
        ]

        if self.project_context:
            context_message = f"Here is the current project context:\n{self.project_context}"
            messages.append({"role": "assistant", "content": context_message})

        if research_summary:
            research_message = f"I did some research on your request:\n{research_summary}"
            messages.append({"role": "assistant", "content": research_message})

        messages.append({"role": "user", "content": prompt})

        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            assistant_reply = response.choices[0].message.content
            # Update project context
            self.project_context['last_reply'] = assistant_reply
            # Extract code from the assistant's reply
            code_files = self.extract_code(assistant_reply)
            return code_files, assistant_reply
        except Exception as e:
            logger.error(f"Error in AIAgent.generate_code: {e}")
            return [], "An error occurred while generating the code."

    def extract_code(self, assistant_reply):
        code_files = []
        code_block_started = False
        code_block_content = ""
        code_filename = "generated_code.py"  # Default filename
        for line in assistant_reply.split('\n'):
            if line.strip().startswith("```"):
                if code_block_started:
                    # End of code block
                    code_files.append((code_filename, code_block_content.strip()))
                    code_block_content = ""
                    code_block_started = False
                    code_filename = "generated_code.py"
                else:
                    # Start of code block
                    code_block_started = True
                    # Extract filename if provided
                    code_info = line.strip().strip("```").strip()
                    if code_info:
                        parts = code_info.split()
                        if len(parts) >= 2 and parts[0] == "python":
                            code_filename = parts[1]
            elif code_block_started:
                code_block_content += line + '\n'
        return code_files