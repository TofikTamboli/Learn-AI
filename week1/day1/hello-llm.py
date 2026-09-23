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
prompt = "What is mean by Agentic toll calling"


# Store the conversetion 4
message={
    "role": "user",
    "content": prompt,
}

messages=[message]

# print the response 5
response = client.chat.completions.create(model=model, messages=messages)
print(response)

print("################")
# # Data destructering carry out 6
# actual answer from the response
answer=response.choices[0].message.content
print(answer)