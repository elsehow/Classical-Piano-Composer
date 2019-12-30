import glob
import pickle
from music21 import converter, instrument, note, chord

def get_elements (midi):
    try: # file has instrument parts
        s2 = instrument.partitionByInstrument(midi)
        return s2.parts[0].recurse()
    except: # file has notes in a flat structure
        return midi.flat.notes

if __name__ == '__main__':
    """
    Save two pickle files: data/notes and data/durations.
    (NB. The sequence of these two files are aligned.)
    """
    notes = []
    durations = []

    def append_duration (el):
        dur = float(el.duration.quarterLength)
        durations.append(dur)

    for file in glob.glob("midi_songs/*.mid"):
        print("Parsing %s" % file)
        midi = converter.parse(file)
        elements = get_elements(midi)

        for element in elements:
            if isinstance(element, note.Note):
                notes.append(str(element.pitch))
                append_duration(element)
            elif isinstance(element, chord.Chord):
                chrd = '.'.join(str(n) for n in element.normalOrder)
                notes.append(chrd)
                append_duration(element)

    with open('data/notes', 'wb') as filepath:
        pickle.dump(notes, filepath)
    print('wrote data/notes')

    with open('data/durations', 'wb') as filepath:
        pickle.dump(durations, filepath)
    print('wrote data/durations')
