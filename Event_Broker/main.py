from broker import Broker
from publisher import Publisher
from subscriber import Subscriber

def subscriber_callback(message):
    print(message)

if __name__ == "__main__":

    broker = Broker.get_instance()
    broker.register_subscriber(Subscriber('firstsub', subscriber_callback), 'sample1.txt')
    broker.register_subscriber(Subscriber('secondsub', subscriber_callback), 'sample2.txt')

    directory = './sample_text_files/'

    publisher = Publisher(directory)
    publisher.track_file_changes()

