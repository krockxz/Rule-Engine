from fastapi.testclient import TestClient
from app.main import app  # Correctly import the app from the app.main module
import json

client = TestClient(app)

def test_create_rule():
    rule_string = "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)"
    response = client.post("/create_rule/", json={"rule_string": rule_string})
    assert response.status_code == 200
    data = response.json()
    assert "ast" in data
    assert "id" in data

def test_combine_rules():
    rule_strings = [
        "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)",
        "((age > 30 AND department = 'Marketing')) AND (salary > 20000 OR experience > 5)"
    ]
    response = client.post("/combine_rules/", json={"rule_strings": rule_strings})
    assert response.status_code == 200
    data = response.json()
    assert "combined_ast" in data

def test_evaluate_rule():
    ast_json = {
        "type": "operator",
        "value": "AND",
        "left": {
            "type": "operator",
            "value": "OR",
            "left": {
                "type": "operator",
                "value": "AND",
                "left": {"type": "operand", "value": "age"},
                "right": {"type": "operand", "value": "department"}
            },
            "right": {
                "type": "operator",
                "value": "AND",
                "left": {"type": "operand", "value": "age"},
                "right": {"type": "operand", "value": "department"}
            }
        },
        "right": {
            "type": "operator",
            "value": "OR",
            "left": {"type": "operand", "value": "salary"},
            "right": {"type": "operand", "value": "experience"}
        }
    }
    data_dict = {"age": 35, "department": "Sales", "salary": 60000, "experience": 3}
    response = client.post("/evaluate_rule/", json={"ast_json": ast_json, "data_dict": data_dict})
    assert response.status_code == 200
    data = response.json()
    assert "result" in data
    assert data["result"] == True

def test_modify_rule():
    # First, create a rule
    rule_string = "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)"
    create_response = client.post("/create_rule/", json={"rule_string": rule_string})
    assert create_response.status_code == 200
    create_data = create_response.json()
    rule_id = create_data["id"]

    # Now, modify the rule
    new_rule_string = "((age > 35 AND department = 'Sales') OR (age < 20 AND department = 'Marketing')) AND (salary > 70000 OR experience > 8)"
    modify_response = client.put(f"/modify_rule/{rule_id}", json={"rule_string": new_rule_string})
    assert modify_response.status_code == 200
    modify_data = modify_response.json()
    assert "ast" in modify_data
    assert modify_data["id"] == rule_id
