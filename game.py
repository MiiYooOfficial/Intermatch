import pygame
import random
import time

# GLOBAL VARIABLES
DISPLAY = (900, 600)
QUALITY_BUTTONS_POS = (250, 660)
NUMBER_BUTTONS_POS = (740, 660)
PITCH_SCALING_FACTOR = 8.5
TIME = 60

# answer object
class Answer:
    def __init__(self, correct_answer, clef, note_1_scale, note_2_scale, note_1_accidental, note_2_accidental, interval_quality, interval_number, time_taken):
        self.correct_answer = correct_answer
        self.clef = clef
        self.note_1_scale = note_1_scale
        self.note_2_scale = note_2_scale
        self.note_1_accidental = note_1_accidental
        self.note_2_accidental = note_2_accidental
        self.interval_quality = interval_quality
        self.interval_number = interval_number
        self.compound = abs(note_1_scale - note_2_scale) > 7
        self.time_taken = time_taken

    def __repr__(self):
        return f"Answer(correct_answer={self.correct_answer}, clef={self.clef}, note_1_scale={self.note_1_scale}, note_2_scale={self.note_2_scale}, note_1_accidental={self.note_1_accidental}, note_2_accidental={self.note_2_accidental}, interval_quality={self.interval_quality}, interval_number={self.interval_number}, time_taken={self.time_taken})"

# helper functions
def generate_question(answers):
    clefs = []
    intervals = []
    for answer in answers:
        if answer.correct_answer == False or answer.time_taken > 5:
            clefs.append(answer.clef)
            intervals.append((answer.interval_quality, answer.interval_number, answer.compound))

    clef = random.choice(clefs) if clefs != [] else random.choice(["g", "c", "f"])
    note_1_scale, note_2_scale, first_note_accidental, second_note_accidental = build_interval(clef, random.choice(intervals)) if intervals != [] else (random.randint(-5, 5), random.randint(-5, 5), random.choice(["flat", "none", "sharp"]), random.choice(["flat", "none", "sharp"]))

    return clef, note_1_scale, note_2_scale, first_note_accidental, second_note_accidental

def build_interval(clef, interval):
    # generate base notes
    note_1_scale = random.randint(-5, 5)
    note_2_scale = note_1_scale + interval[1] - 1 if note_1_scale < 0 else note_1_scale - (interval[1] - 1)
    if interval[2]: # compound interval
        if note_1_scale < note_2_scale:
            if note_2_scale + 7 <= 5:
                note_2_scale += 7
            else:
                note_1_scale -= 7
        else:
            if note_2_scale - 7 >= -5:
                note_2_scale -= 7
            else:
                note_1_scale += 7

    interval_quality, interval_number = find_answer(clef, note_1_scale, note_2_scale, "none", "none")

    # add accidentals according to desired quality
    note_1_accidental, note_2_accidental = "none", "none"
    if interval_number in [1, 4, 5, 8]:
        interval_qualities = ["diminished", "perfect", "augmented"]
        delta_quality = interval_qualities.index(interval[0]) - interval_qualities.index(interval_quality)
        if delta_quality == -2:
            if note_1_scale < note_2_scale:
                note_1_accidental = "sharp"
                note_2_accidental = "flat"
            else:
                note_1_accidental = "flat"
                note_2_accidental = "sharp"
        elif delta_quality == -1:
            if note_1_scale < note_2_scale:
                note_1_accidental = "sharp"
            else:
                note_1_accidental = "flat"
        elif delta_quality == 1:
            if note_1_scale < note_2_scale:
                note_2_accidental = "sharp"
            else:
                note_2_accidental = "flat"
        elif delta_quality == 2:
            if note_1_scale < note_2_scale:
                note_1_accidental = "flat"
                note_2_accidental = "sharp"
            else:
                note_1_accidental = "sharp"
                note_2_accidental = "flat"
    else:
        interval_qualities = ["diminished", "minor", "major", "augmented"]
        delta_quality = interval_qualities.index(interval[0]) - interval_qualities.index(interval_quality)
        if delta_quality == -2:
            if note_1_scale < note_2_scale:
                note_1_accidental = "sharp"
                note_2_accidental = "flat"
            else:
                note_1_accidental = "flat"
                note_2_accidental = "sharp"
        elif delta_quality == -1:
            if note_1_scale < note_2_scale:
                note_2_accidental = "flat"
            else:
                note_2_accidental = "sharp"
        elif delta_quality == 1:
            if note_1_scale < note_2_scale:
                note_2_accidental = "sharp"
            else:
                note_2_accidental = "flat"
        elif delta_quality == 2:
            if note_1_scale < note_2_scale:
                note_1_accidental = "flat"
                note_2_accidental = "sharp"
            else:
                note_1_accidental = "sharp"
                note_2_accidental = "flat"

    return note_1_scale, note_2_scale, note_1_accidental, note_2_accidental
    
