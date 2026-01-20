from .keyboard import *

from .alphas import ALPHAS
from .generic_mobs import (
  Parentheses,
  get_update_relative_note_part,
  # AdditionalLineNote,
)
from .regex_funcs import *
from .show_addition_parts_funcs import *

from numpy import sign
import itertools as it
from copy import Error


FRAME_WIDTH = config.frame_width
FRAME_HEIGHT = config.frame_height


class Minim(VGroup):
    def __init__(self,
                 note=0,
                 context=None, # staff
                 alteration=None,
                 proportion=0.2,
                 reference_line=0,
                 body_kwargs={
                   "stroke_width": 0,
                   "stroke_opacity":1,
                   "fill_opacity": 1,
                   "fill_color": WHITE,
                 },
                 stem_kwargs={
                   "stroke_width": 5.5,
                   "stroke_opacity": 1,
                   "fill_opacity": 0
                 },
                 add_stem=True,
                 stem_direction=DOWN,
                 type_note="minim",
                 fix_size_factor=1,
                 alteration_buff=0,
                 **kwargs):
        super().__init__(**kwargs)
        self.body_kwargs = body_kwargs
        self.stem_kwargs = stem_kwargs
        self.add_stem = add_stem
        self.stem_direction = stem_direction
        self.type_note = type_note
        self.fix_size_factor = fix_size_factor
        self.alteration_buff = alteration_buff
        self.set_type_note()
        self.add(self.body)
        self.set_custom_properties()
        self.reference_line = reference_line
        self.note_parts = {"body": self.body}
        self.principal = VGroup(self.body)
        self.sign = self.stem_direction[1]
        self.proportion = proportion
        self.additional_lines_level = note
        if context != None:
            self.context = context
            self.note = note
            self.context.set_note_at(self, note, proportion, reference_line)
        if self.add_stem:
            self.stem = self.set_symbol("stem")
            self.principal.add(self.stem)
            self.add(self.stem)
            # self.add_updater(get_update_relative_note_part(self,"body","stem"))
        if alteration != None:
            self.add_alteration(alteration)
        else:
            self.alteration_name = None
            self.alteration = None

    def set_custom_properties(self):
        pass

    def alteration_updater(self,alteration):
        return get_update_relative_note_part(self,"body",alteration)

    def add_alteration(self,alteration):
        self.alteration_name = alteration
        self.alteration = self.set_symbol(alteration)
        self.add(self.alteration)
        # self.add_updater(get_update_relative_note_part(self,"body",alteration))

    def set_type_note(self):
        if self.type_note != "semibreve":
            index = 1
        else:
            index = 0
        self.body = SVGMobject(f"manimusic/music_symbols/{self.type_note}",**self.body_kwargs)[index]

    def valid_context(self, context):
        if context != None:
            self.context = context

    def set_symbol(self, symbol):
        if symbol in ["stem"]:
          symbol_object = SVGMobject(f"manimusic/music_symbols/{self.type_note}",**self.body_kwargs)[0]
        elif symbol in ["sharp", "flat", "natural"]:
          symbol_object = SVGMobject(f"manimusic/music_symbols/{symbol}",**self.body_kwargs)[0]
        main_width = self.body.width
        symbol_object.scale_to_fit_width(main_width / ALPHAS[symbol]["width"])
        vector_lenght_stem = main_width / ALPHAS[symbol]["vector_length"]
        vector_stem = vector_lenght_stem * ALPHAS[symbol]["unit_vector"]
        if symbol == "stem":
          vector_stem *= self.sign
        symbol_object.move_to(self.body.get_center()+vector_stem)
        if symbol != "stem":
          symbol_object.shift(LEFT*self.alteration_buff)
          self.note_parts["alteration"] = symbol_object
        self.note_parts[symbol] = symbol_object
        return self.note_parts[symbol]

    def set_note(self, note, proportion=None, reference_line=None, context=None):
        self.valid_context(context)
        if proportion != None:
            try:
                alteration_width = abs(self.body.get_left() - self.alteration.get_left())
            except:
                alteration_width = 0
            x_coord = self.context.get_proportion_line(proportion,reference_line)[0] - alteration_width/2
        else:
            x_coord = self.get_x()
        if reference_line == None:
            reference_line = self.reference_line
        x_distance = x_coord - self.get_x()
        y_distance = self.body.get_y()-self.context.reference_lines[reference_line].get_y()
        note_distance = self.context.get_space_between_lines()/2
        note_self = np.round(y_distance/note_distance)
        if note != None:
            self.shift(UP*self.context.get_space_between_lines()*(note-note_self)/2+x_distance*RIGHT)

    def get_note_str(self, reference_line=0):
        y_distance = abs(self.body.get_y()-self.context.reference_lines[reference_line].get_y())
        note_distance = self.context.get_space_between_lines()/2
        note_self = np.round(y_distance/note_distance)
        return note_self

    def get_parts(self, *args):
        return VGroup(*[getattr(self, arg) for arg in args if hasattr(self, arg)])


