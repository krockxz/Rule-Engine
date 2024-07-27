import streamlit as st
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def create_rule(rule_string):
    response = requests.post(f"{BASE_URL}/create_rule/", json={"rule_string": rule_string})
    return response.json()

def combine_rules(rule_strings):
    response = requests.post(f"{BASE_URL}/combine_rules/", json={"rule_strings": rule_strings})
    return response.json()

def evaluate_rule(ast_json, data_dict):
    response = requests.post(f"{BASE_URL}/evaluate_rule/", json={"ast_json": ast_json, "data_dict": data_dict})
    return response.json()

def modify_rule(rule_id, modification_type, target_node, new_value=None):
    payload = {
        "modification_type": modification_type,
        "target_node": target_node,
        "new_value": new_value
    }
    response = requests.put(f"{BASE_URL}/modify_rule/{rule_id}", json=payload)
    return response.json()

st.title("Rule Engine UI")

st.header("Create Rule")
rule_string = st.text_area("Enter Rule String")
if st.button("Create Rule"):
    result = create_rule(rule_string)
    st.json(result)

st.header("Combine Rules")
rule_strings = st.text_area("Enter Rule Strings (one per line)").splitlines()
if st.button("Combine Rules"):
    result = combine_rules(rule_strings)
    st.json(result)

st.header("Evaluate Rule")
ast_json = st.text_area("Enter AST JSON")
data_dict = st.text_area("Enter Data Dict JSON")
if st.button("Evaluate Rule"):
    try:
        ast_json = json.loads(ast_json)
        data_dict = json.loads(data_dict)
        result = evaluate_rule(ast_json, data_dict)
        st.json(result)
    except json.JSONDecodeError as e:
        st.error(f"Invalid JSON format: {e}")

st.header("Modify Rule")
rule_id = st.text_input("Enter Rule ID")
modification_type = st.selectbox("Select Modification Type", ["change_operator", "change_operand_value", "add_sub_expression", "remove_sub_expression"])
target_node = st.text_area("Enter Target Node JSON")
new_value = st.text_area("Enter New Value JSON (if applicable)")
if st.button("Modify Rule"):
    try:
        target_node = json.loads(target_node)
        new_value = json.loads(new_value) if new_value else None
        result = modify_rule(rule_id, modification_type, target_node, new_value)
        st.json(result)
    except json.JSONDecodeError as e:
        st.error(f"Invalid JSON format: {e}")
