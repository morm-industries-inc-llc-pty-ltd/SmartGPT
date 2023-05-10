import json
from dotenv import load_dotenv
import os
import openai
import streamlit as st
from src.GPTInterface.SimpleQuery import SimpleQuery
from pathlib import Path
import sys




# I don't really understand this, but it fixes import errors
sys.path.append(str(Path(__file__).resolve().parent.parent))

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

input_text = st.text_area("Input prompt: ", height=200, max_chars=1000, key="input_prompt")
num_of_alternatives = st.slider('How many alternatives to generate', 1, 5, 2)

model_choice = st.selectbox("Model", ["text-davinci-003", "gpt-3.5-turbo", "gpt-4"], index=1)

if 'resolver_response' not in st.session_state:
    st.session_state['resolver_response'] = 'nothing yet...'
    
if 'progress' not in st.session_state:
    st.session_state['progress'] = "Not run yet"

my_bar = st.progress(0, text=st.session_state['progress'])

def run_smart_gpt():
    # Add chain of thought suffix (Hebenstreit et al.) (https://arxiv.org/pdf/2305.02897.pdf)
    chain_of_thought_suffix = "Let's work this out in a step by step way to be sure we have the right answer"
    prompt = input_text + "\n\n" + chain_of_thought_suffix

    query = SimpleQuery(quiet = True, model = model_choice)
    query.append("user", prompt)

    responses = []
    for i in range(num_of_alternatives):
        st.session_state['progress'] = f"Generating alternative {i + 1} of {num_of_alternatives}"
        my_bar.progress((i + 1) / num_of_alternatives, text=st.session_state['progress'])
        response = query.run()
        print(response)
        responses.append(response)
    
    # Add Reflexion (Shinn, et al.) (https://arxiv.org/pdf/2303.11366.pdf)

    reflexion_prompt_suffix = f"You are a researcher tasked with investigating the {num_of_alternatives} response options provided. List the flaws and faulty logic of each answer option. Let's work this out in a step by step way to be sure we have all the errors:"

    reflexion_prompt = ""
    for i, response in enumerate(responses):
        reflexion_prompt += f"Answer number {i + 1}: \n{response}\n\n"

    reflexion_prompt += "\n\n" + reflexion_prompt_suffix

    print(reflexion_prompt)
    query.append("user", reflexion_prompt)

    st.session_state['progress'] = "Generating reflexion"
    my_bar.progress(0.5, text=st.session_state['progress'])
    reflexion_response = query.run()
    print(reflexion_response)
    query.append("assistant", reflexion_response)

    # Add Resolver (https://arxiv.org/pdf/2303.17071.pdf)
    resolver_prompt = f"You are a resolver tasked with:\n1) interpreting which of the {num_of_alternatives} answers the researcher thought was best\n2) Improving that answer based on the feedback and the content of other answers, and\n3) Printing the improved answer in full.\nLet's work this out in a step by step way to be sure we have the right answer:"

    query.append("user", resolver_prompt)
    
    st.session_state['progress'] = "Generating resolver response"
    my_bar.progress(0.75, text=st.session_state['progress'])
    st.session_state["resolver_response"] = query.run()
    st.session_state['progress'] = "Done!"


st.button("Run", on_click=run_smart_gpt)
st.markdown(st.session_state["resolver_response"])

