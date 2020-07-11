from universal import add_trans_chunk
import sys
import re

# Given a system output and which channel it is from, the final transcript is stored.
# This is to calculate the WER.
infile = sys.argv[1]
side = sys.argv[2]
if side == "left":
    filename_prep = re.search(r"(?<=left\/)(.*?)(?=\.txt)", infile).group(0)
elif side == "right":
    filename_prep = re.search(r"(?<=right\/)(.*?)(?=\.txt)", infile).group(0)
else:
    print("Which side?")
trans_file = "./results/ibm/split-system-trans-text/" + side + "-" + filename_prep + "-trans.txt"

with open(infile, 'r') as f:
    for line in f:
        check = line.replace(" ", "").replace("%HESITATION", "")
        try:
            number = re.search(r"[+-]?([0-9]*[.])?[0-9]+", line).group(0)
        except AttributeError:
            pass
        if check.startswith("\"transcript"):
            utt = re.search(r"(?<=transcript\"\: \")(.*?)(?=\")", line).group(0)
            utt = utt.lower().replace("%hesitation", "")
        if check.startswith("\"final"):
            if not utt.isspace():
                if "true" in line:
                    add_trans_chunk(trans_file, utt)