def generate_basic_major_scale(tonic):
    match tonic:
        case "C":
            return ["C", "D", "E", "F", "G", "A", "B"]
        case "D":
            return ["D", "E", "F#", "G", "A", "B", "C#"]
        case "E":
            return ["E", "F#", "G#", "A", "B", "C#", "D#"]
        case "F":
            return ["F", "G", "A", "Bb", "C", "D", "E"]
        case "G":
            return ["G", "A", "B", "C", "D", "E", "F#"]
        case "A":
            return ["A", "B", "C#", "D", "E", "F#", "G#"]
        case "B":
            return ["B", "C#", "D#", "E", "F#", "G#", "A#", "B"]

def find_answer(clef, note_1_scale, note_2_scale, note_1_accidental, note_2_accidental):
    base_notes = ["C", "D", "E", "F", "G", "A", "B"]
    
    # determine interval number
    middle_note_index = 0
    if clef == "g":
        middle_note_index = 6
    elif clef == "f":
        middle_note_index = 1
        
    note_1_index = (note_1_scale + middle_note_index) % 7 if note_1_scale + middle_note_index >= 0 else - (abs(note_1_scale + middle_note_index) % 7)
    note_2_index = (note_2_scale + middle_note_index) % 7 if note_2_scale + middle_note_index >= 0 else - (abs(note_2_scale + middle_note_index) % 7)

    bottom_note_index, top_note_index, bottom_note_accidental, top_note_accidental = (note_1_index, note_2_index, note_1_accidental, note_2_accidental) if note_1_scale <= note_2_scale else (note_2_index, note_1_index, note_2_accidental, note_1_accidental)
        
    print(base_notes[bottom_note_index] + bottom_note_accidental, base_notes[top_note_index] + top_note_accidental) # debugging
    if note_1_scale == note_2_scale:
        interval_number = 1
    else:
        if (note_1_scale < 0 and note_2_scale > 0) or (note_1_scale > 0 and note_2_scale < 0):
            interval_number = (abs(note_1_scale) + abs(note_2_scale)) % 7 + 1 if abs(note_1_scale) + abs(note_2_scale) != 7 else 8
        else:
            interval_number = abs(note_1_scale - note_2_scale) % 7 + 1
            
    # determine interval quality
    interval_quality = ""
    if interval_number == 1:
        if bottom_note_accidental == top_note_accidental:
            interval_quality = "perfect"
        elif (bottom_note_accidental == "none" and top_note_accidental == "sharp") or (bottom_note_accidental == "sharp" and top_note_accidental == "none") or (bottom_note_accidental == "flat" and top_note_accidental == "none") or (bottom_note_accidental == "none" and top_note_accidental == "flat"):
            interval_quality = "augmented"
    else:
        bare_bottom_note = base_notes[bottom_note_index]
        bare_top_note = base_notes[top_note_index]
        bare_major_scale = generate_basic_major_scale(bare_bottom_note)
        
        # process top note
        if bare_top_note in bare_major_scale:
            if interval_number in [4, 5, 8]:
                interval_quality = "perfect"
            else:
                interval_quality = "major"
        else:
            if bare_top_note + "#" in bare_major_scale:
                if interval_number in [4, 5, 8]:
                    interval_quality = "diminished"
                else:
                    interval_quality = "minor"
            elif bare_top_note + "b" in bare_major_scale and interval_number == 4:
                    interval_quality = "augmented"
                    
        if top_note_accidental == "sharp":
            if interval_number in [4, 5, 8]:
                if interval_quality == "perfect":
                    interval_quality = "augmented"
                elif interval_quality == "augmented":
                    interval_quality = ""
                elif interval_quality == "diminished":
                    interval_quality = "perfect"
            else:
                if interval_quality == "major":
                    interval_quality = "augmented"
                elif interval_quality == "minor":
                    interval_quality = "major"
                elif interval_quality == "augmented":
                    interval_quality = ""
                elif interval_quality == "diminished":
                    interval_quality = "minor"
        elif top_note_accidental == "flat":
            if interval_number in [4, 5, 8]:
                if interval_quality == "perfect":
                    interval_quality = "diminished"
                elif interval_quality == "augmented":
                    interval_quality = "perfect"
                elif interval_quality == "diminished":
                    interval_quality = ""
            else:
                if interval_quality == "major":
                    interval_quality = "minor"
                elif interval_quality == "minor":
                    interval_quality = "diminished"
                elif interval_quality == "augmented":
                    interval_quality = "major"
                elif interval_quality == "diminished":
                    interval_quality = ""
            
        # process bottom note
        if bottom_note_accidental == "sharp":
            if interval_number in [4, 5, 8]:
                if interval_quality == "perfect":
                    interval_quality = "diminished"
                elif interval_quality == "augmented":
                    interval_quality = "perfect"
                elif interval_quality == "diminished":
                    interval_quality = ""
            else:
                if interval_quality == "major":
                    interval_quality = "minor"
                elif interval_quality == "minor":
                    interval_quality = "diminished"
                elif interval_quality == "augmented":
                    interval_quality = "major"
                elif interval_quality == "diminished":
                    interval_quality = ""
        elif bottom_note_accidental == "flat":
            if interval_number in [4, 5, 8]:
                if interval_quality == "perfect":
                    interval_quality = "augmented"
                elif interval_quality == "augmented":
                    interval_quality = ""
                elif interval_quality == "diminished":
                    interval_quality = "perfect"
            else:
                if interval_quality == "major":
                    interval_quality = "augmented"
                elif interval_quality == "minor":
                    interval_quality = "major"
                elif interval_quality == "augmented":
                    interval_quality = ""
                elif interval_quality == "diminished":
                    interval_quality = "minor"
            
    if interval_quality != "":
        return (interval_quality, interval_number)
    return None

