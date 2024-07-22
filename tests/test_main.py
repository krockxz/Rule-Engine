from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_rule():
    response = client.post("/create_rule/", json={"rule_string": "age > 30"})
    assert response.status_code == 200
    assert "ast" in response.json()

def test_combine_rules():
    response = client.post("/combine_rules/", json={"rule_strings": ["age > 30", "salary > 50000"]})
    assert response.status_code == 200
    assert "combined_ast" in response.json()

def test_evaluate_rule():
    ast_json = {
        "type": "operator",
        "value": "AND",
        "left": {
            "type": "operator",
            "value": ">",
            "left": {"type": "operand", "value": "age"},
            "right": {"type": "operand", "value": 30}
        },
        "right": {
            "type": "operator",
            "value": "=",
            "left": {"type": "operand", "value": "department"},
            "right": {"type": "operand", "value": "Sales"}
        }
    }
    data_dict = {"age": 35, "department": "Sales"}
    response = client.post("/evaluate_rule/", json={"ast_json": ast_json, "data_dict": data_dict})
    assert response.status_code == 200
    assert response.json()["result"] == True
