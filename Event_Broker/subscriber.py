class Subscriber:
    """
    subscribers express interest in one or more classes and only receive messages that are of interest, 
    without knowledge of which publishers, if any, there are.
    """

    def __init__(self, name, callback):
        self.name = name
        self.callback = callback

    def on_message_received(self, message):
        self.callback(message)

