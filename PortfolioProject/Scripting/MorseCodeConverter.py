MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....',
    'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.',
    'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....', '6': '-....',
    '7': '--...', '8': '---..', '9': '----.',
    ' ': '/'
}

def text_to_morse(text):
    text = text.upper()
    morse_code = ' '.join(MORSE_CODE_DICT.get(char, '?') for char in text)
    return morse_code

if __name__ == "__main__":
    user_input = input("Enter text to convert to Morse code: ")
    morse_output = text_to_morse(user_input)
    print("Morse Code:", morse_output)
