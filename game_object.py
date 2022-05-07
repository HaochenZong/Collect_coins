"""
COMP.CS.100 Ohjelmointi 1 / Programming 1
Student Id: 293196
Name:       Haochen Zong
Email:      haochen.zong@tuni.fi

a game called "A Penguin Collecting Coins in front of a Cat"

This file includes the class of ObjectStatus and the inherited classes.

P.S. the main description is shown in "game_scene.py"
"""

import os
import random
from PIL import Image, ImageTk


class ObjectStatus:
    """
    defined data type by myself that consists of the game objects' status
    It works same as "enumeration" in C++
    """
    stand = 0
    move = 1


class ObjectDirection:
    """
    defined data type by myself that consists of the game objects' direction
    It works same as "enumeration" in C++
    """
    right = 0
    left = 1


class GameObject:
    """
    the game object
    """
    def __init__(self, x, y, image_dir, max_width, max_height, owner):
        self._image_list = []   # the list of images
        self._x = x             # horizontal coordinate
        self._y = y             # vertical coordinate
        self._count = 0         # the count of the list of images
        self._speed = {'x': 0.0, 'y': 0.0}  # the horizontal and vertical speed
        self._width = None      # the width of an image
        self._height = None     # the height of an image
        self._max_width = max_width     # maximum width
        self._max_height = max_height   # maximum height
        self._owner = owner             # class MainScene
        self._alive = True              # if this object alive or not
        self.init_image_list(image_dir, self._image_list)

        # the image's id
        self._id = owner.get_canvas().create_image(
            x, y, image=self.get_current_image(), anchor='sw')

    def get_id(self):
        """
        get object's ID
        """
        return self._id

    def init_image_list(self, image_dir, image_list, flip=True):
        """
        initialize the image list

        :param image_dir: str, the direction of image files in your computer
        :param image_list: list, the image list
        :param flip: bool, "True" means filpping the image. "False" means don't
            flipping
        """
        try:
            images = sorted(os.listdir(image_dir))
            for pi in images:

                # generate the direction of images in computer
                pi_path = image_dir + '/' + pi

                # flip the image (go left) or not (go right)
                if flip:
                    image = ImageTk.PhotoImage(
                        Image.open(pi_path).transpose(Image.FLIP_LEFT_RIGHT))
                else:
                    image = ImageTk.PhotoImage(Image.open(pi_path))
                image_list.append(image)
        except FileNotFoundError as err:
            print(f'{self.__class__}: {err}')
            self._alive = False
            del self

    def get_current_image(self):
        """
        get the current image from the image list
        :return: list, an element in the image list
        """
        try:
            return self._image_list[self._count]
        except IndexError as err:
            print(f'{self.__class__}: {err}')

    def get_count(self):
        """
        get _count
        """
        return self._count

    def update_count(self):
        """
        update _count
        """
        self._count += 1
        try: self._count = self._count % len(self._image_list)
        except ZeroDivisionError as err:
            print(f'{self.__class__}: {err}')

    def get_x(self):
        """
        :return: the horizontal coordinate
        """
        return self._x

    def get_y(self):
        """
        :return: the vertical coordinate
        """
        return self._y

    def update_animation(self):
        """
        update the animation of game object
        """
        if self._alive and len(self._image_list) > 1:
            self._owner.get_canvas().itemconfig(self._id,
                                                image=self.get_current_image())
            self.update_count()
        self._owner.get_canvas().after(200, self.update_animation)

    def update_position(self, delta_time):
        """
        update the position of game object
        :return: float, new positions
        """
        self._x += self._speed['x'] * delta_time
        self._y += self._speed['y'] * delta_time

        # clamps a value between an upper and lower bound
        self._x = max(0.0, min(self._x, self._max_width - self._width))
        self._y = max(self._height, min(self._y, self._max_height))
        return 0.0, 0.0

    def set_speed(self, speed):
        """
        set the horizontal and vertical speed
        """
        try:
            self._speed['x'] = speed['x']
            self._speed['y'] = speed['y']
        except TypeError:
            print('keys: x or y not in speed variable')

    def delete_item(self):
        """
        delete object
        """
        if self._alive:
            self._owner.destroy_object(self.get_id())
            self._alive = False


