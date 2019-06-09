from pyfirmata import Arduino,util

import time

board = Arduino('COM4')

while 1:
	board.digital[5].write(0)
	time.sleep(1)
	board.digital[5].write(1)
	time.sleep(1)
