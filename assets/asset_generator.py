from manim import *
from manimusic import *

class staff_generator(Scene):
    def construct(self):
        staff = Staff(clefs="c", width=3).scale(0.5)
        self.add(staff)

class first_note_generator(Scene):
    def construct(self):
        staff = Staff(clefs="g", width=3).scale(0.5)
        note = Note(staff, "sB#", 0.5).set_color(BLUE)
        self.add(note)

class second_note_generator(Scene):
    def construct(self):
        staff = Staff(clefs="g", width=3).scale(0.5)
        note = Note(staff, "sB#", 0.8).set_color(YELLOW)
        self.add(note)

class quality_buttons(Scene):
    def make_button(self, label, color, padding=0.4):
        text = Text(label, font_size=24)

        rect = Rectangle(
            width=text.width + padding,
            height=0.5,
            color=color,
        ).set_fill(color, opacity=0.5)

        text.move_to(rect.get_center())
        rect.add(text)
        return rect

    def construct(self):
        # top row
        major = self.make_button("Major", BLUE)
        minor = self.make_button("Minor", GREEN)
        perfect = self.make_button("Perfect", RED)
        top_row = VGroup(major, minor, perfect).arrange(RIGHT, buff=0.19)

        # bottom row
        diminished = self.make_button("Diminished", YELLOW)
        augmented = self.make_button("Augmented", PURPLE)
        bottom_row = VGroup(diminished, augmented).arrange(RIGHT, buff=0.2)

        # stack
        buttons = VGroup(top_row, bottom_row).arrange(DOWN, buff=0.2)
        buttons.to_edge(DOWN).scale(0.75)

        self.add(buttons)

class number_buttons(Scene):
    def make_button(self, label, color, padding=0.4):
        text = Text(label, font_size=24)

        rect = Rectangle(
            width=0.5,
            height=0.5,
            color=color,
        ).set_fill(color, opacity=0.5)

        text.move_to(rect.get_center())
        rect.add(text)
        return rect

    def construct(self):
        # top row
        buttons_top = VGroup(
            self.make_button("1", BLUE),
            self.make_button("2", GREEN),
            self.make_button("3", RED),
            self.make_button("4", YELLOW),
        ).arrange(RIGHT, buff=0.19)

        # bottom row
        buttons_bottom = VGroup(
            self.make_button("5", YELLOW),
            self.make_button("6", RED),
            self.make_button("7", GREEN),
            self.make_button("8", BLUE).set_fill(BLUE, opacity=0.75),
        ).arrange(RIGHT, buff=0.19)

        # stack
        buttons = VGroup(buttons_top, buttons_bottom).arrange(DOWN, buff=0.2)
        buttons.to_edge(DOWN).scale(0.75)

        self.add(buttons)
