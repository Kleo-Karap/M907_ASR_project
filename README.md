# M907_Automatic Speech Recognition
M.Sc. in Language Technology M907- ASR Assignment: Experiments and Evaluation on Mozilla DeepSpeech

This is a useful repo for you to experiment with the effect of the lanugage model, the word insertion bonus, as well as background noise in the transcription performance of the pretrained English model of Mozilla Deepspeech. The evaluation metric used is the Word Error Rate, which is the sum of word substitutions, deletions and insertions divided by the number of words in the reference sentence.

## User Instructions

### 1) Generating Noisy files with SNR(signal to noise ratio)= [3,6,9] dB and comparing the spectograms of clean and noisy files.
Refer to the notebook "Adding noise.ipynb"

```
signal, sr = librosa.load("C:/Users/path_to_your_original_audio_file.wav", sr=16000)
noise, sr_noise = librosa.load("C:/Users/path_to_your_chosen_noise.wav", sr=16000)
```
For more noise recordings check DEMAND database: https://zenodo.org/record/1227121#.ZCxVHuwvPvV
Choose the ones that end in _16k.zip to have sampling rate=16000 Hz

### 2) Generating transcriptions with Mozilla DeepSpeech

a)From noisy .wav files

b)From clean .wav files by adjusting the effect of the language model (lm_alpha) or/and the word insertion bonus (lm_beta)

Refer to the notebook "Transcriptions with Mozilla Deepspeech.ipynb"

Download the pretrained language (deepspeech-0.9.3-models.scorer)  and acoustic models (deepspeech-0.9.3-models.pbmm)  from : https://github.com/mozilla/DeepSpeech/releases

Experiment with several lm_alpha and lm_beta values

Special thanks to Rosario-Moscato-Lab. GitHub. [https://github.com/rosariomoscato/Rosario-Moscato-Lab](https://github.com/rosariomoscato/Rosario-Moscato-Lab/blob/main/Audio/DeepSpeech.ipynb), for helping me in the generating the transcription files with DeepSpeech!


### 3) Comparing the WER results
Refer to folder "WER calculation scripts"

```
pair_files = [
    ("C:/Users/path_to_original_transcription.txt", "C:/Users/path_to_noisy_file_transcription_(or)_to_transcription_with_new_lm_alpha_or_beta_value.txt")]
```
Each script will generate a .csv file, containing all WAV files with their WAV_ids as identifiers along with their WER score, as well as 
1) the number of Correctly transcribed words (C)
2) the number of Substitutions (S)
3)  Deletions (D)
4)  Insertions (I)
5) word count per .wav file. (N)

These .csv files can be used for comparing the WER-results in the generated versions of the transcribed datasets and for making more application-specific decisions on fine-tuning Mozilla DeepSpeech. The image below shows an example comparatory plot of the different vlaues I tried on the language model(lm_alpha), the word insertion bonus(lm_beta=2) and the signal to noise ratio in the noisy transcritpions for my assignment. You can experiment with more extreme values for fun.
![image](https://github.com/Kleo-Karap/M907_ASR/assets/117507917/c7c151e5-8321-4a44-8885-afeaf3b1df70)

Since you're plotting mean vlaues of WER ,it's best practice to preprocess the .csv files and eliminate outliers from your datasets in order to avoid misrepresenting your results. For this purpose, you can check the notebook "Comparing WER results.ipynb".

## Contributor Expectations
1. Experiment with new datasets apart from [MiniLibriSpeech](https://www.openslr.org/31/)  (perhaps domain specific ones)
2. Adjust the code to add more evaluation metrics on the experiment setting, like (Character Error Rate (CER), Word Information Lost (WIL) or Match Error Rate (MER)

## References
1. How to calculate Word Error Rate in Python. (2023, July 27). PyZone. https://pyzone.dev/how-to-calculate-word-error-rate-in-python/
2. Morris, A., Maier, V., & Green, P. (n.d.). From WER and RIL to MER and WIL: improved evaluation measures for connected speech recognition. Retrieved September 9, 2023, from https://www.isca-speech.org/archive_v0/archive_papers/interspeech_2004/i04_2765.pdf
3. Using a Pre-trained Model — Mozilla DeepSpeech 0.9.3 documentation. (n.d.). Deepspeech.readthedocs.io. Retrieved September 9, 2023, from https://deepspeech.readthedocs.io/en/r0.9/USING.html
4. Speech To Text with DeepSpeech (Python Package). (Moscato, R. ). Www.youtube.com. Retrieved September 9, 2023, from https://www.youtube.com/watch?v=LGuCaXw79U4&ab_channel=AIDemistified
