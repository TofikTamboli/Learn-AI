import os
from pathlib import Path
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API Key Are Missing")

client=Groq(api_key=my_api_key)

system_prompt="Your an expert script writer for maharshtra village story age gropu 20-24 love story type."

message_system={
    "role":"system",
    "content":system_prompt,
}
Query="provide me a script"


message={
        "role":"system",
        "content":system_prompt,
        "role":"user",
        "content":Query,
    }

messages=[message_system,message]

response = client.chat.completions.create(model = "openai/gpt-oss-120b",messages=messages,temperature=2)


answer = response.choices[0].message.content
print(answer)