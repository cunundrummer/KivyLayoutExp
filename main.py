""" 
    Layout practice using kivy
    Begin version 2 using new info learnt from freecodecamp Kivy.
"""
from typing import List, Dict, Tuple, Union

from kivy.app import App
from kivy.properties import NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

BLACK = (0, 0, 0, 1)
RED = (128, 0, 0, 1)
DARK_GREEN = (0, 100, 0, 1)
BLACK_hex = '#000000'
RED_hex = '#FF0000'
DARK_GREEN_hex = '#228B22'  # forest green https://flaviocopes.com/rgb-color-codes/

RED_NUMS = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
BLACK_NUMS = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]

EVEN = 2
ODD = 1


def is_even(num: int) -> int:
    return num % 2


def is_odd(num: int) -> int:
    return num % 1


def create_cols(begin: int, end: int, step: int = 3) -> list:
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


def create_roulette_num_button_colors(data: int) -> Button:
    """
    Specifically creates the buttons of the roulette table for the number 1-36.  Assigns the appropriate colors.
    :param data: int between 1-36
    :return: kivy Button object
    """

    def get_color(num: int, use_hex: bool = True) -> Dict[str, Union[List[float], Tuple[int, int, int, int]]]:
        background_normal = dict()  # background-normal fixes quirky dark tint of buttons when using hex code.
        if use_hex:
            red = get_color_from_hex(RED_hex)
            black = get_color_from_hex(BLACK_hex)
            green = get_color_from_hex(DARK_GREEN_hex)
            background_normal.update({'background_normal': ''})
        else:
            red = RED
            black = BLACK
            green = DARK_GREEN
            background_normal = None

        color_dict = {'color': red if num in RED_NUMS else black if num in BLACK_NUMS else green}
        if background_normal is not None:
            color_dict.update(background_normal)
        return color_dict

    color = get_color(data, False)
    if 'background_normal' in color:
        return Button(text=str(data),
                      background_color=color.get('color'),
                      background_normal=str(color.get('background-normal')))
    return Button(text=str(data), background_color=color.get('color'))


def create_roulette_num_buttons() -> List[Button]:
    """
    Creates a list of buttons to be used in roulette grid/stack container).

    :return: A list of red and black buttons ranged from 1 to 36.  Number order is according to roulette tables -
             top row (3-36); middle row (2 -35); bottom row (1-34). .
    """
    button_text = (tuple(create_cols(3, 36)) + tuple(create_cols(2, 35)) + tuple(create_cols(1, 34)))
    return [create_roulette_num_button_colors(int(num)) for num in button_text]


class MasterLayout(BoxLayout):
    window_height = NumericProperty()

    # def do_action(self):
    #     self.label_wid.text = 'Button pressed'

    def get_win_height(self):
        self.window_height = Window.height
        return self.window_height

    def get_num_children(self):
        num_btn = len(self.ids.left_layout.children)
        return num_btn

    def get_right_coords(self):
        pos = self.ids.left_layout.pos
        child_width = self.ids.left_layout.children[0].size
        print('pos:', pos, 'btn width', child_width, 'right_coord_x:', pos[0]+child_width[0])


class NumbersLayout(GridLayout):
    def __init__(self, **kwargs):
        super(NumbersLayout, self).__init__(**kwargs)
        self.rows = 3
        self.cols = 12
        buttons = create_roulette_num_buttons()
        for btn in buttons:
            self.ids.num_table_layout.add_widget(btn)


class ZeroOnly(Widget):
    def __init__(self, **kwargs):
        super(ZeroOnly, self).__init__(**kwargs)
        print('kwargs', kwargs)
        self.pos = kwargs.get('pos')
        self.ids.zero_btn.pos = self.pos


class ThirdsLayout(GridLayout):  # also known as dozens
    def __init__(self, **kwargs):
        super(ThirdsLayout, self).__init__(**kwargs)
        self.cols = 3
        self.rows = 1
        texts = ['1st 12', '2nd 12', '3rd 12']
        texts.reverse()
        for i, btn in enumerate(self.children[0].children):
            btn.text = texts[i]


class OutsideLayout(Widget):
    pass


class DoubleZero(Widget):
    def __init__(self, **kwargs):
        super(DoubleZero, self).__init__(**kwargs)
        print('kwargs', kwargs)
        self.pos = kwargs.get('pos')
        print('dbl pos', self.pos)
        self.ids.dbl_zero_btn.pos = self.pos


class Zeros(Widget):
    def __init__(self, is_euro: bool = False):
        super(Zeros, self).__init__()
        if is_euro:
            print('showing EURO --> single zero (only_zero)...')
        padding = 20

        if is_euro:
            self.pos = (padding, 780 + 20 + (125 * 3) / 3)
            self.add_widget(ZeroOnly(pos=self.pos))
            return
        self.pos = (padding, 780 + 20 + (125 * 3) / 2)
        # self.add_widget(ZeroOnly(pos=self.pos))
        self.add_widget(ZeroOnly(pos=(-15, 1020)))
        print(self.x, self.y-125)
        # self.add_widget(DoubleZero(pos=(self.x, self.y-125)))
        self.add_widget(DoubleZero(pos=(-15, 780+54)))


class LayoutApp(App):
    def build(self):
        print('Window size:', Window.width, Window.height)
        root = MasterLayout()
        print(root.ids.main_content.ids)
        root.ids.main_content.ids.numbers.add_widget(NumbersLayout())
        root.ids.main_content.ids.thirds.add_widget(ThirdsLayout())
        # root.add_widget(Zeros(is_euro=False))

        return root


if __name__ == '__main__':
    LayoutApp().run()
