# -*- coding: utf8 -*-
import msvcrt, sys
from threading import Thread
from model import Model
from util import BufferMessage

STREAM = sys.stdout
UP = -1
DOWN = 1
CURRENT = 0
ARROW_KEY = 224
UP_KEY = 72
DOWN_KEY = 80

class UI(object):
    def __init__(self):
        self.bufferMessage = BufferMessage()
        self.receiver_editing_mode = False
        self.model = Model()
        self.model.addUI(self)
        self.model.addBot()
        self.keyboard_listener = Thread(target=self.__keyboardListenerRun)
        self.keyboard_listener.start()

    def __keyboardListenerRun(self):      
        while True:
            if msvcrt.kbhit():
                key = msvcrt.getwch()
                ordkey = ord(key)
                if ordkey == 0: # control key pressed (F1-F10 allowed)
                    self.__change_receiver()
                elif ordkey == 13: # enter pressed
                    self.__enter_pressed()
                elif ordkey == ARROW_KEY: # up and down allowed
                    self.__arrow_pressed()
                else:
                    if self.receiver_editing_mode:
                        self.bufferMessage.append_receiver(key)
                    else:
                        self.bufferMessage.append_body(key)
                self.model.show_composing_message(self.bufferMessage)

    def __change_receiver(self):
        # get control detail, which of F1-F10
        control_key = ord(msvcrt.getwch()) - 58
        if 0 < control_key < 9: 
            self.bufferMessage.set_receiver(self.model.get_email_from_number(control_key)) 
        elif control_key == 9:
            self.receiver_editing_mode = True
            self.bufferMessage.empty_receiver()
        elif control_key == 10:
            self.model.show_help_message()
            
    def __enter_pressed(self):
        if not self.receiver_editing_mode:
            if self.bufferMessage.valid_message():
                self.__send_message()
                self.bufferMessage.empty_body()
        else:
            self.receiver_editing_mode = False
        if not self.bufferMessage.has_receiver():
            self.set_current_receiver()
            
    def __arrow_pressed(self):
        arrow_key = ord(msvcrt.getwch())
        key = None
        if arrow_key == UP_KEY:
            key = UP
        elif arrow_key == DOWN_KEY:
            key = DOWN
        if key != None:
            self.__set_receiver(key)

    def __send_message(self):
        self.model.send_message(self.bufferMessage)

    def __set_receiver(self, up_or_down):
        self.bufferMessage.set_receiver(self.model.get_receiver(up_or_down))

    def showMessage(self, message_to_show):
        STREAM.write(message_to_show)
        
    def set_current_receiver(self):
        self.__set_receiver(CURRENT)
        
    def close(self):
        self.keyboard_listener.join()
        exit()
        
if __name__ == "__main__":
    UI()