# -*- coding: utf8 -*-
import msvcrt, sys
from threading import Thread
from model import Model
from util import BufferMessage

STREAM = sys.stdout
UP = -1
DOWN = 1
ARROW_KEY = 224

class UI(object):
    def __init__(self):
        self.model = Model()
        self.model.addUI(self)
        self.keyboard_listener = Thread(target=self.__keyboardListenerRun)
        self.keyboard_listener.start()
        self.bufferMessage = BufferMessage()
        self.receiver_editing_mode = False

    def __keyboardListenerRun(self):      
        while True:
            if msvcrt.kbhit():
                key = msvcrt.getwch()
                ordkey = ord(key)
                if ordkey == 0: # control key pressed
                    self.__deal_control()
                elif ordkey == 13: # enter pressed
                    self.__enter_pressed()
                elif ordkey == ARROW_KEY:
                    self.__arrow_pressed()
                else:
                    if self.receiver_editing_mode:
                        self.bufferMessage.append_receiver(key)
                    else:
                        self.bufferMessage.append_body(key)
                self.model.show_composing_message(self.bufferMessage)

    def __deal_control(self):
        # get control detail, which of F1, F2... is the control
        control_key = ord(msvcrt.getwch()) - 58
        if 0< control_key < 9: 
            self.bufferMessage.set_receiver(self.model.get_email_from_number(control_key)) 
        elif control_key == 9:
            self.receiver_editing_mode = True
            self.bufferMessage.empty_receiver()
            
    def __enter_pressed(self):
        if not self.receiver_editing_mode:
            if self.bufferMessage.valid_message():
                self.__send_message()
                self.bufferMessage.empty_body()
            if not self.bufferMessage.has_receiver():
                self.bufferMessage.set_receiver(self.model.get_receiver(UP))
                # not sure this is the right behavior
        else:
            self.receiver_editing_mode = False
            
    def __arrow_pressed(self):
        arrow_key = ord(msvcrt.getwch())
        key = 0
        if arrow_key == 72:
            key = UP
        elif arrow_key == 80:
            key = DOWN
        if key != 0:
            self.__set_receiver(key)

    def __send_message(self):
        self.model.send_message(self.bufferMessage)

    def __set_receiver(self, up_or_down):
        self.bufferMessage.set_receiver(self.model.get_receiver(up_or_down))

    def showMessage(self, message_to_show):
        STREAM.write(message_to_show)
        
    def close(self):
        self.keyboard_listener.join()
        exit()
        
if __name__ == "__main__":
    UI()