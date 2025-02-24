from openai import OpenAI
import os
import base64

XAI_API_KEY = os.getenv("XAI_API_KEY")
image_path = "C:/Users/Aditya/Desktop/jan.jpg"

client = OpenAI(
    api_key=XAI_API_KEY,
    base_url="https://api.x.ai/v1",
)

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return encoded_string

# Getting the base64 string
base64_image = encode_image(image_path)

messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}",
                    "detail": "high",
                },
            },
            {
                "type": "text",
                "text": "what are your remarks about this cartoon character, try to be funny. make sure you do not end on a positive note. Be as sarcastic as you can, please limit it to one sentence and make it spicy. You can be rude because this a nonexistent being and does not have feelings. Try to include stuff included in the picture in the joke. Do not mention that this is a cartoon character. Do not include mentions of the background. Try not to mention the cartoon characters cloths and refer to odd facial features. Try to make it as personal as you can.",
            },
        ],
    },
]

completion = client.chat.completions.create(
    model="grok-2-vision-latest",
    messages=messages,
    temperature=0.01,
)

print(completion.choices[0].message.content)