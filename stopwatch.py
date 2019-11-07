import time
import funcs

def start_time():
    i = 0
    while True:
        time.sleep(1)
        i += 1
        print(i // 3600, (i // 60) % 60, i % 60, sep=':')
start_time()
