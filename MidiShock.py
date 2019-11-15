import rtmidi
from inputs import *
from copy import deepcopy
from tkinter import *
import threading

root = Tk()

header = Label(root, text="M I D I S H O C K", bg='#000000', fg='#ffffff', font=('Arial', '16')).pack(fill=X)
rootNote = 55


def set_key_c():
    global rootNote
    rootNote = 60


def set_key_cs():
    global rootNote
    rootNote = 61


def set_key_d():
    global rootNote
    rootNote = 62


def set_key_ds():
    global rootNote
    rootNote = 63


def set_key_e():
    global rootNote
    rootNote = 64


def set_key_f():
    global rootNote
    rootNote = 53


def set_key_fs():
    global rootNote
    rootNote = 54


def set_key_g():
    global rootNote
    rootNote = 55


def set_key_gs():
    global rootNote
    rootNote = 56


def set_key_a():
    global rootNote
    rootNote = 57


def set_key_as():
    global rootNote
    rootNote = 58


def set_key_b():
    global rootNote
    rootNote = 59
    print(rootNote)


rightFrame = Frame(root, width=16)
inversionSliderFrame = Frame(rightFrame)
velocitySliderFrame = Frame(rightFrame)
inversionLabel = Label(inversionSliderFrame, text='Inversion Range', font=('Arial', '14')).pack(fill=X)
inversionScale = Scale(inversionSliderFrame, from_=1, to=12, orient=HORIZONTAL)
inversionScale.pack()
velocityLabel = Label(velocitySliderFrame, text='Velocity', font=('Arial', '14')).pack(fill=X)
velocityScale = Scale(velocitySliderFrame, from_=0, to=127, orient=HORIZONTAL)
velocityScale.pack()
inversionSliderFrame.pack(fill=X, padx=20, pady=20)
velocitySliderFrame.pack(fill=X, padx=20, pady=20)

keySignature = Frame(rightFrame)
keySigLabel = Label(keySignature, text='Root Key', font=('Arial', '14')).pack(fill=X)

keyC = Radiobutton(keySignature, text='C', value=1, variable=1, command=set_key_c).pack()
keyCS = Radiobutton(keySignature, text='C#', value=2, variable=1, command=set_key_cs).pack()
keyD = Radiobutton(keySignature, text='D', value=3, variable=1, command=set_key_d).pack()
keyDS = Radiobutton(keySignature, text='D#', value=4, variable=1, command=set_key_ds).pack()
keyE = Radiobutton(keySignature, text='E', value=5, variable=1, command=set_key_e).pack()
keyF = Radiobutton(keySignature, text='F', value=6, variable=1, command=set_key_f).pack()
keyFS = Radiobutton(keySignature, text='F#', value=7, variable=1, command=set_key_fs).pack()
keyG = Radiobutton(keySignature, text='G', value=8, variable=1, command=set_key_g).pack()
keyGS = Radiobutton(keySignature, text='G#', value=9, variable=1, command=set_key_gs).pack()
keyA = Radiobutton(keySignature, text='A', value=10, variable=1, command=set_key_a).pack()
keyAS = Radiobutton(keySignature, text='A#', value=11, variable=1, command=set_key_as).pack()
keyB = Radiobutton(keySignature, text='B', value=12, variable=1, command=set_key_b).pack()

keySignature.pack(fill=X, padx=20, pady=20)
rightFrame.pack(side=LEFT)

chordNameVar = StringVar()
chordText = Label(root, textvariable=chordNameVar, font=('Arial', '40'), bg='#000000', fg='#ffffff', width=18, height=9).pack( padx=20, pady=20)
chordNameVar.set('HELLO')

midiOut = rtmidi.MidiOut()
availablePorts = midiOut.get_ports()

velocity = 112
inversionRange = 4
BASE = [0, 2, 4, 5, 7, 9, 11]
MINOR = [0, 2, 3, 5, 7, 8, 10]
MAJOR = [1, 2, 4, 6, 8, 9, 11]
NOTE_NAMES = ['C', 'C\u266f', 'D', 'D\u266f', 'E', 'F', 'F\u266f', 'G', 'G\u266f', 'A', 'A\u266f', 'B']
chordName = ''

