# -*- coding: utf8 -*-
from secret import USER, PD
import sleekxmpp, logging, sys
logging.basicConfig()
sys.setdefaultencoding('utf8') #@UndefinedVariable
    
class Chat(object): 
    def __init__(self, jid, password) : 
        self.xmpp = sleekxmpp.ClientXMPP(jid, password) 
        self.xmpp.add_event_handler("session_start", self.handleXMPPConnected) 
        self.xmpp.add_event_handler("message", self.handleIncomingMessage) 
        
    def run(self) : 
        self.xmpp.connect() 
        self.xmpp.process(threaded=True) 
        
    def handleXMPPConnected(self, event): 
        self.xmpp.sendPresence()
        
    def handleIncomingMessage(self, message):
        self.model.handleIncomingMessage(message)
        
    def sendChat(self, message):
        self.xmpp.sendMessage(message["to"], message["body"], mtype="chat")
        # set mtype = chat to let gchat save history
        
    def addUI(self, ui):
        self.ui = ui
        
    def addModel(self, model):
        self.model = model
        
if __name__ == '__main__':
    bot = Chat(USER, PD)
    bot.run()