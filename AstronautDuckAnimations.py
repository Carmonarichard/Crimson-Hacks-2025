import os
import platform
import random
import tkinter as tk
import time
from _ast import Return

import pygetwindow as gw


class AstronautDuckAnimations:
    STATE_STANDING = 0
    STATE_JUMP = 1
    STATE_WALK_LEFT = 3
    STATE_WALK_RIGHT = 4
    STATE_WALK_UP = 5
    STATE_WALK_DOWN = 6
    STATE_ANGRY = 7

    def __init__(self):
        print("🦆 Initializing duck...")

        # window config
        try:
            self.window = tk.Tk()
            print("✓ Window created")
        except Exception as e:
            print(f"✗ Failed to create window: {e}")
            raise

        self.window.overrideredirect(True)

        system = platform.system()
        print(f"✓ Platform: {system}")

        if system == 'Darwin':  # Mac
            self.window.wm_attributes('-transparent', True)
            print("✓ Using Mac transparency")
        elif system == 'Windows':
            self.window.wm_attributes('-transparentcolor', 'black')
            print("✓ Using Windows transparency")

        self.window.wm_attributes('-topmost', True)

        # Get screen size
        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()
        print(f"✓ Screen size: {self.screen_width}x{self.screen_height}")

        self.pet_width = 100
        self.pet_height = 100

        # Starting position (center of screen)
        self.x = self.screen_width // 2
        self.y = self.screen_height // 2
        print(f"✓ Starting position: ({self.x}, {self.y})")

        # duck speed
        self.speed = 5

        # tracking direction that duck is facing
        self.facing_direction = 'right'

        # duck state
        self.current_state = self.STATE_STANDING
        self.state_counter = 0
        self.max_state_counter = random.randint(30, 100)

        # animation variables
        self.frame_index = 0
        self.animations = {}
        self.standing_right_image = None
        self.standing_left_image = None

        # Angry state cooldown
        self.last_angry_time = 0
        self.angry_cooldown = 30
        self.has_closed_window = False

        # timer for jumping
        self.last_jump_time = time.time()

        # label for images
        self.label = tk.Label(self.window, bg='black')
        self.label.pack()
        print("✓ Label created")

        # load animations
        self.load_animations()

        # Position window
        self.window.geometry(f'{self.pet_width}x{self.pet_height}+{self.x}+{self.y}')

        print("✓ Starting animation loop...")
        # start animation
        self.animate()

    def load_animations(self):
        print("\n📁 Loading images...")
        print(f"Current directory: {os.getcwd()}")

        # Check if images folder exists
        if not os.path.exists('images'):
            print("⚠️  WARNING: 'images' folder not found!")
            print("   Please create an 'images' folder with your duck images")
            return

        for img_name, img_path in [
            ('standing_right', 'images/StandingRight.gif'),  # Changed from .png
            ('standing_left', 'images/StandingLeft.gif')  # Changed from .png
        ]:
            try:
                if img_name == 'standing_right':
                    self.standing_right_image = tk.PhotoImage(file=img_path)
                else:
                    self.standing_left_image = tk.PhotoImage(file=img_path)
                print(f'  ✓ Loaded {img_name}')
            except Exception as e:
                print(f'  ✗ Failed to load {img_name}: {e}')

        # loading animations
        animations_config = {
            'jump_right': ('images/JumpingRight.gif', 3),
            'walk_left': ('images/WalkingLeft.gif', 5),
            'walk_right': ('images/WalkingRight.gif', 5),
            'jump_left': ('images/JumpingLeft.gif', 3),
            'closing_right': ('images/ClosingRight.gif', 3),
        }

        for animation_name, (image_path, frame_count) in animations_config.items():
            if os.path.exists(image_path):
                try:
                    frames = [
                        tk.PhotoImage(file=image_path, format=f'gif -index {i}')
                        for i in range(frame_count)
                    ]
                    self.animations[animation_name] = frames
                    print(f'  ✓ Loaded {animation_name}: {len(frames)} frames')
                except Exception as e:
                    print(f'  ✗ Failed to load {animation_name}: {e}')
                    self.animations[animation_name] = []
            else:
                print(f'  ✗ Not found: {image_path}')
                self.animations[animation_name] = []

        print("✓ Image loading complete\n")

    def get_current_animation(self):
        if self.current_state == self.STATE_STANDING:
            return None

        elif self.current_state == self.STATE_JUMP:
            if self.facing_direction == 'left':
                return self.animations.get('jump_left', [])
            else:
                return self.animations.get('jump_right', [])

        elif self.current_state == self.STATE_WALK_LEFT:
            return self.animations.get('walk_left', [])

        elif self.current_state == self.STATE_WALK_RIGHT:
            return self.animations.get('walk_right', [])

        elif self.current_state == self.STATE_WALK_UP:
            if self.facing_direction == 'left':
                return self.animations.get('walk_left', [])
            else:
                return self.animations.get('walk_right', [])

        elif self.current_state == self.STATE_WALK_DOWN:
            if self.facing_direction == 'left':
                return self.animations.get('walk_left', [])
            else:
                return self.animations.get('walk_right', [])
        elif self.current_state == self.STATE_ANGRY:
            return self.animations.get('closing_right', [])

        return []

    def get_random_window_to_close(self):
        system = platform.system()
        try:
            all_windows = gw.getAllWindows()

            safe_windows = [
                w for w in all_windows
                if w.title
                   and w.title != "Astronaut Duck"
                   and w.title != ""
                   and "Program Manager" not in w.title
                   and "Task Switching" not in w.title
                   and "Windows Input Experience" not in w.title
                   and "Settings" not in w.title
                   and "CrimsonHacks" not in w.title
            ]
            if safe_windows:
                target = random.choice(safe_windows)
                return target
        except Exception as e:
            print(f"Error getting windows{e}")
        return None

    def close_random_window(self):
        system = platform.system()
        try:
            target = self.get_random_window_to_close()
            if target:
                print(f">:| Angry duck closes: {target.title}")
                target.close()
                return True
        except Exception as e:
            print("Error closing window")
        return False

    def choose_next_state(self):
        """Pick a new state"""
        current_time = time.time()
        can_be_angry = (current_time - self.last_angry_time) > self.angry_cooldown

        if can_be_angry and random.random() > 0.15:
            self.current_state = self.STATE_ANGRY
            self.last_angry_time = current_time
            self.has_closed_window = False
            print("Duck is getting angry")

        else:

            rng = random.randint(1, 6)
            if rng == 1:
                self.current_state = self.STATE_STANDING
            elif rng == 2:
                self.current_state = self.STATE_WALK_UP
            elif rng == 3:
                self.current_state = self.STATE_WALK_RIGHT
                self.__private_set_direction()
            elif rng == 4:
                self.current_state = self.STATE_WALK_LEFT
                self.__private_set_direction()
            elif rng == 5:
                self.current_state = self.STATE_WALK_DOWN
            elif rng == 6:
                self.current_state = self.STATE_JUMP
            self.max_state_counter = random.randint(30, 100)


        # Reset counters
        self.state_counter = 0
        self.frame_index = 0

        state_names = {
            0: "STANDING", 1: "JUMP", 3: "WALK_LEFT",
            4: "WALK_RIGHT", 5: "WALK_UP", 6: "WALK_DOWN", 7: "ANGRY"
        }
        print(f"→ {state_names.get(self.current_state, 'UNKNOWN')}")

    def update_position(self):
        if self.current_state == self.STATE_WALK_LEFT:
            self.x -= self.speed
        elif self.current_state == self.STATE_WALK_RIGHT:
            self.x += self.speed
        elif self.current_state == self.STATE_WALK_UP:
            self.y -= self.speed
        elif self.current_state == self.STATE_WALK_DOWN:
            self.y += self.speed

    def check_screen_boundaries(self):
        if self.x < 0:
            self.x = 0
        elif self.x > self.screen_width - self.pet_width:
            self.x = self.screen_width - self.pet_width

        if self.y < 0:
            self.y = 0
        elif self.y > self.screen_height - self.pet_height:
            self.y = self.screen_height - self.pet_height

    def update_animation_frame(self):
        try:
            if self.current_state == self.STATE_STANDING:
                if self.facing_direction == 'left' and self.standing_left_image:
                    self.label.configure(image=self.standing_left_image)
                elif self.standing_right_image:
                    self.label.configure(image=self.standing_right_image)
                return

            current_animation = self.get_current_animation()

            if len(current_animation) > 0:
                frame = current_animation[self.frame_index]
                self.label.configure(image=frame)
                self.frame_index = (self.frame_index + 1) % len(current_animation)
        except Exception as e:
            print(f"Error updating frame: {e}")

    def animate(self):
        try:
            # Update frame
            self.update_animation_frame()

            # Update position
            self.update_position()

            # Check boundaries
            self.check_screen_boundaries()

            # Move the window
            self.window.geometry(f'{self.pet_width}x{self.pet_height}+{self.x}+{self.y}')

            if self.current_state == self.STATE_ANGRY:
                if self.state_counter == 10 and not self.has_closed_window:
                    self.close_random_window()
                    self.has_closed_window = True

            # State management
            self.state_counter += 1
            if self.state_counter >= self.max_state_counter:
                self.choose_next_state()

            # Continue loop
            self.window.after(100, self.animate)
        except Exception as e:
            print(f"Error in animate: {e}")
            import traceback
            traceback.print_exc()

    def run(self):
        print("🚀 Starting mainloop...\n")
        self.window.mainloop()

    def __private_set_direction(self):
        if self.current_state == self.STATE_WALK_LEFT:
            self.facing_direction = 'left'
        elif self.current_state == self.STATE_WALK_RIGHT:
            self.facing_direction = 'right'


# Run the duck!
if __name__ == "__main__":
    try:
        duck = AstronautDuckAnimations()
        duck.run()
    except Exception as e:
        print(f"\n❌ FATAL ERROR: {e}")
        import traceback

        traceback.print_exc()
        input("\nPress Enter to exit...")
