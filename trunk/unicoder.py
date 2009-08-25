# Maps integers in base 40336 to unicode ideographs, syllables and radicals.

ranges = [
    ("Kangxi Radicals", 0x2F00, 0x2FD5),
    ("CJK Unified Ideographs Ext. A", 0x3400, 0x4DB5),
    ("CJK Unified Ideographs", 0x4E00, 0x9FB1), # 9FB2, 9FB3 no glyphs on a mac, otherwise goes up to 9FBB.
    ("Yi Syllables", 0xA000, 0xA48C),
    ("Hangul Syllables", 0xAC00, 0xD7A3),
    ("CJK Compatibility Ideographs", 0xF900, 0xFA20),
    # ("CJK Unified Ideographs Ext. B", 0x20000, 0x2A6DF), # Very sparse on a mac.
]

# Calculates offsets for use when mapping.
distances = [ (last-first+1, first) for (name, first, last) in ranges]

def unicodise(num):
    for (count, offset) in distances:
        if num < count:
            # This number can be mapped to this range.
            return offset + num
        else:
            # This number exceeds the current range, subtract and try the next.
            num -= count
            
    # If we fall through, there aren't enough graphs to represent this input number
    raise Exception("Input number greater than codomain size.")
    
