class Broker:
    """
    Middle man between the subscriber and publisher
    """ 
    __instance = None

    def __init__(self):
        if Broker.__instance != None:
            raise Exception('Singleton broker')
        else:
            Broker.__instance = self
        self.subscribers_map = dict()

    @staticmethod
    def get_instance():
        if Broker.__instance == None:
            Broker()
        return Broker.__instance

    def push(self, topic_name, message):
        '''
            All subscribers that are subscribed to this topic will be notified of this change
        '''
        # Get all subscribers with this topic name and call the on_message_recevied
        subscribers = self.subscribers_map.get(topic_name)
        if subscribers is not None:
            for subscriber in subscribers:
                subscriber.on_message_received(message)

    def register_subscriber(self, subscriber, topic_name):
        topic = self.subscribers_map.get(topic_name)
        if topic is None:
            self.subscribers_map[topic_name] = []
            self.subscribers_map[topic_name].append(subscriber)
        else:
            self.subscribers_map[topic_name].append(subscriber)

    def deregister(self, subscriber, topic_name):
        self.subscribers_map[topic_name].pop(subscriber)