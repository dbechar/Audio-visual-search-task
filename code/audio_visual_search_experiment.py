from os.path import join
from pandas import read_csv
import expyriment
import random

exp = expyriment.design.Experiment(name="audio-visual search task")
expyriment.control.initialize(exp)
control.set_develop_mode(on=True) ## Set develop mode. Comment out for actual experiment

fixcross = expyriment.stimuli.FixCross(size=(25, 25),
                                 line_width=3,
                                 colour=expyriment.misc.constants.C_WHITE)

code_directory = dirname(__file__) 
triallists_directory = join(dirname(code_directory), "triallists")
trial_list_filename = join(triallists_directory, f"trials_{participant_number.zfill(2)}_.csv")
trials = read_csv(trial_list_filename)


exp.add_data_variable_names(['key', 'rt'])

expyriment.control.start()


instructions = (
    "Welcome to this audio-visual search experiment! Please carefully read the instructions below before beginning."
    "In each trial, you'll be presented with an object that you'll need to locate in the following search display."
    "Your task is to determine whether the previously cued object is present by pressing the F-key for 'present' or the J-key for 'not present'."
    "Press any key to begin with some practice trials.")
expyriment.stimuli.TextLine(instructions).present()
exp.keyboard.wait()


for row in trials.itertuples():
    cue = row.cue
    target_present = row.present
    audio_congruent = row.congruent
    audio = expyriment.stimuli.Audio(join("sounds", row.audio))
    images = [expyriment.stimuli.Picture(join("pictures", getattr(row, f"img{i}"))) for i in range(1, 5)] 
    for image in images:
        image.preload()

    fixcross.present()
    exp.clock.wait(500)

    expyriment.stimuli.TextLine(cue).present() 
    exp.clock.wait(1500)

    fixation_duration = random.randint(300, 500)
    fixcross.present()
    exp.clock.wait(fixation_duration) 

    audio.present()
    for image in images:
        image.present()

    response_given = False
    exp.clock.reset_stopwatch()
    while not response_given:  
        key, rt = exp.keyboard.check()
        if key:  
            response_given = True  
        
    exp.data.add([row.cue, row.present, row.congruent, row.audio, row.img1, row.img2, row.img3, row.img4 key, rt])

expyriment.control.end()