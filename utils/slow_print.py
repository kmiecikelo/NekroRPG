import time
import sys

def slow_print(text, delay=0.08):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()