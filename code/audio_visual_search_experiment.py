from os.path import join, dirname
from pandas import read_csv
import expyriment
import random
import math

participant_number = input("Please enter your participant number: ")

exp = expyriment.design.Experiment(name="audio-visual search task")
expyriment.control.initialize(exp)
expyriment.control.set_develop_mode(on=True)  # Set develop mode. Comment out for actual experiment

fixcross = expyriment.stimuli.FixCross(size=(25, 25),
                                       line_width=3,
                                       colour=expyriment.misc.constants.C_WHITE)

code_directory = dirname(__file__)
triallists_directory = join(dirname(code_directory), "triallists")
trial_list_filename = join(triallists_directory, f"triallist_{participant_number.zfill(2)}.csv")
trials = read_csv(trial_list_filename)

exp.add_data_variable_names(['key', 'rt'])
expyriment.control.start()

instructions = (
    "Welcome to this audio-visual search experiment! Please carefully read the instructions below before beginning."
    "In each trial, you'll be presented with the name of an object (for example 'dog') that you'll need to locate in the following search display."
    "Your task is to determine whether the previously cued object is present by pressing the F-key for 'present' or the J-key for 'not present'."
    "Press any key to start.")
expyriment.stimuli.TextLine(instructions).present()
exp.keyboard.wait()

def get_non_overlapping_positions(num_positions, radius, image_size, center):
    positions = []
    while len(positions) < num_positions:
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(0, radius)
        x = center[0] + distance * math.cos(angle)
        y = center[1] + distance * math.sin(angle)
        
        # Check if the new position overlaps with any existing positions
        overlap = False
        for pos in positions:
            if abs(x - pos[0]) < image_size[0] and abs(y - pos[1]) < image_size[1]:
                overlap = True
                break
        
        if not overlap:
            positions.append((x, y))
    
    return positions

for row in trials.itertuples():
    cue = row.cue
    target_present = row.present
    audio_congruent = row.congruent
    audio = expyriment.stimuli.Audio(join("sounds", row.audio))
    images = [expyriment.stimuli.Picture(join("pictures", getattr(row, f"img{i}"))) for i in range(1, 5)]
    
    # Resize all images to 100x100 pixels
    for image in images:
        image.resize((100, 100))
        image.preload()
    
    fixcross.present()
    exp.clock.wait(500)

    expyriment.stimuli.TextLine(cue).present()
    exp.clock.wait(1500)

    fixation_duration = random.randint(300, 500)
    fixcross.present()
    exp.clock.wait(fixation_duration)

    audio.preload()
    audio.present()

    # Randomly position images within a circle around the center
    screen_center = (exp.screen.window_size[0] // 2, exp.screen.window_size[1] // 2)
    radius = 800  # Example radius, adjust as needed
    image_size = (100, 100)
    positions = get_non_overlapping_positions(4, radius, image_size, screen_center)
    
    for image, position in zip(images, positions):
        image.position = position
        image.present()

    response_given = False
    exp.clock.reset_stopwatch()
    max_duration = 5000  # maximum duration in milliseconds

    while not response_given and exp.clock.stopwatch_time < max_duration:
        key, rt = exp.keyboard.check()
        if key:
            response_given = True

    exp.data.add([row.cue, row.present, row.congruent, row.audio, row.img1, row.img2, row.img3, row.img4, key if response_given else None, rt if response_given else None])

expyriment.control.end()