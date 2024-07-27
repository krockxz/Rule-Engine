# Rule Engine

This project provides a rule engine that allows you to create, combine, evaluate, and modify rules.

## Setup and Installation

### Prerequisites

- Python 3.8+
- Virtual Environment (venv)
- MongoDB (with credentials)

### Clone the Repository

```bash
git clone https://github.com/your-repo/rule-engine.git
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

#### 2. **Combine Rules:**

```bash
curl -X POST "http://127.0.0.1:8000/combine_rules/" -H "Content-Type: application/json" -d '{"rule_strings": ["((age > 30 AND department = '\''Sales'\'') OR (age < 25 AND department = '\''Marketing'\'')) AND (salary > 50000 OR experience > 5)", "((age > 30 AND department = '\''Marketing'\'')) AND (salary > 20000 OR experience > 5)"]}'
```

#### 3. **Evaluate Rule:**

```bash
curl -X POST "http://127.0.0.1:8000/evaluate_rule/" -H "Content-Type: application/json" -d '{"ast_json": {"type": "operator", "value": "AND", "left": {"type": "operator", "value": "OR", "left": {"type": "operator", "value": "AND", "left": {"type": "operand", "value": "age"}, "right": {"type": "operand", "value": "department"}}, "right": {"type": "operator", "value": "AND", "left": {"type": "operand", "value": "age"}, "right": {"type": "operand", "value": "department"}}}, "right": {"type": "operator", "value": "OR", "left": {"type": "operand", "value": "salary"}, "right": {"type": "operand", "value": "experience"}}}, "data_dict": {"age": 35, "department": "Sales", "salary": 60000, "experience": 3}}'
```

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
