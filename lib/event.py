from enum import Enum, auto


class EventType(Enum):
    NEW_GAME = auto()
    NEW_ROUND = auto()
    NEW_TRUMP_CARD = auto()
    TURN_CHANGED = auto()
    DEAL = auto()
    CARD_PLAYED = auto()
    HAND_FINISHED = auto()
    ROUND_FINISHED = auto()
    BID_MADE = auto()


class Event:

    def __init__(self, event_type, message, data):
        self.type = event_type
        self.message = message
        self.data = data


class EventListener:
    def on_event(event: Event):
        pass


class EventLog:

    def __init__(self):
        self.events = []
        self.listeners = []

    def add_event(self, event_type: EventType, message: str = None, data=None):
        event = Event(event_type, message, data)
        print(' - {}: {} ({})'.format(event.type, event.message, event.data))
        self.events.append(event)
        for listener in self.listeners:
            listener.on_event(event)

    def add_event_listener(self, listener: EventListener):
        self.listeners.append(listener)


