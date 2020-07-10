from metrics import full_wer
import sys

# Given a system and a swb code, relevant files are gathered.
system = sys.argv[1]
code = sys.argv[2]

if system == "microsoft" or system == "msoft":
    system = "msoft"
    sub_dir = "msoft/"
elif system == "ibm":
    sub_dir = "ibm/"
elif system == "google":
    sub_dir = "google/"
else:
    print("System not implemented") ## TODO Add elif statements as new systems are added.

# These are the files needed to calculate the mean WER over the split channels (per swb code)
trans_left = "./results/" + sub_dir + "split-system-trans-text/left-sw0" + code + "-trans.txt"
trans_right = "./results/" + sub_dir + "split-system-trans-text/right-sw0" + code + "-trans.txt"
gold_a = "./results/gold-split-text/a/" + code + "-A-joined-transcript.txt"
gold_b = "./results/gold-split-text/b/" + code + "-B-joined-transcript.txt"

# The left audio channel may not be speaker A (and vice versa).
# To find this out, we find the mean WER for (left=A, right=B) & (left=B, right=A)
# Then we output the minimum as that is clearly when the audio channel transcript (from the system) matches the speaker transcript.

# This calculation finds the mean WER assuming the left channel is speaker A.
left_a = full_wer(gold_a, trans_left)
right_b = full_wer(gold_b, trans_right)
mean1 = (left_a + right_b)/2

# This calculation finds the mean WER assuming the left channel is speaker B.
left_b = full_wer(gold_b, trans_left)
right_a = full_wer(gold_a, trans_right)
mean2 = (left_b + right_a)/2

# Again, the mimimum of these means is when the channels and speakers are corectly matched.
# Obviously the other mean is larger because the transcript is matched with the wrong speaker.
correct_mean = min(mean1, mean2)

# Store.
outfile = "./results/" + sub_dir + "split-wer/original/wer-" + code + "-mean.txt"
with open(outfile, 'w') as f:
    f.write(str(correct_mean))