class Crotchet(Minim):
  def __init__(self, *args, type_note="crotchet", **kwargs):
    super().__init__(*args, type_note=type_note, **kwargs)


class Semibreve(Minim):
  def __init__(self, *args, type_note="semibreve", add_stem=False, **kwargs):
    super().__init__(*args, type_note=type_note, add_stem=add_stem, **kwargs)

class LaggedAnim(AnimationGroup):
  def __init__(self, pause=0.3, *anims, wrap_anim=AnimationGroup, lag_ratio=0, **kwargs):
    super().__init__(
      Wait(pause),
      wrap_anim(*anims, lag_ratio=lag_ratio),
      lag_ratio=1,
      **kwargs
    )


class Staff(VGroup):
    DEFAULT_ARRANGE_CONFIG = {
      "direction": DOWN, "buff":1
    }
    DEFAULT_STAFF_CONFIG = {
      "stroke_width": 3,
      "stroke_opacity": 1,
      "fill_opacity": 1,
      "stroke_color": WHITE,
    }
    DEFAULT_CLEFF_CONFIG = {
      "fill_opacity": 1,
      "stroke_opacity": 1,
      "fill_color": WHITE,
      "stroke_color": WHITE
    }
    reference = 2
    def __init__(self,
                 num_staffs=0,
                 clefs=None,
                 arrange_config={},
                 staff_config={},
                 clef_config={},
                 left_buff=0.08,
                 show_reference=False,
                 bars=[],
                 partition=30,
                 width=8,
                 height=1,
                **kwargs):
        super().__init__(**kwargs)
        self.num_staffs = num_staffs
        self.clefs = clefs
        self.arrange_config = merge_dicts_recursively(
           self.DEFAULT_ARRANGE_CONFIG, arrange_config
        )
        self.staff_config = merge_dicts_recursively(
           self.DEFAULT_STAFF_CONFIG, staff_config
        )
        self.clef_config = merge_dicts_recursively(
           self.DEFAULT_CLEFF_CONFIG, clef_config
        )
        self.left_buff = left_buff
        self.show_reference = show_reference
        self.bars = bars
        self.partition = partition
        self.staff = SVGMobject("manimusic/music_symbols/c_clef",**self.staff_config)[:5]
        self.staff[0].set_style(**staff_config)
        self.p_height = height
        # Fix lines
        for i in range(1,len(self.staff)):
            self.staff[i].points[-1][0] = self.staff[0].points[-1][0]
        self.staff.stretch_to_fit_width(width)
        self.staff.stretch_to_fit_height(height)
        self.staffs = VGroup()
        self.clefs_group = VGroup()
        self.reference_lines = VGroup()
        self.reference_numbers = VGroup()
        self.additional_lines = VGroup()
        self.bars_group = VGroup()
        self.choord_names = VGroup()
        self.key_signatures = VGroup()
        self.tempo = VGroup()
        self.tempo_group = VGroup()
        if self.num_staffs == 0 and self.clefs != None:
            self.num_staffs = len(self.clefs)
        if self.num_staffs == 0 and self.clefs == None:
            self.num_staffs = 1
            self.clefs = "g"
        self.set_staffs()
        if self.clefs != None:
            self.set_clefs()
        if self.num_staffs == 2 and self.clefs == None:
            self.clefs = "gf"
            self.set_clefs()
        if self.show_reference:
            self.set_reference_system()
        for bar in self.bars:
            self.add_bar(bar)
        self.clefs_group.set_style(**clef_config)
        self.add(
            self.staffs,
            self.clefs_group,
            self.reference_numbers,
            self.additional_lines,
            self.bars_group,
            self.tempo,
        )


    def set_staffs(self):
        for _ in range(self.num_staffs):
            staff = self.staff.copy()
            self.staffs.add(staff)
            self.reference_lines.add(staff[self.reference])
        self.staffs.arrange(**self.arrange_config)

    def add_bar(self, bar):
        reference_up = self.staffs[0][0]
        reference_down = self.staffs[-1][-1]

        proportion = 1 / self.partition
        line = Line(
            reference_up.point_from_proportion(proportion * bar),
            reference_down.point_from_proportion(proportion * bar),
            **self.staff_config
        )
        self.bars_group.add(line)

    def get_clef_val(self, clef):
        if clef == "g":
          return -6
        elif clef == "f":
          return -1
        elif clef == "c":
          return -7
        else:
          raise Error("Clef not found")


    def set_clefs(self):
        count = 0
        try:
            for c in self.clefs:
                clef = ALPHAS["clefs"][c]["symbol"].copy()
                clef.set_style(**self.clef_config)
                clef.scale_to_fit_height(self.p_height / ALPHAS["clefs"][c]["height"])
                clef.next_to(self.staffs[count].get_left(),RIGHT,buff=self.left_buff)
                self.staffs[count].set(clef_val=self.get_clef_val(c))
                self.staffs[count].set(clef=c)
                if c != "c":
                    clef.shift(DOWN*(self.p_height / ALPHAS["clefs"][c]["down"]))
                self.clefs_group.add(clef)
                count += 1
        except:
            print(ERROR_NUMBER_CLEFS)

    def get_space_between_lines(self):
        return abs(self.staffs[0][1].get_y() - self.staffs[0][2].get_y())

    def get_proportion_line(self,proportion,reference_line):
        return self.reference_lines[reference_line].point_from_proportion(proportion)

    def get_space_note(self,position):
        return self.get_space_between_lines() * position / 2

    def set_note_at(self, mob, note=0, proportion=0.2, reference_line=0):
        mob.scale_to_fit_height(self.get_space_between_lines() * mob.fix_size_factor)
        if proportion > 1:
           raise Error(f"prop={proportion} > 1, note cannot be outside the lines")
        mob.move_to(self.get_proportion_line(proportion,reference_line))
        mob.shift(UP * self.get_space_note(note))

    def set_reference_system(self):
        for staff in self.staffs:
            for n in range(5):
                number = Text(f"{-n+2}")
                number.scale_to_fit_height(self.get_space_between_lines()*0.8)
                number.next_to(staff[n],LEFT,buff=0.1)
                self.reference_numbers.add(number)

    def add_additional_line(self,nivel=2,proportion=0.2,reference_line=0,fade=0,color=None):
        note_space = self.get_space_between_lines()
        if nivel == 0:
            raise ValueError("nivel must be != 0")
        length_line = note_space / ALPHA_STAFF_ADDITIONAL_LINE
        additional_line = Line(ORIGIN,RIGHT*length_line, **self.staff_config)
        # additional_line.match_style(self.staffs[0])
        reference_dot = Dot()
        reference_dot.next_to(self.staffs[reference_line],UP*sign(nivel),buff=0)
        x_coord = self.get_proportion_line(proportion,reference_line)[0]
        group_lines = VGroup()
        for i in range(abs(nivel)):
            line = additional_line.copy()
            line.next_to(self.staffs[reference_line], UP*sign(nivel), buff = (note_space * (i + 1)))
            line.move_to([x_coord,line.get_y(),0])
            group_lines.add(line)
        group_lines.fade(fade)
        if color is not None:
          group_lines.set_color(color)
        self.additional_lines.add(group_lines)
        return self.additional_lines[-1]

    def add_additional_line_from_note(self, note: Minim, *args, **kwargs):
        if abs(note.note) <= 5:
          return False
        val = 5 if note.note < 0 else 4
        reff = note.note - val * np.sign(note.note)
        nivel = int(np.floor(reff / 2))
        return self.add_additional_line(nivel, note.proportion, note.reference_line, *args, **kwargs)

    def add_key_signature(self,
                          type_alt="sharp",
                          n=7,
                          # reference_line=0,
                          buff=0.1):
        for staff,clef in zip(self.staffs,self.clefs_group):
            pre_key_signature = SVGMobject(f"manimusic/music_symbols/key_signature_{type_alt}")[7:]
            main_width = self.staff.p_height
            pre_key_signature.scale_to_fit_width(main_width/ALPHAS[f"ks_{type_alt}"]["width"])
            pre_key_signature.next_to(clef,RIGHT,buff=buff)
            pre_key_signature.match_y(staff)
            pre_key_signature.shift(UP*main_width/ALPHAS[f"ks_{type_alt}"]["dy"])
            dh = clef.p_height - self.staffs[0].p_height #<
            if abs(dh)<0.1:
                pre_key_signature.shift(DOWN*self.get_space_between_lines()/2)
            elif dh < -0.1:
                pre_key_signature.shift(DOWN*self.get_space_between_lines())
            key_signature = pre_key_signature[:n]
            self.key_signatures.add(key_signature)
        for i in range(len(self.key_signatures)):
            if i <= len(self.key_signatures) - 1 and i > 0:
                ks_pos = self.key_signatures[i]
                ks_pre = self.key_signatures[i-1]
                if ks_pos.get_x() > ks_pre.get_x():
                    ks_pre.match_x(ks_pos)

    def get_ticks(self,number_height=0.2,buff=0.5,tick_height=0.4):
        partition = 1 / self.partition
        direction = UP*sign(buff)
        reference_line = Line(
          self.staffs.get_corner(direction+LEFT),
          self.staffs.get_corner(direction+RIGHT),
        )
        reference_line.shift(direction*abs(buff))
        reference_group = VGroup(reference_line)

        tick = Line(ORIGIN,UP*tick_height)
        for i in range(self.partition+1):
            tick_position = reference_line.point_from_proportion(i * partition)
            new_tick = tick.move_to(tick_position).copy()
            number = Text(f"{i}").scale_to_fit_height(number_height)
            number.next_to(new_tick,direction,buff=0.1)
            reference_group.add(new_tick,number)
        return reference_group

    def add_tempo(self,num=4,den=None,proportion=0.2):
        if den == None:
            den = num
        num_mob = MathTex("\\mathbf{%s}"%num)
        den_mob = MathTex("\\mathbf{%s}"%den)
        tempo = VGroup(num_mob,den_mob)
        tempo.arrange(DOWN,buff=0)
        tempo.match_height(self.staffs[0])
        tempo_grp = VGroup()
        for staff in self.staffs:
            position = staff[2].point_from_proportion(proportion)
            tempo_copy = tempo.copy()
            tempo_copy.move_to(position)
            self.tempo.add(tempo_copy)
            tempo_grp.add(tempo_copy)
        self.tempo_group.add(tempo_grp)


    def return_chord_name(self,mob,note,buff=0.6,note_height=0.4,**tex_kwargs):
        tex = MathTex(f"\\rm {note}",**tex_kwargs).scale_to_fit_height(note_height)
        dot = Dot()
        dot.scale_to_fit_height(self.get_space_between_lines())
        line = Line(DOWN,UP)
        line.next_to(mob,RIGHT,buff=0)
        dot.next_to(line,LEFT,buff=0)
        coord_x = dot.get_x()
        coord_y = self.staffs[-1][-1].get_y() - buff
        tex.move_to([coord_x,coord_y,0])
        return tex

    def add_chord_name(self,mob,note,**tex_kwargs):
        tex = self.return_chord_name(mob,note,**tex_kwargs)
        self.choord_names.add(tex)

    def scale(self, *args, **kwargs):
        mob = super().scale(*args, **kwargs)
        mob.p_height = mob.staffs[0].height
        return mob
    
    def get_signature(self, symbol, prog, n, start_at=0.3, refs=None, buff=0.2):
      signatures = VGroup()
      if refs is None:
        refs = range(len(self.staffs))
      for r in refs:
        for i in range(n):
          alt = Semibreve(prog[i]+KEY_SIGNATURE_D[self.staffs[r].clef], self, symbol, start_at, r)
          alt.alteration.match_x(alt.body)
          alt.alteration.shift(RIGHT * i * buff)
          signatures.add(alt.alteration)
      return signatures

    def get_sharp_signature(self, *args, **kwargs):
      return self.get_signature("sharp", SHARP_PROG, *args, **kwargs)

    def get_flat_signature(self, *args, **kwargs):
      return self.get_signature("flat", FLAT_PROG, *args, **kwargs)

    def get_natural_sharp_signature(self, *args, **kwargs):
      return self.get_signature("natural", SHARP_PROG, *args, **kwargs)

    def get_natural_flat_signature(self, *args, **kwargs):
      return self.get_signature("natural", FLAT_PROG, *args, **kwargs)


