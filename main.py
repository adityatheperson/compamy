import os
from nicegui import ui, events
from openai import OpenAI
import base64

import os

current_directory = os.getcwd()

XAI_API_KEY = os.getenv("XAI_API_KEY")

client = OpenAI(
    api_key=XAI_API_KEY,
    base_url="https://api.x.ai/v1",
)


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return encoded_string


def chat_with_gpt(image_path, user_message="What is in this image?"):
    try:
        base64_image = encode_image(image_path)

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": ""},
                {"role": "user", "content": [
                    {"type": "text", "text": user_message},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ]}
            ],
            max_tokens=500
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {e}"


def grok(imagepath, message):
    base64_image = encode_image(imagepath)

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
        temperature=0.2,
    )
    return completion.choices[0].message.content

def save_image(e: events.UploadEventArguments):
    if e.content:
        file_path = os.path.join(current_directory, e.name)
        with open(file_path, 'wb') as f:
            f.write(e.content.read())
        ui.notify(f'Uploaded and saved as {e.name}')
    image_path = current_directory + "/" + e.name
    user_prompt = "roast this person based on their facial features, do not be lighthearted"
    response = grok(image_path, user_prompt)
    output_label.text = response
    print(response)
    if os.path.exists(image_path):
        os.remove(image_path)
        print("deleted")



with ui.header(elevated=True).style('background-color: #689cd4'):
    ui.label("Roast Generator").style('font-size: 5em; font-weight: bold;')

# Main content area
with ui.row().classes('justify-center items-center w-full h-[80vh]'):
    with ui.column().classes('items-center'):
        ui.upload(on_upload=save_image, label="Upload Image").props('accept=image/*').classes('max-w-full').style('width: 500px; height: 700px;')
        ui.label("Roast:").props('autogrow').classes('max-w-full').style('font-size: 2em; height: 60px;')
        output_label = ui.label("Status: Waiting for input...").style('margin-top: 10px; font-size: 2em')

# Footer
with ui.footer().style('background-color: #689cd4; padding: 15px;'):
    ui.label("Aditya, Aarush, Edan").style('font-size: 1em;')

ui.run()