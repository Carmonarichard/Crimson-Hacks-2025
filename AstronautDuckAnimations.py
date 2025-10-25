import os

import pyautogui
import random
import tkinter as tk

class AstronautDuckAnimations:

    STATE_STANDING = 0
    STATE_JUMP = 1
    STATE_WALK_LEFT = 3
    STATE_WALK_RIGHT = 4
    STATE_WALK_UP = 5
    STATE_WALK_DOWN = 6

    def __init__(self):
        # window config
        window = tk.Tk()
        window.overrideredirect(True);
        self.window.wm_attributes('-transparentcolor', 'black')
        self.window.wm_attributes('-topmost', True)

        self.pet_width = 100
        self.pet_height = 100

        # save starting position
        # TODO: will update later using window.geometry
        self.x = self.screen_width
        self.y = self.screen_height

        # duck speed
        self.speed = 5

        # tracking direction that duck is facing
        self.facing_direction = 'left'

        # duck state
        self.state = self.STATE_STANDING
        self.state_counter = 0
        self.max_state_counter = random.randint(30, 100)

        # animation variables TODO: will update later
        self.frame_index = 0
        self.animations = {}
        self.standing_image = None

        # label for images
        self.label = tk.Label(self.window, bg='black')
        self.label.pack()

        # load placeholder TODO: will update later
        self.load_animations()

        # start animation
        self.animate

    def load_animations(self):
        # load image and gifs
        try:
            self.standing_image = tk.PhotoImage(file='images/duck_standing.png')
            print('Successfully loaded standing image') #TODO: remove later
        except Exception as e:
            print('Failed to load standing image')

        # loading animations
        animations_config = {
            'jump' : ('images/duck_jump.gif', 3),
            'walk_left' : ('images/duck_walk_left.gif', 5),
            'walk_right' : ('images/duck_walk_right.gif', 5),
        }

        for animation_name, (image_path, frame_count) in animations_config.items():
            if os.path.exists(image_path):
                try:
                    frames = [
                        tk.PhotoImage(file=image_path, format=f'gif -index {i}')
                        for i in range(frame_count)
                    ]
                    self.animations[animation_name] = frames
                    print(f'Successfully loaded {animation_name} animation') #TODO: remove later
                except Exception as e:
                    print(f'Failed to load {animation_name} animation')
                    self.animations[animation_name] = []
            else:
                print(f'Image path {image_path} does not exist')
                self.animations[animation_name] = []



    def animate(self):
        # update position on computer TODO: update pixel size later
        self.window.geometry(f'200x200+{self.x}+{self.y}')

        # update next frame
        self.window.after(100, self.animate)

    def run(self):
        self.window.mainloop()







