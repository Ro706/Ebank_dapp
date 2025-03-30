from typing import Dict
from dataclasses import dataclass

@dataclass
class BankContract:
    """
    Python implementation of the Bank.sol contract
    """
    account_balances: Dict[str, int]
    
    def __init__(self):
        self.account_balances = {}
    
    def check_balance(self, address: str) -> int:
        """Check account balance"""
        return self.account_balances.get(address, 0)
    
    def deposit(self, address: str, amount: int) -> None:
        """Deposit funds"""
        if amount <= 0:
            raise ValueError("Amount must be greater than 0")
        current = self.account_balances.get(address, 0)
        self.account_balances[address] = current + amount
    
    def withdraw(self, address: str, amount: int) -> None:
        """Withdraw funds"""
        if amount <= 0:
            raise ValueError("Amount must be greater than 0")
        if self.account_balances.get(address, 0) < amount:
            raise ValueError("Insufficient balance")
        self.account_balances[address] -= amount
    
    def transfer(self, sender: str, recipient: str, amount: int) -> None:
        """Transfer funds between accounts"""
        if amount <= 0:
            raise ValueError("Amount must be greater than 0")
        if self.account_balances.get(sender, 0) < amount:
            raise ValueError("Insufficient balance")
        if not recipient:
            raise ValueError("Invalid recipient address")
        
        self.account_balances[sender] -= amount
        self.account_balances[recipient] = self.account_balances.get(recipient, 0) + amount


# Ethereum version using web3.py
class EthereumBankContract:
    """
    Wrapper for actual Ethereum contract using web3.py
    """
    def __init__(self, contract_address, abi, provider_url):
        from web3 import Web3
        self.w3 = Web3(Web3.HTTPProvider(provider_url))
        self.contract = self.w3.eth.contract(address=contract_address, abi=abi)
    
    def check_balance(self, address):
        return self.contract.functions.checkBalance().call({'from': address})
    
    def deposit(self, address, amount):
        tx_hash = self.contract.functions.deposit(amount).transact({'from': address})
        return self.w3.eth.wait_for_transaction_receipt(tx_hash)
    
    def withdraw(self, address, amount):
        tx_hash = self.contract.functions.withdraw(amount).transact({'from': address})
        return self.w3.eth.wait_for_transaction_receipt(tx_hash)
    
    def transfer(self, sender, recipient, amount):
        tx_hash = self.contract.functions.transfer(amount, recipient).transact({'from': sender})
        return self.w3.eth.wait_for_transaction_receipt(tx_hash)