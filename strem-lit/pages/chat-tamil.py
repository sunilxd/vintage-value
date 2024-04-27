import streamlit as st
# from pathlib import Path
# import pandas as pd

from translate import Translator
get_tamil = Translator(to_lang="ta", from_lang="en").translate
get_english = Translator(to_lang="en", from_lang="ta").translate

from llama_cpp import Llama

@st.cache_resource
def get_model(file):
    return Llama(model_path=file)

llm = get_model("/home/sunil/Documents/alpaca-linux/ggml-alpaca-7b-q4.bin")
history = ["the following is a conversation between bot and farmer."]
display_history = []
person1 = 'farmer'
person2 = 'bot'


def send_message(message):

    # return "This service is currently disabled due to lack of resource"
    message_english = get_english(message)

    display_history.append(message)

    history.append(f"{person1}: {message_english}")
    history.append(f"{person2}: ")
    
    output = llm('\n'.join(history), max_tokens=64, stop=[f"{person1}:"], echo=True)
    reply = output['choices'][0]['text'].split(f'{person2}: ')[-1]

    history[-1] += reply
    tamil_reply = get_tamil(reply)
    display_history.append(tamil_reply)
    return tamil_reply
    


if prompt := st.chat_input("Say something"):
    st.chat_message("user").write(prompt)
    st.chat_message("assistant").write(send_message(prompt))