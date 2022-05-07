"""
COMP.CS.100 Ohjelmointi 1 / Programming 1
Student Id: 293196
Name:       Haochen Zong
Email:      haochen.zong@tuni.fi

a game called "A Penguin Collecting Coins in front of a Cat"

operating system: macOS version 12.3.1
operating software: PyCharm 2021.3.2 (Community Edition)

project category: advanced GUI

I. the rules of the game:
control a penguin to collect coins falling from the sky as mush as possible
over a period of time. Meanwhile, try to avoid falling stones to avoid reducing
your scores. Each coin adds 1 point and each stone reduces 1 point.

II. the process of the game:
Game starts immediately when you run this program. Use "right arrow" or "left
arrow" to control the main character. When the game overs, you should click the
button "restart" to restart this game or click "quit" to quit this game.

III. increase/decrease the difficulty of this game
self.__total_time = 30
                               ------ each round of this game lasts 30 seconds
self.__canvas.after(500, ) in init_item()
                                               ------ new item falls in 500 ms
random.choice() in class Item() in game_object.py
                                             ------ the speed of falling items
set_speed() in move_left() and move_right()
                ------ positive/negative denotes the penguin moving direction,
                       value denotes the penguin moving speed


IV. how this program works?
This program used widgets of Tkinter: label, button, frame, canvas

in game_scene.py,
class ObjectType: I defined the game objects' types
class MainScene: It initializes or defines the games'
                                background,
                                UI,
                                user input,
                                objects/items (i.e. penguin, coin, stone),
                                start & restart & end,
                                movement of canvas and items
                                objects collision
                                destroy game items

in game_object.py,
class ObjectStatus: I defined the game objects' status
class ObjectDirection: I defined the game objects' direction
class GameObject: It initializes or updates the games' objects'
                                            images,
                                            animation,
                                            ID,
                                            position,
                                            movement speed,
                                            delete
class Penguin: It inherits from GameObject to define the main game character
class Item: It inherits from GameObject to define the falling items: coin,
                                                                     stone
"""

from tkinter import *
from game_object import Penguin, Item
import random


class ObjectType:
    """
    defined data type by myself that consists of the game objects' types
    It works same as "enumeration" in C++
    """
    penguin = 0
    coin = 1
    stone = 2


