# Day 3 of My AI Journey: Steering the Beast with System Prompts and Temperature

*How to give your LLM a distinct persona and dial in the perfect balance between laser precision and wild creativity.*

---

On Day 1, we learned the "Hello World" of AI engineering: pinging an LLM and getting a response back. 

It was exhilarating! But once the initial excitement wore off, a natural question popped up:

> *"How do I stop the AI from sounding like a generic encyclopedia and actually make it behave the way I want?"*

What if you need it to roleplay as a witty code reviewer? Or a financial analyst who never hallucinates numbers? Or in my case today—**an expert scriptwriter crafting rural Maharashtra village love stories**?

Today, on Day 3 of my AI Engineer journey, I explored the two most fundamental levers you can pull to control an LLM's behavior: **The System Role** and **Temperature**.

Here is everything you need to know to master both.

---

## 1. The System Role: The Director Behind the Actor

When you send a query to an LLM, you're not just chatting with a bot; you're directing an actor on stage. 

If you just say `"provide me a script"`, the model has to guess: *What kind of script? A Hollywood thriller? A Python automation script? A high-school drama?*

This is where the **`system`** message comes in.

```
┌────────────────────────────────────────────────────────┐
│  SYSTEM ROLE                                           │
│  "You are an expert scriptwriter for Maharashtra       │
│   village romance stories (age group 20–24)."          │
└──────────────────────────┬─────────────────────────────┘
                           │ Sets Persona, Tone & Rules
                           ▼
┌────────────────────────────────────────────────────────┐
│  USER ROLE                                             │
│  "Provide me a script"                                 │
└──────────────────────────┬─────────────────────────────┘
                           │ Triggers the Request
                           ▼
┌────────────────────────────────────────────────────────┐
│  AI RESPONSE                                           │
│  A culturally authentic, emotionally rich story!       │
└────────────────────────────────────────────────────────┘
```

### Why Use a System Prompt?
- **Sets Persona & Tone**: Tell the model who it is, how it talks, and what perspective it takes.
- **Enforces Guardrails**: You can define constraints (e.g., *"Respond only in valid JSON"*, *"Never mention competitor products"*).
- **Domain Specialization**: Guides the model to draw from specific domain knowledge and vocabulary.

In Python, you pass it as the very first dictionary in your `messages` array:

```python
messages = [
    {
        "role": "system",
        "content": "You are an expert scriptwriter for Maharashtra village love stories (age group 20–24)."
    },
    {
        "role": "user",
        "content": "Provide me a script."
    }
]
```

---

## 2. Temperature: The Imagination Knob

Once you've given the model its persona, you need to decide: **how creative or predictable should it be?**

That’s where **Temperature** comes in.

Mathematically, temperature controls how the model samples words (tokens). When predicting the next word, the model assigns probabilities to thousands of candidates. Temperature dictates how strictly it sticks to the top candidate versus taking creative risks.

In APIs like Groq and OpenAI, temperature typically ranges from **0.0 to 2.0**:

| Temperature Range | Vibe | Best Used For |
| :--- | :--- | :--- |
| **0.0 – 0.2** | **Cold & Laser-Focused** | Code generation, math problems, structured data/JSON extraction, fact-checking. Deterministic and predictable. |
| **0.7 – 0.9** | **Warm & Balanced** | General conversation, drafting blog posts, helpful Q&A assistants. Good flow without going off the rails. |
| **1.2 – 2.0** | **Hot & Wildly Creative** | Fiction writing, brainstorming out-of-the-box ideas, poetry, dialogue generation. |

> ⚠️ **Watch Out:** If you crank the temperature all the way to 2.0, the model might produce wild, unpredictable results or even grammatical chaos! For high-creativity storytelling, a sweet spot is usually between **1.0 and 1.5**, while for coding you’ll almost always stick to **0.0 to 0.2**.

---

## Hands-On Code: Bringing It All Together

Here’s the complete Python script using the free Groq API to put system prompts and temperature into practice:

```python
import os
from dotenv import load_dotenv
from groq import Groq

# 1. Load API credentials securely
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("API Key is missing! Check your .env file.")

client = Groq(api_key=api_key)

# 2. Define the persona (System Prompt) and the request (User Prompt)
system_prompt = (
    "You are an expert scriptwriter specialized in rural Maharashtra village love stories "
    "tailored for the 20–24 age demographic. Capture authentic rustic nuances and emotions."
)
user_query = "Write an opening scene script where two childhood friends meet near the village well."

# 3. Structure conversation turns
messages = [
    {
        "role": "system",
        "content": system_prompt,
    },
    {
        "role": "user",
        "content": user_query,
    },
]

# 4. Fire the completion with a high temperature for creative flair!
response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=messages,
    temperature=1.2  # High creativity for storytelling!
)

# 5. Extract and print the generated script
answer = response.choices[0].message.content

print("🎬 --- GENERATED SCENE --- 🎬\n")
print(answer)
```

---

## Key Takeaways from Day 3

1. **The System Prompt is Your Superpower**: Don't rely solely on user prompts. Use the `system` role to lock in rules, context, and character before the user ever types a word.
2. **Temperature is Your Style Dial**:
   - Need exact facts or code? **Turn it down near 0.0.**
   - Writing drama, stories, or jokes? **Turn it up above 1.0.**
3. **Clean Message Schema**: Always structure your conversations as a sequential list of clean `{"role": ..., "content": ...}` dictionaries.

Step by step, LLMs are turning from mysterious black boxes into predictable, steerable tools in our developer toolkit!

---

*Enjoying this series? Leave your thoughts below or share how you use system prompts in your own projects!*