KEY_SIGNATURE_D = {
    "g": 0,
    "c": -1,
    "f": -2
}

class Note(Minim):
  def __init__(self, staff:Staff, params, prop, line=None, **kwargs):
    if len(staff.staffs) == 1 and line is None:
       line = 0
    if len(staff.staffs) > 1 and line is None:
      raise Error("Lines > 1 so line<int> after proportion")
    if "s" in params and "x" not in params:
      params += "x"
    shift = extract_number(params)
    val = staff.staffs[line].clef_val
    note_str = self.get_note_str(params)
    alt_name  = self.get_alteration(params)
    note = self.get_note_number(note_str, shift, val)
    type_note = self.get_type_note(params[0])
    stem_config = self.get_stem_config(params)
    all_kwargs = {**kwargs, **stem_config}
    self.params = params
      
        
    super().__init__(
      note, staff, alt_name, prop, line,
      type_note=type_note,
      **all_kwargs
    )
    if "l" in params:
      shift = LEFT * self.body.width * self.shift_val *0.95
      self.body.shift(shift)
      try:
        self.alteration.shift(shift)
      except:
        pass
      self.shifted_left = True
    if "a" in params:
      self.alteration.shift(LEFT * self.alteration.width*1.1)
      self.shifted_left = True
    if "h" in params:
      self.alteration.shift(LEFT * self.alteration.width*1.5)
      self.shifted_left = True
    if "H" in params:
      self.alteration.shift(LEFT * self.alteration.width*2)
      self.shifted_left = True
    if "r" in params:
      self.body.shift(RIGHT * self.body.width * self.shift_val)
      self.shifted_right = True
    if "R" in params:
      self.shift(RIGHT * self.body.width*0.96)
    if "L" in params:
      self.shift(LEFT * self.body.width*0.96)
    if "_" in params:
      n_underscore = count_trailing_underscore(params)
      self.alteration.shift(LEFT * n_underscore * 0.05)
      self.shifted_left = True

    if hasattr(self, "stem") and hasattr(self, "shifted_right"):
      self.remove(self.stem)
      del self.stem
    if abs(note) > 5:
      self.additional_lines = staff.add_additional_line_from_note(self)
      if hasattr(self, "shifted_right"):
        self.additional_lines.shift(RIGHT * self.body.width)

  def get_note_str(self, params):
    for i in "ABCDEFGH":
      if i in params:
        return i
    raise Error("Note not found")

  def get_alteration(self, params):
    for i in params:
      if i == "#":
        return "sharp"
      elif i == "b":
        return "flat"
      elif i == "n":
        return "natural"
    return None

  def get_stem_config(self, params):
    args = {"add_stem": True}
    if "x" in params:
      return {"add_stem": False}
    elif "d" in params:
      return {"stem_direction": DOWN, **args}
    elif "u" in params:
      return {"stem_direction": UP, **args}
    else:
      return args

  def get_note_number(self, note_str, shift, val):
    return KEY_DICTIONARY_REG[note_str] + val + 7 * shift

  def get_type_note(self, n):
    if "m" == n:
      self.shift_val = 0.95
      return "minim"
    elif "c" == n:
      self.shift_val = 0.95
      return "crotchet"
    elif "s" == n:
      self.shift_val = 0.9
      return "semibreve"
    else:
      raise Error(f"{n}: Type note not found")

  def show_note(self, anim=Write, add_alteration=False, *args, **kwargs):
    return AnimationGroup(
      anim(self, *args, **kwargs),
      *ShowAdditionLinesNote(self, anim, add_alteration=add_alteration, *args, **kwargs)
    )

  @classmethod
  def get_note(self, n):
    if n == "m":
      return Minim
    elif n == "c":
      return Crotchet
    elif n == "s":
      return Semibreve
    else:
      raise Error("Note not found")

  @classmethod
  def get_alt(self, alt):
    if alt == "x":
      return None
    elif alt == "f":
      return "flat"
    elif alt == "s":
      return "sharp"
    elif alt == "n":
      return "natural"
    else:
      raise Error("Alt not found")

  @classmethod
  def get_chord(self, p, note_string, note_class, prop, ref_line, stem_dirs=[DOWN,UP]):
    notes = note_string.split(",")
    chord = VGroup()
    stem_dirs_it = it.cycle(stem_dirs)
    for n in notes:
      if len(n) == 0:
        continue
      val = int(n[:-1])
      alt = n[-1]
      c = note_class(
        val, p, Note.get_alt(alt), prop,
        reference_line=ref_line,
        stem_direction=next(stem_dirs_it)
      )
      chord.add(c)
      p.add_additional_line_from_note(c)

    return chord

  @classmethod
  def get_interval_chord(self, chord, n1, n2, direction=RIGHT, buff=0.1, **kwargs):
    line = Line(chord[n1].body.get_center(), chord[n2].body.get_center())
    return Parentheses(line, direction, buff=buff, **kwargs)

  @classmethod
  def get_multi_chord(self, p, ch_str, prop, order_ref=[1, 0]):
    chord = VGroup()
    note, *ch = fm(ch_str)
    note_class = Note.get_note(note)
    for r, c in zip(order_ref, ch):
      chord.add(*Note.get_chord(p, c, note_class, prop, r))
    return chord


