with open('A2/q2_ciphertext.txt', 'r') as file: 
    cipher_text = file.read()

cipher_plain_map = {
    'a' : 'l',
    'b' : 'j',
    'c' : 'r',
    'd' : 'y',
    'e' : 'b',
    'f' : 'i',          
    'g' : 'e',
    'h' : 'h',
    'i' : 'g',
    'j' : 'd',
    'k' : 'm',
    'l' : 'a',
    'm' : 'q',
    'n' : 'u',
    'o' : 'v',
    'p' : 'n',
    'q' : 'q',
    'r' : 'x',
    's' : 's',
    't' : 'p',
    'u' : 'o',
    'v' : 'z',
    'w' : 'f',
    'x' : 'w',
    'y' : 'c',
    'z' : 'k'
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

def word_analysis(text, num_letters):
    two_letter_words = {}
    words = text.split()
    for word in words:
        if len(word) == num_letters and word.isalpha():
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
    with open('A2/q2_decrypted.txt', 'w') as file:
        file.write(decrypted_text)
    return decrypted_text

# check the freq in valid words.txt
with open('A2/wordlist.txt', 'r') as file:
    valid_words_text = file.read()

print("Valid word frequency analysis:\n")
frequency_analysis(valid_words_text)

print("\nCipher text frequency analysis:\n")
frequency_analysis(cipher_text)

# two_letter_word_analysis(cipher_text)
# print("\nValid word n-letter word analysis:\n")
# word_analysis(valid_words_text, 3)
# print("\nCipher text n-letter word analysis:\n")
# word_analysis(cipher_text, 3)

decrypted_text = decrypt(cipher_text, cipher_plain_map)

def check_decrypted_valid(decrypted_text, cipher_text):
    # check if the decrypted text has valid words
    # Build a mapping from word length -> set(valid words of that length)
    from string import punctuation
    valid_words_by_len = {}
    with open('A2/wordlist.txt', 'r') as file:
        for w in file.read().split():
            w_clean = w.lower().strip()
            if not w_clean:
                continue
            valid_words_by_len.setdefault(len(w_clean), set()).add(w_clean)

    results = []
    # Iterate over tokens in the decrypted text and collect candidate translations
    for raw in decrypted_text.split():
        # strip surrounding punctuation but keep the original raw token for output
        word = raw.strip(punctuation).lower()
        # If empty or non-alphabetic, record with empty candidate list
        if not word or not word.isalpha():
            results.append((raw, word, []))
            continue

        length = len(word)
        candidates = sorted(valid_words_by_len.get(length, set()))
        results.append((raw, word, candidates))

    # Align decrypted tokens with the original cipher tokens so we can
    # check consistency against the current `cipher_plain_map` and only keep
    # candidate words that are consistent and introduce at least one new
    # mapping (i.e. map an unmapped cipher letter to a plaintext letter).
    cipher_tokens = cipher_text.split()
    dec_tokens = decrypted_text.split()
    pairs = list(zip(cipher_tokens, dec_tokens))

    out_path = 'A2/q2_candidates.txt'
    skipped_exact = 0
    written_pairs = 0
    mismatches_only = 0

    # reverse mapping plain -> cipher for checking injective constraints
    plain_to_cipher = {v: k for k, v in cipher_plain_map.items() if v}

    def pattern(s: str) -> str:
        # normalize repeated-letter pattern, e.g. 'apple' -> '0.1.1.2.3'
        m = {}
        next_id = 0
        parts = []
        for ch in s:
            if ch not in m:
                m[ch] = str(next_id)
                next_id += 1
            parts.append(m[ch])
        return '.'.join(parts)

    with open(out_path, 'w') as out:
        out.write('raw_cipher_token\traw_dec_token\tcleaned_word\tcandidate\n')
        for (cipher_raw, dec_raw) in pairs:
            cleaned_cipher = cipher_raw.strip(punctuation).lower()
            cleaned_dec = dec_raw.strip(punctuation).lower()
            if not cleaned_dec or not cleaned_cipher:
                continue
            # only consider tokens with same length after stripping punctuation
            if len(cleaned_cipher) != len(cleaned_dec):
                continue

            candidates = valid_words_by_len.get(len(cleaned_dec), set())

            # compute cipher pattern once (used to filter potential candidates)
            cipher_pat = pattern(cleaned_cipher)

            # If there are no candidates of this length, record as a mismatch with no candidates
            if not candidates:
                out.write(f"{cipher_raw}\t{dec_raw}\t{cleaned_dec}\t<MISMATCH_NO_CANDIDATES>\n")
                mismatches_only += 1
                continue

            # If the cleaned decrypted token is not itself a valid word (mismatch)
            # collect potential candidates (pattern + mapping-consistent) and write them
            if cleaned_dec not in candidates:
                potential = []
                for cand in sorted(candidates):
                    if pattern(cand) != cipher_pat:
                        continue
                    # check basic consistency (don't require that it introduces new mappings)
                    consistent = True
                    for i, c_cipher in enumerate(cleaned_cipher):
                        c_cand = cand[i]
                        mapped = cipher_plain_map.get(c_cipher, '')
                        if mapped and mapped != c_cand:
                            consistent = False
                            break
                        # also ensure injective: if plaintext letter already maps to another cipher
                        if c_cand in plain_to_cipher and plain_to_cipher[c_cand] != c_cipher:
                            consistent = False
                            break
                    if consistent:
                        potential.append(cand)

                # write potential candidates (one line per candidate) so user can inspect
                if potential:
                    for cand in potential:
                        out.write(f"{cipher_raw}\t{dec_raw}\t{cleaned_dec}\t{cand}\n")
                else:
                    out.write(f"{cipher_raw}\t{dec_raw}\t{cleaned_dec}\t<MISMATCH_NO_POTENTIALS>\n")
                mismatches_only += 1

            # skip token entirely if cleaned_dec matches a candidate exactly
            if cleaned_dec in candidates:
                skipped_exact += 1
                continue

            # For monoalphabetic ciphers the equality pattern must match
            cipher_pat = pattern(cleaned_cipher)

            # For each candidate, check pattern, consistency with cipher_plain_map
            for cand in sorted(candidates):
                if len(cand) != len(cleaned_cipher):
                    continue

                # pattern must match (same repeated-letter positions)
                if pattern(cand) != cipher_pat:
                    continue

                consistent = True
                introduces_new = False

                for i, c_cipher in enumerate(cleaned_cipher):
                    c_cand = cand[i]
                    mapped = cipher_plain_map.get(c_cipher, '')
                    if mapped:
                        # existing mapping must match candidate letter
                        if mapped != c_cand:
                            consistent = False
                            break
                    else:
                        # if candidate letter is already assigned to a different
                        # cipher letter, that's a conflict
                        if c_cand in plain_to_cipher and plain_to_cipher[c_cand] != c_cipher:
                            consistent = False
                            break
                        introduces_new = True

                if not consistent:
                    continue

                # require that candidate introduces at least one new mapping
                if not introduces_new:
                    continue

                # candidate passes checks; write pair
                out.write(f"{cipher_raw}\t{dec_raw}\t{cleaned_dec}\t{cand}\n")
                written_pairs += 1

        out.write('\n')
        out.write(f"Summary: skipped_exact={skipped_exact}, written_pairs={written_pairs}, total_tokens={len(pairs)}\n")

    print(f"Wrote candidate pairs to {out_path} (skipped_exact={skipped_exact}, written_pairs={written_pairs})")

    return results



# check_decrypted_valid(decrypted_text, cipher_text)
print(decrypt("ytsy436s{rwueskizzwfklzkhgdsnpspffgwzwepg}", cipher_plain_map))
    