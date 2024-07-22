import streamlit as st
import requests
import json

api_base_url = "http://127.0.0.1:8000"

st.title("Rule Engine UI")

# Function to create a rule
def create_rule(rule_string):
    response = requests.post(f"{api_base_url}/create_rule/", json={"rule_string": rule_string})
    return response.json()

# Function to combine rules
def combine_rules(rule_strings):
    response = requests.post(f"{api_base_url}/combine_rules/", json={"rule_strings": rule_strings})
    return response.json()

# Function to evaluate a rule
def evaluate_rule(ast_json, data_dict):
    response = requests.post(f"{api_base_url}/evaluate_rule/", json={"ast_json": ast_json, "data_dict": data_dict})
    return response.json()

# Create Rule Section
st.header("Create Rule")
rule_string = st.text_area("Enter Rule String", "")
if st.button("Create Rule"):
    if rule_string:
        result = create_rule(rule_string)
        st.json(result)
    else:
        st.error("Please enter a rule string.")

# Combine Rules Section
st.header("Combine Rules")
rule_strings = st.text_area("Enter Rule Strings (one per line)", "").split("\n")
if st.button("Combine Rules"):
    if rule_strings:
        result = combine_rules(rule_strings)
        st.json(result)
    else:
        st.error("Please enter rule strings.")

# Evaluate Rule Section
st.header("Evaluate Rule")
ast_json = st.text_area("Enter AST JSON", "")
data_dict = st.text_area("Enter Data Dict JSON", "")
if st.button("Evaluate Rule"):
    if ast_json and data_dict:
        try:
            ast_json = json.loads(ast_json)
            data_dict = json.loads(data_dict)
            result = evaluate_rule(ast_json, data_dict)
            st.json(result)
        except json.JSONDecodeError:
            st.error("Please enter valid JSON.")
    else:
        st.error("Please enter both AST JSON and Data Dict JSON.")
