📘 C++ Operator Precedence Trainer

An interactive web-based trainer designed to help developers learn and practice C++ operator precedence — a common topic in technical interviews and an essential part of mastering expression evaluation in C++.

Use the live version here:
👉 https://operator-trainer.onrender.com/

# Features
## Learning Mode
A random operator is shown
You must choose its precedence level
Full explanation is displayed afterwards:
  * operator description
  * precedence group
  * usage example

## Test Mode
Two random operators are shown
You choose which operator has higher precedence (or if they are equal)
Detailed explanations for both operators are provided 

## Check Mode
Enter any two operators manually
The trainer compares them and displays:
  * which one has higher precedence
  * operator description and examples

## Theory Page
A complete, structured table of ==all C++ operators grouped by precedence==
Mobile-friendly and formatted for quick reference

# Running Locally
```bash
git clone https://github.com/Antkom777/operator-trainer.git
cd operator-trainer
pip install -r requirements.txt
python app.py
```

The app will be available at:
```bash
http://127.0.0.1:5000/
```