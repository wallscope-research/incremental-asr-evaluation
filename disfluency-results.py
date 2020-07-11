import sys
import os

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

# Add all methods to loop through.
methods = []
methods.append("swbc-gold+fp+et+res")
methods.append("swbc-gold+fp+et-res")
methods.append("swbc-gold+fp-et+res")
methods.append("swbc-gold+fp-et-res")
methods.append("swbc-gold-fp+et+res")
methods.append("swbc-gold-fp+et-res")
methods.append("swbc-gold-fp-et+res")
methods.append("swbc-gold-fp-et-res")

for method in methods:
    wer_path = "./results/" + sub_dir + "split-wer/" + method + "/"

    wer_sum = 0
    wer_count = 0

    # Aggregate results per method and report.
    for wer_file in os.listdir(wer_path):
        with open(wer_path + wer_file, 'r') as wf:
            addition = float(wf.read())
            wer_sum = wer_sum + addition
            wer_count = wer_count + 1
            wer_result = wer_sum / wer_count
    print(method + " WER:  " + str(wer_result))