class MainScene(Frame):
    """
    the main scene of the game
    """
    def __init__(self):
        self.__main_id = None   # the main game character, i.e. a penguin
        self.__canvas = None    # the game scene is shown on this canvas
        self.__bg_image = None  # the background image
        self.__score_label = None   # the label of score
        self.__remaining_time_label = None  # the label of remaining time
        self.__game_process_label = None    # the label of game's state
        self.__quit_button = None           # the button of "quit game"
        self.__restart_button = None        # the button of "restart game"
        self.__afterId_left = None
        self.__afterId_right = None

        self.__object_dict = {}     # the dictionary of game objects

        self.__canvas_width = 0     # the width of the canvas
        self.__canvas_height = 0    # the height of the canvas
        self.__score = 0            # the score of the game
        self.__total_time = 30    # the total time of the game, i.e. 30 seconds
        self.__current_time = self.__total_time   # the current time in seconds

        self.__window = Tk()
        self.__window.title("A Penguin Collecting Coins in front of a Cat")

        # the class "Frame" in Tkinter. "Mainscene" works based on "Frame"
        Frame.__init__(self, self.__window)
        self.pack()

        self.init_bg()   # initialize background
        self.init_UI()   # initialize game's UI
        self.init_object(ObjectType.penguin)    # initialize game objects
        self.init_item()    # initialize games' items, i.e. stone, coin
        self.init_input()   # initialize user's input
        self.start_game()   # game start

        self.__window.mainloop()

    def init_input(self):
        """
        bind user's command with some keys on keyboard
        """
        self.__window.bind('<Left>', self.move_left)
        self.__window.bind('<Right>', self.move_right)
        self.__window.bind('<KeyRelease-Left>', self.move_left_stop)
        self.__window.bind('<KeyRelease-Right>', self.move_right_stop)

    def init_bg(self):
        """
        initialize background
        """
        self.__bg_image = PhotoImage(file="cat.png")

        self.__canvas_width = self.__bg_image.width()
        self.__canvas_height = self.__bg_image.height()

        # the size of "cat.png" is 600*600, the left 50 is used for game UI
        self.__window.geometry("600x650")

        # the canvas shows the game interface without UI
        self.__canvas = Canvas(self.__window,
                               width=self.__bg_image.width(),
                               height=self.__bg_image.height())
        self.__canvas.pack(fill=X, side=TOP)
        self.__canvas.create_image(0, 0, image=self.__bg_image, anchor='nw')

    def init_UI(self):
        """
        initialize game's UI
        """

        # the label of score
        self.__score_label = Label(self.__window, text=f"score: 0")
        self.__score_label.pack(side=LEFT, padx=5, pady=5)

        # the label of remaining time
        self.__remaining_time_label = Label(self.__window,
                                            text=f"remaining time: {self.__current_time} s")
        self.__remaining_time_label.pack(side=LEFT, padx=15, pady=5)

        # the label of game's state
        self.__game_process_label = Label(self.__window, text="game in progress")
        self.__game_process_label.pack(side=LEFT, padx=30, pady=5)

        # the button of "quit game"
        self.__quit_button = Button(self.__window, text="Quit",
                                    command=self.quit)
        self.__quit_button.pack(side=RIGHT, padx=5, pady=5)

        # the button of "restart game"
        self.__restart_button = Button(self.__window, text="restart",
                                       state=DISABLED, command=self.game_restart)
        self.__restart_button.pack(side=RIGHT, padx=15, pady=5)

    def init_item(self):
        """
        initialize game items: coin and stone
        """
        random_number = random.randrange(0, 2)

        # "1" determines half of coins, half of stones
        if random_number < 1:
            self.init_object(ObjectType.coin)
        else:
            self.init_object(ObjectType.stone)

        # new items would be generated in 500 ms
        self.__canvas.after(500, self.init_item)

    def init_object(self, object_type):
        """
        initialize game objects, items based on their "ObjectType"
        :param object_type: ObjectType, referenced by the class "ObjectType"
        """
        if object_type == ObjectType.penguin:
            name = 'main'
            game_object = Penguin(0.0, self.__canvas_height, './penguins',
                                  self.__canvas_width, self.__canvas_height, self)

        if object_type == ObjectType.coin:
            name = 'coin'
            game_object = Item(0.0, 0.0, './coin', self.__canvas_width,
                               self.__canvas_height,  self, 1)

        if object_type == ObjectType.stone:
            name = 'stone'
            game_object = Item(0.0, 0.0, './stone', self.__canvas_width,
                               self.__canvas_height, self, -1)

        image_id = game_object.get_id()

        # the main_id is the penguin's id
        if name == 'main':
            self.__main_id = image_id

        # "object_dict" is a nested dictionary. It includes the dictionary;
        # "object_info"
        object_info = {'name': name, 'object': game_object}
        self.__object_dict[image_id] = object_info

    def start_game(self):
        """
        game starts
        """
        self.__window.after(1000, self.on_time_change)

    def on_time_change(self):
        """
        change current_time, remaining_time based on current_time
        """
        if self.__current_time != 0:
            self.__current_time -= 1
            self.__remaining_time_label['text'] = \
                f"remaining time: {self.__current_time} s"
            self.__window.after(1000, self.on_time_change)
        else:
            self.end_game()

    def end_game(self):
        """
        game ends
        """
        self.__game_process_label['text'] = "game over!"
        self.__restart_button['state'] = NORMAL

    def game_restart(self):
        """
        game restarts
        """
        # reset some parameters before game restarting
        self.__score = 0
        self.__score_label['text'] = f"score: {self.__score}"
        self.__current_time = self.__total_time
        self.__game_process_label['text'] = "game in progress"

        self.start_game()

    def get_canvas(self):
        """
        :return: get __canvas
        """
        return self.__canvas

    def move_left(self, event):
        """
        penguin goes left
        """
        if self.__afterId_left is not None:
            self.after_cancel(self.__afterId_left)
            self.__afterId_left = None
        else:
            game_object = self.__object_dict[self.__main_id]['object']
            game_object.set_speed(-300.0)

    def move_right(self, event):
        """
        penguin goes right
        """
        if self.__afterId_right is not None:
            self.after_cancel(self.__afterId_right)
            self.__afterId_right = None
        else:
            game_object = self.__object_dict[self.__main_id]['object']
            game_object.set_speed(300.0)

    def move_left_stop(self, event):
        """
        enable process_left_release
        """
        self.__afterId_left = self.after_idle(self.process_left_release, event)

    def process_left_release(self, event):
        """
        set the speed of going left
        """
        game_object = self.__object_dict[self.__main_id]['object']
        game_object.set_speed(0.0)
        self.__afterId_left = None

    def move_right_stop(self, event):
        """
        enable process_right_release
        """
        self.__afterId_right = self.after_idle(self.process_right_release, event)

    def process_right_release(self, event):
        """
        set the speed of going right
        """
        game_object = self.__object_dict[self.__main_id]['object']
        game_object.set_speed(0.0)
        self.__afterId_right = None

    def on_collision(self, ids):
        """
        determines the value of __score, if on_score_changed(), delete_item()
            operates
        :param ids: int, the id of image
        """
        for object_id in ids:
            if object_id in self.__object_dict.keys():
                game_item = self.__object_dict[object_id]['object']
                self.__score += game_item.get_score()

                if self.__current_time != 0:
                    self.on_score_changed()

                game_item.delete_item()

    def on_score_changed(self):
        """
        set the score shown on __score_label
        """
        self.__score_label['text'] = f"score: {self.__score}"

    def destroy_object(self, object_id):
        """
        destroy the game object from __object_dict
        :param object_id: int, the id of objects
        """
        if object_id in self.__object_dict.keys():
            self.__canvas.delete(object_id)
            del self.__object_dict[object_id]['object']
            del self.__object_dict[object_id]

    def quit(self):
        """
        quit game
        """
        self.__window.destroy()


def main():
    MainScene()


if __name__ == "__main__":
    main()
