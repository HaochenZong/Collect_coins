# Collect_coins
a simple game of collecting coins implemented by Python Tkinter.

## environment
- operating system: macOS version 12.3.1
- operating software: PyCharm 2021.3.2 (Community Edition)

## rules of the game:
control a penguin to collect coins falling from the sky as mush as possible
over a period of time. Meanwhile, try to avoid falling stones to avoid reducing
your scores. Each coin adds 1 point and each stone reduces 1 point.

## whole process of the game:
1. Game starts immediately when you run this program. 
2. Use "right arrow" or "left arrow" to control the main character. 
3. When the game overs, you should click the button "restart" to restart this game or click "quit" to quit this game.

## increase/decrease the difficulty of this game
- `self.__total_time = 30` each round of this game lasts 30 seconds                                
- `self.__canvas.after(500, )` in `init_item()` new item falls in 500 ms 
- `random.choice()` in `class Item()` in `game_object.py` the speed of falling items                                                                               
- `set_speed()` in `move_left()` and `move_right()` positive/negative denotes the penguin moving direction, value denotes the penguin moving speed         
                                                                 
## user interface
![The user interface](https://github.com/HaochenZong/Collect_coins/blob/main/user_interface.png) 

## origin of images
- the images of items and penguin were extracted from MapleStory by Nexon
- the image of the background was obtained from weibo:"Pinkpig阿璐儿-异国短毛猫"