nState = 0
sState = 0
wState = 0
eState = 0
hxState = 0
hyState = 0
trState = 0
tlState = 0
zlState = 0
zrState = 0
minorMode = False
majorMode = False
dominantMode = False
lydianMode = False
chordIsOn = False
lastChord = {0, 0, 0, 0}
lastBass = 0
lastNine = 0
lastChordDeg = 0
inversion = 0
leftMode = False


if availablePorts:
    midiOut.open_port(1)
    print(midiOut.get_port_name(1))
else:
    midiOut.open_virtual_port("My virtual output")


for device in devices.gamepads:
    print(device)


def note_on(note, vel):
     midiOut.send_message([0x90, note, vel])


def note_off(note):
    midiOut.send_message([0x80, note, 0])


def change_inversion(new_inversion, vel):
    global inversion
    global lastNine
    global lastChord
    full_chord = deepcopy(lastChord)
    if zrState == 1:
        full_chord.add(lastNine)
    if new_inversion > inversion:
        while inversion != new_inversion:
            min_note = min(full_chord)
            note_off(min_note)
            note_on(min_note + 12, vel)
            full_chord.remove(min_note)
            full_chord.add(min_note + 12)
            if lastNine == min_note and zrState == 1:
                lastNine += 12
            else:
                lastChord.remove(min_note)
                lastChord.add(min_note + 12)
            inversion += 1
            print(inversion)
    elif new_inversion < inversion:
        while inversion != new_inversion:
            max_note = max(full_chord)
            note_off(max_note)
            note_on(max_note - 12, vel)
            full_chord.remove(max_note)
            full_chord.add(max_note - 12)
            if lastNine == max_note and zrState == 1:
                lastNine -= 12
            else:
                lastChord.remove(max_note)
                lastChord.add(max_note - 12)
            inversion -= 1
            print(inversion)


def regular_chord_on(scale, deg, vel):
    global lastBass
    global lastNine
    global lastChord
    global inversion
    global chordName
    if zlState == 1:
        note_off(lastBass)
        note_on(rootNote + scale[deg] - 12, velocity)
        lastBass = rootNote + scale[deg] - 12
    if inversion != 0:
        full_chord = set()
        num_notes = 4
        if zrState == 1:
            note_off(lastNine)
            num_notes += 1
            note_on(rootNote + scale[(deg + 8) % 7] + 12 + 12*math.modf(inversion/num_notes)[1], vel)
        for x in range(0, 4):
            full_chord.add(rootNote + scale[(deg + 2*x) % 7])
        lastChord = set()
        for x in range(num_notes-4, num_notes):
            note = max(full_chord)+12*math.modf((inversion + x)/num_notes)[1]
            note_on(note, vel)
            lastChord.add(note)
            full_chord.remove(max(full_chord))
        lastNine = rootNote + scale[(deg + 8) % 7] + 12 + 12 * math.modf(inversion / num_notes)[1]
    else:
        for x in range(0, 4):
            note_on(rootNote + scale[(deg + 2*x) % 7], vel)
        if zrState == 1:
            note_off(lastNine)
            note_on(rootNote + scale[(deg + 8) % 7] + 12, velocity)
        lastChord = {rootNote + scale[deg], rootNote + scale[(deg + 2) % 7], rootNote + scale[(deg + 4) % 7],
                     rootNote + scale[(deg + 6) % 7]}
        lastNine = rootNote + scale[(deg + 8) % 7] + 12


