from diffusers import StableDiffusionPipeline
import torch
import openai
import telebot
import os
from dotenv import load_dotenv

load_dotenv()

ffmpeg_path=os.path.join(os.getcwd(),"ffmpeg")

openai.api_key = api_key=os.getenv('API_KEY')
bot = telebot.TeleBot(token=os.getenv('TOKEN'))
isgm=False
model_id = "runwayml/stable-diffusion-v1-5"
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
pipe = pipe.to("cuda")
@bot.message_handler(commands=['generate'])
def generate(message):
    global isgm
    isgm = True
    bot.send_message(message.chat.id, "Пожалуйста, введите описание изображения")

@bot.message_handler(func=lambda _: True)
def handle_all_other_messages(message):
    global isgm
    
    if isgm:
        prompt = message.text
        image = pipe(prompt).images[0]

        

        bot.send_photo(message.chat.id, image)
        
        isgm = False
        bot.send_message(message.chat.id, "Теперь вы можете работать с ChatGPT дальше либо же отправить ещё один запрос на Stable Diffusion")
    else:
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": message.text},
            ]
        )
        bot.send_message(chat_id=message.from_user.id, text = response.choices[0].message.content)

bot.infinity_polling()