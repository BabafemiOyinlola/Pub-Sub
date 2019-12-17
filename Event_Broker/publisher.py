import time
import difflib
from os import listdir, path
from broker import Broker


class Publisher:
    """
    This class sends messages but not to a specific subscriber instead, 
    categorize published messages into classes without knowledge of which subscribers,
    """

    def __init__(self, directory):
        self.broker = Broker.get_instance()
        self.directory = directory
        self.topics = []

    def publish(self, topic_name, message):
        self.broker.push(topic_name, message)

    def track_file_changes(self):
        '''
        tracks changes in files in a  directory
        '''
        folder = self.directory
        files = [i for i in listdir(folder) if path.isfile(path.join(folder, i))]
        file_descriptor = {}
        files_changed = {}
    
        while len(file_descriptor) != len(files):
            for i in files:
                f = path.join(folder, i)
                details = []
                content = ''
                with open(f, 'r') as opened_file:
                    content = opened_file.read()
                
                details.append({'last_changed': time.ctime(path.getmtime(f)), 
                                'content': content,
                                'difference': 'No difference'})

                filename = path.basename(f)
                file_descriptor[filename] = details

        while True:
            for key in file_descriptor:
                f = path.join(folder, key)
                last_modified = time.ctime(path.getmtime(f))
                if last_modified != file_descriptor[key][0]['last_changed']:
                    files_changed[key] = file_descriptor[key]

                    new_content = ''
                    with open(f, 'r') as opened_file:
                        new_content = opened_file.read()

                    diff = [i for i in difflib.ndiff(new_content, file_descriptor[key][0]['content']) if i[0] != ' ']
                    diff = ' '. join(diff)
                    file_descriptor[key][0]['difference'] = diff
                message = "\nFilename - " + key + \
                                "\nDiff - " + file_descriptor[key][0]['difference'] + \
                                "\nDate - " + file_descriptor[key][0]['last_changed'] + "\n"

                self.publish(key, message)