def dominant_chord_on(scale, deg, vel, majorDeg):
    global lastBass
    global lastNine
    global lastChord
    global inversion
    num_notes = 4
    if deg == majorDeg or deg == (majorDeg + 3) % 7 or deg == (majorDeg + 4) % 7:
        if zrState == 1:
            note_off(lastNine)
            num_notes += 1
            note_on(rootNote + scale[deg] + 9 + 12*math.modf(inversion/5)[1], vel)
        lastNine = rootNote + scale[deg] + 9 + 12*math.modf(inversion/5)[1]
    else:
        if zrState == 1:
            note_off(lastNine)
            note_on(rootNote + scale[deg] + 8 + 12*math.modf(inversion/5)[1], vel)
            num_notes += 1
        lastNine = rootNote + scale[deg] + 8 + 12*math.modf(inversion/5)[1]
    if zlState == 1:
        note_off(lastBass)
        note_on(rootNote + scale[deg] + 7 - 24, vel)
        lastBass = rootNote + scale[deg] + 7 - 24
    note_on(rootNote + scale[deg] - 5 + 12*math.modf((inversion + (num_notes - 1))/num_notes)[1], vel)
    note_on(rootNote + scale[deg] - 1 + 12*math.modf((inversion + (num_notes - 2))/num_notes)[1], vel)
    note_on(rootNote + scale[deg] + 2 + 12*math.modf((inversion + (num_notes - 3))/num_notes)[1], vel)
    note_on(rootNote + scale[deg] + 5 + 12*math.modf((inversion + (num_notes - 4))/num_notes)[1], vel)
    lastChord = {rootNote + scale[deg] - 5 + 12*math.modf((inversion + (num_notes - 1))/num_notes)[1],
                 rootNote + scale[deg] - 1 + 12*math.modf((inversion + (num_notes - 2))/num_notes)[1],
                 rootNote + scale[deg] + 2 + 12*math.modf((inversion + (num_notes - 3))/num_notes)[1],
                 rootNote + scale[deg] + 5 + 12*math.modf((inversion + (num_notes - 4))/num_notes)[1]}


def lydian_chord_on(scale, deg, vel):
    global lastBass
    global lastNine
    global lastChord
    num_notes = 4
    if zlState == 1:
        note_off(lastBass)
        note_on(rootNote + scale[deg] - 11, vel)
        lastBass = rootNote + scale[deg] - 11
    if zrState == 1:
        note_off(lastNine)
        num_notes += 1
        note_on(rootNote + scale[deg] + 17 + 12*math.modf(inversion/5)[1], vel)
    note_on(rootNote + scale[deg] + 1 + 12 * math.modf((inversion + 4) / 5)[1], vel)
    note_on(rootNote + scale[deg] + 5 + 12 * math.modf((inversion + 3) / 5)[1], vel)
    note_on(rootNote + scale[deg] + 7 + 12 * math.modf((inversion + 2) / 5)[1], vel)
    note_on(rootNote + scale[deg] + 12 + 12 * math.modf((inversion + 1) / 5)[1], vel)
    lastChord = {rootNote + scale[deg] + 1 + 12 * math.modf((inversion + (num_notes - 1)) / num_notes)[1],
                 rootNote + scale[deg] + 5 + 12 * math.modf((inversion + (num_notes - 2)) / num_notes)[1],
                 rootNote + scale[deg] + 7 + 12 * math.modf((inversion + (num_notes - 3)) / num_notes)[1],
                 rootNote + scale[deg] + 12 + 12 * math.modf((inversion + (num_notes - 4)) / num_notes)[1]}
    lastNine = rootNote + scale[deg] + 17 + 12 * math.modf(inversion / 5)[1]


