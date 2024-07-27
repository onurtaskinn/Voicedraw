import google.generativeai as genai
import PIL.Image
import requests
import os
from dotenv import load_dotenv
from openai import OpenAI
from io import BytesIO
from datetime import datetime


load_dotenv()

my_key_openai = os.getenv("openai_apikey")

client = OpenAI(api_key=my_key_openai)


def generate_image_with_dalle(prompt):
    
    AI_response = client.images.generate(
        model="dall-e-2",
        size="1024x1024",
        quality="hd",
        n=1,
        response_format="url",
        prompt=prompt
    )

    image_url = AI_response.data[0].url

    response = requests.get(image_url)
    image_bytes = BytesIO(response.content)

    timestampt =  datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"./img/generated_image_{timestampt}.png"

    if not os.path.exists("./img"):
        os.makedirs("./img")

    with open(filename, "wb") as file:        
        file.write(image_bytes.getbuffer())


    return filename


my_key_google = os.getenv("google_apikey")

genai.configure(api_key=my_key_google)

def gemini_vision_with_local_file(image_path , prompt):

    multimodality_prompt = f"""Bu gönderdiğim resmi, bazı ek yönergelerle birlikte yeniden oluşturmanı istiyorum.
    Bunun için ilk olarak resmi son derece ayrıntılı biçimde betimle. Daha sonra sonucunda bana vereceğin metni, bir yapay zeka
    modelini kullanarak görsel oluşturmakta kullanacağım. O yüzden yanıtına son halini verirken bunun resim üretmekte kullanılacak bir
    girdi yani prompt olduğunu dikkate al. İşte ek yönerge şöyle: {prompt}
    """
    client = genai.GenerativeModel(model_name='gemini-pro-vision')
    source_image = PIL.Image.open(image_path)

    AI_response = client.generate_content(
        [multimodality_prompt, source_image]
    )

    AI_response.resolve()

    return AI_response.text


def generate_image(image_path , prompt):
    
    image_based_prompt = gemini_vision_with_local_file(image_path , prompt)
    
    filename = generate_image_with_dalle(image_based_prompt)

    return filename







    




