from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from typing import List, Dict
from service import parse_rule, combine_rules, evaluate_rule
from node import Node  # Ensure this import is correct
from mongo import rules_collection  # Ensure this import is correct
from bson import ObjectId  # Import ObjectId to handle MongoDB IDs

app = FastAPI()

class RuleInput(BaseModel):
    rule_string: str

class RulesInput(BaseModel):
    rule_strings: List[str]

class EvaluationInput(BaseModel):
    ast_json: Dict
    data_dict: Dict

@app.post("/create_rule/")
def api_create_rule(input: RuleInput):
    try:
        ast = parse_rule(input.rule_string)
        if ast is None:
            raise ValueError("Failed to parse rule. Check the rule syntax.")
        result = rules_collection.insert_one({"rule_string": input.rule_string, "ast": ast.to_dict()})
        return {"ast": ast.to_dict(), "id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/combine_rules/")
def api_combine_rules(input: RulesInput):
    try:
        combined_ast = combine_rules(input.rule_strings)
        return {"combined_ast": combined_ast.to_dict()} 
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/evaluate_rule/")
def api_evaluate_rule(input: EvaluationInput):
    try:
        result = evaluate_rule(input.ast_json, input.data_dict)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/modify_rule/{rule_id}")
def api_modify_rule(rule_id: str, input: RuleInput):
    try:
        # Convert the rule_id to an ObjectId
        rule_id = ObjectId(rule_id)
        
        existing_rule = rules_collection.find_one({"_id": rule_id})
        if not existing_rule:
            raise HTTPException(status_code=404, detail="Rule not found")
        
        existing_ast = Node.parse_obj(existing_rule["ast"])
        new_ast = parse_rule(input.rule_string)

        existing_rule["ast"] = new_ast.to_dict()
        rules_collection.replace_one({"_id": rule_id}, existing_rule)
        
        return {"ast": new_ast.to_dict(), "id": str(rule_id)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