class Melody(VGroup):
  def __init__(self,
               staff,
               notes,
               start_prop=0.2,
               line=None,
               glob="m",
               increment=0.2,
               split_symbol="|",
               merge_stems=False,
               remove_extra_additional_lines=False):
    if len(staff.staffs) == 0 and line is None:
      line = 0
    elif len(staff.staffs) > 1 and line is None:
       raise Error("Lines > 1 so line<int> arg is needed")
    self.glob = glob
    notes_list = fm(notes, split_symbol)
    notes_str = "mcs"
    points_count = []
    has_note_str = False
    # Check if glob have "m" or "c" or "s"
    for ns in notes_str:
      if ns in glob:
        has_note_str = True
        break
    if not has_note_str:
      glob = "m" + glob
    for i in range(len(notes_list)):
      points_count.append(count_trailing_dots(notes_list[i]))
      if glob is None:
        continue
      for g in glob:
        if g in notes_str:
          # Ignore if glob has "mcs"
          if notes_list[i][0] in notes_str:
            continue
          notes_list[i] = g + notes_list[i]
        else:
          notes_list[i] = notes_list[i] + g
        # print(notes_list[i])
    notes = [
      Note(staff, params, start_prop + (i + sum(points_count[:i])) * increment, line)
      for i, params in enumerate(notes_list)
    ]
    if not remove_extra_additional_lines:
      super().__init__(*notes)
      if merge_stems:
        self.merge_stems()
      return
    add_lines_up = VGroup()
    add_lines_down = VGroup()
    max_up   = 0
    min_down = 0
    min_element = None
    max_element = None
    direction_flag = None
    for n in notes:
      if hasattr(n, "additional_lines"):
        if n.additional_lines_level > 0:
          add_lines_up.add(n)
          if len(n.additional_lines) > max_up:
            max_up = len(n.additional_lines)
        elif n.additional_lines_level < 0:
          add_lines_down.add(n)
          if len(n.additional_lines) > min_down:
            min_down = len(n.additional_lines)
        else:
          raise Error("Level must be != 0")
      if "r" in n.params and direction_flag is None:
        direction_flag = 1
      if "l" in n.params and direction_flag is None:
        direction_flag = -1

    # Get levels
    if len(add_lines_down) + len(add_lines_up) == 0:
      super().__init__(*notes)
      if merge_stems:
        self.merge_stems()
      return
    self.additional_lines = VGroup()
    # DOWN process
    if len(add_lines_down) > 1: # Multiple
      min_element = list(filter(
          lambda mob: len(mob.additional_lines) == min_down, add_lines_down
      ))[0]
      self.additional_lines.add(*min_element.additional_lines)
      min_element.selected = True
    elif len(add_lines_down) == 1: # Single
      min_element = add_lines_down[0]
      self.additional_lines.add(*min_element.additional_lines)
      min_element.selected = True
    #UP
    if len(add_lines_up) > 1: # Multiple
      max_element = list(filter(
          lambda mob: len(mob.additional_lines) == max_up, add_lines_up
      ))[0]
      self.additional_lines.add(*max_element.additional_lines)
      max_element.selected = True
    elif len(add_lines_up) == 1: # Single
      max_element = add_lines_up[0]
      self.additional_lines.add(*max_element.additional_lines)
      max_element.selected = True

    are_down_grow = False
    are_up_grow   = False
    
    for n in notes:
      if hasattr(n, "additional_lines") and not hasattr(n, "selected"):
        n.additional_lines.remove(*n.additional_lines)
        delattr(n, 'additional_lines')
      if ("r" in n.params or "l" in n.params):
        if n.additional_lines_level < 0 and not are_down_grow and min_element is not None:
          are_down_grow = True
          if len(add_lines_down) == 1:
            pass
          elif len(add_lines_up) > 1:
            min_element.additional_lines.scale([
              1.6 if "s" in min_element.params else 1.5,
              1, 1], about_edge=LEFT * direction_flag)
        if n.additional_lines_level > 0 and not are_up_grow and max_element is not None:
          are_up_grow = True
          if len(add_lines_up) == 1:
            max_element.additional_lines.match_x(max_element)
          elif len(add_lines_up) > 1:
            max_element.additional_lines.scale([
              1.6 if "s" in max_element.params else 1.5,
              1, 1], about_edge=LEFT * direction_flag)
        
      super().__init__(*notes)
      if merge_stems:
        self.merge_stems()

  def merge_stems(self):
    if "x" in self.glob:
      raise Error("You have 'x' in the glob argument, you can't merge stems")
    if "s" in self.glob:
      raise Error("Semibreve does't have stem")
    stems = VGroup(*[n.get_parts("stem").copy() for n in self])
    d_up = stems.get_top()
    d_down = stems.get_bottom()
    height = abs(d_up[1] - d_down[1])
    width = stems[0].width
    big_stem = stems[0].copy()
    big_stem.stretch_to_fit_height(height)
    big_stem.stretch_to_fit_width(width)
    big_stem.next_to(stems.get_bottom(), UP, buff=0)
    self[0].stem.become(big_stem)
    self.stem = self[0].stem
    for i in range(1,len(self)):
      if hasattr(self[i], "stem"):
        self[i].remove(self[i].stem)
        delattr(self[i], 'stem')

  def show_chord(self, anim=Write, add_alteration=False, *args, **kwargs):
    return AnimationGroup(
      anim(self, *args, **kwargs),
      *ShowAdditionLinesChord(self, anim,add_alteration=add_alteration, *args, **kwargs)
    )


