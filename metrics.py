from jiwer import wer
import csv
import re
import json

# Given a swb example in our universal format, calculate hypothesis stabilities.
def calc_stability(filename):
    ranges = [{'min':99999999999, 'max':-1}]
    result = []
    # These headers match universal format csv.
    fieldnames = ['Word Location', 'Hypothesis Time', "Edit Type", "Word"]

    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=fieldnames)
        for row in reader:
            # For hypothesis (by word placement), find the first and last hypothesis.
            if row['Word Location'] != 'Word Location':
                loc = int(row['Word Location'])
                time = float(row['Hypothesis Time'])
                if row['Word Location'] == 'Word Location':
                    continue
                else:
                    if loc < len(ranges):
                        if time > ranges[loc]['max']:
                            ranges[loc]['max'] = time
                        if time < ranges[loc]['min']:
                            ranges[loc]['min'] = time
                    else:
                        ranges.append({'min':time, 'max':time})
    for item in ranges:
        # The life of a hypothesis = the time of final hypothesis - the time of first hypothesis.
        length = item['max'] - item['min']
        result.append(length)
    return result

# Given the gold transcript and system output, return the WER.
def full_wer(ground_file, hyp_file):
    transcript = ""
    gold = ""

    with open(ground_file, 'r') as g_file:
        gold = g_file.read()
    
    with open(hyp_file, 'r') as h_file:
        transcript = h_file.read()

    error = wer(gold, transcript)
    return error

# This function calculates the FO and FD latencies.
def latency(transcript_file, univ_csv, gold, system):
    timings = []
    gold_list = []
    fo_latencies = []
    fd_latencies = []
    # Again, these match the universal format csv.
    fieldnames = ['Word Location', 'Hypothesis Time', "Edit Type", "Word"]
    transcript = ""

    if system == "microsoft":
        # This multiplier converts timings into seconds.
        multiplier = 10**-7
    elif system == "ibm": ## TODO Check IBM multiplier
        multiplier = 1
    else:
        multiplier = 1 ## For example, Google. Add above for non-1 multipliers

    with open(transcript_file, 'r') as f:
        transcript = f.read()
    
    # For every word in the transcript, add a set item in the timings list.
    for i in range(0, len(transcript.split())):
        timings.append({'Word':transcript.split()[i].lower(), 'fo':-1.5, 'fd':-1.5})
    
    # Add the EOF (end of file) for looping reasons. This is deleted later.
    timings.append({'Word':'EOF', 'fo':-2.5, 'fd':-2.5})

    with open(univ_csv, newline='') as ucsv:
        universal = csv.DictReader(ucsv, fieldnames=fieldnames)
        for row in universal:
            if row['Word Location'] != 'Word Location':
                loc = int(row['Word Location'])
                # If a non-delete action and not the start of the file, set fo and fd timings.
                if row['Edit Type'] in ('insert', 'replace', 'set'):
                    if row['Word'] != 'tsotf':
                        try:
                            if timings[loc]['fd'] == -1.5:
                                timings[loc]['fo'] = float(row['Hypothesis Time'])*multiplier
                                timings[loc]['fd'] = float(row['Hypothesis Time'])*multiplier
                                if row['Edit Type'] == 'set':
                                    timings[loc+1]['fo'] = float(row['Hypothesis Time'])*multiplier
                            else:
                                timings[loc]['fd'] = float(row['Hypothesis Time'])*multiplier
                        except IndexError:
                            pass
                        continue
                if loc > 1:
                    try:
                        if timings[loc-2]['fd'] == -1.5:
                            timings[loc-2]['fd'] = timings[loc-2]['fo']
                    except IndexError:
                        pass
                    continue
    # Delete EOF added above.
    del timings[-1]

    with open(gold, 'r') as g:
        for line in json.loads(g.read()):
            gold_list.append(line)

    for i, item in enumerate(gold_list):
        # Set scan size of latencies. Using purely word location (e.g. comparing 10th word in gold to 10th word in system output),
        # Latencies get huge (missing umms) and words align with the same word but a different point (e.g. two 'the' tokens matching 4 minutes apart).
        # We use a scan approach that limits the search space (therefore no 4 minute latencies as clearly incorrect matching).
        for hypothesis in timings:
            # FO is limited between 0 (negative FO impossible) and 4 seconds (reported in Baumann et al 2016).
            if float(hypothesis['fo']) > float(item['ws']) and float(hypothesis['fo']) < float(item['ws'])+4:
                if hypothesis['Word'] == item['Word']:
                    fo_latencies.append(float(hypothesis['fo']) - float(item['ws']))
                    hypothesis['Word'] = 'abcdefghijklmnopqrstuvwxyz'
            # FD is limited between -2 and 4 seconds (reported in Baumann et al 2016).
            if float(hypothesis['fd']) > float(item['we'])-2 and float(hypothesis['fd']) < float(item['we'])+4:
                if hypothesis['Word'] == item['Word']:
                    fd_latencies.append(float(hypothesis['fd']) - float(item['we']))
                    hypothesis['Word'] = 'abcdefghijklmnopqrstuvwxyz'

    return fo_latencies, fd_latencies

