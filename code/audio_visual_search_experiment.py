from os.path import join, dirname, abspath
from pandas import read_csv
import expyriment
import random
import math

participant_number = input("Please enter your participant number: ")

exp = expyriment.design.Experiment(name="audio-visual search task")
expyriment.control.initialize(exp)
expyriment.control.set_develop_mode(on=True)  # Set develop mode. Comment out for actual experiment

fixcross = expyriment.stimuli.FixCross(size=(25, 25), line_width=3, colour=expyriment.misc.constants.C_WHITE)


code_directory = dirname(abspath(__file__))
triallists_directory = join(dirname(code_directory), "triallists")
trial_list_filename = join(triallists_directory, f"triallist_{participant_number.zfill(2)}.csv")
trials = read_csv(trial_list_filename)

exp.add_data_variable_names(['cue', 'present', 'congruent', 'audio', 'img1', 'img2', 'img3', 'img4', 'key', 'rt'])
expyriment.control.start()

instructions = (
    "Welcome to this audio-visual search experiment!\n\n"
    "Please carefully read the instructions below before beginning:\n\n"
    "In each trial, you'll be presented with the name of an object (for example 'dog')."
    "Your task is to locate this object in the following search display.\n\n"
    "For each search display, an audio cue will also be played. Please ensure your audio is on and at a comfortable volume level.\n\n"
    "Your task is to determine whether the previously cued object is present in the display. "
    "Press the 'F' key if the object is present, and press the 'J' key if the object is not present.\n\n"
    "When you are ready, press any key to start the experiment.\n\n"
    "Thank you for your participation and good luck!"
)

instruction_box = expyriment.stimuli.TextBox(
    size=(900, 500),  
    text=instructions,
    text_size=25,
    text_colour=expyriment.misc.constants.C_WHITE,
    background_colour=expyriment.misc.constants.C_BLACK,
    position=(0, 0))
instruction_box.present()
exp.keyboard.wait()

def get_non_overlapping_positions(num_positions, radius, image_size, center):
    positions = []
    while len(positions) < num_positions:
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(0, radius)
        x =  distance * math.cos(angle)
        y =  distance * math.sin(angle)
        
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

    images = [expyriment.stimuli.Picture(join("pictures", getattr(row, f"img{i}"))) for i in range(1, 9)]
    for image in images:
        image.preload()
    
    exp.screen.clear()
    exp.clock.wait (1500)

    fixcross.present()
    exp.clock.wait(500)

    expyriment.stimuli.TextLine(cue, text_size = 25, text_colour = (255, 255, 255)).present()
    exp.clock.wait(800)

    fixation_duration = random.randint(200, 400)
    fixcross.present()
    exp.clock.wait(fixation_duration)

    audio.preload()
    audio.present()

    screen_center = (exp.screen.window_size[0] // 2, exp.screen.window_size[1] // 2)
    radius = 350  # adjust as needed (depending on screen size)
    image_size = (100, 100)
    positions = get_non_overlapping_positions(8, radius, image_size, screen_center)
    
    can = expyriment.stimuli.Canvas(exp.screen.window_size)
    for image, position in zip(images, positions):
        image.reposition(position)
        image.plot(can)
        
    can.present()

    exp.clock.reset_stopwatch()
    response_given = False

    while not response_given:
        key_rt = exp.keyboard.wait(duration = 5000)
        if key_rt:
            key, rt = key_rt
            response_given = True
            audio.stop()
        else:
            key, rt = None, None

    exp.data.add([row.cue, row.present, row.congruent, row.audio, row.img1, row.img2, row.img3, row.img4, row.img5, row.img6, row.img7, row.img8, key, rt])

thank_you_message = ("Thank you for your participation!\n\n"
                     "You have now finished the experiment and can close it.\n\n"
                    "I hope you enjoyed it :)")

thank_you_box = expyriment.stimuli.TextBox(
    size=(800, 400),  
    text=thank_you_message,
    text_size=25,
    text_colour=expyriment.misc.constants.C_WHITE,
    background_colour=expyriment.misc.constants.C_BLACK,
    position=(0, 0))  

thank_you_box.present()
exp.keyboard.wait()

expyriment.control.end()