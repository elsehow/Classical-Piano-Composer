import glob
import pickle
from music21 import converter, instrument, note, chord

if __name__ == '__main__':
    """
    Save two pickle files: data/notes and data/durations.
    (NB. The sequence of these two files are aligned.)
    """
    notes = []
    durations = []

    for file in glob.glob("midi_songs/*.mid"):
        midi = converter.parse(file)

        print("Parsing %s" % file)

        notes_to_parse = None

        try: # file has instrument parts
            s2 = instrument.partitionByInstrument(midi)
            notes_to_parse = s2.parts[0].recurse()
        except: # file has notes in a flat structure
            notes_to_parse = midi.flat.notes

        def append_duration (el):
            dur = float(el.duration.quarterLength)
            durations.append(dur)

        for element in notes_to_parse:
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
