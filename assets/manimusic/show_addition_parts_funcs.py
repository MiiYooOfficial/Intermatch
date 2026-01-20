def ShowAdditionLinesNote(note, anim, add_alteration=True, *args, **kwargs):
  anims = []
  if hasattr(note, "additional_lines"):
    anims.append(anim(note.additional_lines, *args, **kwargs))
  if note.alteration is not None and add_alteration:
    anims.append(anim(note.alteration, *args, **kwargs))
  return anims

def ShowAdditionLinesChord(chord, anim, *args, **kwargs):
  anims = []
  for note in chord:
    anims = [*anims, *ShowAdditionLinesNote(note, anim, *args, **kwargs)]
  return anims

def ShowAdditionLinesMultiChord(chords, anim, *args, **kwargs):
  anims = []
  for chord in chords:
    anims = [*anims, *ShowAdditionLinesChord(chord, anim, *args, **kwargs)]
  return anims

