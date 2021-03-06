# -*- coding: utf8 -*-
from util import beautify_incoming_message, beautify_outgoing_message, \
    beautify_composing_message # TODO: this three methods may need to change (priority: low)
from util import default_alias_from_email
from chat import Chat
from secret import USER, PD
import time

NUMBER_RANGE = xrange(1,9)
MAX_RECIEVER_LIST_LEN = 50
HELP_MESSAGE = "use F1 - F8 for users that has a number, e.g. if you see '(5)bajie90=>hello'," + \
               " you can reply bajie90 by pressing F5. use F9 to manually edit receiver field," + \
               " enter to end editing message. If you are typing the message itself, enter to" + \
               " send the message. In the message, press F10 to see this help message again," + \
               " press F12 to quit the window. Email bajie90 at gmail to report bugs.\n"

class Model(object):
    def __init__(self):
        self.email_to_number = {} 
        self.number_to_email = {}
        self.email_to_most_recent_time_used = {}
        self.email_to_alias = {} # TODO: import buddy list to get alias (priority: low)
        self.emails = []
        self.receiver_list = []
        self.random_counter = -1
        self.receiver_index = -1
    
    def addUI(self, ui):
        self.ui = ui
        
    def addBot(self):
        self.bot = Chat(USER, PD)
        self.bot.addModel(self)
        self.bot.run()
    
    def handleIncomingMessage(self, message):
        from_field = message["from"]
        body_field = message["body"]
        email = from_field.bare 
        alias = from_field.user
        if email not in self.receiver_list:
            self.receiver_list.append(email)
        
        self.__register_email(email, alias)
        buddy_number = self.email_to_number[email]
        message_to_show = beautify_incoming_message(alias, buddy_number, body_field)
        # TODO: need to refactor alias, buddy_number, body_field to a class or something (priority: low)
        self.ui.showMessage(message_to_show)
        self.ui.set_current_receiver()
        self.show_composing_message(self.ui.bufferMessage)
        
    def __register_email(self, email, alias):
        if email not in self.email_to_alias:
            self.email_to_alias[email] = alias
            self.emails.append(email)
        self.__register_buddy_number(email)
        self.email_to_most_recent_time_used[email] = time.time()
        
    def __register_buddy_number(self, email):
        if email in self.email_to_number:
            return
        for number in NUMBER_RANGE:
            if not number in self.number_to_email:
                break
        if number in self.number_to_email:
            number = self.__pop_oldest_used_indexnumber()
        self.email_to_number[email] = number
        self.number_to_email[number] = email
    
    def __pop_oldest_used_indexnumber(self): # untested
        number, min_last_used_time = 0, 1e10
        for i in NUMBER_RANGE:
            last_used_time = self.email_to_most_recent_time_used[self.number_to_email[i]]
            if  last_used_time < min_last_used_time:
                number, min_last_used_time = i, last_used_time
        email = self.number_to_email[number]
        del self.number_to_email[number]
        del self.email_to_number[email]

    def get_receiver(self, up_or_down):
        self.receiver_index += up_or_down
        if self.receiver_index < 0: 
            self.receiver_index = 0
        if len(self.receiver_list) <= self.receiver_index:
            self.receiver_list.append(self.get_any_receiver())
        self.__clean_receiver_list()
        return self.receiver_list[self.receiver_index]
    
    def insert_receiver(self, email):
        if self.receiver_list[self.receiver_index] != email:
            self.receiver_index +=1
            self.receiver_list = self.receiver_list[:self.receiver_index] + [email] + \
                                 self.receiver_list[self.receiver_index:]
        self.__clean_receiver_list()
        
    def __clean_receiver_list(self):
        if self.receiver_index > MAX_RECIEVER_LIST_LEN:
            self.receiver_index -= MAX_RECIEVER_LIST_LEN/2
            self.receiver_list = self.receiver_list[MAX_RECIEVER_LIST_LEN/2:]

    def get_any_receiver(self):
        if not self.emails:
            return ''
        self.random_counter += 1
        return self.emails[self.random_counter % len(self.emails)]
    
    def send_message(self, bufferMessage):
        email = bufferMessage.get_receiver()
        self.__register_email(email, default_alias_from_email(email))
        buddy_number = self.email_to_number[email]
        alias = self.email_to_alias[email]
        body_field = bufferMessage.get_body()
        message_to_show = beautify_outgoing_message(alias, buddy_number, body_field)
        self.ui.showMessage(message_to_show)
        self.bot.sendChat(bufferMessage)
        
    def get_email_from_number(self, number):
        if number in self.number_to_email:
            return self.number_to_email[number]
        return self.get_any_receiver()
    
    def show_composing_message(self, bufferMessage):
        email = bufferMessage.get_receiver()
        buddy_number = self.email_to_number.get(email, 0)
        body_field = bufferMessage.get_body()
        message_to_show = beautify_composing_message(email, buddy_number, body_field)
        self.ui.showMessage(message_to_show)
        
    def show_help_message(self):
        self.ui.showMessage(HELP_MESSAGE)
        self.show_composing_message(self.ui.bufferMessage)
        # still need to think about this, the updation of bufferMessage