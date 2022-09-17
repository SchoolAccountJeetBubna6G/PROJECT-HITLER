import time
from traceback import print_tb

t = time.localtime()
current_time = time.strftime("%I:%M:%S", t)
print(current_time)
time.sleep(60)
t1 = time.localtime()
print('this message will be dellvered after 6 min')
current_time1 = time.strftime("%I:%M:%S", t1)
print(current_time1)