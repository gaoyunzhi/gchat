''' util for model '''
CLEAR_LINE = '\r'+' '*100+'\r'

def beautify_incoming_message(alias, buddy_number,  message):
    return CLEAR_LINE+'('+str(buddy_number)+')'+alias+'=>'+message.strip()+'\n'

def beautify_outgoing_message(alias, buddy_number,  message):
    return CLEAR_LINE+('('+str(buddy_number)+')'+alias+'<='+message.strip()).rjust(50)+'\n'

def beautify_composing_message(alias, buddy_number, message):
    return CLEAR_LINE+' '*5+'composing:'+'('+str(buddy_number)+')'+alias+'<--'+message.strip()

def to_email(text):
    if '@' in text:
        return text
    return text + '@gmail.com'

''' util for ui '''  
class BufferText(object):
    def __init__(self):
        self.text = []

    def append_text(self, key):
        if ord(key) == 8: # backspace
            self.text = self.text[:-1]
        elif ord(key) == 27: # ESC
            self.text = []
        else:
            self.text.append(key)
            
    def has_text(self):
        return self.text != []
    
    def set_text(self, text):
        self.text = [text]
        
    def get_text(self):
        return ''.join(self.text)
        
class BufferMessage(object):
    def __init__(self):
        self.body = BufferText()
        self.receiver = BufferText()

    def get_body(self):
        return self.body.get_text()
    
    def get_receiver(self):
        return to_email(self.receiver.get_text())
    
    def set_receiver(self, email):
        self.receiver.set_text(email)
    
    def append_body(self, key):
        return self.body.append_text(key)
    
    def append_receiver(self, key):
        return self.receiver.append_text(key)
    
    def empty_receiver(self):
        self.receiver = BufferText()
        
    def valid_message(self):
        return self.body.has_text() and self.receiver.has_text()
    
    def has_receiver(self):
        return self.receiver.has_text()
    
    def empty_body(self):
        self.body = BufferText()