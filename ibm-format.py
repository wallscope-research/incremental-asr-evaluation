from universal import process, clean_csv, add_trans_chunk
import sys
import re

# The infile is the system trancript.
infile = sys.argv[1]

# Using the system output name, the relevant universal format and full transcripts are gathered.
filename_prep = re.search(r"(?<=system-output\/)(.*?)(?=\.txt)", infile).group(0)
outfile = "./results/ibm/universal/ibm-" + filename_prep + ".csv"
trans_file = "./results/ibm/system-trans-text/ibm-" + filename_prep + "-trans.txt"

# setting initial utterance as jiwer can't handle empty strings.
# tsoft = the start of the file.
prev = "tsotf"
utt = ""

# IBM specific processing.
# This function extracts each new hypothesis with its time and processes it.
# Simultaneously, finalised hypotheses are stored for final WER calculations.
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
        if check.startswith(number) and not "," in line:
            time = check.replace("\n", "")
        if check.startswith("\"final"):
            if not utt.isspace():
                # print(utt)
                if "false" in line:
                    process(outfile, time, prev, utt)
                    prev = utt
                else:
                    process(outfile, time, prev, utt)
                    add_trans_chunk(trans_file, utt)
                    prev = "tsotf"

# Universal output finalised.
clean_csv(outfile)

