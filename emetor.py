from microbit import *
import random
import radio
import music


def generate_random_sequence(length):
    instructions = ["up", "down", "left", "right", "0", "1", "2", "A", "B"]
    sequence = []
    prev_action = ""
    
    for _ in range(length):
        action = random.choice(instructions)
        while prev_action == action:
            action = random.choice(instructions)
        
        sequence.append(action)
        prev_action = action

    return sequence


def display_action(action):
    hash_table = {
        "up": Image.ARROW_S,
        "down": Image.ARROW_N,
        "left": Image.ARROW_W,
        "right": Image.ARROW_E,
    }

    if action not in hash_table.keys():
        display.show(action)
    else:
        display.show(hash_table[action])


def game_over():
    music.play(music.POWER_DOWN, wait=False)
    display.scroll("GAME OVER")
    ending = []
    for k in range(6, 0, -1):
        ending.append(Image.ANGRY.shift_up(k))
    for k in range(0, 6):
        ending.append(Image.ANGRY.shift_down(k))
    
    display.show(ending, delay=100, loop=True)


def win_game():
    music.play(music.RINGTONE, wait=False)
    radio.send("win")
    display.scroll("WIN")
    ending = []
    for k in range(6, 0, -1):
        ending.append(Image.HAPPY.shift_up(k))
    for k in range(0, 6):
        ending.append(Image.HAPPY.shift_down(k))
    
    display.show(ending, delay=100, loop=True)


startup = False
music.play(music.PRELUDE, wait=False, loop=True)

while not startup:
    for clock in Image.ALL_CLOCKS:
        if not pin_logo.is_touched():
            display.show(clock)
            sleep(100)
        else:
            startup = True

radio.send("startup")
music.play(music.POWER_UP)

flash_animation = [Image().invert() * (i/9) for i in range(9, -1, -1)]
display.show(flash_animation, delay=100)
sequence = generate_random_sequence(15)

incoming = radio.receive()
while not incoming == "ready":
    incoming = radio.receive()
    
music.play(music.NYAN, wait=False, loop=True)
for action in sequence:
    display_action(action)
    radio.send(action)
    while True:
        status_receive = radio.receive()
        if status_receive == "next":
            break
        elif status_receive == "loose":
            game_over()

win_game()