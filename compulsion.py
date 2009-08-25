#
# compulsion.py provides a Url class with a single function to_5bit().
# to_5bit() exploits low entropy in URL strings in order to represent
# the Url using less bits as a sequence of 5-bit characters.
#

class Url(str):
    """Augmented string with some useful functions for encoding URLs as compressed integer streams."""
    
    def to_5bit(self):
        "The 5 bit encoding scheme uses four character maps and special characters to select between them. URLs are expected to mostly incorporate characters from the first map, compressing most characters by three bits and common sequences by more"
        return encode(self)

# Constants for 5-bit "special characters". The preprocessor uses these to pad
# a 7-bit string before the mapper converts the string to a 5-bit sequence.
# This works because all of the ordinals from 0 to 31 are unprintable and thus won't
# appear in URLs.    
SWITCH_MAP = SWITCH_TO_MAP_ONE = SWITCH_TO_MAP_TWO = "\x00"
SHIFT_MAP = NEXT_CHAR_MAP_ONE = NEXT_CHAR_MAP_TWO = "\x01"
NEXT_CHAR_MAP_THREE = "\x02"
NEXT_CHAR_MAP_RARE_AND_SHORT = "\x1F"

# Constants for 5-bit shorthands, mapped by the preprocessor to the ASCII extended range
HTTP_COLON_SLASH_SLASH = "\x80"
DOT_HTML = "\x81"
DOT_COM = "\x82"
DOT_ORG = "\x83"
INDEX = "\x84"
WWW_DOT = "\x85"
HTTP_COLON_SLASH_SLASH_WWW_DOT = "\x86"

shorthands = {
    "http://www.": ord(HTTP_COLON_SLASH_SLASH_WWW_DOT),
    "http://": ord(HTTP_COLON_SLASH_SLASH),
    "www.": ord(WWW_DOT),
    ".com/": ord(DOT_COM),
    ".org/": ord(DOT_ORG),
    "index": ord(INDEX),
    ".html": ord(DOT_HTML),
}

shorthandable_strings = shorthands.keys()

def chars_to_ords(l):
    """Converts all characters in a list to their ordinal values."""
    return [ord(x) for x in l]
    
five_bit_map_one = chars_to_ords([
    SWITCH_TO_MAP_TWO, NEXT_CHAR_MAP_TWO, NEXT_CHAR_MAP_THREE, '=', '/', '_', '+', '&',
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
    'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
    'q', 'r', 's', 't', 'u', 'v', 'w', 'y', 
])

five_bit_map_two = chars_to_ords([
    SWITCH_TO_MAP_ONE, NEXT_CHAR_MAP_ONE, NEXT_CHAR_MAP_THREE, 'x', 'z', '0', '1', '2',
    '3', '4', '5', '6', '7', '8', '9', '%',
    'A', 'B', 'C', 'D', 'E', 'F', 'H', 'I', 
    'L', 'M', 'N', 'O', 'R', 'S', 'T', 'U',
])

five_bit_map_three = chars_to_ords([
    'G', 'J', 'K', 'P', 'Q', 'V', 'W', 'X',
    'Y', 'Z', '!', '"', '#', '$', '(', ')',
    '?', ',', ';', '<', ':', '>', '@', '[', 
    '\\',']', '^', '.', '-', '~', '|', NEXT_CHAR_MAP_RARE_AND_SHORT, 
])

five_bit_map_rare_and_short = chars_to_ords([
    ' ', '^', '`', '{', '}', "'", '*', HTTP_COLON_SLASH_SLASH, 
    DOT_HTML, DOT_COM, DOT_ORG, INDEX, WWW_DOT, HTTP_COLON_SLASH_SLASH_WWW_DOT
    # TODO: Space for more shorthands here.
])

def encode(inp):
    """Encodes a 7-bit string by adding special chars to indicate where the map must be switched or shifted, mapping to 5-bit numbers and encoding shorthands."""
    out = []
    
    active_map = five_bit_map_one
    inactive_map = five_bit_map_two
    
    while len(inp) > 0:
        # First test to see if the next characters in the string can be shorthanded.
        shorthanded = False
        for sk in shorthands.keys():
            if inp.startswith(sk):
                # Add the shorthand flags and character to the output stream.
                out.append(ord(NEXT_CHAR_MAP_THREE))
                out.append(ord(NEXT_CHAR_MAP_RARE_AND_SHORT))
                out.append(five_bit_map_rare_and_short.index(shorthands[sk]))
                # Remove the shorthanded characters from the input stream.
                inp = inp[len(sk):]
                shorthanded = True

        if shorthanded:
            continue
                
        # Determine which map the first character exists in.
        char = ord(inp[0])
        
        if char in active_map:
            # Character is in the active map, and can be written through.
            out.append(active_map.index(char))
            inp = inp[1:]
            continue
        
        if char in five_bit_map_rare_and_short:
            # Character is rare. Pad with the map three and rare and short flags.
            out.append(ord(NEXT_CHAR_MAP_THREE))
            out.append(ord(NEXT_CHAR_MAP_RARE_AND_SHORT))
            out.append(five_bit_map_rare_and_short.index(char))
            inp = inp[1:]
            continue
            
        if char in five_bit_map_three:
            # Character is in map three. Pad with map three flag.
            out.append(ord(NEXT_CHAR_MAP_THREE))
            out.append(five_bit_map_three.index(char))
            inp = inp[1:]
            continue
        
        if char in inactive_map:
            # Check the following character to see whether it would be more efficient
            # to shift or switch.
            if (len(inp) > 1) and ord(inp[1]) in inactive_map:
                # The next char is also in the inactive map, so switch maps.
                active_map, inactive_map = inactive_map, active_map
                out.append(ord(SWITCH_MAP))
                out.append(active_map.index(char))
                inp = inp[1:]
            else:
                # The next character either doesn't exist, or is in the existing map - 
                # so just temporarily shift map for this character.
                out.append(ord(SHIFT_MAP))
                out.append(inactive_map.index(char))
                inp = inp[1:]
            continue
                
        else:
            raise Exception("Preprocessing failed: couldn't encode character '%s'" 
                % char)
    
    return out