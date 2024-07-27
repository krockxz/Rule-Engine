uvicorn main:app --reload
streamlit run app.py

Now you can test the API endpoints again using `curl` with the updated `evaluate` function.

1. **Create Rule:**
   ```bash
   curl -X POST "http://127.0.0.1:8000/create_rule/" -H "Content-Type: application/json" -d '{"rule_string": "((age > 30 AND department = '\''Sales'\'') OR (age < 25 AND department = '\''Marketing'\'')) AND (salary > 50000 OR experience > 5)"}'
   ```

2. **Combine Rules:**
   ```bash
   curl -X POST "http://127.0.0.1:8000/combine_rules/" -H "Content-Type: application/json" -d '{"rule_strings": ["((age > 30 AND department = '\''Sales'\'') OR (age < 25 AND department = '\''Marketing'\'')) AND (salary > 50000 OR experience > 5)", "((age > 30 AND department = '\''Marketing'\'')) AND (salary > 20000 OR experience > 5)"]}'
   ```

3. **Evaluate Rule:**
   ```bash
   curl -X POST "http://127.0.0.1:8000/evaluate_rule/" -H "Content-Type: application/json" -d '{"ast_json": {"type": "operator", "value": "AND", "left": {"type": "operator", "value": "OR", "left": {"type": "operator", "value": "AND", "left": {"type": "operand", "value": "age"}, "right": {"type": "operand", "value": "department"}}, "right": {"type": "operator", "value": "AND", "left": {"type": "operand", "value": "age"}, "right": {"type": "operand", "value": "department"}}}, "right": {"type": "operator", "value": "OR", "left": {"type": "operand", "value": "salary"}, "right": {"type": "operand", "value": "experience"}}}, "data_dict": {"age": 35, "department": "Sales", "salary": 60000, "experience": 3}}'
   ```