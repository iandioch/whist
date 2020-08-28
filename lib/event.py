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

class Event:
    def __init__(self, event_type, message, data):
        self.type = event_type
        self.message = message
        self.data = data

class EventLog:
    def __init__(self):
        self.events = []

    def add_event(self, event_type: EventType, message: str = None, data = None):
        event = Event(event_type, message, data)
        print(' - {}: {} ({})'.format(event.type, event.message, event.data))
        self.events.append(event)
