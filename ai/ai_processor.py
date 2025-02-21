"""Run this model in Python

> pip install openai
"""
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
# To authenticate with the model you will need to generate a personal access token (PAT) in your GitHub settings. 
# Create your PAT token by following instructions here: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens
client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=os.environ["API_TOKEN"],
)

def ask_ai(prompt):
    response = client.chat.completions.create(
        messages = [{"role": "user", "content" : prompt}],
        model = "gpt-4o",
        temperature = 1,
        max_tokens = 4096,
        top_p = 1
    )
    return response.choices[0].message.content

