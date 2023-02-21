'''
    This library converts a piece of text into piglatin. This library includes:
        Basic Piglatin conversion
        Punctuation handling
        Uppercase handling
        Sentence Handling

    To use application, replace INPUT with input and OUTPUT with output:
        python piglatin.py --input $INPUT --output $OUTPUT

'''


import argparse

# Vowels list
vowels = ["a","e","i","o","u"]

# Cursed lower punctuation
punctuation = [
    ',',
    '.',
    ';',
    '(',
    ')',
    '!',
    '?',
]

# Cursed higher punctuation
higher_punctuation = [
    "\'",
    "\"",
    "(",
    ")"
]

def parse_arguments():
    # Argument Parsing
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', dest="input")
    parser.add_argument('--output', dest="output")
    args = parser.parse_args()
    return args

def load_in_file(args):
    # Load input file as reader
    infile = open(str(args.input), "r")
    return infile

def load_out_file(args):
    # Load output file as writer
    outfile = open(str(args.output), 'w')
    return outfile

def write_out_file(output_sentence, outfile):
    # write to file and close
    outfile.write(output_sentence)
    outfile.flush()
    outfile.close()

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
        if input_word[0] == p:
            return True
        elif input_word[len(input_word) - 1] == p:
            return True

    return False

def parse_data(data):
	# Remove trailing endline
    data = data[:-1]
    # Split sentence into words
    input_sentence = data.split(" ", -1)
    return input_sentence



def pig_latin(input_sentence):
    output_sentence = ""
    for input_word_orig in input_sentence:
        # Set suffix and prefix
        ending = ""
        suffix = "ay"
        prefix = ""
        beginning = ""

        if len(input_word_orig) == 0:
            output_sentence += "\n\n"
            continue

        input_word = input_word_orig.lower() # Ignore uppercase for now


        if check_high_punct(input_word, True):
            # Check for higher punctuation in front
            input_word = input_word[1:]

        if check_high_punct(input_word, False):
            # Check for higher punctuation in back
            input_word = input_word[:-1]

        # Check for vowel in every letter for current word
        i = 0
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
            # Check for uppercase word
            if len(prefix) > 0:
                prefix = prefix[0].upper() + prefix[1:]
            elif len(suffix) > 0:
                suffix = suffix[0].upper() + suffix[1:]
        # append current new prefix and suffix to the output sentence
        output_sentence += beginning + prefix + suffix + ending + " "
    return output_sentence





def main():
    args = parse_arguments()
    infile = load_in_file(args)
    outfile = load_out_file(args)
    data = infile.readlines()
    input_sentence = ""
    output_sentence = ""
    for line in data:
        output_sentence += pig_latin(parse_data(line))
    print(output_sentence)
    write_out_file(output_sentence, outfile)

if __name__ == "__main__":
    main()
