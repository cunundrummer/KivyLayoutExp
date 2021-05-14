""" 
    Layout practice using kivy 
"""

from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.core.window import Window


BLACK = (0, 0, 0, 1)
RED = (128, 0, 0, 1)
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


class Controller(Widget):
    label_wid = ObjectProperty()
    info = StringProperty()
    window_height = NumericProperty()

    def do_action(self):
        self.label_wid.text = 'Button pressed'
        self.info = 'Bye'

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


class NumbersLayout(Widget):
    num_layout_id = ObjectProperty()

    def __init__(self, **kwargs):
        super(NumbersLayout, self).__init__(**kwargs)

        # number order according to roulette tables
        button_text = (tuple(create_cols(3, 36)) + tuple(create_cols(2, 35)) + tuple(create_cols(1, 34)))
        buttons = [create_button(int(num)) for num in button_text]
        table = self.ids.num_table_layout
        for btn in buttons:
            btn.size_hint = (None, None)
            btn.height = 125
            btn.width = 92
            table.add_widget(btn)


class ZeroOnly(Widget):
    def __init__(self, **kwargs):
        super(ZeroOnly, self).__init__(**kwargs)
        print('kwargs', kwargs)
        self.pos = kwargs.get('pos')
        self.ids.zero_btn.pos = self.pos


class ThirdsLayout(Widget):
    pass


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
        print(self.x, self.y-125 )
        # self.add_widget(DoubleZero(pos=(self.x, self.y-125)))
        self.add_widget(DoubleZero(pos=(-15, 780+54)))

class LayoutApp(App):
    def build(self):
        root = Controller(info='Hello Fool!')
        print('Window size:', Window.width, Window.height)
        # print('Root size:', root.width, root.height)
        root.add_widget(NumbersLayout())
        root.add_widget(ThirdsLayout())
        root.add_widget(OutsideLayout())
        root.add_widget(Zeros(is_euro=False))

        return root


if __name__ == '__main__':
    LayoutApp().run()