def chord_on(deg, vel):
    global inversion
    #inversion = 0
    global chordIsOn
    if chordIsOn:
        chord_off()
    global lastChord
    global lastChordDeg
    global lastBass
    global lastNine
    global chordName
    offset = 0
    if dominantMode:
        if majorMode:
            dominant_chord_on(MAJOR, deg, vel, 5)
            offset = -2
            chordName = NOTE_NAMES[(rootNote + MAJOR[deg] + 7) % 12]
        elif minorMode:
            dominant_chord_on(MINOR, deg, vel, 2)
            chordName = NOTE_NAMES[(rootNote + MINOR[deg] + 7) % 12]
            offset = 2
        else:
            dominant_chord_on(BASE, deg, vel, 0)
            chordName = NOTE_NAMES[(rootNote + BASE[deg] + 7) % 12]
        if zrState == 1:
            if deg == ((0 + offset) % 7) or deg == ((3 + offset) % 7) or deg == ((4 + offset) % 7):
                chordName += '9'
            else:
                chordName += '7\u266d9'
        else:
            chordName += '7'
    elif lydianMode:
        if majorMode:
            lydian_chord_on(MAJOR, deg, vel)
            chordName = NOTE_NAMES[(rootNote + MAJOR[deg] + 1) % 12]
        elif minorMode:
            lydian_chord_on(MINOR, deg, vel)
            chordName = NOTE_NAMES[(rootNote + MINOR[deg] + 1) % 12]
        else:
            lydian_chord_on(BASE, deg, vel)
            chordName = NOTE_NAMES[(rootNote + BASE[deg] + 1) % 12]
        if zrState == 1:
            chordName += 'maj9\u266d5'
        else:
            chordName += 'maj7\u266d5'
    else:
        if majorMode:
            regular_chord_on(MAJOR, deg, vel)
            offset = -2
            chordName = NOTE_NAMES[(rootNote + MAJOR[deg]) % 12]
        elif minorMode:
            regular_chord_on(MINOR, deg, vel)
            offset = 2
            chordName = NOTE_NAMES[(rootNote + MINOR[deg]) % 12]
        else:
            regular_chord_on(BASE, deg, vel)
            chordName = NOTE_NAMES[(rootNote + BASE[deg]) % 12]
        if zrState == 1:
            if deg == (offset % 7) or deg == ((3 + offset) % 7):
                chordName += 'maj9'
            elif deg == ((1 + offset) % 7) or deg == ((5 + offset) % 7):
                chordName += 'm9'
            elif deg == ((2 + offset) % 7):
                chordName += 'm7\u266d9'
            elif deg == ((4 + offset) % 7):
                chordName += '9'
            else:
                chordName += 'm7\u266d5\u266d9'
        else:
            if deg == (offset % 7) or deg == ((3 + offset) % 7):
                chordName += 'maj7'
            elif deg == ((1 + offset) % 7) or deg == ((5 + offset) % 7) or deg == ((2 + offset) % 7):
                chordName += 'm7'
            elif deg == ((4 + offset) % 7):
                chordName += '7'
            else:
                chordName += 'm7\u266d5'
    chordIsOn = True
    lastChordDeg = deg
    chordNameVar.set(chordName)


def chord_off():
    global chordIsOn
    global lastChord
    global lastBass
    global lastNine
    note_off(lastNine)
    note_off(lastBass)
    for note in lastChord:
        note_off(note)
    chordIsOn = False


