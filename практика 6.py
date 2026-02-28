from abc import ABC, abstractmethod

class ICostCalculationStrategy(ABC):
    @abstractmethod
    def calculate(self, distance: float, passengers: int, service_class: str, discount_type: str) -> float:
        pass

class FlightStrategy(ICostCalculationStrategy):
    def calculate(self, distance, passengers, service_class, discount_type):
        if distance <= 0 or passengers <= 0: raise ValueError("Invalid data")
        base = distance * 50
        if service_class == "business": base *= 2.5
        if discount_type == "child": base *= 0.5
        return (base * passengers) + 5000

class TrainStrategy(ICostCalculationStrategy):
    def calculate(self, distance, passengers, service_class, discount_type):
        if distance <= 0 or passengers <= 0: raise ValueError("Invalid data")
        base = distance * 20
        if service_class == "business": base *= 1.8
        if discount_type == "pensioner": base *= 0.7
        return base * passengers

class BusStrategy(ICostCalculationStrategy):
    def calculate(self, distance, passengers, service_class, discount_type):
        if distance <= 0 or passengers <= 0: raise ValueError("Invalid data")
        base = distance * 10
        if discount_type == "child": base *= 0.4
        return base * passengers

class TravelBookingContext:
    def __init__(self):
        self._strategy = None

    def set_strategy(self, strategy: ICostCalculationStrategy):
        self._strategy = strategy

    def calculate_cost(self, distance, passengers, service_class, discount_type):
        if not self._strategy: raise ValueError("Strategy not set")
        return self._strategy.calculate(distance, passengers, service_class, discount_type)

class IObserver(ABC):
    @abstractmethod
    def update(self, stock_name: str, price: float):
        pass

class ISubject(ABC):
    @abstractmethod
    def attach(self, stock_name: str, observer: IObserver): pass
    @abstractmethod
    def detach(self, stock_name: str, observer: IObserver): pass
    @abstractmethod
    def notify(self, stock_name: str): pass

class StockExchange(ISubject):
    def __init__(self):
        self._stocks = {}
        self._subscriptions = {}

    def set_price(self, stock_name: str, price: float):
        self._stocks[stock_name] = price
        self.notify(stock_name)

    def attach(self, stock_name, observer):
        if stock_name not in self._subscriptions:
            self._subscriptions[stock_name] = []
        self._subscriptions[stock_name].append(observer)

    def detach(self, stock_name, observer):
        if stock_name in self._subscriptions:
            self._subscriptions[stock_name].remove(observer)

    def notify(self, stock_name):
        if stock_name in self._subscriptions:
            for observer in self._subscriptions[stock_name]:
                observer.update(stock_name, self._stocks[stock_name])

class Trader(IObserver):
    def __init__(self, name):
        self.name = name

    def update(self, stock_name, price):
        print(f"Trader {self.name}: {stock_name} is now {price}")

class TradingRobot(IObserver):
    def __init__(self, threshold):
        self.threshold = threshold

    def update(self, stock_name, price):
        if price < self.threshold:
            print(f"Robot: Buying {stock_name} at {price}")

if __name__ == "__main__":
    booking = TravelBookingContext()
    booking.set_strategy(FlightStrategy())
    try:
        total = booking.calculate_cost(1000, 2, "business", "child")
        print(f"Travel Cost: {total}")
    except Exception as e:
        print(e)

    exchange = StockExchange()
    trader_ali = Trader("Ali")
    bot = TradingRobot(100.0)

    exchange.attach("AAPL", trader_ali)
    exchange.attach("AAPL", bot)
    exchange.attach("TSLA", trader_ali)

    exchange.set_price("AAPL", 95.5)
    exchange.set_price("TSLA", 750.0)