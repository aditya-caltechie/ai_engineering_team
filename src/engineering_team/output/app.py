import gradio as gr
from accounts import Account, get_share_price

account = None

def create_account(username, initial_deposit):
    global account
    account = Account(username, float(initial_deposit))
    return f"Account created for {username} with initial deposit of ${initial_deposit}"

def deposit(amount):
    if account:
        account.deposit_funds(float(amount))
        return f"Deposited ${amount}. New balance: ${account.balance:.2f}"
    return "No account created."

def withdraw(amount):
    if account:
        if account.withdraw_funds(float(amount)):
            return f"Withdrew ${amount}. New balance: ${account.balance:.2f}"
        return "Withdrawal failed. Insufficient funds."
    return "No account created."

def buy_shares(symbol, quantity):
    if account:
        if account.buy_shares(symbol, int(quantity)):
            return f"Bought {quantity} shares of {symbol}. New holdings: {account.holdings}"
        return "Purchase failed. Insufficient funds or invalid quantity."
    return "No account created."

def sell_shares(symbol, quantity):
    if account:
        if account.sell_shares(symbol, int(quantity)):
            return f"Sold {quantity} shares of {symbol}. New holdings: {account.holdings}"
        return "Sale failed. Insufficient shares or invalid quantity."
    return "No account created."

def report_holdings():
    if account:
        return account.report_holdings()
    return "No account created."

def report_value():
    if account:
        return f"Total portfolio value: ${account.calculate_portfolio_value():.2f}, Profit/Loss: ${account.calculate_profit_loss():.2f}"
    return "No account created."

def report_transactions():
    if account:
        return account.report_transactions()
    return "No account created."

iface = gr.Interface(
    fn=create_account,
    inputs=["text", "number"],
    outputs="text",
    title="Trading Account Management",
    description="Create an account and manage deposits, withdrawals, and shares."
)

iface.add_component(gr.Interface(
    fn=deposit,
    inputs="number",
    outputs="text",
    title="Deposit Funds"
))

iface.add_component(gr.Interface(
    fn=withdraw,
    inputs="number",
    outputs="text",
    title="Withdraw Funds"
))

iface.add_component(gr.Interface(
    fn=buy_shares,
    inputs=["text", "number"],
    outputs="text",
    title="Buy Shares"
))

iface.add_component(gr.Interface(
    fn=sell_shares,
    inputs=["text", "number"],
    outputs="text",
    title="Sell Shares"
))

iface.add_component(gr.Interface(
    fn=report_holdings,
    inputs=None,
    outputs="json",
    title="Report Holdings"
))

iface.add_component(gr.Interface(
    fn=report_value,
    inputs=None,
    outputs="text",
    title="Report Portfolio Value"
))

iface.add_component(gr.Interface(
    fn=report_transactions,
    inputs=None,
    outputs="json",
    title="Report Transactions"
))

iface.launch()