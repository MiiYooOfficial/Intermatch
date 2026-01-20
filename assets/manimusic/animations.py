from .music_mobs import *

class SoundKey(Animation):
  def __init__(self, file_name, sound_kwargs, *args, **kwargs):
    self.file_name = file_name
    self.some_mob = Mobject()
    self.sound_kwargs = sound_kwargs
    super().__init__(self.some_mob, *args, **kwargs)

  def _setup_scene(self, scene: Scene) -> None:
    scene.add_sound(self.file_name, **self.sound_kwargs)
    return super()._setup_scene(scene)

  def clean_up_from_scene(self, scene: Scene) -> None:
    scene.remove(self.mobject)
    return super().clean_up_from_scene(scene)


class KeyboardSoundIndexes(Succession):
  def __init__(self,
               keyboard,
               indexes,
               pause=0.5,
               folder="notes",
               sound_kwargs={"gain": -10},
               *args,
               lag_ratio=1,
               **kwargs):
    self.keyboard = keyboard
    super().__init__(
      Wait(pause),
      AnimationGroup(*[
        SoundKey(keyboard.get_note_sound(ind, folder), sound_kwargs)
        for ind in indexes
      ]),
      *args,
      **kwargs,
      lag_ratio=lag_ratio
    )

class KeyboardSound(KeyboardSoundIndexes):
  def __init__(self, keyboard, chord, **kwargs):
    super().__init__(keyboard, chord.indexes, **kwargs)


class ShowStaff(AnimationGroup):
  def __init__(self, staff: Staff, anim=GrowFromCenter, **kwargs):
    super().__init__(*[
        AnimationGroup(*[
          anim(l)
          for l in line
        ])
        for line in staff.staffs
      ],
      Write(staff.clefs_group),
      **kwargs
    )

class ShowKeyboard(LaggedStart):
  def __init__(self, keyboard: Keyboard, anim=GrowFromEdge, *args, lag_ratio=0.05, **kwargs):
      self.keyboard = keyboard
      if DOWN not in args and anim == GrowFromEdge and "edge" not in kwargs.keys():
         args = [DOWN, *args]
      super().__init__(*[
          anim(key, *args, **kwargs)
          for key in keyboard
        ],
        lag_ratio=lag_ratio,
      )

  def _setup_scene(self, scene) -> None:
      scene.add_foreground_mobjects(*self.keyboard.black_keys)
      super()._setup_scene(scene)

  def clean_up_from_scene(self, scene: Scene) -> None:
      scene.remove_foreground_mobjects(*self.keyboard.black_keys)
      super().clean_up_from_scene(scene)



