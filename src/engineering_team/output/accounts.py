class Account:
    def __init__(self, username: str, initial_deposit: float) -> None:
        self.username = username
        self.balance = initial_deposit
        self.initial_deposit = initial_deposit
        self.portfolio = {}
        self.transactions = []

    def deposit(self, amount: float) -> None:
        self.balance += amount
        self.transactions.append({'type': 'deposit', 'amount': amount})

    def withdraw(self, amount: float) -> bool:
        if amount <= self.balance:
            self.balance -= amount
            self.transactions.append({'type': 'withdraw', 'amount': amount})
            return True
        return False

    def buy_shares(self, symbol: str, quantity: int) -> bool:
        share_price = get_share_price(symbol)
        total_cost = share_price * quantity
        if total_cost <= self.balance:
            self.balance -= total_cost
            if symbol in self.portfolio:
                self.portfolio[symbol] += quantity
            else:
                self.portfolio[symbol] = quantity
            self.transactions.append({'type': 'buy', 'symbol': symbol, 'quantity': quantity, 'cost': total_cost})
            return True
        return False

    def sell_shares(self, symbol: str, quantity: int) -> bool:
        if symbol in self.portfolio and self.portfolio[symbol] >= quantity:
            share_price = get_share_price(symbol)
            total_earning = share_price * quantity
            self.balance += total_earning
            self.portfolio[symbol] -= quantity
            if self.portfolio[symbol] == 0:
                del self.portfolio[symbol]
            self.transactions.append({'type': 'sell', 'symbol': symbol, 'quantity': quantity, 'earning': total_earning})
            return True
        return False

    def calculate_portfolio_value(self) -> float:
        total_value = 0.0
        for symbol, quantity in self.portfolio.items():
            total_value += get_share_price(symbol) * quantity
        return total_value

    def calculate_profit_loss(self) -> float:
        return (self.balance + self.calculate_portfolio_value()) - self.initial_deposit

    def get_holdings(self) -> dict:
        return self.portfolio.copy()

    def get_profit_loss(self) -> float:
        return self.calculate_profit_loss()

    def list_transactions(self) -> list:
        return self.transactions.copy()


def get_share_price(symbol: str) -> float:
    # Test prices for shares
    test_prices = {'AAPL': 150.0, 'TSLA': 700.0, 'GOOGL': 2800.0}
    return test_prices.get(symbol, 0.0)