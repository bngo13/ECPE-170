import argparse

# Vowels list
vowels = ["a","e","i","o","u"]

# Argument Parsing
parser = argparse.ArgumentParser()
parser.add_argument('--input')
parser.add_argument('--output')
args = parser.parse_args()

# Load input file as reader
infile = open(str(args.input), "r")
data = infile.read().lower()
data = data[:-1]

# Load output file as writer
outfile = open(str(args.output), 'w')

# Split sentence into words
input_sentence = data.split(" ", -1)

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

for input_word in input_sentence:
    # Set suffix and prefix
    suffix = "ay"
    prefix = ""

    # Check for vowel in every letter for current word
    i = 0
    for input_letter in input_word:
        if check_vowel(input_letter) == False:
            i = i + 1
        else:
            break

    # i = 0 when vowel is the first letter
    if i == 0:
        prefix = input_word
        suffix = "y" + suffix
    # i = length of word when there are no vowels in word
    elif i == len(input_word):
        prefix = input_word[-1]
        suffix = input_word[:-1] + suffix
    else:
    # i is neither when there is a vowel in the word somewhere other than front
        prefix = input_word[i:]
        suffix = input_word[:i] + suffix

    # append current new prefix and suffix to the output sentence
    output_sentence = output_sentence + prefix + suffix + " "

# remove the trailing space at the end
output_sentence = output_sentence[:-1]

# write to file and close
outfile.write(output_sentence)
outfile.flush()
outfile.close()
