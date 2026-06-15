import os
from openai import OpenAI
from google import genai
from dotenv import load_dotenv
load_dotenv("API_KEY.env")
import base64

with open("instruction_prompt.txt", "r")as f:
    system_prompt = f.read()
    

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
messages = []

print("What's your problem")
while True:
    user_input = input("Student: ")
    parts = user_input.split()
    image_path = None
    for part in parts:
        if os.path.exists(part):
            image_path = part
            break
    question = user_input.replace(image_path, "").strip() if image_path else user_input
    if image_path:
        with open(image_path, "rb") as f:
            image_data = f.read()
        image_base64 = base64.b64encode(image_data).decode("utf-8")
        messages.append({"role": "user", "parts": [
        {"text": question},
        {"inline_data": {"mime_type": "image/png", "data": image_base64}}
        ]})
    else:
        messages.append({"role": "user", "parts": [
        {"text": user_input}]})
    
    

    if user_input == "quit":
        break

    response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents=messages,
    config={"system_instruction": system_prompt}
    )
    ai_reply = response.text

    messages.append({"role": "model", "parts": [{"text": ai_reply}]})
    
    print(f"AI：{ai_reply}\n")