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
slider_value = 20


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


def grok(imagepath, message, temperature_value):  # Added temperature_value as argument
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
                    "text": "use this image to roast this individual, try to be as personal as you can and be as mean as you can. Try to go off physical features. Make it one sentence long",
                },
            ],
        },
    ]

    print(f"Temperature value sent to Grok: {temperature_value/100}") # Print statement to verify temperature
    completion = client.chat.completions.create(
        model="grok-2-vision-latest",
        messages=messages,
        temperature= temperature_value/100, # Use the passed temperature_value
    )
    return completion.choices[0].message.content

def save_image(e: events.UploadEventArguments):
    if e.content:
        file_path = os.path.join(current_directory, e.name)
        with open(file_path, 'wb') as f:
            f.write(e.content.read())
        ui.notify(f'Uploaded and saved as {e.name}')
    image_path = current_directory + "/" + e.name
    user_prompt = "roast this person based on their facial features, do not be lighthearted, try to be unique and personal"
    # Pass slider_value to grok function
    response = grok(image_path, user_prompt, slider_value)
    output_label.text = response
    print(response)
    if os.path.exists(image_path):
        os.remove(image_path)
        print("deleted")
    print(f"Current slider_value: {slider_value}") # Print slider_value after upload


ui.html("""
<style>
body {
    background-color: white;
    color: #ff2600;
}
</style>
""")

with ui.header(elevated=True).style('background-color: #141E46; border-bottom: 2px solid #ff2600; color: #ff2600;'): # Header style modified
    ui.image('loge.png').style('width: 80px; height: auto; margin-right: 10px;') # Image added before text
    ui.label("SlanderBot").style('font-size: 4em; font-weight: bold;')

# Main content area
with ui.row().classes('justify-center items-center w-full h-[80vh]'):
    with ui.column().classes('items-center'):
        ui.upload(on_upload=save_image, label="Upload Image").props('accept=image/* color="red"').classes('max-w-full').style('width: 500px; height: 700px; background-color: #f0f0f0; padding: 20px; border-radius: 10px;') # Styled upload button, slightly darker background for contrast
        ui.label("Temperature:").props('autogrow').classes('max-w-full').style('font-size: 1em; height: 60px;')
        slider = ui.slider(min=0, max=99, value = slider_value).props('label-always color="red" track-color="red"').bind_value_to(globals(), 'slider_value').style('color: #ff2600;') # Styled slider with accent color
        # Display temperature value divided by 100 to show the actual temperature range
        ui.label().bind_text_from(slider, 'value', lambda value: f"{(value / 100):.2f}") # Display as 0.xx
        ui.label("Roast:").props('autogrow').classes('max-w-full').style('font-size: 2em; color: #ff2600;') # "Roast" label in accent color
        output_label = ui.label("Status: Waiting for input...").style('margin-top: 10px; font-size: 2em;') # Output label


# Footer
with ui.footer().style('background-color: #141E46; border-top: 2px solid #ff2600; color: #ff2600;'): # Footer style modified
    ui.label("Aditya, Aarush, Edan").style('font-size: 1em;')

ui.run()