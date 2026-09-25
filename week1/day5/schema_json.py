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

# Import The pydantic Librory and create a class with the name of Ticket and set The (BaseModel)
# Then write the schema
# Then In schema varaible store the Ticket.model_json_schema()

from pydantic import BaseModel
class Ticket(BaseModel):
    name:str
    issue:str
    specfic_issue:str
    email: str | None = None
    phone: str | None = None

schema=Ticket.model_json_schema()

# Mentioend the  response Format
response_format={
    "type":"json_object"
}

# Write the actual System Prompt for pydantic response
system_prompt=f"""Extract The Query and provide me in the Given JSON format {schema} If any value are not present pas the null in value and i want the JSON data In prety format one by one"""
system_prompt={
    "role":"system",
    "content":system_prompt
}

# Store the client message in Query and then send it with addetional prompting to the LLM
query="My name Is Tofik Tamboli I Bay your i Phone and The mobile are not charged properly, I need my mony back or new mobile or coonect me on 7020109848"
prompt=f"""Your task Is extract Name, Issue Type, specefic Probeleme Faced by user and there contact if mentioned , email,phone number addres if mentioned.
here is the query{query}"""    

# Define the Role and Content 
message={
    "role":"user",
    "content":prompt
}

# To store the Conversetion built an Array With The Messages
messages=[system_prompt,message]

# Take the response from LLM by passing the model, message, response format
response = client.chat.completions.create(
    model=model,
    messages=messages,
    response_format=response_format
)

# Extract The actual Data from the response by destructering response.choices[0].message.content
answer = response.choices[0].message.content
print(answer)

# /////////////////////////////////////////////////////////////
import json
raw_json = answer
data_file = json.loads(raw_json)
ticket_info = Ticket(**data_file)

print(ticket_info.name)