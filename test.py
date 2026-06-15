import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv("API_KEY.env")
with open("instruction_prompt.txt", "r")as f:
    system_prompt = f.read()
    

client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)
messages = []
messages.append({"role": "system", "content": system_prompt})
print("What's your problem")
while True:
    user_input = input("Student: ")
    if user_input == "quit":
        break
    messages.append({"role": "user", "content": user_input})
    

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages
    )

    ai_reply = response.choices[0].message.content

    messages.append({"role": "assistant", "content": ai_reply})
    
    print(f"AI：{ai_reply}\n")