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

This repository is a modified version of [JiWER](https://github.com/jitsi/jiwer) with a vast range of additional scripts to run our experiments, calculate metrics, and produce final charts. The unmodified [JiWER](https://github.com/jitsi/jiwer) is used to calculate the WER but we exposed some of its inner workings for our use. For example, [JiWER](https://github.com/jitsi/jiwer) calculates the minimum edit distance and we grab the exact 'edit steps' which describe this transformation.

### Structure (in progress)

TODO

## Installation (in progress)

TODO

## User Guide (in progress)

TODO

## Switchboard Corpus

We use the [Switchboard Corpus](https://catalog.ldc.upenn.edu/LDC97S62) to evaluate incremental ASR systems - if you would like to recreate the experiments in our COLING 2020 paper, you can find the information in the `switchboard` directory. Within you will find our script to 'clean' disfluencies in the gold transcriptions, and find the script to format Switchboard with its timings into the several required formats.

## Acknowlegements

[Angus Addlesee](http://addlesee.co.uk/) is funded by [Wallscope](https://wallscope.co.uk/) and [The Data Lab](https://www.thedatalab.com/). [Yanchao Yu](https://www.researchgate.net/profile/Yanchao_Yu) is funded by the Horizon2020 [SPRING Project](https://spring-h2020.eu/). We thank them for their support.