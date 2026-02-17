import unittest

class Account:
    def __init__(self, username: str, initial_deposit: float) -> None:
        self.username = username
        self.initial_deposit = initial_deposit
        self.balance = initial_deposit
        self.holdings = {}
        self.transactions = []

    def deposit_funds(self, amount: float) -> None:
        self.balance += amount
        self._create_transaction('deposit', amount=amount)

    def withdraw_funds(self, amount: float) -> bool:
        if amount <= self.balance:
            self.balance -= amount
            self._create_transaction('withdraw', amount=amount)
            return True
        return False

    def buy_shares(self, symbol: str, quantity: int) -> bool:
        total_cost = get_share_price(symbol) * quantity
        if total_cost <= self.balance:
            self.balance -= total_cost
            if symbol in self.holdings:
                self.holdings[symbol] += quantity
            else:
                self.holdings[symbol] = quantity
            self._create_transaction('buy', symbol=symbol, quantity=quantity, amount=total_cost)
            return True
        return False

    def sell_shares(self, symbol: str, quantity: int) -> bool:
        if symbol in self.holdings and self.holdings[symbol] >= quantity:
            total_income = get_share_price(symbol) * quantity
            self.holdings[symbol] -= quantity
            if self.holdings[symbol] == 0:
                del self.holdings[symbol]
            self.balance += total_income
            self._create_transaction('sell', symbol=symbol, quantity=quantity, amount=total_income)
            return True
        return False

    def calculate_portfolio_value(self) -> float:
        return self.balance + self._calculate_value_of_holdings()

    def calculate_profit_loss(self) -> float:
        return self.calculate_portfolio_value() - self.initial_deposit

    def report_holdings(self) -> dict:
        return self.holdings

    def report_transactions(self) -> list:
        return self.transactions

    def _create_transaction(self, type: str, symbol: str = '', quantity: int = 0, amount: float = 0.0) -> None:
        self.transactions.append({'type': type, 'symbol': symbol, 'quantity': quantity, 'amount': amount})

    def _calculate_value_of_holdings(self) -> float:
        return sum(get_share_price(symbol) * quantity for symbol, quantity in self.holdings.items())


def get_share_price(symbol: str) -> float:
    prices = {'AAPL': 150.0, 'TSLA': 700.0, 'GOOGL': 2800.0}
    return prices.get(symbol, 0.0)


class TestAccount(unittest.TestCase):
    def setUp(self):
        self.account = Account('test_user', 1000.0)

    def test_initial_balance(self):
        self.assertEqual(self.account.balance, 1000.0)

    def test_deposit_funds(self):
        self.account.deposit_funds(500.0)
        self.assertEqual(self.account.balance, 1500.0)

    def test_withdraw_funds_success(self):
        result = self.account.withdraw_funds(300.0)
        self.assertTrue(result)
        self.assertEqual(self.account.balance, 700.0)

    def test_withdraw_funds_failure(self):
        result = self.account.withdraw_funds(2000.0)
        self.assertFalse(result)
        self.assertEqual(self.account.balance, 1000.0)

    def test_buy_shares_success(self):
        result = self.account.buy_shares('AAPL', 2)
        self.assertTrue(result)
        self.assertEqual(self.account.balance, 700.0)
        self.assertEqual(self.account.holdings['AAPL'], 2)

    def test_buy_shares_failure(self):
        result = self.account.buy_shares('AAPL', 10)
        self.assertFalse(result)
        self.assertEqual(self.account.balance, 1000.0)

    def test_sell_shares_success(self):
        self.account.buy_shares('AAPL', 2)
        result = self.account.sell_shares('AAPL', 1)
        self.assertTrue(result)
        self.assertEqual(self.account.balance, 850.0)
        self.assertEqual(self.account.holdings['AAPL'], 1)

    def test_sell_shares_failure(self):
        result = self.account.sell_shares('AAPL', 2)
        self.assertFalse(result)

    def test_calculate_portfolio_value(self):
        self.account.buy_shares('AAPL', 2)
        self.assertEqual(self.account.calculate_portfolio_value(), 700.0 + 300.0)

    def test_calculate_profit_loss(self):
        self.account.deposit_funds(500.0)
        self.account.buy_shares('AAPL', 2)
        self.assertEqual(self.account.calculate_profit_loss(), (700.0 + 300.0) - 1000.0)

    def test_report_holdings(self):
        self.account.buy_shares('AAPL', 2)
        self.assertEqual(self.account.report_holdings(), {'AAPL': 2})

    def test_report_transactions(self):
        self.account.deposit_funds(500.0)
        self.account.withdraw_funds(200.0)
        transactions = self.account.report_transactions()
        self.assertEqual(len(transactions), 2)

if __name__ == '__main__':
    unittest.main()