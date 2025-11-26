from flask import Flask, render_template, request
import random
from priorities import PRIORITY_TABLE, ALL_OPERATORS

app = Flask(__name__)

# ---------------------------
# Main page
# ---------------------------
@app.route("/")
def index():
    return render_template("index.html")


# ---------------------------
# Learning mode
# ---------------------------
@app.route("/learning")
def learning():
    op, p = random.choice(ALL_OPERATORS)
    return render_template("learning.html", op=op, priority=p)


@app.route("/learning_result", methods=["POST"])
def learning_result():
    op = request.form["op"]
    correct_priority = int(request.form["priority"])
    user_answer = request.form["answer"]

    is_correct = user_answer.isdigit() and int(user_answer) == correct_priority

    return render_template(
        "learning_result.html",
        op=op,
        correct_priority=correct_priority,
        correct=is_correct,
        table=PRIORITY_TABLE[correct_priority]
    )


# ---------------------------
# Test mode
# ---------------------------
@app.route("/test")
def test():
    op1, p1 = random.choice(ALL_OPERATORS)
    op2, p2 = random.choice(ALL_OPERATORS)
    while op1 == op2:
        op2, p2 = random.choice(ALL_OPERATORS)

    return render_template("test.html", op1=op1, p1=p1, op2=op2, p2=p2)


@app.route("/test_result", methods=["POST"])
def test_result():
    op1 = request.form["op1"]
    op2 = request.form["op2"]
    p1 = int(request.form["p1"])
    p2 = int(request.form["p2"])
    user_answer = request.form["answer"]

    # Determine the correct answer
    if p1 == p2:
        correct = 3  # same priority
    elif p1 < p2:
        correct = 1
    else:
        correct = 2

    is_correct = (user_answer == str(correct))

    # Get operator descriptions
    op1_info = next(item for item in PRIORITY_TABLE[p1] if item[0] == op1)
    op2_info = next(item for item in PRIORITY_TABLE[p2] if item[0] == op2)

    return render_template(
        "test_result.html",
        op1=op1, p1=p1, info1=op1_info,
        op2=op2, p2=p2, info2=op2_info,
        correct=correct,
        is_correct=is_correct
    )

# ---------------------------
# Сheck mode
# ---------------------------
@app.route("/check")
def check():
    return render_template("check.html")

@app.route("/check_result", methods=["POST"])
def check_result():
    op1 = request.form["op1"].strip()
    op2 = request.form["op2"].strip()

    # List of operators that have ambiguous forms
    AMBIGUOUS = {
        "++": ["++ (префіксний)", "++ (постфіксний)"],
        "--": ["-- (префіксний)", "-- (постфіксний)"],
        "+":  ["+ (унарний)", "+ (бінарний)"],
        "-":  ["- (унарний)", "- (бінарний)"],
    }

    # Collect ambiguous operators
    ambiguous_ops = {}

    if op1 in AMBIGUOUS:
        ambiguous_ops["op1"] = AMBIGUOUS[op1]

    if op2 in AMBIGUOUS:
        ambiguous_ops["op2"] = AMBIGUOUS[op2]

    # If there are ambiguous operators, ask user to disambiguate
    if ambiguous_ops:
        return render_template(
            "check_disambiguate.html",
            op1=op1,
            op2=op2,
            ambiguous=ambiguous_ops
        )

    # If no ambiguities, perform the check directly
    return perform_check(op1, op2)

def perform_check(op1, op2):

    def find_operator_info(operator):
        for p, lst in PRIORITY_TABLE.items():
            for name, desc, ex in lst:
                if operator == name:
                    return p, (name, desc, ex)
        return None, None

    p1, info1 = find_operator_info(op1)
    p2, info2 = find_operator_info(op2)

    errors = []
    if p1 is None:
        errors.append(f"Оператор '{op1}' не знайдено")
    if p2 is None:
        errors.append(f"Оператор '{op2}' не знайдено")

    if errors:
        return render_template("check_result.html", errors=errors)

    if p1 == p2:
        result = 3
    elif p1 < p2:
        result = 1
    else:
        result = 2

    return render_template(
        "check_result.html",
        op1=op1, p1=p1, info1=info1,
        op2=op2, p2=p2, info2=info2,
        result=result
    )

@app.route("/check_final", methods=["POST"])
def check_final():
    op1 = request.form["op1"]
    op2 = request.form["op2"]
    return perform_check(op1, op2)

if __name__ == "__main__":
    app.run(debug=True)
