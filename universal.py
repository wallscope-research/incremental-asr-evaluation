from jiwer import ops
import csv
import os.path
import fileinput

def clean(utt):
    # Takes utterance and returns it in lower case for processing.
    cleaned = utt.lower()
    return cleaned

def store(result, csv_writer):
    # Store results to csv.
    csv_writer.writerow(result)


def complete_sets(t, loc, s, edit, csv_writer):
    # Takes an integer location in sentence (s) where edit happened at time t.
    # This happens when edit is not at the end of the utterance.
    # It sets the rest of the sentence in place for metric calculations.
    if edit == "delete":
        for i in range(loc+1, len(s)):
            result = {'Word Location': i-1, 'Hypothesis Time': t, 'Edit Type': "set", 'Word': s[i]}
            store(result, csv_writer)
    else:
        for i in range(loc, len(s)):
            result = {'Word Location': i+1, 'Hypothesis Time': t, 'Edit Type': "set", 'Word': s[i]}
            store(result, csv_writer)


def detect_change(time, prev, utt, csv_writer):
    # Takes the time of current utterance (utt),
    # the previous utterance, and the current utterance.
    # Outputs the difference with time in our universal format.
    
    prev = clean(prev)
    utt = clean(utt)
    prev_length = len(prev.split())
    
    editops = ops(prev, utt)

    for edit in editops:
        if edit[0] == "insert":
            word_location = edit[2]
            word = utt.split()[word_location]
            diff = word_location - prev_length
        elif edit[0] == "delete":
            word_location = edit[1]
            word = prev.split()[word_location]
            diff = word_location - (prev_length - 1) 
        elif edit[0] == "replace":
            word_location = edit[2]
            word = utt.split()[word_location]
            diff = 1
        else:
            print("duplicate")
            word_location = -10
            diff = 1
        
        result = {'Word Location': word_location, 'Hypothesis Time': time, 'Edit Type': edit[0], 'Word': word}
        if word_location > -9:
            store(result, csv_writer)

        if diff < 0:
            complete_sets(time, word_location, prev.split(), edit[0], csv_writer)


def process(filename, time, previous_utterance, current_utterance):
    # Outer function that is called by platform specific processors.
    # This initialises the output csv with headings.
    file_exists = os.path.isfile(filename)
    fieldnames = ['Word Location', 'Hypothesis Time', "Edit Type", "Word"]

    if not file_exists:
        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

    with open(filename, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        detect_change(time, previous_utterance, current_utterance, writer)


def clean_csv(csv_file):
    # Takes complete csv and cleans indexes as restarts in word numbering occur.
    # This is for the metrics calculations.
    full_history = []
    tmp_index = 0
    index = 0
    edit_history = ""
    at_start = True
    fix_started = False
    fieldnames = ['Word Location', 'Hypothesis Time', "Edit Type", "Word"]
    with fileinput.input(files=(csv_file), inplace=True, mode='r') as f:
        reader = csv.DictReader(f, fieldnames=fieldnames)
        for row in reader:
            if row['Word Location'] == 'Word Location':
                continue
            else:
                word_loc = int(row['Word Location'])
            if word_loc > 0:
                if fix_started:
                    row['Word Location'] = str(word_loc + index)
                if row['Edit Type'] in ('insert', 'delete', 'set'):
                    if row['Edit Type'] in ('insert', 'delete'):
                        edit_history = row['Edit Type']
                    tmp_index = word_loc + index
            else:
                if at_start:
                    at_start = False
                else:
                    if edit_history == 'delete':
                        index = tmp_index - 1
                        row['Word Location'] = str(word_loc + index)
                        fix_started = True
                    else:
                        index = tmp_index +1
                        row['Word Location'] = str(word_loc + index)
                        fix_started = True
            if row['Edit Type'] == "set":
                if row['Word'] != "tsotf":
                    for dct in full_history:
                        if edit_history == 'delete':
                            if int(dct['Loc']) == int(row['Word Location'])+1 and dct['Word'] == row['Word']:
                                row['Hypothesis Time'] = dct['Time']
                        else:
                            if int(dct['Loc']) == int(row['Word Location'])-1 and dct['Word'] == row['Word']:
                                row['Hypothesis Time'] = dct['Time']
            full_history.append({'Loc':row['Word Location'], 'Time':row['Hypothesis Time'], 'Word':row['Word']})
            print(",".join([row['Word Location'], row['Hypothesis Time'], row['Edit Type'], row['Word']]))

def add_trans_chunk(txtFile, text):
    # Takes filename and chunk of final transcript to be stored.
    with open(txtFile, "a") as transFile:
        transFile.write(text + " ")


