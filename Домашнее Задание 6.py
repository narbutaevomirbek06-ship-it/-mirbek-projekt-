from abc import ABC, abstractmethod

class IPaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: float):
        pass

class CreditCardPayment(IPaymentStrategy):
    def pay(self, amount):
        print(f"Оплата картой: {amount}")

class PayPalPayment(IPaymentStrategy):
    def pay(self, amount):
        print(f"Оплата PayPal: {amount}")

class CryptoPayment(IPaymentStrategy):
    def pay(self, amount):
        print(f"Оплата криптовалютой: {amount}")

class PaymentContext:
    def __init__(self):
        self._strategy = None

    def set_strategy(self, strategy: IPaymentStrategy):
        self._strategy = strategy

    def execute_payment(self, amount: float):
        if self._strategy:
            self._strategy.pay(amount)
        else:
            print("Ошибка: Стратегия не выбрана")

class IObserver(ABC):
    @abstractmethod
    def update(self, rate: float):
        pass

class ISubject(ABC):
    @abstractmethod
    def attach(self, observer: IObserver): pass
    @abstractmethod
    def detach(self, observer: IObserver): pass
    @abstractmethod
    def notify(self): pass

class CurrencyExchange(ISubject):
    def __init__(self):
        self._observers = []
        self._usd_rate = 0.0

    @property
    def usd_rate(self):
        return self._usd_rate

    @usd_rate.setter
    def usd_rate(self, value):
        self._usd_rate = value
        self.notify()

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self):
        for observer in self._observers:
            observer.update(self._usd_rate)

class Bank(IObserver):
    def update(self, rate):
        print(f"Банк уведомлен: {rate}")

class Broker(IObserver):
    def update(self, rate):
        print(f"Брокер получил курс: {rate}")

class NewsAgency(IObserver):
    def update(self, rate):
        print(f"Новости: Курс USD {rate}")

if __name__ == "__main__":
    payment_context = PaymentContext()
    
    choice = input("1-Card, 2-PayPal, 3-Crypto: ")
    strategies = {"1": CreditCardPayment(), "2": PayPalPayment(), "3": CryptoPayment()}
    
    payment_context.set_strategy(strategies.get(choice))
    payment_context.execute_payment(1000.0)

    print("-" * 20)

    exchange = CurrencyExchange()
    bank = Bank()
    broker = Broker()
    news = NewsAgency()

    exchange.attach(bank)
    exchange.attach(broker)
    exchange.attach(news)

    exchange.usd_rate = 450.5
    
    exchange.detach(broker)
    exchange.usd_rate = 455.0