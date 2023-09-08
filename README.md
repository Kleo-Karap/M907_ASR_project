# M907_Automatic Speech Recognition
M.Sc. in Language Technology M907- ASR Assignment

This is a useful repo for you to experiment with the effect of the lanugage model (lm_alpha),the effect of the word insertion bonus(lm_beta), as well as the effect of background noise in the transcription performance of the pretrained English model of Mozilla Deepspeech. The evaluation metric used is the Word Error Rate, which is the sum of word substitutions, deletions and insertions divided by the number of words in the reference sentence.

## User Instructions

### 1) Generating Noisy files with SNR(signal to noise ratio)= [3,6,9] dB and comparing the spectograms of clean and noisy files.
Refer to the notebook "Adding noise.ipynb"

```
signal, sr = librosa.load("C:/Users/path_to_your_original_audio_file.wav", sr=16000)
noise, sr_noise = librosa.load("C:/Users/path_to_your_chosen_noise.wav", sr=16000)
```
