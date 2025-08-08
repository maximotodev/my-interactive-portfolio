import os
import json
from groq import Groq

def stream_llm_response(user_question, context, system_prompt):
    """Streams the LLM response using a dynamically chosen system prompt."""
    try:
        client = Groq(api_key=os.getenv('GROQ_API_KEY'))
        user_prompt = (f"Context:\n{context}\n\nUser Question: {user_question}\n\nGenerate your response.")
        stream = client.chat.completions.create(messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}], model="llama3-70b-8192", stream=True)
        for chunk in stream:
            content = chunk.choices[0].delta.content
            if content: yield content
    except Exception as e:
        yield json.dumps({"error": "I'm sorry, but the AI model is currently experiencing issues."})