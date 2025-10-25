import os

import pyautogui
import random
import tkinter as tk
import time

class AstronautDuckAnimations:

    STATE_STANDING = 0
    STATE_JUMP = 1
    STATE_WALK_LEFT = 3
    STATE_WALK_RIGHT = 4
    STATE_WALK_UP = 5
    STATE_WALK_DOWN = 6
    STATE_ANGRY = 7

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

    def get_current_animation(self):
        if self.state == self.STATE_STANDING:
            return None

        elif self.state == self.STATE_JUMP:
            return self.animations.get('jump', [])

        elif self.state == self.STATE_WALK_LEFT:
            return self.animations.get('walk_left', [])

        elif self.current == self.STATE_WALK_RIGHT:
            return self.animations.get('walk_right', [])

        elif self.current == self.STATE_WALK_UP:
            if self.facing_direction == 'left':
                return self.animations.get('walk_up_left', [])
            else:
                return self.animations.get('walk_up_right', [])

        elif self.current == self.STATE_WALK_DOWN:
            if self.facing_direction == 'left':
                return self.animations.get('walk_down_left', [])
            else:
                return self.animations.get('walk_down_right', [])

        return []

    def choose_Next_State(self):
        """Pick a new state"""

        start_time = time.time()
        rng = random.randint(1,6)
        match rng:
            case 1:
                self.currentState = self.STATE_ANGRY
            case 2:
                self.current_state = self.STATE_WALK_UP
            case 3:
                self.current_state = self.STATE_WALK_RIGHT
                self.__private_SetDirection()
            case 4:
                self.current_state = self.STATE_WALK_LEFT
                self.__private_SetDirection()
            case 5:
                self.current_state = self.STATE_WALK_DOWN
            case 6:
                self.current_state = self.STATE_STANDING

        if self.current_state == self.STATE_STANDING:
            if (time.time() - start_time) >= 5:
                start_time = time.time()  # reset timer
                for i in range(random.randint(1, 3)):
                    self.current_state = self.STATE_JUMP
                self.current_state = self.STATE_STANDING


    def animate(self):
        # update position on computer TODO: update pixel size later
        self.window.geometry(f'200x200+{self.x}+{self.y}')

        # update next frame
        self.window.after(100, self.animate)

    def run(self):
        self.window.mainloop()

    def __private_SetDirection(self):
        if self.current_state == self.STATE_WALK_LEFT:
            self.facing_direction = 'left'
        elif self.current_state == self.STATE_WALK_RIGHT:
            self.facing_direction = 'right'




