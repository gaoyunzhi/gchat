''' util for model '''
def beautify_incoming_message(alias, buddy_number,  message):
    return 'From ('+buddy_number+')'+alias+':'+message.strip()

def beautify_outgoing_message(alias, buddy_number,  message):
    return 'To   ('+buddy_number+')'+alias+':'+message.strip()

''' util for ui '''
class BufferMessage():
    def __init__(self):
        self.message = []
        self.reciever = None
        
    def append_message(self, key):
        self.message.append(key)
        
    def get_xmpp_message(self):
        return {'to': self.reciever,
                'body': self.get_message()}
    
    def has_reciever(self):
        return self.reciever != None
    
    def has_message(self):
        return self.message != []
    
    def get_reciever(self):
        return self.reciever
    
    def get_message(self):
        return ''.join(self.message)
    
    def set_reciever(self, receiver):
        self.reciever = receiver