def get_ds():

    global velocity
    global inversionRange
    global nState
    global sState
    global wState
    global eState
    global hxState
    global hyState
    global trState
    global tlState
    global lastChord
    global velocity
    global inversionRange
    global BASE
    global MINOR
    global MAJOR
    global zlState
    global zrState
    global minorMode
    global majorMode
    global dominantMode
    global lydianMode
    global chordIsOn
    global lastBass
    global lastNine
    global lastChordDeg
    global inversion
    global leftMode

    while 1:
        inversionRange = inversionScale.get()
        velocity = velocityScale.get()
        events = get_gamepad()
        for event in events:
            if event.code == 'BTN_SOUTH':
                if event.state == 1:
                    chord_on(0, velocity)
                    sState = 1
                elif lastChordDeg == 0:
                    chord_off()
                    sState = 0
            elif event.code == 'BTN_WEST':
                if event.state == 1:
                    chord_on(1, velocity)
                    wState = 1
                elif lastChordDeg == 1:
                    chord_off()
                    wState = 0
            elif event.code == 'BTN_NORTH':
                if event.state == 1:
                    chord_on(2, velocity)
                    nState = 1
                elif lastChordDeg == 2:
                    chord_off()
                    nState = 0
            elif event.code == 'BTN_EAST':
                if event.state == 1:
                    chord_on(3, velocity)
                    eState = 1
                elif lastChordDeg == 3:
                    chord_off()
                    eState = 0
            elif event.code == 'ABS_HAT0Y':
                if event.state == 1:
                    chord_on(4, velocity)
                    hyState = 1
                elif event.state == -1:
                    chord_on(6, velocity)
                    hyState = -1
                elif lastChordDeg == 4 or lastChordDeg == 6:
                    chord_off()
                    hyState = 0
            elif event.code == 'ABS_HAT0X':
                if event.state == -1:
                    chord_on(5, velocity)
                    hxState = -1
                elif event.state == 0 and lastChordDeg == 5:
                    chord_off()
                    hxState = 0
            elif event.code == 'BTN_TR':
                if event.state == 1:
                    if minorMode:
                        minorMode = False
                    majorMode = True
                    if chordIsOn:
                        chord_off()
                        chord_on(lastChordDeg, velocity)
                    trState = 1
                else:
                    majorMode = False
                    if tlState == 1:
                        minorMode = True
                    if chordIsOn:
                        chord_off()
                        chord_on(lastChordDeg, velocity)
                    trState = 0
            elif event.code == 'BTN_TL':
                if event.state == 1:
                    if majorMode:
                        majorMode = False
                    minorMode = True
                    if chordIsOn:
                        chord_off()
                        chord_on(lastChordDeg, velocity)
                    tlState = 1
                else:
                    minorMode = False
                    if trState == 1:
                        majorMode = True
                    if chordIsOn:
                        chord_off()
                        chord_on(lastChordDeg, velocity)
                    tlState = 0
            elif event.code == 'ABS_Z':
                if event.state > 20 and zlState == 0:
                    if dominantMode:
                        if majorMode:
                            note_on(rootNote + MAJOR[lastChordDeg] + 7 - 24, velocity)
                            lastBass = rootNote + MAJOR[lastChordDeg]
                        elif minorMode:
                            note_on(rootNote + MINOR[lastChordDeg] + 7 - 24, velocity)
                            lastBass = rootNote + MINOR[lastChordDeg] + 7 - 24
                        else:
                            note_on(rootNote + BASE[lastChordDeg] + 7 - 24, velocity)
                            lastBass = rootNote + BASE[lastChordDeg] + 7 - 24
                    elif lydianMode:
                        if majorMode:
                            note_on(rootNote + MAJOR[lastChordDeg] - 11, velocity)
                            lastBass = rootNote + MAJOR[lastChordDeg] - 11
                        elif minorMode:
                            note_on(rootNote + MINOR[lastChordDeg] - 11, velocity)
                            lastBass = rootNote + MINOR[lastChordDeg] - 11
                        else:
                            note_on(rootNote + BASE[lastChordDeg] - 11, velocity)
                            lastBass = rootNote + BASE[lastChordDeg] - 11
                    else:
                        if majorMode:
                            note_on(rootNote + MAJOR[lastChordDeg] - 12, velocity)
                            lastBass = rootNote + MAJOR[lastChordDeg] - 12
                        elif minorMode:
                            note_on(rootNote + MINOR[lastChordDeg] - 12, velocity)
                            lastBass = rootNote + MINOR[lastChordDeg] - 12
                        else:
                            note_on(rootNote + BASE[lastChordDeg] - 12, velocity)
                            lastBass = rootNote + BASE[lastChordDeg] - 12
                    zlState = 1
                elif event.state <= 20 and zlState == 1:
                    note_off(lastBass)
                    zlState = 0
            elif event.code == 'ABS_RZ':
                if event.state > 20 and zrState == 0:
                    if dominantMode:
                        if majorMode:
                            if lastChordDeg == 5 or lastChordDeg == 1 or lastChordDeg == 2:
                                note_on(rootNote + MAJOR[lastChordDeg] + 9 + 12*math.modf(inversion/5)[1], velocity)
                                lastNine = rootNote + MAJOR[lastChordDeg] + 9 + 12*math.modf(inversion/5)[1]
                            else:
                                note_on(rootNote + MAJOR[lastChordDeg] + 8 + 12*math.modf(inversion/5)[1], velocity)
                                lastNine = rootNote + MAJOR[lastChordDeg] + 8 + 12*math.modf(inversion/5)[1]
                        elif minorMode:
                            if lastChordDeg == 2 or lastChordDeg == 5 or lastChordDeg == 6:
                                note_on(rootNote + MINOR[lastChordDeg] + 9 + 12*math.modf(inversion/5)[1], velocity)
                                lastNine = rootNote + MINOR[lastChordDeg] + 9 + 12*math.modf(inversion/5)[1]
                            else:
                                note_on(rootNote + MINOR[lastChordDeg] + 8 + 12*math.modf(inversion/5)[1], velocity)
                                lastNine = rootNote + MINOR[lastChordDeg] + 8 + 12*math.modf(inversion/5)[1]
                        else:
                            if lastChordDeg == 0 or lastChordDeg == 3 or lastChordDeg == 4:
                                note_on(rootNote + BASE[lastChordDeg] + 9 + 12*math.modf(inversion/5)[1], velocity)
                                lastNine = rootNote + BASE[lastChordDeg] + 9 + 12*math.modf(inversion/5)[1]
                            else:
                                note_on(rootNote + MAJOR[lastChordDeg] + 8 + 12*math.modf(inversion/5)[1], velocity)
                                lastNine = rootNote + MAJOR[lastChordDeg] + 8 + 12*math.modf(inversion/5)[1]
                    elif lydianMode:
                        if majorMode:
                            note_on(rootNote + MAJOR[lastChordDeg] + 17, velocity)
                            lastNine = rootNote + MAJOR[lastChordDeg] + 17
                        elif minorMode:
                            note_on(rootNote + MINOR[lastChordDeg] + 17 + 12*math.modf(inversion/5)[1], velocity)
                            lastNine = rootNote + MINOR[lastChordDeg] + 17 + 12*math.modf(inversion/5)[1]
                        else:
                            note_on(rootNote + BASE[lastChordDeg] + 17 + 12*math.modf(inversion/5)[1], velocity)
                            lastNine = rootNote + BASE[lastChordDeg] + 17 + 12*math.modf(inversion/5)[1]
                    else:
                        if majorMode:
                            note_on(rootNote + MAJOR[(lastChordDeg + 8) % 7] + 12 + 12*math.modf(inversion/5)[1], velocity)
                            lastNine = rootNote + MAJOR[(lastChordDeg + 8) % 7] + 12 + 12*math.modf(inversion/5)[1]
                        elif minorMode:
                            note_on(rootNote + MINOR[(lastChordDeg + 8) % 7] + 12 + 12*math.modf(inversion/5)[1], velocity)
                            lastNine = rootNote + MINOR[(lastChordDeg + 8) % 7] + 12 + 12*math.modf(inversion/5)[1]
                        else:
                            note_on(rootNote + BASE[(lastChordDeg + 8) % 7] + 12 + 12*math.modf(inversion/5)[1], velocity)
                            lastNine = rootNote + BASE[(lastChordDeg + 8) % 7] + 12 + 12*math.modf(inversion/5)[1]
                    zrState = 1
                elif event.state <= 20 and zrState == 1:
                    note_off(lastNine)
                    zrState = 0
            elif event.code == 'BTN_START' or event.code == 'BTN_SELECT':
                if event.state == 1:
                    dominantMode = True
                else:
                    dominantMode = False
            elif event.code == 'ABS_Y' and (leftMode or abs(event.state) > (32767 // inversionRange)) and math.modf(event.state / (32767 // inversionRange))[1] != inversion:
                leftMode = True
                if chordIsOn:
                    change_inversion(math.modf(event.state / (32767 // inversionRange))[1], velocity)
                else:
                    inversion = math.modf(event.state / (32767 // inversionRange))[1]
            elif event.code == 'ABS_RY' and ((not leftMode) or abs(event.state) > (32767 // inversionRange)) and math.modf(event.state / (32767 // inversionRange))[1] != inversion:
                leftMode = False
                if chordIsOn:
                    change_inversion(math.modf(event.state / (32767 // inversionRange))[1], velocity)
                else:
                    inversion = math.modf(event.state / (32767 // inversionRange))[1]
            elif event.code == 'BTN_THUMBR' or event.code == 'BTN_THUMBL':
                if event.state == 1:
                    lydianMode = True
                else:
                    lydianMode = False


t = threading.Thread(target=get_ds)
t.daemon = True
t.start()

root.mainloop()