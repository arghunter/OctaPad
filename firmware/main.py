# You import all the IOs of your board
import board

from kmk.extensions.display import Display, TextEntry, ImageEntry

# These are imports from the kmk library
from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners.keypad import KeysScanner
from kmk.keys import KC
from kmk.modules.macros import Press, Release, Tap, Macros
from kmk.modules.encoder import EncoderHandler
from kmk.extensions.LED import LED
from kmk.extensions.display import Display, TextEntry, ImageEntry

# This is the main instance of your keyboard
keyboard = KMKKeyboard()
i2c_bus = busio.I2C(board.GP07, board.GP06)
driver = SSD1306(
    # Mandatory:
    i2c=i2c_bus,

)
led = LED(led_pin=[board.GP0])

# Add the macro extension
macros = Macros()
encoder_handler = EncoderHandler()
keyboard.modules.append(macros)
keyboard.modules.append(encoder_handler)
keyboard.extensions.append(led)
# Define your pins here!
PINS = [board.GP1, board.GP2, board.GP4, board.GP3]

# Tell kmk we are not using a key matrix
keyboard.matrix = KeysScanner(
    pins=PINS,
    value_when_pressed=False,
)

# Here you define the buttons corresponding to the pins
# Look here for keycodes: https://github.com/KMKfw/kmk_firmware/blob/main/docs/en/keycodes.md
# And here for macros: https://github.com/KMKfw/kmk_firmware/blob/main/docs/en/macros.md
keyboard.keymap = [
    [KC.GRAVE, KC.LGUI, KC.Macro(Press(KC.LGUI),Press(KC.LSHIFT), Tap(KC.S), Release(KC.LCMD),Release(KC.LSHIFT)),KC.PAUSE]
]

encoder_handler.pins = (
    # regular direction encoder and a button
    (board.GP26, board.GP127, None,), # encoder #1 
    # reversed direction encoder with no button handling and divisor of 2
    (board.GP28, board.GP29, None,), # encoder #2
    )


# For all display types
display = Display(
    # Mandatory:
    display=driver,
    # Optional:
    width=128, # screen size
    height=32, # screen size
    flip = False, # flips your display content
    flip_left = False, # flips your display content on left side split
    flip_right = False, # flips your display content on right side split
    brightness=0.8, # initial screen brightness level
    brightness_step=0.1, # used for brightness increase/decrease keycodes
    dim_time=20, # time in seconds to reduce screen brightness
    dim_target=0.1, # set level for brightness decrease
    off_time=60, # time in seconds to turn off screen
    powersave_dim_time=10, # time in seconds to reduce screen brightness
    powersave_dim_target=0.1, # set level for brightness decrease
    powersave_off_time=30, # time in seconds to turn off screen
)

display.entries = [
    TextEntry(text="Octopad", x=0, y=0),
    TextEntry(text="Why?", x=0, y=12),
    TextEntry(text="Because", x=0, y=24),
]
keyboard.extensions.append(display)
# Start kmk!
if __name__ == '__main__':
    keyboard.go()
