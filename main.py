
from machine import Pin, PWM, reset
led = machine.Pin("LED", machine.Pin.OUT)
led.on()

import chess_project.chess_lib as chess
import os
from utime import sleep
import networking.start_wifi

# BUTTONS:
# 0 - start program
# 1 - reset fen and start program
# 2 - reset fen and start as black (and input whites move first)
# 3 - input position
# 4 - accept position
# 5 - restart position input
# 6 - ignore best move
# 7 - repeat best move

# LED SIGNALS:
# Led on - executing program
# Led off - turned off
# Led flickers - error

# TODO: Should not be able to ignore more then once.

try:
    # Peripherals
    buzzer = PWM(Pin(15))
    pin_nums = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    buttons = [Pin(i, Pin.IN, Pin.PULL_DOWN) for i in pin_nums]

    def playSound(freq, duty=500, duration=0.5):
        buzzer.freq(freq)
        buzzer.duty_u16(duty)
        sleep(duration)
        buzzer.duty_u16(0)
        
    def signal_startgame():
        for i in range(4):
            playSound(150+i*50, duration=0.3)
            
    def signal_inputprompt():
        playSound(100, duration=0.2)
        
    def signal_clickdetected():
        playSound(300, duration=0.1)
        
    def signal_moveignored():
        for i in range(4):
            playSound(30, duration=0.5)
            sleep(0.2)
            
    def signal_switchingsides():
        playSound(500, duration=0.5)

    ignore_rest = False
    def readClickNumber(clicker_index=3, termination_index=4, reset_index=5, ignore_index=6, ignoring_blocked=False, repeat_index=7, best_move=None):
        global ignore_rest
        if not ignore_rest:
            print("Reading click number")
            signal_inputprompt()
        sleep(0.3)
        clicks = 0
        previous_clicker_value = False
        try:
            while True:
                clicker_value = buttons[clicker_index].value()
                if clicker_value != previous_clicker_value:
                    previous_clicker_value = clicker_value
                    if clicker_value:
                        clicks += 1
                        print("click")
                        signal_clickdetected()
                        sleep(0.1)
                if buttons[termination_index].value():
                    print("Returning", clicks, "clicks")
                    return clicks
                if buttons[reset_index].value():
                    clicks = 0
                    print("Resetting clicks")
                    sleep(0.1)
                if buttons[repeat_index].value():
                    if best_move is not None:
                        move_to_sound(best_move)
                if not ignoring_blocked and (buttons[ignore_index].value() or ignore_rest):
                    print("Ignoring best move")
                    ignore_rest = True
                    return 0
        finally:
            buzzer.duty_u16(0)

    letters_to_clicks = {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5, "f": 6, "g": 7, "h": 8}
    def click_num_to_move(click_arr):
        text = ""
        text += clicks_to_letters[click_arr[0]]
        text += str(click_arr[1])
        text += clicks_to_letters[click_arr[2]]
        text += str(click_arr[3])
        return text

    clicks_to_letters = {1: "a", 2: "b", 3: "c", 4: "d", 5: "e", 6: "f", 7: "g", 8: "h"}
    def move_to_sound(move):
        def play_n_sounds(n):
            for i in range(n):
                playSound(400)
                sleep(0.5)
        def stop():
            playSound(50, duration=1)
            sleep(1)
        move_str = str(move)
        play_n_sounds(int(letters_to_clicks[move_str[0]]))
        stop()
        play_n_sounds(int(move_str[1]))
        stop()
        play_n_sounds(int(letters_to_clicks[move_str[2]]))
        stop()
        play_n_sounds(int(move_str[3]))


    # Awaiting user signal to start
    reset_fen = False
    start_as_black = False
    print("WAITING TO START")
    signal_startgame()
    while not buttons[0].value():
        if buttons[1].value():
            reset_fen = True
            print("Reseting fen")
            break
        if buttons[2].value():
            reset_fen = True
            start_as_black = True
            print("Reseting fen and starting as black")
            break
    print("STARTING")

    # Resetting game state
    if "fen.txt" not in os.listdir(".") or reset_fen:
        if not reset_fen:
            print("Not found", os.listdir("."))
        f = open("fen.txt", "w")
        f.write("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        f.close()
        
    # Reading game state
    f = open("fen.txt", "r")
    for line in f:
        fen = line
    f.close()

    print("FEN READ")

    # Dictating best move
    if not start_as_black:
        best_move_data = chess.best_move(fen)
        print("Best move:", best_move_data["move"])
        move_to_sound(best_move_data["move"])

    # Modifying FEN with enemy move
    print("Input enemy move")
    move_clicks = [readClickNumber(best_move=best_move_data["move"]) for _ in range(4)]
    
    # Player can choose to ignore dictated move
    if not ignore_rest:
        move = click_num_to_move(move_clicks)    
        print("Chosen move:", move)
        if not start_as_black:
            new_fen = chess.respond_to_best_move(best_move_data["mid_fen"], best_move_data["controler"], move)
        else:
            new_fen = chess.respond_to_best_move(fen, None, move)

        # Saving game state
        print()
        print("New fen:", new_fen)        
        f = open("fen.txt", "w")
        f.write(new_fen)
        f.close()
            
        # Resetting
        led.off()
        machine.reset()
    else:
        signal_moveignored()
        ignore_rest = False
        
        print("Input desired move")
        move_clicks = [readClickNumber(ignoring_blocked=True) for _ in range(4)]
        move = click_num_to_move(move_clicks)
        fen = chess.respond_to_best_move(fen, None, move)
        signal_switchingsides()
        
        print("Input enemy move")
        move_clicks = [readClickNumber(ignoring_blocked=True) for _ in range(4)]
        move = click_num_to_move(move_clicks)
        fen = chess.respond_to_best_move(fen, None, move)
        
        # Saving state
        f = open("fen.txt", "w")
        f.write(fen)
        f.close()
            
        # Resetting
        led.off()
        machine.reset()

except Exception as e:
    print(e)
    while True:
        led.on()
        sleep(0.2)
        led.off()
        sleep(0.2)
finally:
    led.off()

