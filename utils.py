import streamlit as st
from openai import OpenAI
import datetime
import os
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv(override=True)

# Access the API key
api_key = os.getenv("OPENAI_API_KEY")

# Load environment variables from .env file

client = OpenAI(api_key=api_key)


def history_teller(city):
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {
                "role": "system",
                "content": (
                    "Sen, Türkiye'deki bir şehir hakkında detaylı bilgi veren bir yardımcı asistansın. Şehir hakkında şu bilgileri sağla:\n"
                    "- Tarihsel hava durumu desenleri\n"
                    "- Önemli tarihi olaylar\n"
                    "- Bitki örtüsü\n\n"
                    "Bilgileri başlıklar, madde işaretleri ve uygun yerlerde emoji kullanarak kısa ve etkileyici bir şekilde sun. Markdown formatını kullan."
                )
            },
            {"role": "user", "content": f"{city} hakkında bilgi ver."},
        ]
    )
    history_of_location = response.choices[0].message.content
    return history_of_location

