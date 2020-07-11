import sys
import os

# Given the system name, this script calculates and outputs the overall split WER (i.e. no overlaps).
system = sys.argv[1]

if system == "microsoft" or system == "msoft":
    system = "msoft"
    sub_dir = "msoft/"
elif system == "ibm":
    sub_dir = "ibm/"
elif system == "google":
    sub_dir = "google/"
else:
    print("System not implemented") ## TODO Add elif statements as new systems are added.

wer_path = "./results/" + sub_dir + "split-wer/original/"

wer_sum = 0
wer_count = 0

for wer_file in os.listdir(wer_path):
    with open(wer_path + wer_file, 'r') as wf:
        addition = float(wf.read())
        wer_sum = wer_sum + addition
        wer_count = wer_count + 1
        wer_result = wer_sum / wer_count
print(system + " WER:  " + str(wer_result))

