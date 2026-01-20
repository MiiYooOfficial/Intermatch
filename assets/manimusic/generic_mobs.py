from manim import *
from .alphas import *

class WhiteKeySVG(SVGMobject):
  def __init__(self, **kwargs):
    super().__init__("manimusic/music_symbols/white_key.svg", **kwargs)

class BlackKeySVG(SVGMobject):
  def __init__(self, **kwargs):
    super().__init__("manimusic/music_symbols/black_key.svg", **kwargs)

PARENTHESES_TEX_TEMPLATE = TexTemplate()
PARENTHESES_TEX_TEMPLATE.add_to_preamble(r"\usepackage{abraces}")

class Parentheses(MathTex):
    CONFIG = {
        "width_multiplier": 2,
        "max_num_quads": 15,
        "min_num_quads": 0,
    }

    def __init__(self, mobject, direction=DOWN, buff=0, **kwargs):
        for k in self.CONFIG.keys():
          setattr(self, k, self.CONFIG[k])
        self.buff = buff
        self.direction = direction
        angle = -np.arctan2(*direction[:2]) + np.pi
        
        mobject.rotate(-angle, about_point=ORIGIN)
        left = mobject.get_corner(DOWN + LEFT)
        right = mobject.get_corner(DOWN + RIGHT)
        target_width = right[0] - left[0]

        # Adding int(target_width) qquads gives approximately the right width
        num_quads = np.clip(
            int(self.width_multiplier * target_width),
            self.min_num_quads, self.max_num_quads
        )
        tex_string = "\\aoverbrace[l@{}r]{%s}" % (num_quads * "\\qquad")
        MathTex.__init__(self, tex_string, tex_template=PARENTHESES_TEX_TEMPLATE, **kwargs)
        self.tip_point_index = np.argmin(self.get_all_points()[:, 1])
        self.stretch_to_fit_width(target_width)
        self.shift(left - self.get_corner(UP + LEFT) + self.buff * DOWN)
        for mob in mobject, self:
            mob.rotate(angle, about_point=ORIGIN)

    def get_text(self, *text, buff=0.1, background_buff=0.04, **kwargs):
        text_mob = Text(*text, **kwargs)
        text_mob.next_to(self, self.direction, buff=buff)
        text_mob.add_background_rectangle(buff=background_buff)
        return text_mob

    def get_tex(self, *text, buff=0.1, background_buff=0.04, **kwargs):
        tex_mob = MathTex(*text, **kwargs)
        tex_mob.next_to(self, self.direction, buff=buff)
        tex_mob.add_background_rectangle(buff=background_buff)
        return tex_mob


def get_update_relative_note_part(self,main,relative):
    alpha_width = self.note_parts[main].width / self.note_parts[relative].width
    reference_line = Line(
      self.note_parts[main].get_center(),
      self.note_parts[relative].get_center(),
    )
    unit_vector = reference_line.get_unit_vector()
    vector_length = reference_line.get_length()
    alpha_vector_length = self.note_parts[main].width / vector_length
    def update_relative(mob):
        width = mob.note_parts[main].width / alpha_width
        mob.note_parts[relative].scale_to_fit_width(width)
        length = mob.note_parts[main].width / alpha_vector_length
        vector = unit_vector * length
        if relative == "stem":
            _sign = int(mob.sign)
        else:
            _sign = 1
        mob.note_parts[relative].move_to(mob.note_parts[main].get_center()+vector*_sign)
    return update_relative

class AdditionalLineNote(VMobject):
    def __init__(self,note,**kwargs):
        super().__init__(**kwargs)
        line_height = note.width / ALPHA_ADDITIONAL_LINE
        self.set_points_as_corners([ORIGIN,RIGHT*line_height])
        self.move_to(note.body)
        self.set_stroke(None,note.width / ALPHA_STROKE_STEM)

