import os
import random
import pandas as pd

present_ratio = 0.5
congruent_ratio = 0.5
n_triallists = 10
n_trials = 10

try:
    experiment_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
except NameError:
    experiment_directory = os.getcwd()
stimuli_directory = os.path.join(experiment_directory, "stimuli")
audio_directory = os.path.join(stimuli_directory, "audio")
visual_directory = os.path.join(stimuli_directory, "visual")
triallists_directory = os.path.join(experiment_directory, "triallists")

print(f"Experiment Directory: {experiment_directory}")
print(f"Stimuli Directory: {stimuli_directory}")
print(f"Audio Directory: {audio_directory}")
print(f"Visual Directory: {visual_directory}")
print(f"Triallists Directory: {triallists_directory}")

targets_df = pd.read_csv(os.path.join(stimuli_directory, "target.csv"))
targets = targets_df['target'].tolist()

def create_trial(targets, present_ratio, congruent_ratio):
    cue = random.choice(targets)
    present = 1 if random.random() < present_ratio else 0
    congruent = 1 if random.random() < congruent_ratio else 0
    
    if congruent:
        audio_file = f"{cue}.wav"
    else:
        non_cue_targets = [t for t in targets if t != cue]
        audio_file = f"{random.choice(non_cue_targets)}.wav"
    
    audio_path = os.path.join(audio_directory, audio_file)

    images = []
    if present:
        images.append(f"{cue}.png")
        non_cue_targets = [t for t in targets if t != cue]
        images += [f"{img}.png" for img in random.sample(non_cue_targets, 3)]
    else:
        non_cue_targets = [t for t in targets if t != cue]
        images = [f"{img}.png" for img in random.sample(non_cue_targets, 4)]
    
    image_paths = [os.path.join(visual_directory, img) for img in images]
    
    return [cue, present, congruent, audio_path] + image_paths

for i in range(n_triallists):
    trials = [create_trial(targets, present_ratio, congruent_ratio) for _ in range(n_trials)]
    triallist_df = pd.DataFrame(trials, columns=['cue', 'present', 'congruent', 'audio', 'img1', 'img2', 'img3', 'img4'])

    triallist_filename = f"triallist_{str(i+1).zfill(2)}.csv"
    triallist_path = os.path.join(triallists_directory, triallist_filename)
    triallist_df.to_csv(triallist_path, index=False)

print(f"{n_triallists} trial lists created successfully.")
