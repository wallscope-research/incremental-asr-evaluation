import sys
import re

# This script generates the swb code list. This is to be looped through for other scripts.
# For example, if you have a batch - you can run 'for line in file' in bash or zsh.
# Where the 'file' is the output of this script.
filename = sys.argv[1]
five_code = re.search(r"[0-9]{5}", filename).group(0)
final_code = five_code[1:]

with open('./results/codes.txt', 'a') as codes:
    codes.write(final_code)
    codes.write("\n")