from pynput import mouse, keyboard
from pynput.mouse import Controller as MouseController, Button
from pynput.keyboard import Controller as KeyboardController, Key
import time

events = []
mouse_controller = MouseController()
keyboard_controller = KeyboardController()
start_time = None

stop_recording = False  # Added flag to stop listeners

def on_click(x, y, button, pressed):
    if pressed:
        print(f"Mouse clicked at ({x}, {y}) with {button}")
        events.append(('click', time.time() - start_time, x, y, button))

def on_press(key):
    global stop_recording
    print(f"Key pressed: {key}")
    if key == Key.esc:
        stop_recording = True
        return False
    events.append(('key', time.time() - start_time, key))

def record():
    global start_time
    print("Recording... Press ESC to stop.")
    start_time = time.time()

    with mouse.Listener(on_click=on_click) as mouse_listener, keyboard.Listener(on_press=on_press) as keyboard_listener:
        while not stop_recording:
            time.sleep(0.1)
        mouse_listener.stop()
        keyboard_listener.stop()

def replay():
    print("Replaying...")
    start = time.time()
    for event in events:
        delay = event[1] - (time.time() - start)
        if delay > 0:
            time.sleep(delay)
        if event[0] == 'click':
            _, _, x, y, button = event
            mouse_controller.position = (x, y)
            mouse_controller.click(button)
        elif event[0] == 'key':
            _, _, key = event
            try:
                keyboard_controller.press(key.char)
                keyboard_controller.release(key.char)
            except AttributeError:
                keyboard_controller.press(key)
                keyboard_controller.release(key)

record()
time.sleep(1)
replay()
