with open('A2/q1_ciphertext.txt', 'r') as file: 
    cipher_text = file.read()

cipher_plain_map = {
    'a' : 'd',
    'b' : 'h',
    'c' : 'a',
    'd' : 'v',
    'e' : 'i',
    'f' : 'j',          
    'g' : 'q',
    'h' : 't',
    'i' : 'e',
    'j' : 'g',
    'k' : 'c',
    'l' : 'w',
    'm' : 'z',
    'n' : 'n',
    'o' : 'p',
    'p' : 'y',
    'q' : 'k',
    'r' : 'r',
    's' : 's',
    't' : 'b',
    'u' : 'o',
    'v' : 'f',
    'w' : 'u',
    'x' : 'x',
    'y' : 'l',
    'z' : 'm'
}


def frequency_analysis(text):
    frequency = {}
    for char in text:
        if char.isalpha():  # Consider only alphabetic characters
            char = char.lower()
            if char in frequency:
                frequency[char] += 1
            else:
                frequency[char] = 1
    print(sorted(frequency.items(), key=lambda item: item[1], reverse=True))

def two_letter_word_analysis(text):
    two_letter_words = {}
    words = text.split()
    for word in words:
        if len(word) == 2:
            word_lower = word.lower()
            if word_lower in two_letter_words:
                two_letter_words[word_lower] += 1
            else:
                two_letter_words[word_lower] = 1
    print(sorted(two_letter_words.items(), key=lambda item: item[1], reverse=True))


def decrypt(text, cipher_map):
    decrypted_text = ''
    for char in text:
        if char.lower() in cipher_map and cipher_map[char.lower()] != '':
            new_char = cipher_map[char.lower()]
            if char.isupper():
                new_char = new_char.upper()
            decrypted_text += new_char
        else:
            decrypted_text += char
    with open('A2/q1_decrypted.txt', 'w') as file:
        file.write(decrypted_text)

# frequency_analysis(cipher_text)
two_letter_word_analysis(cipher_text)
decrypt(cipher_text, cipher_plain_map)
# decrypt('kosk436s{cndmfcqosibpucixvwfwcpouetaijfgv}', cipher_plain_map)