class Penguin(GameObject):
    """
    class of the main character in the game by inheriting GameObject
    """
    def __init__(self, x, y, image_dir, max_width, max_height, owner):

        # different lists of penguin's movement animation
        self.__move_image_list_right = []
        self.__stand_image_list_right = []
        self.__move_image_list_left = []
        self.__stand_image_list_left = []

        super().__init__(x, y, image_dir, max_width, max_height, owner)

        # penguin's width and height
        self._width = 107
        self._height = 65

        # penguin's status, direction and animation dictionary
        self.__status = ObjectStatus.stand
        self.__direction = ObjectDirection.right
        self.__animation = {ObjectStatus.stand:
            {
                ObjectDirection.right:
                    self.__stand_image_list_right,
                ObjectDirection.left:
                    self.__stand_image_list_left},
            ObjectStatus.move:
                {
                    ObjectDirection.right:
                        self.__move_image_list_right,
                    ObjectDirection.left:
                        self.__move_image_list_left}
        }

        self.update_animation()
        self.update_position(0.01)

    def init_image_list(self, image_dir, image_list, flip=False):
        """
        initialize the image list

        :param image_dir: str, the direction of image files in your computer
        :param image_list: list, the image list
        :param flip: bool, "True" means filpping the image. "False" means don't
            flipping
        """
        super().init_image_list(image_dir + '/stand',
                                self.__stand_image_list_right)
        super().init_image_list(image_dir + '/move',
                                self.__move_image_list_right)
        super().init_image_list(image_dir + '/stand',
                                self.__stand_image_list_left, False)
        super().init_image_list(image_dir + '/move',
                                self.__move_image_list_left, False)
        self._image_list = self.__stand_image_list_right

    def update_position(self, delta_time):
        """
        update the object's position
        :param delta_time: float, object moves within the time
        """
        if self._alive:
            x = self._x + self._speed['x'] * delta_time

            x = max(0.0, min(x, self._max_width - self._width))

            delta_x = x - self._x
            self._x = x
            self._owner.get_canvas().move(self._id, delta_x, 0.0)
            self.check_collision()
        self._owner.get_canvas().after(10, self.update_position, delta_time)

    def check_collision(self):
        """
        check if the collision happens
        """
        ids = self._owner.get_canvas().find_overlapping(self._x, self._y,
                                                        self._x +self._width,
                                                        self._y+self._height)
        if len(ids):
            self._owner.on_collision(ids)

    def set_speed(self, speed):
        """
        set the speed of the object
        :param speed: int, the speed of the object
        """
        if self._speed['x'] != speed:
            self.on_speed_change(speed)
        self._speed['x'] = speed

    def on_speed_change(self, speed):
        """
        change the direction of the object
        :param speed: int, the speed of the object
        """
        if speed == 0.0:
            self.__status = ObjectStatus.stand
        elif speed > 0:
            self.__status = ObjectStatus.move
            self.__direction = ObjectDirection.right
        else:
            self.__status = ObjectStatus.move
            self.__direction = ObjectDirection.left

        self.on_animation_change()

    def on_animation_change(self):
        """
        change the animation of the object
        """
        self._image_list = self.__animation[self.__status][self.__direction]
        self._count = 0


class Item(GameObject):
    """
    class of the items (e.g. coin, stone) in the game by inheriting GameObject
    """
    def __init__(self, x, y, image_dir, max_width, max_height, owner, score):
        # the range of the starting points of coins/stones
        x = random.randrange(max_width - 26)

        super().__init__(x, y, image_dir, max_width, max_height, owner)

        # the size of coins/stones
        self._width = 26
        self._height = 26

        # the speed of coins/stones is 200, 300, 400 or 500
        self._speed = {'x': 0.0, 'y': random.choice([200, 300, 400, 500])}

        # update coins/stones
        self.update_animation()
        self.update_position(0.01)

        self.__score = score

    def init_image_list(self, image_dir, image_list, flip=False):
        """
        initialize the image list

        :param image_dir: str, the direction of image files in your computer
        :param image_list: list, the image list
        :param flip: bool, "True" means filpping the image. "False" means don't
            flipping
        """
        super().init_image_list(image_dir, self._image_list, False)

    def update_position(self, delta_time):
        """
        update the object's position
        :param delta_time: float, object moves within the time
        """
        if self._alive:
            # only vertical coordinates of coins/stone change
            y = self._y + self._speed['y'] * delta_time

            # distance between new y and old y
            delta_y = y - self._y

            self._y = y

            # canvas move based on delta_y
            self._owner.get_canvas().move(self._id, 0.0, delta_y)

            self.check_position()

        # update position
        self._owner.get_canvas().after(10, self.update_position, delta_time)

    def check_position(self):
        """
        delete items if items move outside the canvas
        """
        if self._y > self._max_height + self._height:
            self.delete_item()

    def get_score(self):
        """
        :return: get __score
        """
        return self.__score

