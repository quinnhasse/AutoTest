from exa_py import Exa
import os
import openai
from dotenv import load_dotenv
import logging

load_dotenv()
logger = logging.getLogger(__name__)

class ResearchAgent:
    def __init__(self):
        self.exa_api_key = os.getenv('EXA_API_KEY')
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        if not self.exa_api_key or not self.openai_api_key:
            raise ValueError("Please set EXA_API_KEY and OPENAI_API_KEY in your environment variables")
        self.exa = Exa(self.exa_api_key)
        openai.api_key = self.openai_api_key

    def perform_research(self, query):
        try:
            # Perform a search using Exa
            result = self.exa.search_and_contents(
                query,
                type="neural",
                use_autoprompt=True,
                num_results=10,
                text=True
            )

            # Log the raw search results
            logger.debug(f"Exa search results: {result}")

            # Summarize the search results using OpenAI
            system_prompt = "You are a helpful AI assistant. Summarize the given search results."
            user_message = f"Please provide a brief summary based on the following search results about '{query}':\n{result}"

            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ]
            )

            summary = response.choices[0].message.content
            logger.debug(f"Research summary: {summary}")
            return summary

        except Exception as e:
            logger.error(f"Error in ResearchAgent.perform_research: {e}")
            return ""