class ChordLine(Melody):
  def __init__(self,
               *args,
               remove_extra_additional_lines=True,
               merge_stems=False,
               **kwargs):
    super().__init__(*args,
               increment=0,
               merge_stems=merge_stems,
               remove_extra_additional_lines=remove_extra_additional_lines,
               **kwargs)

class MultiChord(VGroup):
  def __init__(self,
               staff,
               notes,
               start_prop=0.2,
               line=None,
               glob="",
               refs_symbol_separator="|",
               chords_symbol_separatior=",",
               **kwargs):
    note, *chords_str_raw = fm(notes, refs_symbol_separator)

    if line is None:
      line = list(range(len(staff.staffs)))[::-1]
      line = line[:len(chords_str_raw)]

    assert len(line) == len(chords_str_raw), f"Lines: {len(line)} != #chords: {len(chords_str_raw)}"
    self.chords_symbol_separatior = chords_symbol_separatior

    for i in "mcs":
      if i in glob:
        glob.replace(i, '')
    chords = [
      ChordLine(
        staff,
        self.get_params_formated(note, params),
        start_prop,
        line[i],
        glob=glob,
        split_symbol=chords_symbol_separatior,
        **kwargs
      )
      for i, params in enumerate(chords_str_raw)
    ]
    super().__init__(*chords)
    additional_lines = VGroup()
    for c in chords:
      if hasattr(c, "additional_lines"):
        additional_lines.add(c.additional_lines)
    if len(additional_lines) > 0:
      self.additional_lines = additional_lines

  def show_chord(self, anim=Write, add_alteration=False, *args, **kwargs):
    return AnimationGroup(
      anim(self, *args, **kwargs),
      *ShowAdditionLinesMultiChord(self, anim, add_alteration=add_alteration, *args, **kwargs)
    )

  def get_params_formated(self, note, params):
    return self.chords_symbol_separatior.join([
      note + p 
      for p in fm(params, self.chords_symbol_separatior)
    ])


