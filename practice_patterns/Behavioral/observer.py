from abc import ABC, abstractmethod

class Subscriber(ABC):
    @abstractmethod
    def notify(self, event):
        pass


class EmailService(Subscriber):
    def notify(self, event):
        print(f"Email: {event}")


class AnalyticsService(Subscriber):
    def notify(self, event):
        print(f"Analytics: {event}")


class EventBus:
    def __init__(self):
        self.subscribers = []

    def subscribe(self, subscriber: Subscriber):
        self.subscribers.append(subscriber)

    def publish(self, event):
        for subscriber in self.subscribers:
            subscriber.notify(event)


bus = EventBus()

bus.subscribe(EmailService())
bus.subscribe(AnalyticsService())

bus.publish("ORDER_CREATED")