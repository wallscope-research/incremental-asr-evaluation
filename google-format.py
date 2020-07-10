from universal import process, clean_csv, add_trans_chunk
import sys
import re

# The infile is the system trancript.
infile = sys.argv[1]

# Using the system output name, the relevant universal format and full transcripts are gathered.
filename_prep = re.search(r"(?<=system-output\/)(.*?)(?=\.txt)", infile).group(0)
outfile = "./results/google/universal/google-" + filename_prep + ".csv"
trans_file = "./results/google/system-trans-text/google-" + filename_prep + "-trans.txt"

# setting initial utterance as jiwer can't handle empty strings.
# tsoft = the start of the file.
prev = "tsotf"
utt = ""

# Google specific processing.
# This function extracts each new hypothesis with its time and processes it.
# Simultaneously, finalised hypotheses are stored for final WER calculations.
with open(infile, 'r') as f:
    for line in f:
        if line.startswith("Finished"):
            fin = re.search(r"(?<=Finished: )(.*)(?=\n)", line).group(0)
        if line.startswith("Time"):
            time = re.search(r"(?<=Time: )(.*)(?=\n)", line).group(0)
        if line.startswith("Transcript"):
            utt = re.search(r"(?<=Transcript: )(.*)(?=\n)", line).group(0)
            utt = utt.replace(".", "")
            if fin == "False":
                process(outfile, time, prev, utt)
                prev = utt
            else:
                process(outfile, time, prev, utt)
                add_trans_chunk(trans_file, utt.lower())
                prev = "tsotf"

# Universal output finalised.
clean_csv(outfile)