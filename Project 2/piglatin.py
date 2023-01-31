import argparse

# Vowels list
vowels = ["a","e","i","o","u"]

#
punctuation = [
    ',',
    '.',
    ';',
    '(',
    ')',
    '!',
    '?',
]

higher_punctuation = [
    "\'",
    "\"",
    "(",
    ")"
]

# Argument Parsing
parser = argparse.ArgumentParser()
parser.add_argument('--input')
parser.add_argument('--output')
args = parser.parse_args()

# Load input file as reader
infile = open(str(args.input), "r")
data = infile.readlines()

# Load output file as writer
outfile = open(str(args.output), 'w')

# Init output sentence
output_sentence = ""

def check_vowel(input_letter):
    '''
    Checks if input letter is a vowel or not
    '''
    for vowel in vowels:
        if input_letter == vowel:
                return True
    return False

def check_punctutation(input_letter):
    '''
    Checks if input letter is punctation char
    '''
    for punct in punctuation:
        if input_letter == punct:
            return True
    return False

def check_high_punct(input_word, front):
    for p in higher_punctuation:
        if input_word[0] == p and front:
            return True
        elif input_word[len(input_word) - 1] == p and not front:
            return True

    return False
for line in data:
    line = line[:-1]
    # Split sentence into words
    input_sentence = line.split(" ", -1)

    for input_word_orig in input_sentence:
        if len(input_word_orig) == 0:
            output_sentence = output_sentence + "\n\n"
            continue

        input_word = input_word_orig.lower()
        # Set suffix and prefix
        ending = ""
        suffix = "ay"
        prefix = ""
        beginning = ""

        # Check for vowel in every letter for current word
        i = 0
        if check_high_punct(input_word, True):
            input_word = input_word[1:]

        if check_high_punct(input_word, False):
            input_word = input_word[:-1]

        for input_letter in input_word:
            if not check_vowel(input_letter):
                i = i + 1
            else:
                break
        for input_letter in input_word:
            if input_word == "...":
                suffix = ""
                break
            if check_punctutation(input_letter):
                suffix = suffix + input_letter
                input_word = input_word.replace(input_letter, '')
                #i = i - 1
                continue
        # i = 0 when vowel is the first letter
        if check_high_punct(input_word_orig, True):
            beginning = input_word_orig[0] + beginning
        if check_high_punct(input_word_orig, False):
            ending = input_word_orig[len(input_word_orig) - 1] + ending
        if i == 0:
            prefix = input_word
            suffix = "w" + suffix
        # i = length of word when there are no vowels in word
        elif i == len(input_word):
            prefix = input_word[-1]
            suffix = input_word[:-1] + suffix
        else:
        # i is neither when there is a vowel in the word somewhere other than front
            prefix = input_word[i:]
            suffix = input_word[:i] + suffix

        if input_word_orig[0].isupper():
            if len(prefix) > 0:
                prefix = prefix[0].upper() + prefix[1:]
            elif len(suffix) > 0:
                suffix = suffix[0].upper() + suffix[1:]
        print(input_word_orig[len(input_word_orig) - 1])
        # append current new prefix and suffix to the output sentence
        output_sentence = output_sentence + beginning + prefix + suffix + ending + " "


# write to file and close
outfile.write(output_sentence)
outfile.flush()
outfile.close()
