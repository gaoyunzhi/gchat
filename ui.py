# -*- coding: utf8 -*-
import msvcrt

num = 0
done = False
while not done:
    # print num
    num += 1

    if msvcrt.kbhit():
        key = msvcrt.getwch()
        print "you pressed %(key)s, with ord = %(ord)s" % {'key': key, "ord": ord(key)} 
