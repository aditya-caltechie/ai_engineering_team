import gradio as gr
from accounts import Account

def create_account(username, initial_deposit):
    global account
    account = Account(username, float(initial_deposit))
    return f"Account created for {username} with initial deposit of {initial_deposit}"

def deposit_funds(amount):
    account.deposit(float(amount))
    return f"Deposited: {amount}. Current Balance: {account.balance}"

def withdraw_funds(amount):
    if account.withdraw(float(amount)):
        return f"Withdrew: {amount}. Current Balance: {account.balance}"
    return "Withdrawal failed: Insufficient funds!"

def buy_shares(symbol, quantity):
    if account.buy_shares(symbol, int(quantity)):
        return f"Bought {quantity} shares of {symbol}. Current Balance: {account.balance}"
    return "Buy failed: Insufficient funds or invalid quantity!"

def sell_shares(symbol, quantity):
    if account.sell_shares(symbol, int(quantity)):
        return f"Sold {quantity} shares of {symbol}. Current Balance: {account.balance}"
    return "Sell failed: Not enough shares!"

def portfolio_value():
    return f"Total Portfolio Value: {account.calculate_portfolio_value()}"

def profit_loss():
    return f"Profit/Loss: {account.get_profit_loss()}"

def holdings():
    return f"Current Holdings: {account.get_holdings()}"

def transactions():
    return f"Transactions: {account.list_transactions()}"

with gr.Blocks() as demo:
    gr.Markdown("### Trading Account Management System")
    username = gr.Textbox(label="Username")
    initial_deposit = gr.Number(label="Initial Deposit", value=1000.0)
    gr.Button("Create Account").click(create_account, inputs=[username, initial_deposit])
    
    deposit_amount = gr.Number(label="Deposit Amount")
    gr.Button("Deposit").click(deposit_funds, inputs=deposit_amount)
    
    withdraw_amount = gr.Number(label="Withdraw Amount")
    gr.Button("Withdraw").click(withdraw_funds, inputs=withdraw_amount)
    
    buy_symbol = gr.Textbox(label="Buy Share Symbol")
    buy_quantity = gr.Number(label="Buy Quantity")
    gr.Button("Buy Shares").click(buy_shares, inputs=[buy_symbol, buy_quantity])
    
    sell_symbol = gr.Textbox(label="Sell Share Symbol")
    sell_quantity = gr.Number(label="Sell Quantity")
    gr.Button("Sell Shares").click(sell_shares, inputs=[sell_symbol, sell_quantity])
    
    gr.Button("Portfolio Value").click(portfolio_value)
    gr.Button("Profit/Loss").click(profit_loss)
    gr.Button("Current Holdings").click(holdings)
    gr.Button("Transactions").click(transactions)

if __name__ == "__main__":
    demo.launch()