# Day 5 of My AI Journey: Taming LLMs with Pydantic & Structured JSON Output

*Moving beyond raw chatbots: How to force Large Language Models to return clean, reliable, validated JSON data for real-world software applications.*

---

Welcome back to Day 5 of my journey to becoming an AI Engineer! 🚀

Over the last few days, we interacted with LLMs like conversational chat partners—tweaking system prompts, adjusting temperature, and understanding token economics. 

That’s great for a chatbot UI, but **real software systems cannot operate on unstructured text**. 

Imagine building an automated customer support triage system:
- If a customer sends an angry paragraph about a broken phone, your backend API doesn't need polite conversational fluff.
- It needs a **clean, structured dictionary or database record**: Who is the user? What is their issue? What is their phone number? Is there an email?

Today, I explored the bridge between conversational AI and robust software engineering: **Pydantic, JSON Schema, and Structured Output**.

Let’s dive into how it works!

---

## 1. The Core Problem: LLMs Love Freeform Text

By default, an LLM is a text predictor. If you ask it:
> *"Extract the customer name and phone number from this message"*

It might return:
> *"Sure! Here is the extracted information: Name is Tofik and phone is 7020109848. Have a nice day! 😊"*

While human-friendly, this is a **nightmare for code**. If you try to save that directly to a PostgreSQL database or trigger a webhook, your program will break.

We need the model to output **deterministic, machine-readable JSON**, like this:

```json
{
  "name": "Tofik Tamboli",
  "issue": "Mobile charging issue",
  "specfic_issue": "Mobile not charging properly; user requests refund or replacement",
  "email": null,
  "phone": "7020109848"
}
```

---

## 2. Enter Pydantic: The Python Standard for Data Validation

**Pydantic** is Python’s most popular data modeling and validation library. It allows you to define data models using standard Python type hints.

```python
from pydantic import BaseModel

class Ticket(BaseModel):
    name: str
    issue: str
    specfic_issue: str
    email: str | None = None
    phone: str | None = None
```

### Why use Pydantic with LLMs?
1. **Schema Generation**: With one line (`Ticket.model_json_schema()`), Pydantic generates a full JSON Schema definition that you can feed directly to the LLM.
2. **Type Safety & Autocomplete**: Once parsed, you can access properties cleanly (`ticket.name`, `ticket.phone`) with full IDE autocompletion instead of guessing dictionary keys.
3. **Automatic Validation**: If the LLM produces invalid types (e.g., a number instead of a string, or missing mandatory fields), Pydantic catches it immediately before bad data enters your database.

---

## 3. The 3-Step Pipeline: From Prompt to Typed Object

Here is how the end-to-end flow works:

```
┌─────────────────────────┐
│  Define Pydantic Class  │  ──► Ticket.model_json_schema()
└─────────────────────────┘
            │
            ▼
┌─────────────────────────┐
│    Prompt the LLM       │  ──► System prompt with schema + response_format={"type": "json_object"}
└─────────────────────────┘
            │
            ▼
┌─────────────────────────┐
│ Deserialization & Parse │  ──► json.loads(raw_json) ──► Ticket(**data) ──► Type-Safe Python Object!
└─────────────────────────┘
```

### 1. Generating the JSON Schema
```python
schema = Ticket.model_json_schema()
```
This produces a strict JSON specification describing required fields, data types, and default values.

### 2. Instructing the Model via System Prompt & `response_format`
We give the model the schema and instruct it to return strictly JSON:

```python
response_format = {
    "type": "json_object"
}

system_prompt = f"""
Extract the query information and return it strictly matching this JSON schema: {schema}.
If any field is not mentioned in the query, pass null as the value.
"""
```

Passing `response_format={"type": "json_object"}` tells the LLM provider (Groq / OpenAI) to enforce pure JSON output and prevent conversational chit-chat.

### 3. Converting Raw JSON into a Validated Pydantic Object
```python
import json

raw_json = response.choices[0].message.content
data_file = json.loads(raw_json)

# Convert dictionary into a strongly typed Ticket instance
ticket_info = Ticket(**data_file)

print(ticket_info.name)   # "Tofik Tamboli"
print(ticket_info.phone)  # "7020109848"
```

---

## 4. Real Gotchas & Debugging Lessons from Today

Building this hands-on taught me several crucial lessons that tutorials rarely mention:

### Gotcha 1: The `null` vs `str` Pitfall
If a customer doesn't mention their email, the LLM sets `"email": null`.
If your model defines `email: str`, Pydantic will raise:
```text
pydantic_core._pydantic_core.ValidationError: Input should be a valid string, input_value=None
```
**Fix:** Always mark optional fields as nullable: `email: str | None = None`.

### Gotcha 2: The Markdown Code Fence Bug
If you forget to specify `response_format={"type": "json_object"}`, the LLM might wrap the JSON inside markdown triple backticks:
````text
```json
{ "name": "Tofik" }
```
````
Calling `json.loads()` on this string throws `JSONDecodeError: Expecting value: line 1 column 1 (char 0)` because `json.loads` cannot parse backticks!

### Gotcha 3: `messages` Structure
Every message in the `messages` array must be an object containing both `"role"` and `"content"`. Passing a raw string into `messages = [system_prompt, message]` will cause API rejection (`400 Bad Request`).

---

## 5. The Full Working Code

Here is the complete script built and tested today:

```python
import os
import json
from groq import Groq
from dotenv import load_dotenv
from pydantic import BaseModel

# 1. Load environment variables
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY not found in environment!")

# 2. Initialize client and model
client = Groq(api_key=api_key)
model = "openai/gpt-oss-120b"

# 3. Define Pydantic schema
class Ticket(BaseModel):
    name: str
    issue: str
    specfic_issue: str
    email: str | None = None
    phone: str | None = None

schema = Ticket.model_json_schema()

# 4. Prepare system and user prompts
response_format = {"type": "json_object"}

system_prompt = f"""
Extract the query and provide the output in the given JSON format: {schema}.
If any value is not present in the user text, set its value to null.
"""

user_query = "My name Is Tofik Tamboli I Bay your i Phone and The mobile are not charged properly, I need my mony back or new mobile or coonect me on 7020109848"
prompt = f"Extract ticket details from this customer query: {user_query}"

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": prompt}
]

# 5. Call API with JSON format enforcement
response = client.chat.completions.create(
    model=model,
    messages=messages,
    response_format=response_format
)

raw_json = response.choices[0].message.content
print("Raw JSON Response:\n", raw_json)

# 6. Parse and validate with Pydantic
data_dict = json.loads(raw_json)
ticket = Ticket(**data_dict)

print("\n--- Validated Object ---")
print(f"Customer Name : {ticket.name}")
print(f"Main Issue    : {ticket.issue}")
print(f"Detail        : {ticket.specfic_issue}")
print(f"Contact Phone : {ticket.phone}")
print(f"Contact Email : {ticket.email}")
```

---

## Key Takeaways from Day 5

1. **Unstructured text is for humans; structured JSON is for software.** Real AI applications depend on reliable data schemas.
2. **Pydantic bridges the gap**: It converts Python classes into schemas the LLM understands, and parses raw JSON back into safe Python objects.
3. **Plan for missing data**: Always make optional fields nullable (`str | None = None`) when dealing with user-generated text.
4. **Enforce `response_format`**: Always instruct the provider's API to enforce JSON mode so you never have to parse markdown fences manually.

On to Day 6! 💡