# Rule Engine

This project provides a rule engine that allows you to create, combine, evaluate, and modify rules.

## Setup and Installation

### Prerequisites

- Python 3.8+
- Virtual Environment (venv)
- MongoDB (with credentials)

### Clone the Repository

```bash
git clone https://github.com/krockxz/Rule-Engine.git
cd rule-engine
```

### Create and Activate Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the root directory with the following content:

```env
MONGO_USER=kunal
MONGO_PASSWORD=EhSuFjXAY2NiKoQw
```

### Start the FastAPI Server

```bash
uvicorn app.main:app --reload
```

### Start Streamlit UI

```bash
streamlit run app.py
```

## Usage

### CURL Commands

#### 1. **Create Rule:**

```bash
curl -X POST "http://127.0.0.1:8000/create_rule/" -H "Content-Type: application/json" -d '{"rule_string": "((age > 30 AND department = '\''Sales'\'') OR (age < 25 AND department = '\''Marketing'\'')) AND (salary > 50000 OR experience > 5)"}'
```

To use this in the Streamlit UI, enter the rule string in the "Create Rule" section and click "Create Rule".

#### 2. **Combine Rules:**

```bash
curl -X POST "http://127.0.0.1:8000/combine_rules/" -H "Content-Type: application/json" -d '{"rule_strings": ["((age > 30 AND department = '\''Sales'\'') OR (age < 25 AND department = '\''Marketing'\'')) AND (salary > 50000 OR experience > 5)", "((age > 30 AND department = '\''Marketing'\'')) AND (salary > 20000 OR experience > 5)"]}'
```

To use this in the Streamlit UI, enter the rule strings (one per line) in the "Combine Rules" section and click "Combine Rules".

#### 3. **Evaluate Rule:**

```bash
curl -X POST "http://127.0.0.1:8000/evaluate_rule/" -H "Content-Type: application/json" -d '{"ast_json": {"type": "operator", "value": "AND", "left": {"type": "operator", "value": "OR", "left": {"type": "operator", "value": "AND", "left": {"type": "operand", "value": "age"}, "right": {"type": "operand", "value": "department"}}, "right": {"type": "operator", "value": "AND", "left": {"type": "operand", "value": "age"}, "right": {"type": "operand", "value": "department"}}}, "right": {"type": "operator", "value": "OR", "left": {"type": "operand", "value": "salary"}, "right": {"type": "operand", "value": "experience"}}}, "data_dict": {"age": 35, "department": "Sales", "salary": 60000, "experience": 3}}'
```

To use this in the Streamlit UI, enter the AST JSON and Data Dict JSON in the "Evaluate Rule" section and click "Evaluate Rule".

#### 4. **Modify Rule:**

```bash
curl --location --request PUT 'http://127.0.0.1:8000/modify_rule/{rule_id}' \
--header 'Content-Type: application/json' \
--data '{
    "modification_type": "change_operator",
    "target_node": {
        "type": "operator",
        "value": ">",
        "left": {
            "type": "operand",
            "value": "age",
            "left": null,
            "right": null
        },
        "right": {
            "type": "operand",
            "value": 30,
            "left": null,
            "right": null
        }
    },
    "new_value": {
        "type": "operator",
        "value": "="
    }
}'
```

Replace `{rule_id}` with the actual rule ID you wish to modify.

To use this in the Streamlit UI, enter the Rule ID, select the Modification Type, enter the Target Node JSON, and optionally the New Value JSON in the "Modify Rule" section, and click "Modify Rule".

## Design Choices

### Rule Engine Design

1. **AST (Abstract Syntax Tree)**:
   - The rule engine uses an AST to represent rules. This allows for flexible parsing and evaluation of complex rules.

2. **Tokenization and Parsing**:
   - The engine tokenizes the rule string and parses it into an AST. This ensures that the rule structure is preserved and can be easily manipulated or evaluated.

3. **User-Defined Functions**:
   - The system supports user-defined functions, which can be registered and used within rules. This allows for advanced custom logic to be incorporated into rules.

### MongoDB

1. **Schema Flexibility**:
   - MongoDB's schema-less nature allows us to store rules and their ASTs without a fixed schema. This is beneficial as the structure of rules can vary significantly.

2. **Ease of Use**:
   - MongoDB's document model is intuitive and aligns well with the JSON format used for rules and ASTs.

   ### Run tests

```bash
pytest tests/test_main.py
```
