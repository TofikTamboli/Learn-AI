# Import All the mandotery packeges
import os
from pathlib import Path
from groq import Groq
from dotenv import load_dotenv

# check the API key are in ENV and get it here 1
load_dotenv()
my_api_key = os.getenv("GROQ_API_KEY")
if not my_api_key:
    raise ValueError("API key Kaha Hai Bhai!")

# Connect the user to client 2

client = Groq(api_key = my_api_key)

# config the actual model 
# write the correct name of model withouth any typo mistake 3
model = "openai/gpt-oss-120b"

# Query
query = "What is mean by Agentic toll calling"
# prompt
prompt1="hi"
prompt2="What is machine learning in detail"
prompt3="Write essay on Indian constetuetion 100 words"

prompts=[prompt1,prompt2,prompt3]
for prompt in prompts:
    # Store the conversetion 
    message = {
        "role": "user",
        "content": prompt,
    }
    messages = [message]
    response = client.chat.completions.create(model=model, messages=messages, max_tokens=50)
    usage = response.usage
    print(f"prompt:{prompt} --> your_prompt_token: {usage.prompt_tokens} output_token:{usage.completion_tokens} total_token:{usage.total_tokens} finesh Reson:{response.choices[0].finish_reason}")

# print the response 5
# response = client.chat.completions.create(model=model, messages=messages)
# print(response)

# print("################")
# # # Data destructering carry out 6
# # actual answer from the response
# answer=response.choices[0].message.content
# print(answer)