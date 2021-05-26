""" 
    Layout practice using kivy
    Begin version 2 using new info learnt from freecodecamp Kivy.
"""
from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Color, Line
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.label import Label
from random import randint
from kivy.utils import get_color_from_hex

BLACK = (0, 0, 0, 1)
RED = (100, 0, 0, 1)
DARK_GREEN = (0, 100, 0, 1)

RED_NUMS = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
BLACK_NUMS = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]

EVEN = 2
ODD = 1


def is_even(num: int):
    return num % 2


def is_odd(num: int):
    return num % 1


def create_cols(begin: int, end: int, step: int = 3):
    """
    Creates the inside values of the roulette wheel.

    :param begin: start number
    :param end: end number
    :param step: steps to increment, 3 on roulette
    :return: order list
    """

    offset = 3  # ensures end of sequence
    sorted_nums = sorted([val for val in range(begin, end+offset, step)])
    return [str(val) for val in sorted_nums]


def create_button(data: int):
    def get_color(num):
        # red = get_color_from_hex(RED)
        red = RED
        # black = get_color_from_hex(BLACK)
        black = BLACK
        # green = get_color_from_hex(DARK_GREEN)
        green = DARK_GREEN
        return red if num in RED_NUMS else black if num in BLACK_NUMS else green

    return Button(text=str(data), background_color=get_color(data))


class NumbersGrid(GridLayout):
    """
    The numbers for the roulette table.
    """
    def __init__(self, **kwargs):
        super(NumbersGrid, self).__init__(**kwargs)
        button_text = (tuple(create_cols(3, 36)) + tuple(create_cols(2, 35)) + tuple(create_cols(1, 34)))
        buttons = [create_button(int(num)) for num in button_text]
        for btn in buttons:
            with btn.canvas.before:
                Color(1, 1, 1, 1)
                Line(width=2, rectangle=(btn.x, btn.y, btn.width+1, btn.height))
            self.add_widget(btn)


class NumberHistory(FloatLayout):
    """
    Will contain all the previous numbers selected.
    NotImplemented
    """

    def __init__(self, **kwargs):
        super(NumberHistory, self).__init__(**kwargs)
        print(self.ids)
        for i in range(0, 15):
            num = str(randint(1, 36))
            clr = RED if int(num) in RED_NUMS else BLACK
            print(num, clr)
            self.ids.numbers_history_container.add_widget(
                Label(text=num,
                      size_hint=('.1dp', '.1dp'),
                      color=clr))


class Zeros(RelativeLayout):
    pass


class Header(FloatLayout):
    pass


class Footer(BoxLayout):
    pass


class TableBox(BoxLayout):
    def __init__(self, **kwargs):
        super(TableBox, self).__init__(**kwargs)
        num_grid = NumbersGrid()
        self.add_widget(num_grid)


class Root(BoxLayout):
    pass


class LayoutApp(App):
    def build(self):
        print('Window size:', Window.width, Window.height)
        root = Root()
        return root


if __name__ == '__main__':
    LayoutApp().run()
