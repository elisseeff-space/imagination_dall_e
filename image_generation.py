from openai import OpenAI
from config_imagination import ConfigBox

if __name__ == '__main__':
    print("Hello!")

    client = OpenAI(api_key=ConfigBox.config['openai'])

    response = client.images.generate(
    model="dall-e-3",
    prompt="a white siamese cat",
    size="1024x1024",
    quality="standard",
    n=1,
    )

    image_url = response.data[0].url
    print(image_url)
    
    
    