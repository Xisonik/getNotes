
from music21 import converter, instrument, note, chord

def get_notes(file):
    notes = []
    # Получаем все ноты и аккорды из файла
    midi = converter.parse(file)
    parts = instrument.partitionByInstrument(midi)


    if parts:
        notes_to_parse = parts.parts[0].recurse()
    else:
        notes_to_parse = midi.flat.notes
    for element in notes_to_parse:
        if isinstance(element, note.Note):
            # Добавляем "ноты, типа ля2-до3"
            notes.append(str(element.pitch))

    print(notes)
    return notes

if __name__=="__main__":
    get_notes("/home/kit/Downloads/HW/gorodeckiy/audio/test.mid")