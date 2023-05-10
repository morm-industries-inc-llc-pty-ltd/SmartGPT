import json
import streamlit as st
from src.GPTInterface import SimpleQuery
from pathlib import Path
import sys



# I don't really understand this, but it fixes import errors
sys.path.append(str(Path(__file__).resolve().parent.parent))

config = {
    "Chain_of_thought_suffix": "Let's work this out in a step by step way to be sure we have the right answer"
}

# # read the config.json file
# with open("config.json", "r") as f:
#     config = json.load(f)

input_text = st.text_area("Input prompt: ", height=200, max_chars=1000, key="input_prompt")

def run_smart_gpt():
    # Add chain of thought suffix (Hebenstreit et al.) (https://arxiv.org/pdf/2305.02897.pdf)
    prompt = input_text + "\n\n" + config["Chain_of_thought_suffix"] 

    print(prompt)



st.button("Run", on_click=run_smart_gpt)
