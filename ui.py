# -*- coding: utf8 -*-
import msvcrt
from threading import Thread
from model import Model
from util import BufferMessage

class UI(object):
    def __init__(self):
        self.model = Model()
        self.model.addUI(self)
        self.keyboard_listener = Thread(target=self.__keyboardListenerRun)
        self.keyboard_listener.start()
        self.bufferMessage = BufferMessage()
        self.control_mode = False

    def __keyboardListenerRun(self):      
        while True:
            if msvcrt.kbhit():
                key = msvcrt.getwch()
                ordkey = ord(key)
                if ordkey == 0: # control key pressed
                    self.__deal_control()
                elif ordkey == 13: # enter pressed
                    if self.bufferMessage.has_message():
                        if not self.control_mode:
                            self.__send_message()
                        else:
                            self.__manually_set_reciever()
                            self.control_mode = False
                else:
                    if not self.bufferMessage.has_reciever():
                        self.__set_reciever()
                    self.bufferMessage.append_message(key)
                print "you pressed %(key)s, with ord = %(ord)s" % {'key': key, "ord": ord(key)} 
                # for test

    def __deal_control(self):
        # get control detail, which of F1, F2... is the control
        control_key = ord(msvcrt.getwch()) - 58
        if 0< control_key < 9: 
            self.bufferMessage.set_reciever(self.model.get_email_from_number(control_key)) 
        elif control_key == 9:
            self.control_mode = True
    
    def __send_message(self):
        self.model.send_message(self.bufferMessage)
        self.bufferMessgae = BufferMessage()
        
    def __manually_set_reciever(self):
        receiver = self.bufferMessage.get_message() 
        # TODO: shouldn't use bufferMessage here, should create a parent class
        # bufferText of bufferMessage
        self.bufferMessage = BufferMessage()
        self.bufferMessage.set_reciever(receiver)

    def __set_reciever(self):
        self.bufferMessage.set_reciever(self.model.get_next_reciever())

    def showMessage(self, message_to_show):
        print message_to_show
        
    def close(self):
        self.keyboard_listener.join()
        exit()
        
if __name__ == "__main__":
    UI()