# Incremental ASR Evaluation

This repository allows you to evaluate Incremental ASR systems, using the transcriptions from our [Incremental ASR Processing repository](https://github.com/wallscope-research/incremental-asr-processing). This was originally created for a [paper published at COLING 2020](https://www.aclweb.org/anthology/2020.coling-main.312.pdf).

The paper (by [Angus Addlesee](http://addlesee.co.uk/), [Yanchao Yu](https://www.researchgate.net/profile/Yanchao_Yu), and [Arash Eshghi](https://sites.google.com/site/araesh81/)) can be found [here](https://www.aclweb.org/anthology/2020.coling-main.312.pdf) and is titled: "A Comprehensive Evaluation of Incremental Speech Recognition and Diarization for Conversational AI".

If you use this repository in your work - please cite us:

Harvard:
```
Addlesee, A., Yu, Y. and Eshghi, A., 2020. A Comprehensive Evaluation of Incremental Speech Recognition and Diarization for Conversational AI. COLING 2020.
```

BibTeX:
```
@inproceedings{addlesee2020evaluation,
  title={A Comprehensive Evaluation of Incremental Speech Recognition and Diarization for Conversational AI},
  author={Addlesee, Angus and Yu, Yanchao and Eshghi, Arash},
  journal={COLING 2020},
  year={2020}
}
```

## Outline of Repository

This repository contains both a modified version of [JiWER](https://github.com/jitsi/jiwer) and a range of additional scripts to run our experiments, calculate metrics, and produce final charts. The unmodified [JiWER](https://github.com/jitsi/jiwer) is used to calculate the WER but we exposed some of its inner workings for our use. For example, [JiWER](https://github.com/jitsi/jiwer) calculates the minimum edit distance and we grab the exact 'edit steps' which describe this transformation.

## Installation

We have created a setup script to prepare your system to use this repository. This script will create a virtual Python environment and install the required packages within it. You can clone this repository and run the setup with the following commands:

1. Run `git clone https://github.com/wallscope-research/incremental-asr-evaluation.git`
2. Run `cd incremental-asr-evaluation`
3. Run `./setup.sh`

You need to be within this virtual environment to run any processing. To enter and exit this environment, please use the relevant line:

- To enter the virtual environment, run `source venv/bin/activate`
- To exit the virtual environment, run `deactivate`

Note - you only need to run the setup script once, but it must have been run to use the above two commands.

### User Guide (in progress)

A full user guide with an example walkthrough is en-route!

## Script Descriptions

- `disfluencies.py`: Given a system and code, this script calculates the mean split WER (mean across the two channels). This is done for each disfluency cleaning method and mean split WERs are stored per method.
- `disfluency-results.py`: Given a system, this script calculates the final mean split WER (mean across all conversations) per disfluency cleaning method. These final results are printed.
- `final-results.py`: This script generates and saves all the result charts (and prints the final WERs) for all systems.
- `get-codes.py`: Given a switchboard transcript, the id code of that transcript is grabbed and stored in a list. This list is useful for running other scripts across many conversations.
- `google-format.py`: Given a transcript from Google, this script transforms it into our universal format. A csv in this universal format is stored.
- `google-results.py`: Given a code, this script calculates several metrics (stability, WER, and latencies) and then stores them. These metrics represent Google's performance on the conversation, identified with the given code.
- `ibm-format.py`: Given a transcript from IBM, this script transforms it into our universal format. A csv in this universal format is stored.
- `ibm-results.py`: Given a code, this script calculates several metrics (stability, WER, and latencies) and then stores them. These metrics represent IBMs performance on the conversation, identified with the given code.
- `metrics.py`: This file defines the functions to calculate the stability, WER, and latency metrics.
- `min_wer.py`: This script calculates the MWERI for each system and prints them. This is for the overlap experiment.
- `msoft-format.py`: Given a transcript from Microsoft, this script transforms it into our universal format. A csv in this universal format is stored.
- `msoft-results.py`: Given a code, this script calculates several metrics (stability, WER, and latencies) and then stores them. These metrics represent Microsoft's performance on the conversation, identified with the given code.
- `split-get-codes.py`: Given a switchboard transcript, the id code of that transcript is grabbed and stored in a list. This list is useful for running other scripts across many conversations.
- `split-google-format.py`: Given the single-channel Google transcript and which channel it is (left or right), this script transforms it into our universal format.
- `split-ibm-format.py`: Given the single-channel IBM transcript and which channel it is (left or right), this script transforms it into our universal format.
- `split-msoft-format.py`: Given the single-channel Microsoft transcript and which channel it is (left or right), this script transforms it into our universal format.
- `split_wer.py`: Given a system and code, this script returns the split WER and stores it.
- `universal.py`: This script contains the functions to create and manipulate our universal format.

## Switchboard Corpus

We use the [Switchboard Corpus](https://catalog.ldc.upenn.edu/LDC97S62) to evaluate incremental ASR systems - if you would like to recreate the experiments in our COLING 2020 paper, you can find the information in the `switchboard` directory. Within you will find our script to 'clean' disfluencies in the gold transcriptions, and find the script to format Switchboard with its timings into the several required formats.

## Acknowledgements

[Angus Addlesee](http://addlesee.co.uk/) is funded by [Wallscope](https://wallscope.co.uk/) and [The Data Lab](https://www.thedatalab.com/). [Yanchao Yu](https://www.researchgate.net/profile/Yanchao_Yu) is funded by the Horizon2020 [SPRING Project](https://spring-h2020.eu/). We thank them for their support.