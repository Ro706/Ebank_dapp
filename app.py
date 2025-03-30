from flask import Flask, request, jsonify, render_template
from bank_contract import BankContract
import json

app = Flask(__name__)
bank = BankContract()

# For demo purposes - in production use proper authentication
current_user = "user1"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/balance', methods=['GET'])
def get_balance():
    balance = bank.check_balance(current_user)
    return jsonify({"balance": balance})

@app.route('/deposit', methods=['POST'])
def deposit():
    data = request.get_json()
    amount = data.get('amount', 0)
    try:
        bank.deposit(current_user, amount)
        return jsonify({"status": "success"})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/withdraw', methods=['POST'])
def withdraw():
    data = request.get_json()
    amount = data.get('amount', 0)
    try:
        bank.withdraw(current_user, amount)
        return jsonify({"status": "success"})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/transfer', methods=['POST'])
def transfer():
    data = request.get_json()
    amount = data.get('amount', 0)
    recipient = data.get('recipient', '')
    try:
        bank.transfer(current_user, recipient, amount)
        return jsonify({"status": "success"})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)