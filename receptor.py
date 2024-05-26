from microbit import *
import radio
import music


def game_over():
    music.stop()
    radio.send("loose")
    display.show(Image.SAD)
    sleep(500)
    music.play(music.POWER_DOWN, wait=False, pin=None)


def win_game():
    music.stop()
    display.show(Image.HEART)
    sleep(500)
    music.play(music.RINGTONE, wait=False, pin=None)


incoming = radio.receive()
while not incoming == "startup":
    incoming = radio.receive()
    display.show(Image.ASLEEP)

music.play(music.POWER_UP, pin=None)
flash_animation = [Image().invert() * (i/9) for i in range(9, -1, -1)]
display.show(flash_animation, delay=100)
radio.send("ready")

timer_duration = 3 * 1000
running = True
music.play(music.NYAN, wait=False, loop=True, pin=None)
while running:
    display.clear()
    incoming = radio.receive()
    
    if incoming == "win":
        win_game()
    elif incoming != None:
        action_done = False
        timer_start = running_time()
        while not action_done:
            spent_time = running_time() - timer_start
            left_time = timer_duration - spent_time

            display.show(int(left_time / 1000) + 1, wait=False)
            if left_time <= 0:
                game_over()
                running = False
                break
            
            if accelerometer.is_gesture("up") and incoming == "up":
                action_done = True
            elif accelerometer.is_gesture("down") and incoming == "down":
                action_done = True
            elif accelerometer.is_gesture("left") and incoming == "left":
                action_done = True
            elif accelerometer.is_gesture("right") and incoming == "right":
                action_done = True
            elif button_a.is_pressed() and incoming == "A":
                action_done = True
            elif button_b.is_pressed() and incoming == "B":
                action_done = True
            elif pin0.is_touched() and incoming == "0":
                action_done = True
            elif pin1.is_touched() and incoming == "1":
                action_done = True
            elif pin2.is_touched() and incoming == "2":
                action_done = True

        if action_done:
            display.show(Image.HAPPY)

        sleep(500)
        radio.send("next")