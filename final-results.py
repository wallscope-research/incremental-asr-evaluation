import os
import sys
import ast
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# List systems for final loop through for result charts.
list_of_systems = ['microsoft', 'ibm', 'google'] ## TODO Add systems here as required.
figures_path = "./results/combined-charts/"

def comb_stability(systems):
    for system in systems:
        if system == 'microsoft':
            sub_dir = "msoft/"
            # This multiplier is used to convert Microsoft's reported timings into seconds (in line with all other timings).
            multiplier = 10**-7
        else:
            sub_dir = system + "/"
            multiplier = 1 ## TODO Add elif statements here for other systems with non-1 multipliers.

        path = "./results/" + sub_dir
        stab_path = path + "stability/"

        stability = []

        # For all output stability files (per system), read stabilities.
        for stab_file in os.listdir(stab_path):
            with open(stab_path + stab_file, 'r') as sf:
                new_stabs = ast.literal_eval(sf.read())
                stability = stability + new_stabs

        stab_keys = []
        stab_pcent = []
        prev = 0

        # Sort stabilities for percentage calculations.
        stability = sorted(stability)

        for i, item in enumerate(stability):
            # For each new reported stability time, calculate what percentage of hypotheses are stable.
            if item != prev:
                pcent = (i/len(stability))*100
                stab_keys.append(round(prev*multiplier, 2))
                stab_pcent.append(pcent)
                prev = item

        stab_keys.append(round(prev*multiplier, 2))
        stab_pcent.append(100)

        # Once all stability times are aggregated and percentages calculated - create data frame of info.
        df = pd.DataFrame(list(zip(stab_keys, stab_pcent)), columns = ['seconds', 'pcent'])
        sns.lineplot(x = "seconds", y = "pcent", data = df, label=system)
    # Plot for all systems to compare.
    plt.legend(prop={'size': 10}, title = 'Systems')
    plt.title('Word Survival Rate')
    plt.xlabel('"Age" of Hypothesised Word (s)')
    plt.ylabel('Percentage of Surviving Hypotheses')
    plt.xlim((0, 2.6))
    # Store plot.
    plt.savefig(figures_path + "stability.png")
    plt.clf()


def comb_fo(systems):
    for system in systems:
        if system == 'microsoft':
            sub_dir = "msoft/"
            multiplier = 10**-7
        else:
            sub_dir = system + "/"
            multiplier = 1 ## TODO Add elif statements here for other systems with non-1 multipliers.

        path = "./results/" + sub_dir
        fo_path = path + "latency/fo/"

        fo = []

        # For all of a system's calculated fo latencies, combine.
        for fo_file in os.listdir(fo_path):
            with open(fo_path + fo_file, 'r') as fof:
                new_fos = ast.literal_eval(fof.read())
                fo = fo + new_fos

        df = pd.DataFrame(fo)
        sns.distplot(df, hist=False, kde=True, kde_kws={'shade': True, 'linewidth': 3}, norm_hist=True, label=system)
    # Plot for all systems to compare.
    plt.legend(prop={'size': 10}, title = 'Systems')
    plt.title('Density Plot of First Occurance Times')
    plt.xlabel('FO Time From Start of Word (s)')
    plt.ylabel('Probability Density')
    plt.xlim((0, 4))
    # Store plot.
    plt.savefig(figures_path + "fo.png")
    plt.clf()


def comb_fd(systems):
    for system in systems:
        if system == 'microsoft':
            sub_dir = "msoft/"
            multiplier = 10**-7
        else:
            sub_dir = system + "/"
            multiplier = 1 ## TODO Add elif statements here for other systems with non-1 multipliers.

        path = "./results/" + sub_dir
        fd_path = path + "latency/fd/"

        fd = []

        # For all of a system's calculated fd latencies, combine.
        for fd_file in os.listdir(fd_path):
            with open(fd_path + fd_file, 'r') as fdf:
                new_fds = ast.literal_eval(fdf.read())
                fd = fd + new_fds

        df = pd.DataFrame(fd)
        sns.distplot(df, hist=False, kde=True, kde_kws={'shade': True, 'linewidth': 3}, norm_hist=True, label=system)
    # Plot for all systems to compare.
    plt.legend(prop={'size': 10}, title = 'Systems')
    plt.title('Density Plot of Final Decision Times')
    plt.xlabel('FD Time From End of Word (s)')
    plt.ylabel('Probability Density')
    plt.xlim((-2, 4))
    # Store plot.
    plt.savefig(figures_path + "fd.png")
    plt.gcf()
    plt.clf()


def comb_wer(systems):
    for system in systems:
        if system == 'microsoft':
            sub_dir = "msoft/"
            multiplier = 10**-7
        else:
            sub_dir = system + "/"
            multiplier = 1 ## TODO Add elif statements here for other systems with non-1 multipliers.

        path = "./results/" + sub_dir
        wer_path = path + "full-wer/"

        wer_sum = 0
        wer_count = 0

        # For each conversations WER, aggregate to system level.
        for wer_file in os.listdir(wer_path):
            with open(wer_path + wer_file, 'r') as wf:
                addition = float(wf.read())
                wer_sum = wer_sum + addition
                wer_count = wer_count + 1
        
        # Print final system WER.
        wer_result = wer_sum / wer_count
        print(system + " WER:  " + str(wer_result))


# Call all functions to calc results.
comb_stability(list_of_systems)
comb_fo(list_of_systems)
comb_fd(list_of_systems)
comb_wer(list_of_systems)