class HarmonyProgression(VGroup):
  def __init__(self, p, *args, line=None, glob="", start_prop=0.2, increment=0.2, colors=[WHITE], **kwargs):
    points_count = [count_trailing_dots(arg) for arg in args]
    super().__init__(*[
      MultiChord(
        p,
        arg,
        start_prop + (i + sum(points_count[:i])) * increment,
        line,
        glob,
        **kwargs
      )
      for i, arg in enumerate(args)
    ])
    self.colors = colors
    colors_cycle = it.cycle(colors)
    for multi_chord in self:
      for chord in multi_chord:
        for note in chord:
          note.set_color(next(colors_cycle))


  def show_chord(self, i, anim, add_alteration=False, *args, **kwargs):
    return AnimationGroup(
        anim(self[i], *args, **kwargs),
        *ShowAdditionLinesMultiChord(self[i], anim, add_alteration=add_alteration, *args, **kwargs)
    )
  
  def transform(self,
               start_index,
               end_index,
               transform_anim=TransformFromCopy,
               anim=Write,
               lag=1.2,
               *args,
               **kwargs):
    transforms = [
      transform_anim(
        note_base.get_parts("body", "stem"),
        note_target.get_parts("body", "stem"),
        *args, **kwargs
      )
      for chord_base, chord_target in zip(self[start_index], self[end_index])
      for note_base, note_target in zip(chord_base, chord_target)
    ]
    return [
       *transforms,
       LaggedAnim(
        lag, *ShowAdditionLinesMultiChord(self[end_index], anim)
       )
    ]
 

class VInterval(Parentheses):
  def __init__(self, n1, n2, direction=RIGHT, buff=0, **kwargs):
    l = Line(
       n1.body.get_edge_center(direction),
       n2.body.get_edge_center(direction),
    )
    super().__init__(l, direction=direction, buff=buff, **kwargs)
