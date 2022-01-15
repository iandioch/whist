from lib.event import EventListener, Event, EventType

class Listener(EventListener):
    def on_event(self, event: Event):
        print(event)
