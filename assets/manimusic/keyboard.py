from manim import *
from .constants import *
from .generic_mobs import (
  WhiteKeySVG,
  BlackKeySVG,
)

import itertools as it


FRAME_WIDTH = config.frame_width
FRAME_HEIGHT = config.frame_height


class Keyboard(VGroup):
    def __init__(self,
                 octaves=4,
                 key_type="keyboard",
                 prop=1.32,
                 position=ORIGIN,
                 keyboard_kwargs={
                   "stroke_width": 1,
                   "stroke_opacity":1,
                   "stroke_color":BLACK,
                   "fill_opacity":1
                 },
                 origin_C=ORIGIN,
                 ref=2,
                 chord_colors=[RED_D,TEAL_D,PURPLE_D,BLUE_D],
                 **kwargs):
        super().__init__(**kwargs)
        self.prop = prop
        self.ref = ref
        self.position = position
        self.keyboard_kwargs = keyboard_kwargs
        self.origin_C = origin_C
        self.chord_colors = chord_colors
        self.octaves = octaves
        self.chord_colors_cycle = it.cycle(self.chord_colors)
        self.key_type = key_type
        if key_type == "keyboard":
            keyboard = self.get_keyboard(octaves,**self.keyboard_kwargs)
            self.add(*keyboard)
            self.set_keyboard_keys()
            self.move_to(self.origin_C)
        self.number_keys = self.get_number_keys()
        self.black_keys = self.get_black_keys()
        self.initial_octaves = self.get_initial_octaves()

    def get_note_sound(self, index, folder="notes"):
      return f"manimusic/{folder}/{index + self.ref * 12}"

    def get_keyboard(self, octaves=4, **keyboard_kwargs):
        keyboard = VGroup()
        octave = self.get_octave(**keyboard_kwargs)
        for _ in range(octaves):
            if len(keyboard) == 0:
                keyboard.add(*octave.copy())
            else:
                pre_keyboard = octave.copy()
                pre_keyboard.next_to(keyboard,RIGHT,buff=0)
                keyboard.add(*pre_keyboard)

        keyboard.move_to(ORIGIN)
        return keyboard

    def get_black_keys(self):
        black_keys = VGroup()
        for key in self:
            if key.get_y() > self.get_y():
                black_keys.add(key)
        return black_keys

    def get_octave(self, **keyboard_kwargs):
        white_keys = VGroup(*[WhiteKeySVG(**keyboard_kwargs) for _ in range(7)]).arrange(RIGHT,buff=0)
        black_keys = VGroup()
        for i in [0,1,3,4,5]:
            black_key = BlackKeySVG(**keyboard_kwargs).set_color(BLACK)
            black_key.scale(KEYBOARD_PROPORTION/white_keys[i].height)
            black_key.next_to(white_keys[i].get_top(),DOWN,buff=0)
            black_key.set_x(white_keys[i].get_right()[0])
            black_key.scale([1.4,1,1]) # <-- Scale changed
            black_keys.add(black_key)
        octave = VGroup()
        octave.white_keys = white_keys
        octave.black_key  = black_keys
        sequence = ["D","D","N","D","D","D","N"]
        b = 0;w = 0
        for seq in sequence:
            if seq == "D":
                octave.add(white_keys[w])
                octave.add(black_keys[b])
                b += 1
            elif seq == "N":
                octave.add(white_keys[w])
            w += 1
        return octave

    def get_number_keys(self):
        numbers = VGroup()
        for i in range(len(self)):
            number = Text(f"{i}")
            number.scale_to_fit_height(0.2)
            number.next_to(self[i],DOWN,buff=0.1)
            numbers.add(number)
        return numbers

    def set_piano_keys(self):
        octaves = 7
        self.k = {}
        counter = 0
        for k in KEY_DICTIONARY.keys():
          k_keys = [3 + KEY_DICTIONARY[k] * n for n in range(octaves)]
          if KEY_DICTIONARY[k] >= 9:
            new_key = KEY_PROGRETION[counter]
            self.k[k] = [KEY_DICTIONARY[new_key], *k_keys]
            counter += 1
          else:
            self.k[k] = k_keys


    def set_keyboard_keys(self):
        octaves = self.octaves
        self.k = {}
        self.key = {}
        keys = KEY_PROGRETION
        count = 0
        for key,i in zip(keys,range(len(keys))):
            if key[-1] == "b":
                self.k[key] = self.k[f"{keys[i-1][0]}#"]
            else:
                self.k[key]  = [count+12*n for n in range(octaves)]
            if i < len(keys)-1 and len(keys[i])+len(keys[i+1])<4:
                count += 1

        for key in keys:
            self.key[key] = VGroup(*[self[self.k[key][k]] for k in range(octaves)])

    def get_initial_octaves(self):
        numbers = VGroup()
        for i in range(int(len(self)/12)):
            number = Text(f"{i}")
            number.scale_to_fit_height(0.2)
            number.next_to(self[i*12],DOWN,buff=0.1)
            numbers.add(number)
        numbers.set_color(RED)
        return numbers

    def get_chord(self, reference=0, *keys):
        reference_item = self.get_key_octave(keys[0][:-1],reference)
        reference_octave = self.get_octave_by_item(reference_item)
        chord = VGroup()
        chord.indexes = []
        total_keys = len(keys)
        for pre_key,i in zip(keys, range(total_keys)):
            key = pre_key[:-1]
            octave_increment = int(pre_key[-1])
            reference_octave +=octave_increment
            selected_key = self.key[key][reference_octave]
            # print(f"key={KEY_DICTIONARY[key]}, octave={reference_octave}, note={KEY_DICTIONARY[key] + reference_octave * 12}")
            mob_key = Dot()
            mob_key.match_width(selected_key).scale(0.9)
            mob_key.move_to(
              selected_key.get_bottom() + UP * mob_key.width
            )
            chord.add(mob_key)
            chord.indexes.append(KEY_DICTIONARY[key] + reference_octave * 12)
            if i < total_keys-1:
                if KEY_DICTIONARY[keys[i][:-1]] > KEY_DICTIONARY[keys[i+1][:-1]]:
                    reference_octave +=1
        for c in chord:
            c.set_color(next(self.chord_colors_cycle))
        return chord
    
    def get_chord_with_figures(self, reference, *keys, **figure_config):
        chord = self.get_chord(reference,*keys)
        figure = figure_config["figure"]
        figure_kwargs = figure_config.copy()
        figure_kwargs.pop("figure")
        figures = VGroup(*[
            figure(**figure_kwargs).scale_to_fit_width(c.width*0.8)\
            .next_to(c.get_bottom(),UP,buff=c.width*0.8/2)\
            .match_color(c).set_fill(opacity=1)
            for c in chord
        ])
        for figure in figures: figure.set_stroke(None,0)

        return figures

    def get_chord_with_circles(self, reference=1, *keys, **figure_config):
        figure_config["figure"] = Circle
        return self.get_chord_with_figures(reference,*keys,**figure_config)

    def get_key_octave(self, key, reference):
        return self.k[key][reference]

    def get_octave_by_item(self, item):
        return int(item/12)

