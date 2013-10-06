# -*- coding: utf8 -*-
from util import beautify_incoming_message, beautify_outgoing_message
from chat import Chat
from secret import USER, PD
import time

NUMBER_RANGE = xrange(1,9)

class Model(object):
    def __init__(self):
        self.email_to_number = {} 
        self.number_to_email = {}
        self.email_to_most_recent_time_used = {}
        self.email_to_alias = {} # TODO: import buddy list to get alias
        self.emails = []
        self.bot = Chat(USER, PD)
        self.bot.addUI(self)
        self.bot.addModel(self.model)
        self.bot.run()
        self.reciever_list = []
        self.random_counter = -1
    
    def addUI(self, ui):
        self.ui = ui
    
    def handleIncomingMessage(self, message):
        from_field = message["from"]
        body_field = message["body"]
        email = from_field.bare 
        alias = from_field.user
        self.__register_email(email, alias)
        buddy_number = self.email_to_number[email]
        message_to_show = beautify_incoming_message(alias, buddy_number, body_field)
        self.ui.showMessage(message_to_show)
        
    def __register_email(self, email, alias):
        if email not in self.email_to_alias:
            self.email_to_alias[email] = alias
            self.emails.append(email)
        self.__register_buddy_number(email)
        self.email_to_most_recent_time_used[email] = time.time()
        
    def __register_buddy_number(self, email):
        if email in self.email_to_number:
            return self.email_to_number[email]
        for number in NUMBER_RANGE:
            if not number in self.number_to_email:
                break
        if number in self.number_to_email:
            number = self.__pop_oldest_used_indexnumber()
        self.email_to_number[email] = number
        self.number_to_email[number] = email
    
    def __pop_oldest_used_indexnumber(self):
        number, min_last_used_time = 0, 1e10
        for i in NUMBER_RANGE:
            if self.email_to_most_recent_time_used(i) < min_last_used_time:
                number, min_last_used_time = i, self.email_to_most_recent_time_used(i)
        email = self.number_to_email[number]
        del self.number_to_email[number]
        del self.email_to_number[email]

    def get_next_reciever(self):
        if self.receiver_list:
            return self.receiver_list.pop(0)
        return self.get_random_reciever()

    def get_any_reciever(self):
        if not self.emails:
            return ''
        self.random_counter += 1
        return self.emails[self.random_counter % len(self.emails)]
    
    def send_message(self, bufferMessage):
        email = bufferMessage.get_reciever()
        self.__register_email(email, email.split('@')[0])
        buddy_number = self.email_to_number[email]
        alias = self.email_to_alias[email]
        body_field = bufferMessage.get_message()
        message_to_show = beautify_outgoing_message(alias, buddy_number, body_field)
        self.ui.showMessage(message_to_show)
        self.bot.sendChat(bufferMessage.get_xmpp_message())