# main game loop
pygame.init()
screen = pygame.display.set_mode(DISPLAY)
clock = pygame.time.Clock()

counter, text = TIME, str(TIME).rjust(3)
pygame.time.set_timer(pygame.USEREVENT, 1000)
font = pygame.font.SysFont('Consolas', 30)

running = True
start_page, end_page = True, False
quality_selected, number_selected, new_quality_selection, new_number_selection, quality_answer, number_answer = True, True, True, True, "", ""
quality_buttons_image, number_buttons_image = pygame.image.load("buttons\\quality_buttons\\default.png"), pygame.image.load("buttons\\number_buttons\\default.png")
fade_alpha = 0
new_answers = []
old_answers = []
while running:
    screen.fill((0, 0, 0))

    while start_page:
        text = font.render("Click anywhere to begin", True, (255, 255, 255))
        screen.blit(text, text.get_rect(center = (DISPLAY[0] / 2, DISPLAY[1] / 2)))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                start_page = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                start_page = False

    while end_page:
        text = font.render("Click anywhere to play again", True, (255, 255, 255))
        screen.blit(text, text.get_rect(center = (DISPLAY[0] / 2, DISPLAY[1] / 2)))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                end_page = False
                for answer in new_answers:
                    print(answer) # debugging
            elif event.type == pygame.MOUSEBUTTONDOWN:
                end_page = False
                counter, text = TIME, str(TIME).rjust(3)
                quality_buttons_image, number_buttons_image = pygame.image.load("buttons\\quality_buttons\\default.png"), pygame.image.load("buttons\\number_buttons\\default.png")
                quality_selected, number_selected = True, True
                old_answers = new_answers
                new_answers = []

    if running:
        # populate buttons
        screen.blit(quality_buttons_image, quality_buttons_image.get_rect(midbottom=QUALITY_BUTTONS_POS))
        screen.blit(number_buttons_image, number_buttons_image.get_rect(midbottom=NUMBER_BUTTONS_POS))

        if quality_selected and number_selected: # generate new question
            fade_alpha = 0
            quality_selected, number_selected, quality_answer, number_answer = False, False, "", ""
            quality_buttons_image, number_buttons_image = pygame.image.load("buttons\\quality_buttons\\default.png"), pygame.image.load("buttons\\number_buttons\\default.png")
            question_position = (random.randint(110, 690), random.randint(100, 390))

            correct_answer = None
            while correct_answer is None:
                clef, note_1_scale, note_2_scale, first_note_accidental, second_note_accidental = generate_question(old_answers)
                correct_answer = find_answer(clef, note_1_scale, note_2_scale, first_note_accidental, second_note_accidental)

                if note_1_scale == note_2_scale and first_note_accidental != "none" and second_note_accidental == "none":
                    second_note_accidental = "natural"
            
            staff = pygame.image.load("clefs\\" + clef + "_clef.png").convert_alpha()
            first_note = pygame.image.load("first_notes\\" + clef + "_clef\\" + first_note_accidental  + "\\" + random.choice(["blue", "yellow", "red", "green"]) + ".png").convert_alpha()
            second_note = pygame.image.load("second_notes\\" + clef + "_clef\\" + second_note_accidental + "\\" + random.choice(["blue", "yellow", "red", "green"]) + ".png").convert_alpha()
            start_time = time.time()

        # display question
        question = pygame.Surface(DISPLAY, pygame.SRCALPHA)
        question.blit(staff, staff.get_rect(center=question_position))
        question.blit(first_note, first_note.get_rect(center = (question_position[0], question_position[1] + PITCH_SCALING_FACTOR * -note_1_scale)))
        question.blit(second_note, second_note.get_rect(center = (question_position[0], question_position[1] + PITCH_SCALING_FACTOR * -note_2_scale)))

        fade_alpha = min(fade_alpha + 10, 255)
        question.set_alpha(fade_alpha)
        screen.blit(question, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.USEREVENT:
                if counter > 0:
                    counter -= 1

            elif event.type == pygame.MOUSEBUTTONDOWN: # get user input
                mouse_pos = event.pos

                if 25 < mouse_pos[0] < 475 and 445 < mouse_pos[1] < 575: # player is selecting interval quality
                    if 25 < mouse_pos[0] < 160 and 445 < mouse_pos[1] < 505:
                        if quality_answer != "major":
                            quality_answer = "major"
                            new_quality_selection = True
                            quality_selected = True
                    elif 175 < mouse_pos[0] < 315 and 445 < mouse_pos[1] < 505:
                        if quality_answer != "minor":
                            quality_answer = "minor"
                            new_quality_selection = True
                            quality_selected = True
                    elif 325 < mouse_pos[0] < 475 and 445 < mouse_pos[1] < 505:
                        if quality_answer != "perfect":
                            quality_answer = "perfect"
                            new_quality_selection = True
                            quality_selected = True
                    elif 25 < mouse_pos[0] < 245 and 520 < mouse_pos[1] < 575:
                        if quality_answer != "diminished":
                            quality_answer = "diminished"
                            new_quality_selection = True
                            quality_selected = True
                    elif 260 < mouse_pos[0] < 475 and 520 < mouse_pos[1] < 575:
                        if quality_answer != "augmented":
                            quality_answer = "augmented"
                            new_quality_selection = True
                            quality_selected = True

                    if quality_selected and new_quality_selection:
                        new_quality_selection = False
                        quality_buttons_image = pygame.image.load("buttons\\quality_buttons\\" + quality_answer + "_highlighted.png")

                elif 600 < mouse_pos[0] < 875 and 445 < mouse_pos[1] < 575: # player is selecting interval number
                    if 605 < mouse_pos[0] < 665 and 445 < mouse_pos[1] < 505:
                        if number_answer != "1":
                            number_answer = "1"
                            new_number_selection = True
                            number_selected = True
                    elif 675 < mouse_pos[0] < 735 and 445 < mouse_pos[1] < 505:
                        if number_answer != "2":
                            number_answer = "2"
                            new_number_selection = True
                            number_selected = True
                    elif 745 < mouse_pos[0] < 805 and 445 < mouse_pos[1] < 505:
                        if number_answer != "3":
                            number_answer = "3"
                            new_number_selection = True
                            number_selected = True
                    elif 815 < mouse_pos[0] < 875 and 445 < mouse_pos[1] < 505:
                        if number_answer != "4":
                            number_answer = "4"
                            new_number_selection = True
                            number_selected = True
                    elif 605 < mouse_pos[0] < 665 and 520 < mouse_pos[1] < 575:
                        if number_answer != "5":
                            number_answer = "5"
                            new_number_selection = True
                            number_selected = True
                    elif 675 < mouse_pos[0] < 735 and 520 < mouse_pos[1] < 575:
                        if number_answer != "6":
                            number_answer = "6"
                            new_number_selection = True
                            number_selected = True
                    elif 745 < mouse_pos[0] < 805 and 520 < mouse_pos[1] < 575:
                        if number_answer != "7":
                            number_answer = "7"
                            new_number_selection = True
                            number_selected = True
                    elif 815 < mouse_pos[0] < 875 and 520 < mouse_pos[1] < 575:
                        if number_answer != "8":
                            number_answer = "8"
                            new_number_selection = True
                            number_selected = True

                    if number_selected and new_number_selection:
                        new_number_selection = False
                        number_buttons_image = pygame.image.load("buttons\\number_buttons\\" + number_answer + "_highlighted.png")

            screen.blit(quality_buttons_image, quality_buttons_image.get_rect(center=QUALITY_BUTTONS_POS))
            screen.blit(number_buttons_image, number_buttons_image.get_rect(center=NUMBER_BUTTONS_POS))

        # process answer
        if running and quality_answer and number_answer:
            end_time = time.time()
            time_taken = end_time - start_time

            if (quality_answer, int(number_answer)) == correct_answer:
                print("Correct!") # debugging
                new_answers.append(Answer(True, clef, note_1_scale, note_2_scale, first_note_accidental, second_note_accidental, correct_answer[0], correct_answer[1], time_taken))
            else:
                print("Incorrect! The correct answer was:", correct_answer[0], correct_answer[1]) # debugging
                new_answers.append(Answer(False, clef, note_1_scale, note_2_scale, first_note_accidental, second_note_accidental, correct_answer[0], correct_answer[1], time_taken))

        text = str(counter).rjust(3)
        if counter == 0:
            end_page = True

        screen.blit(font.render(text, True, (255, 255, 255)), (32, 48))
        clock.tick(60)
    
    pygame.display.flip()

pygame.quit()
