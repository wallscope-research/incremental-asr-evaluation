from metrics import calc_stability, full_wer, latency
import sys
import json

# Using the given swb code - all relevant files are gathered.
code = sys.argv[1]
prep = "sw0" + code + "-mono"

incsv = "./results/google/universal/google-" + prep + ".csv"
intext = "./results/google/system-trans-text/google-" + prep + "-trans.txt"
gold_text = "./results/gold-trans-text/" + code + "-full-joined-transcript.txt"
gold_original = "./results/gold-timings/" + code + "-full-transcript.json"

# Now we have all the files, the final metrics are calculated.

# Stability
stab_file = "./results/google/stability/" + prep + ".json"
stability = calc_stability(incsv)
with open(stab_file, 'w') as outfile:
    json.dump(stability, outfile)

# WER
full_wer_file = "./results/google/full-wer/" + prep + ".txt"
word_error_rate = full_wer(gold_text, intext)
with open(full_wer_file, 'w') as wer_out:
    wer_out.write(str(word_error_rate))

# Latency
fo_latency_file = "./results/google/latency/fo/" + prep + ".json"
fd_latency_file = "./results/google/latency/fd/" + prep + ".json"
fo_latencies, fd_latencies = latency(intext, incsv, gold_original, 'google')
with open(fo_latency_file, 'w') as fo_out:
    json.dump(fo_latencies, fo_out)
with open(fd_latency_file, 'w') as fd_out:
    json.dump(fd_latencies, fd_out)