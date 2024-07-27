from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from typing import List, Dict, Optional  
from app.service import parse_rule, combine_rules, evaluate_rule, modify_rule
from .entities.node import Node
from .connection.mongo import rules_collection  
from bson import ObjectId  

app = FastAPI()

class RuleInput(BaseModel):
    rule_string: str

class RulesInput(BaseModel):
    rule_strings: List[str]

class EvaluationInput(BaseModel):
    ast_json: Dict
    data_dict: Dict

class ModifyInput(BaseModel):
    modification_type: str
    target_node: Dict
    new_value: Optional[Dict] = None

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
def api_modify_rule(rule_id: str, input: ModifyInput):
    try:
        rule_id = ObjectId(rule_id)
        
        existing_rule = rules_collection.find_one({"_id": rule_id})
        if not existing_rule:
            raise HTTPException(status_code=404, detail="Rule not found")
        
        existing_ast = Node.model_validate(existing_rule["ast"])
        
        modified_ast = modify_rule(existing_ast, input.modification_type, input.target_node, input.new_value)
        existing_rule["ast"] = modified_ast.to_dict()
        rules_collection.replace_one({"_id": rule_id}, existing_rule)
        
        return {"ast": modified_ast.to_dict(), "id": str(rule_id)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
