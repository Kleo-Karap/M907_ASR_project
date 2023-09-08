# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 16:21:14 2023

@author: kleop
"""


import pandas as pd
import matplotlib.pyplot as plt

#%%
def wer(ref, hyp, debug=True):
    ref_wav_id = ref.split(' ')[0]  # Extract WAV ID from reference line
    hyp_wav_id = hyp.split(' ')[0]  # Extract WAV ID from hypothesis line

    ref = ref.split(' ', 1)[1]  # Remove WAV ID
    hyp = hyp.split(' ', 1)[1]  # Remove WAV ID
 
    r = ref.strip().split()
    h = hyp.strip().split()

    costs = [[0 for _ in range(len(h) + 1)] for _ in range(len(r) + 1)]
    backtrace = [[0 for _ in range(len(h) + 1)] for _ in range(len(r) + 1)]

    OP_OK = 0
    OP_SUB = 1
    OP_INS = 2
    OP_DEL = 3
    DEL_PENALTY = 1
    INS_PENALTY = 1
    SUB_PENALTY = 1

    for i in range(1, len(r) + 1):
        costs[i][0] = DEL_PENALTY * i
        backtrace[i][0] = OP_DEL

    for j in range(1, len(h) + 1):
        costs[0][j] = INS_PENALTY * j
        backtrace[0][j] = OP_INS

    for i in range(1, len(r) + 1):
        for j in range(1, len(h) + 1):
            if r[i - 1] == h[j - 1]:
                costs[i][j] = costs[i - 1][j - 1]
                backtrace[i][j] = OP_OK
            else:
                substitutionCost = costs[i - 1][j - 1] + SUB_PENALTY
                insertionCost = costs[i][j - 1] + INS_PENALTY
                deletionCost = costs[i - 1][j] + DEL_PENALTY

                costs[i][j] = min(substitutionCost, insertionCost, deletionCost)
                if costs[i][j] == substitutionCost:
                    backtrace[i][j] = OP_SUB
                elif costs[i][j] == insertionCost:
                    backtrace[i][j] = OP_INS
                else:
                    backtrace[i][j] = OP_DEL

    i = len(r)
    j = len(h)
    numSub = 0
    numDel = 0
    numIns = 0
    numCor = 0
    if debug:
        print("OP\tREF\tHYP")
        lines = []
    while i > 0 or j > 0:
        if backtrace[i][j] == OP_OK:
            numCor += 1
            i -= 1
            j -= 1
            if debug:
                lines.append("OK\t" + r[i] + "\t" + h[j])
        elif backtrace[i][j] == OP_SUB:
            numSub += 1
            i -= 1
            j -= 1
            if debug:
                lines.append("SUB\t" + r[i] + "\t" + h[j])
        elif backtrace[i][j] == OP_INS:
            numIns += 1
            j -= 1
            if debug:
                lines.append("INS\t" + "****" + "\t" + h[j])
        elif backtrace[i][j] == OP_DEL:
            numDel += 1
            i -= 1
            if debug:
                lines.append("DEL\t" + r[i] + "\t" + "****")
    if debug:
        lines = reversed(lines)
        for line in lines:
            print(line)
        print("#cor " + str(numCor))
        print("#sub " + str(numSub))
        print("#del " + str(numDel))
        print("#ins " + str(numIns))

    wer_result = round((numSub + numDel + numIns) / float(len(r)), 3)
    return {'WER': wer_result, 'numCor': numCor, 'numSub': numSub, 'numIns': numIns, 'numDel': numDel, "numCount": len(r)}
    

#%%
pair_files = [
    ("C:/Users/kleop/Documents/repos/Exercises/ASR_assignment/LibriSpeech/dev-clean-2/84/transcripts/84-121550.trans.txt", "C:/Users/kleop/Documents/repos/Exercises/ASR_assignment/LibriSpeech/dev-clean-2/84/transcripts/trans_noisy_3.txt"),
    ("C:/Users/kleop/Documents/repos/Exercises/ASR_assignment/LibriSpeech/dev-clean-2/174/transcripts/174-168635.trans.txt", "C:/Users/kleop/Documents/repos/Exercises/ASR_assignment/LibriSpeech/dev-clean-2/174/transcripts/trans_noisy_3.txt"),
    ("C:/Users/kleop/Documents/repos/Exercises/ASR_assignment/LibriSpeech/dev-clean-2/251/transcripts_1/251-118436.trans.txt","C:/Users/kleop/Documents/repos/Exercises/ASR_assignment/LibriSpeech/dev-clean-2/251/transcripts_1/trans_noisy_3.txt"),
    ("C:/Users/kleop/Documents/repos/Exercises/ASR_assignment/LibriSpeech/dev-clean-2/251/transcripts_2/251-136532.trans.txt","C:/Users/kleop/Documents/repos/Exercises/ASR_assignment/LibriSpeech/dev-clean-2/251/transcripts_2/trans_noisy_3.txt"),
    ("C:/Users/kleop/Documents/repos/Exercises/ASR_assignment/LibriSpeech/dev-clean-2/777/transcripts/777-126732.trans.txt","C:/Users/kleop/Documents/repos/Exercises/ASR_assignment/LibriSpeech/dev-clean-2/777/transcripts/trans_noisy_3.txt"),
    ("C:/Users/kleop/Documents/repos/Exercises/ASR_assignment/LibriSpeech/dev-clean-2/1272/transcripts_1/1272-135031.trans.txt","C:/Users/kleop/Documents/repos/Exercises/ASR_assignment/LibriSpeech/dev-clean-2/1272/transcripts_1/trans_noisy_3.txt"),
    ("C:/Users/kleop/Documents/repos/Exercises/ASR_assignment/LibriSpeech/dev-clean-2/1272/transcripts_2/1272-141231.trans.txt","C:/Users/kleop/Documents/repos/Exercises/ASR_assignment/LibriSpeech/dev-clean-2/1272/transcripts_2/trans_noisy_3.txt"),
    ("C:/Users/kleop/Documents/repos/Exercises/ASR_assignment/LibriSpeech/dev-clean-2/1462/transcripts_1/1462-170142.trans.txt","C:/Users/kleop/Documents/repos/Exercises/ASR_assignment/LibriSpeech/dev-clean-2/1462/transcripts_1/trans_noisy_3.txt"),
    ("C:/Users/kleop/Documents/repos/Exercises/ASR_assignment/LibriSpeech/dev-clean-2/1462/transcripts_2/1462-170145.trans.txt","C:/Users/kleop/Documents/repos/Exercises/ASR_assignment/LibriSpeech/dev-clean-2/1462/transcripts_2/trans_noisy_3.txt"),
    ("C:/Users/kleop/Documents/repos/Exercises/ASR_assignment/LibriSpeech/dev-clean-2/1988/transcripts_1/1988-24833.trans.txt","C:/Users/kleop/Documents/repos/Exercises/ASR_assignment/LibriSpeech/dev-clean-2/1988/transcripts_1/trans_noisy_3.txt"),
    ("C:/Users/kleop/Documents/repos/Exercises/ASR_assignment/LibriSpeech/dev-clean-2/1988/transcripts_2/1988-147956.trans.txt","C:/Users/kleop/Documents/repos/Exercises/ASR_assignment/LibriSpeech/dev-clean-2/1988/transcripts_2/trans_noisy_3.txt"),
    ("C:/Users/kleop/Documents/repos/Exercises/ASR_assignment/LibriSpeech/dev-clean-2/1993/transcripts/1993-147964.trans.txt","C:/Users/kleop/Documents/repos/Exercises/ASR_assignment/LibriSpeech/dev-clean-2/1993/transcripts/trans_noisy_3.txt"),
    ("C:/Users/kleop/Documents/repos/Exercises/ASR_assignment/LibriSpeech/dev-clean-2/2035/transcripts_2/2035-147961.trans.txt","C:/Users/kleop/Documents/repos/Exercises/ASR_assignment/LibriSpeech/dev-clean-2/2035/transcripts_2/trans_noisy_3.txt"),
    ("C:/Users/kleop/Documents/repos/Exercises/ASR_assignment/LibriSpeech/dev-clean-2/2035/transcripts_3/2035-152373.trans.txt","C:/Users/kleop/Documents/repos/Exercises/ASR_assignment/LibriSpeech/dev-clean-2/2035/transcripts_3/trans_noisy_3.txt"),
    ("C:/Users/kleop/Documents/repos/Exercises/ASR_assignment/LibriSpeech/dev-clean-2/2412/transcripts/2412-153948.trans.txt","C:/Users/kleop/Documents/repos/Exercises/ASR_assignment/LibriSpeech/dev-clean-2/2412/transcripts/trans_noisy_3.txt"),
    ("C:/Users/kleop/Documents/repos/Exercises/ASR_assignment/LibriSpeech/dev-clean-2/2428/transcripts/2428-83699.trans.txt","C:/Users/kleop/Documents/repos/Exercises/ASR_assignment/LibriSpeech/dev-clean-2/2428/transcripts/trans_noisy_3.txt"),
    ("C:/Users/kleop/Documents/repos/Exercises/ASR_assignment/LibriSpeech/dev-clean-2/2803/transcripts_1/2803-154320.trans.txt","C:/Users/kleop/Documents/repos/Exercises/ASR_assignment/LibriSpeech/dev-clean-2/2803/transcripts_1/trans_noisy_3.txt"),
    ("C:/Users/kleop/Documents/repos/Exercises/ASR_assignment/LibriSpeech/dev-clean-2/2803/transcripts_2/2803-161169.trans.txt","C:/Users/kleop/Documents/repos/Exercises/ASR_assignment/LibriSpeech/dev-clean-2/2803/transcripts_2/trans_noisy_3.txt"),
    ("C:/Users/kleop/Documents/repos/Exercises/ASR_assignment/LibriSpeech/dev-clean-2/3000/transcripts/3000-15664.trans.txt","C:/Users/kleop/Documents/repos/Exercises/ASR_assignment/LibriSpeech/dev-clean-2/3000/transcripts/trans_noisy_3.txt"),
    ("C:/Users/kleop/Documents/repos/Exercises/ASR_assignment/LibriSpeech/dev-clean-2/3536/transcripts/3536-23268.trans.txt","C:/Users/kleop/Documents/repos/Exercises/ASR_assignment/LibriSpeech/dev-clean-2/3536/transcripts/trans_noisy_3.txt"),
    ("C:/Users/kleop/Documents/repos/Exercises/ASR_assignment/LibriSpeech/dev-clean-2/3576/transcripts/3576-138058.trans.txt","C:/Users/kleop/Documents/repos/Exercises/ASR_assignment/LibriSpeech/dev-clean-2/3576/transcripts/trans_noisy_3.txt"),
    ("C:/Users/kleop/Documents/repos/Exercises/ASR_assignment/LibriSpeech/dev-clean-2/3752/transcripts/3752-4944.trans.txt","C:/Users/kleop/Documents/repos/Exercises/ASR_assignment/LibriSpeech/dev-clean-2/3752/transcripts/trans_noisy_3.txt"),
    ("C:/Users/kleop/Documents/repos/Exercises/ASR_assignment/LibriSpeech/dev-clean-2/5338/transcripts_1/5338-24640.trans.txt","C:/Users/kleop/Documents/repos/Exercises/ASR_assignment/LibriSpeech/dev-clean-2/5338/transcripts_1/trans_noisy_3.txt"),
    ("C:/Users/kleop/Documents/repos/Exercises/ASR_assignment/LibriSpeech/dev-clean-2/5338/transcripts_2/5338-284437.trans.txt","C:/Users/kleop/Documents/repos/Exercises/ASR_assignment/LibriSpeech/dev-clean-2/5338/transcripts_2/trans_noisy_3.txt"),
    ("C:/Users/kleop/Documents/repos/Exercises/ASR_assignment/LibriSpeech/dev-clean-2/5694/transcripts/5694-64038.trans.txt","C:/Users/kleop/Documents/repos/Exercises/ASR_assignment/LibriSpeech/dev-clean-2/5694/transcripts/trans_noisy_3.txt"),
    ("C:/Users/kleop/Documents/repos/Exercises/ASR_assignment/LibriSpeech/dev-clean-2/5895/transcripts_1/5895-34615.trans.txt","C:/Users/kleop/Documents/repos/Exercises/ASR_assignment/LibriSpeech/dev-clean-2/5895/transcripts_1/trans_noisy_3.txt"),
    ("C:/Users/kleop/Documents/repos/Exercises/ASR_assignment/LibriSpeech/dev-clean-2/5895/transcripts_2/5895-34622.trans.txt","C:/Users/kleop/Documents/repos/Exercises/ASR_assignment/LibriSpeech/dev-clean-2/5895/transcripts_2/trans_noisy_3.txt"),
    ("C:/Users/kleop/Documents/repos/Exercises/ASR_assignment/LibriSpeech/dev-clean-2/5895/transcripts_3/5895-34629.trans.txt","C:/Users/kleop/Documents/repos/Exercises/ASR_assignment/LibriSpeech/dev-clean-2/5895/transcripts_3/trans_noisy_3.txt"),
    ("C:/Users/kleop/Documents/repos/Exercises/ASR_assignment/LibriSpeech/dev-clean-2/6241/transcripts_1/6241-61943.trans.txt","C:/Users/kleop/Documents/repos/Exercises/ASR_assignment/LibriSpeech/dev-clean-2/6241/transcripts_1/trans_noisy_3.txt"),
    ("C:/Users/kleop/Documents/repos/Exercises/ASR_assignment/LibriSpeech/dev-clean-2/6241/transcripts_2/6241-61946.trans.txt","C:/Users/kleop/Documents/repos/Exercises/ASR_assignment/LibriSpeech/dev-clean-2/6241/transcripts_2/trans_noisy_3.txt"),
    ("C:/Users/kleop/Documents/repos/Exercises/ASR_assignment/LibriSpeech/dev-clean-2/6295/transcripts/6295-244435.trans.txt","C:/Users/kleop/Documents/repos/Exercises/ASR_assignment/LibriSpeech/dev-clean-2/6295/transcripts/trans_noisy_3.txt"),
    ("C:/Users/kleop/Documents/repos/Exercises/ASR_assignment/LibriSpeech/dev-clean-2/6319/transcripts/6319-57405.trans.txt","C:/Users/kleop/Documents/repos/Exercises/ASR_assignment/LibriSpeech/dev-clean-2/6319/transcripts/trans_noisy_3.txt"),
    ("C:/Users/kleop/Documents/repos/Exercises/ASR_assignment/LibriSpeech/dev-clean-2/7850/transcripts_1/7850-281318.trans.txt","C:/Users/kleop/Documents/repos/Exercises/ASR_assignment/LibriSpeech/dev-clean-2/7850/transcripts_1/trans_noisy_3.txt"),
    ("C:/Users/kleop/Documents/repos/Exercises/ASR_assignment/LibriSpeech/dev-clean-2/7850/transcripts_2/7850-286674.trans.txt","C:/Users/kleop/Documents/repos/Exercises/ASR_assignment/LibriSpeech/dev-clean-2/7850/transcripts_2/trans_noisy_3.txt"),
    ("C:/Users/kleop/Documents/repos/Exercises/ASR_assignment/LibriSpeech/dev-clean-2/7976/transcripts/7976-110523.trans.txt","C:/Users/kleop/Documents/repos/Exercises/ASR_assignment/LibriSpeech/dev-clean-2/7976/transcripts/trans_noisy_3.txt"),
    ("C:/Users/kleop/Documents/repos/Exercises/ASR_assignment/LibriSpeech/dev-clean-2/8297/transcripts/8297-275156.trans.txt","C:/Users/kleop/Documents/repos/Exercises/ASR_assignment/LibriSpeech/dev-clean-2/8297/transcripts/trans_noisy_3.txt"),
    ("C:/Users/kleop/Documents/repos/Exercises/ASR_assignment/LibriSpeech/dev-clean-2/8842/transcripts/8842-304647.trans.txt","C:/Users/kleop/Documents/repos/Exercises/ASR_assignment/LibriSpeech/dev-clean-2/8842/transcripts/trans_noisy_3.txt")
    
]
#%%
results = []
for ref_file, hyp_file in pair_files:
    ref_lines = []
    hyp_lines = []

    with open(ref_file, 'r') as f:
        ref_lines = f.readlines()

    with open(hyp_file, 'r') as f:
        hyp_lines = f.readlines()

    for ref_line, hyp_line in zip(ref_lines, hyp_lines):
        ref_wav_id = ref_line.split(' ')[0]  # Extract the WAV ID from the reference line
        hyp_wav_id = hyp_line.split(' ')[0]  # Extract the WAV ID from the hypothesis line

        result = wer(ref_line, hyp_line)
        result['WAV_ID'] = hyp_wav_id  # Use the WAV ID from the hypothesis line
        results.append(result)
#%%
df = pd.DataFrame(results)
df = df[['WAV_ID', 'WER', 'numCor', 'numSub', 'numIns', 'numDel', 'numCount']]  # Rearrange columns if needed
#%%
# Save the dataframe to a CSV file
df.to_csv('results_noisy_3.csv', index=False)

#%%
wer_results_noisy_3 = pd.read_csv("results_noisy_3.csv", sep=',', decimal=".")
wer_results_noisy_3.head()
mean_wer_noisy_3 = wer_results_noisy_3['WER'].mean()
print(mean_wer_noisy_3)

#%%
wer_results_noisy_3.describe()
#%%
# Assuming you have already created the DataFrame 'df' with the WER results

# Group the DataFrame by WAV ID and calculate the mean WER for each sentence
wer_by_sentence = wer_results_noisy_3.groupby('WAV_ID')['WER'].mean()

# Plotting the WER values for each sentence
plt.figure(figsize=(10, 6))
wer_by_sentence.plot(kind='box')
plt.xlabel('WAV ID')
plt.ylabel('WER')
plt.title('WER by Sentence')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


#%%







