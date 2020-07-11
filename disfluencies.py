from metrics import full_wer
import sys

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
    # For each method, compare system outputs to gold transcripts cleaned with given method.
    c_gold_A = "./results/cleaned-golds/" + method + "/sw" + code + "-A.out"
    c_gold_B = "./results/cleaned-golds/" + method + "/sw" + code + "-B.out"
    trans_a = "./results/" + sub_dir + "split-system-trans-text/left-sw0" + code + "-trans.txt"
    trans_b = "./results/" + sub_dir + "split-system-trans-text/right-sw0" + code + "-trans.txt"

    # Find WER assuming left channel is speaker A.
    left_a = full_wer(c_gold_A, trans_a)
    right_b = full_wer(c_gold_B, trans_b)
    mean1 = (left_a + right_b)/2

    # Find WER assuming left channel is speaker B.
    left_b = full_wer(c_gold_B, trans_a)
    right_a = full_wer(c_gold_A, trans_b)
    mean2 = (left_b + right_a)/2

    # Store minimum as that is WER when channel and speaker are correctly matched.
    correct_mean = min(mean1, mean2)

    outfile = "./results/" + sub_dir + "split-wer/" + method + "/wer-" + code + "-mean.txt"
    with open(outfile, 'w') as f:
        f.write(str(correct_mean))

