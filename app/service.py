import logging
from node import Node
import re
from typing import List, Union, Optional

# Initialize logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Predefined catalog for validation
ATTRIBUTE_CATALOG = {"age", "department", "salary"}

def validate_attribute(attribute: str):
    if attribute not in ATTRIBUTE_CATALOG:
        raise ValueError(f"Invalid attribute: {attribute}")

def tokenize(expression: str) -> List[str]:
    # Capture string literals correctly and separate identifiers and operators
    tokens = re.findall(r'\bAND\b|\bOR\b|>=|<=|!=|==|>|<|=|\'[^\']+\'|"[^"]+"|\d+|\b\w+\b|\(|\)', expression)
    logging.debug(f"Tokenized '{expression}' into {tokens}")
    return tokens

def parse_rule(rule_str: str):
    try:
        precedence = {'>': 3, '<': 3, '==': 3, '!=': 3, '=': 3, 'AND': 2, 'OR': 1}
        op_stack = []
        output = []
        tokens = tokenize(rule_str)

        for token in tokens:
            logging.debug(f"Processing token: {token}")
            if token.isdigit():
                output.append(Node(type="operand", value=int(token)))
            elif token.startswith("'") and token.endswith("'"):
                output.append(Node(type="operand", value=token.strip("'")))
            elif token.isidentifier() and token not in precedence:
                validate_attribute(token)
                output.append(Node(type="operand", value=token))
            elif token in precedence:
                while op_stack and op_stack[-1] != '(' and precedence[op_stack[-1]] >= precedence[token]:
                    process_operator(op_stack, output)
                op_stack.append(token)
            elif token == '(':
                op_stack.append(token)
            elif token == ')':
                while op_stack and op_stack[-1] != '(':
                    process_operator(op_stack, output)
                op_stack.pop()

        while op_stack:
            process_operator(op_stack, output)

        logging.debug(f"Final AST Output: {output[0] if output else 'No output'}")
        return output[0] if output else None
    except Exception as e:
        logging.error(f"Failed to parse rule: {e}")
        raise

def process_operator(op_stack, output):
    operator = op_stack.pop()
    if len(output) < 2:
        logging.error(f"Not enough operands for operator {operator}")
        return
    
    right = output.pop()
    left = output.pop()
    
    new_node = Node(type="operator", value=operator, left=left, right=right)
    output.append(new_node)
    logging.debug(f"Processed operator: {operator}, formed node: {new_node}")

def evaluate(node, context):
    logging.debug(f"Evaluating node: {node}")
    if node.type == "operand":
        if isinstance(node.value, int):
            return node.value
        value = context.get(node.value, node.value)
        if isinstance(value, str):
            eval_string = f"'{value}'"
        else:
            eval_string = str(value)
        return eval(eval_string)
    elif node.type == "operator":
        left_val = evaluate(node.left, context)
        right_val = evaluate(node.right, context)
        if node.value == "AND":
            result = left_val and right_val
        elif node.value == "OR":
            result = left_val or right_val
        elif node.value == ">":
            result = left_val > right_val
        elif node.value == "<":
            result = left_val < right_val
        elif node.value == "==":
            result = left_val == right_val
        elif node.value == "!=":
            result = left_val != right_val
        elif node.value == "=":
            result = left_val == right_val
        logging.debug(f"Evaluation result: {result}")
        return result
    return False

def combine_rules(rule_strings: List[str]):
    parsed_rules = [parse_rule(rule) for rule in rule_strings]
    if not parsed_rules:
        return None
    if len(parsed_rules) == 1:
        return parsed_rules[0]
    root = parsed_rules[0]
    for rule in parsed_rules[1:]:
        root = Node(type="operator", value="AND", left=root, right=rule)
    logging.debug(f"Combined AST root: {root}")
    return root

def evaluate_rule(ast_json, data_dict):
    ast_root = Node.parse_obj(ast_json)
    result = evaluate(ast_root, data_dict)
    logging.debug(f"Final evaluation result: {result}")
    return result
