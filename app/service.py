import logging
from .entities.node import Node
import re
from typing import List, Union, Optional

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

ATTRIBUTE_CATALOG = {"age", "department", "salary", "experience"}

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
        return context[node.value] if node.value in context else node.value
    elif node.type == "operator":
        left_val = evaluate(node.left, context)
        right_val = evaluate(node.right, context)

        if node.value == "AND":
            return bool(left_val) and bool(right_val)
        elif node.value == "OR":
            return bool(left_val) or bool(right_val)
        elif node.value == ">":
            return left_val > right_val
        elif node.value == "<":
            return left_val < right_val
        elif node.value == "==":
            return left_val == right_val
        elif node.value == "!=":
            return left_val != right_val
        elif node.value == "=":
            return left_val == right_val
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
    ast_root = Node.model_validate(ast_json)
    result = evaluate(ast_root, data_dict)
    logging.debug(f"Final evaluation result: {result}")
    return result

def nodes_equal(node1, node2):
    if isinstance(node1, dict):
        node1 = Node.model_validate(node1)
    if isinstance(node2, dict):
        node2 = Node.model_validate(node2)
    
    if node1.type != node2.type or node1.value != node2.value:
        logging.debug(f"Node type or value mismatch: {node1} vs {node2}")
        return False
    if (node1.left and not node2.left) or (not node1.left and node2.left):
        logging.debug(f"Node left child mismatch: {node1.left} vs {node2.left}")
        return False
    if (node1.right and not node2.right) or (not node1.right and node2.right):
        logging.debug(f"Node right child mismatch: {node1.right} vs {node2.right}")
        return False
    if node1.left and node2.left and not nodes_equal(node1.left, node2.left):
        logging.debug(f"Node left subtree mismatch: {node1.left} vs {node2.left}")
        return False
    if node1.right and node2.right and not nodes_equal(node1.right, node2.right):
        logging.debug(f"Node right subtree mismatch: {node1.right} vs {node2.right}")
        return False
    return True


def find_node(root, target):
    logging.debug(f"Finding node: {target.to_dict() if isinstance(target, Node) else target} in {root.to_dict() if isinstance(root, Node) else root}")
    if isinstance(root, dict):
        root = Node.model_validate(root)
    if nodes_equal(root, target):
        logging.debug(f"Found matching node: {root}")
        return root
    if root.left:
        found = find_node(root.left, target)
        if found:
            return found
    if root.right:
        found = find_node(root.right, target)
        if found:
            return found
    return None


def modify_rule(node, modification_type, target_node, new_value=None):
    target_node = Node.model_validate(target_node)
    new_value = Node.model_validate(new_value) if new_value else None

    logging.debug(f"Modifying rule. Type: {modification_type}, Target Node: {target_node}, New Value: {new_value}")
    
    target = find_node(node, target_node)
    if not target:
        logging.error("Target node not found in the AST")
        raise ValueError("Target node not found in the AST")

    if modification_type == "change_operator":
        if target.type != "operator":
            logging.error("Target node is not an operator")
            raise ValueError("Target node is not an operator")
        target.value = new_value.value
        logging.debug(f"Changed operator value to: {new_value.value}")
    elif modification_type == "change_operand_value":
        if target.type != "operand":
            logging.error("Target node is not an operand")
            raise ValueError("Target node is not an operand")
        target.value = new_value.value
        logging.debug(f"Changed operand value to: {new_value.value}")
    elif modification_type == "add_sub_expression":
        if target.type != "operator":
            logging.error("Target node is not an operator")
            raise ValueError("Target node is not an operator")
        if not target.left:
            target.left = new_value
        elif not target.right:
            target.right = new_value
        else:
            logging.error("Target node already has two children")
            raise ValueError("Target node already has two children")
        logging.debug(f"Added sub-expression: {new_value}")
    elif modification_type == "remove_sub_expression":
        if target.left and nodes_equal(target.left, new_value):
            target.left = None
        elif target.right and nodes_equal(target.right, new_value):
            target.right = None
        else:
            logging.error("Sub-expression not found as a child of the target node")
            raise ValueError("Sub-expression not found as a child of the target node")
        logging.debug(f"Removed sub-expression: {new_value}")

    return node



