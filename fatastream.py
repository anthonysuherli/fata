import json

import streamlit as st
from streamlit_chat import message
import openai
from bs4 import BeautifulSoup
from markdown import markdown
from openai import ChatCompletion
from openai import Completion

import os

# Note: you need to be using OpenAI Python v0.27.0 for the code below to work
with open ('cred/openai.json', 'r') as f:
    creds = json.load(f)

    os.environ['OPENAI_API_KEY'] = creds['OPENAI_API_KEY']

openai.api_key = os.environ['OPENAI_API_KEY']


def message_prompt(message, role='user', chat_history=[]):
    prompt = {
        'role': role,
        "content": message
    }
    chat_history.append(prompt)

    return chat_history


def prompt_chat(messages ,temperature = .5):
    chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages =  messages,
        temperature = temperature,
        n = 1
    )
    response = chat.choices[0].message.content
    return response


if __name__ == '__main__':
    if 'log' not in st.session_state:
        st.session_state['log'] = [{'role': 'system', 'content' : 'you are a financial assistant called Jarvest'}]

    user_input = st.text_input("You:", key='input')
    if user_input:
        st.session_state['log'] = message_prompt(message = user_input, chat_history = st.session_state['log'])
        output = prompt_chat(st.session_state['log'])
        st.session_state['log'] = message_prompt(output, role = 'assistant', chat_history =  st.session_state['log'])


    if st.session_state['log']:
        for i in range(len(st.session_state['log']) - 1, -1, -1):
            l = st.session_state['log'][i]

            if l['role'] == 'system':
                continue
            elif l['role'] == 'user':
                is_user = True
            else:
                is_user = False

            content = f"{str(l['role'])}: {str(l['content'])}"
            html = markdown(content)
            text = ''.join(BeautifulSoup(html, features="html.parser").findAll(text=True))
            try:
                message({st.markdown(text)}, is_user = is_user, key = f"{l['role']}, {i}")
            except:
                pass