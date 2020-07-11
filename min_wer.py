from metrics import full_wer
import sys
import os
import re

# For every system, find the max difference in WER between full and split transcripts for a dialogue.
# This to evaluate the effects of overlaps on incremental WER.
systems = ["msoft", "ibm", "google"] ## TODO Add systems if required.

for system in systems:
    split_path = "./results/" + system + "/split-wer/original/"
    max_diff = 0
    for wer_file in os.listdir(split_path):
        # For each split WER file (output from split format scripts), gather all relevant files.
        code = re.search(r"[0-9]{4}", wer_file).group(0)
        
        trans_full = "./results/" + system + "/system-trans-text/" + system + "-sw0" + code + "-mono-trans.txt"
        gold_full = "./results/gold-trans-text/" + code + "-full-joined-transcript.txt"
        trans_left = "./results/" + system + "/split-system-trans-text/left-sw0" + code + "-trans.txt"
        trans_right = "./results/" + system + "/split-system-trans-text/right-sw0" + code + "-trans.txt"
        gold_a = "./results/gold-split-text/a/" + code + "-A-joined-transcript.txt"
        gold_b = "./results/gold-split-text/b/" + code + "-B-joined-transcript.txt"

        try:
            # Calc WER on transcript with both speakers.
            joined_wer = full_wer(gold_full, trans_full)

            # Find WERs assuming left channel = speaker A
            left_a = full_wer(gold_a, trans_left)
            right_b = full_wer(gold_b, trans_right)

            # Find WERs assuming left channel = speaker B
            left_b = full_wer(gold_b, trans_left)
            right_a = full_wer(gold_a, trans_right)
        except FileNotFoundError:
            # Note any instances where a file is missing.
            print(code)
            pass
            
        if joined_wer and left_a and left_b and left_b and right_b:
            # Calculate overall split WERs by finding the mean of Speakers A & B.
            mean1 = (left_a + right_b)/2
            mean2 = (left_b + right_a)/2

            # Select the minimum WER as that is when the channel and speaker matches.
            check = min(mean1, mean2)
            # Calculate improvement in performance when overlaps are removed.
            temp_max = joined_wer - check
            # Store biggest improvement.
            if temp_max > max_diff:
                max_diff = temp_max
    # For each system, report max diff.
    print(system + " MAX DIFF:  " + str(max_diff))

