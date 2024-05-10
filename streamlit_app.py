import google.generativeai as genai
import os
import configparser
import os
import streamlit as st
import json
import pandas as pd

config = configparser.ConfigParser()
config.read(os.path.expanduser('.config.ini'))

GOOGLE_API_KEY = config['DEFAULT']['GOOGLE_API_KEY']
genai.configure(api_key=GOOGLE_API_KEY)

generation_config = {
    "candidate_count": 1,
    "temperature": 1,
}


model = genai.GenerativeModel(model_name='gemini-1.0-pro',
                              generation_config=generation_config,
                              )

with open('files/output.json') as json_file:
    data = json.load(json_file)

model = genai.GenerativeModel(model_name='gemini-1.0-pro', generation_config={"candidate_count": 1, "temperature": 1})

def generate_response(prompt):
    prompt_inicial = f"Aja como uma especialista em fundos imobiliários, criativo e descritivo, respondendo com as informações fornecidas: {data} ------ Caso o usuário pergunte sobre outros assuntos, responda: Não posso lhe responder sobre este assunto, me pergunte sobre fundos imobiliários."
    chat = model.start_chat(history=[])
    response = chat.send_message(prompt_inicial + prompt)
    return response.text

def main():
    st.title('Chat para Fundos Imobiliários')
    st.write('Bem vindo(a)!')

    st.write('Fundos Imobiliários Disponíveis:')
    num_companies = len(data['Nome Pregao'])
    num_cols = 4
    num_rows = -(-num_companies // num_cols)  

    company_names = data['Nome Pregao']
    companies_reshape = [company_names[i*num_cols:(i+1)*num_cols] for i in range(num_rows)]

    companies_with_numbers = []
    for i, companies_row in enumerate(companies_reshape):
        row_with_numbers = [f"{i*num_cols + j + 1}. {company}" for j, company in enumerate(companies_row)]
        companies_with_numbers.append(row_with_numbers)

    df = pd.DataFrame(companies_with_numbers).transpose()
    st.table(df)


    prompt = st.text_input('Digite sua pergunta e espere alguns instantes...(Exemplo: gostaria de saber sobre a empresa CIELO):').lower()
    if prompt:
        response = generate_response(prompt).lower()
        st.write('Resposta:', response)

if __name__ == '__main__':
    main()

