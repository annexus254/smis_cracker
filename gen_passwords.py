import ProgressBar
from utilities import *

STARTING_PREFIXES = ['37', '38', '39']
ID_LENGTH = 6
MAX_ID_NUMS = 1000000
PROGRESS_INTERVAL = 10

ProgressBar = ProgressBar.ProgressBar(MAX_ID_NUMS)

with open("passwords", "w") as pwdFileHandle:
    for prefix in STARTING_PREFIXES:
        print("Generating passwords for prefix: " + prefix)
        print_progess = PROGRESS_INTERVAL
        for i in range(0, MAX_ID_NUMS):
            pwdFileHandle.write(prefix + leftPad(ID_LENGTH , i) + "\n")
            if i == (print_progess - 1):
                ProgressBar.print(i + 1)
                print_progess += PROGRESS_INTERVAL
        pwdFileHandle.flush()

print("Password generation complete!")
