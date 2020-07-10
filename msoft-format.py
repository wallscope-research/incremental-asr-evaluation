from universal import process, clean_csv, add_trans_chunk
import sys
import re

# The infile is the system trancript.
infile = sys.argv[1]

# Using the system output name, the relevant universal format and full transcripts are gathered.
filename_prep = re.search(r"(?<=system-output\/)(.*?)(?=\.txt)", infile).group(0)
outfile = "./results/msoft/universal/msoft-" + filename_prep + ".csv"
trans_file = "./results/msoft/system-trans-text/msoft-" + filename_prep + "-trans.txt"

# setting initial utterance as jiwer can't handle empty strings.
# tsoft = the start of the file.
prev = "tsotf"
utt = ""

# Microsoft specific processing.
# This function extracts each new hypothesis with its time and processes it.
# Simultaneously, finalised hypotheses are stored for final WER calculations.
with open(infile, 'r') as f:
    for line in f:
        if line.startswith("RECOGNIZING"):
            relevant_info = re.search(r"\{(.*?)\}", line).group(0)
            dictionary = eval(relevant_info)
            time = dictionary.get("Duration") + dictionary.get("Offset")
            utt = dictionary.get("Text")
            process(outfile, time, prev, utt)
            prev = utt
        elif line.startswith("JSON"):
            prev = "tsotf"
            transcript = re.search(r"(?<=DisplayText\":\")(.*?)(?=\")", line)
            if transcript:
                transcript = transcript.group(0)
            add_trans_chunk(trans_file, transcript.lower())

# Universal output finalised.
clean_csv(outfile)