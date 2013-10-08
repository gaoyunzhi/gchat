import msvcrt, sys, time

while True:
    if msvcrt.kbhit():
        key = msvcrt.getwch()
        print key, ord(key)
