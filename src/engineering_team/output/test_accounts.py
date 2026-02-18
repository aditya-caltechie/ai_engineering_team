import unittest
from unittest.mock import patch

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
    test_prices = {'AAPL': 150.0, 'TSLA': 700.0, 'GOOGL': 2800.0}
    return test_prices.get(symbol, 0.0)

class TestAccount(unittest.TestCase):
    def setUp(self):
        self.account = Account('testuser', 1000.0)

    @patch('__main__.get_share_price')
    def test_deposit(self, mock_get_share_price):
        self.account.deposit(500.0)
        self.assertEqual(self.account.balance, 1500.0)
        self.assertEqual(len(self.account.transactions), 1)
        self.assertEqual(self.account.transactions[0], {'type': 'deposit', 'amount': 500.0})

    @patch('__main__.get_share_price')
    def test_withdraw(self, mock_get_share_price):
        self.assertTrue(self.account.withdraw(200.0))
        self.assertEqual(self.account.balance, 800.0)
        self.assertEqual(len(self.account.transactions), 1)
        self.assertEqual(self.account.transactions[0], {'type': 'withdraw', 'amount': 200.0})

    @patch('__main__.get_share_price')
    def test_buy_shares(self, mock_get_share_price):
        mock_get_share_price.return_value = 150.0
        self.assertTrue(self.account.buy_shares('AAPL', 3))
        self.assertEqual(self.account.balance, 550.0)
        self.assertEqual(self.account.portfolio['AAPL'], 3)
        self.assertEqual(len(self.account.transactions), 1)
        self.assertEqual(self.account.transactions[0], {'type': 'buy', 'symbol': 'AAPL', 'quantity': 3, 'cost': 450.0})

    @patch('__main__.get_share_price')
    def test_sell_shares(self, mock_get_share_price):
        mock_get_share_price.return_value = 150.0
        self.account.buy_shares('AAPL', 3)
        self.assertTrue(self.account.sell_shares('AAPL', 2))
        self.assertEqual(self.account.balance, 850.0)
        self.assertEqual(self.account.portfolio['AAPL'], 1)
        self.assertEqual(len(self.account.transactions), 2)
        self.assertEqual(self.account.transactions[1], {'type': 'sell', 'symbol': 'AAPL', 'quantity': 2, 'earning': 300.0})

    def test_calculate_portfolio_value(self):
        with patch('__main__.get_share_price') as mock_get_share_price:
            mock_get_share_price.side_effect = lambda symbol: 150.0 if symbol == 'AAPL' else 0.0
            self.account.buy_shares('AAPL', 3)
            self.assertEqual(self.account.calculate_portfolio_value(), 450.0)

    def test_profit_loss(self):
        self.account.deposit(500.0)
        self.account.buy_shares('AAPL', 3)
        expected_profit_loss = (self.account.balance + self.account.calculate_portfolio_value()) - self.account.initial_deposit
        self.assertEqual(self.account.calculate_profit_loss(), expected_profit_loss)

    def test_list_transactions(self):
        self.account.deposit(500.0)
        transactions = self.account.list_transactions()
        self.assertEqual(len(transactions), 1)

if __name__ == '__main__':
    unittest.main()