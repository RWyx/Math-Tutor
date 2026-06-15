import base64

with open("sample_question.png", "rb") as f:
    image_data = f.read()

image_base64 = base64.b64encode(image_data).decode("utf-8")
print(image_base64[:100])