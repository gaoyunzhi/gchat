import msvcrt

while True:
    if msvcrt.kbhit():
        key = msvcrt.getwch()
        print key, ord(key)