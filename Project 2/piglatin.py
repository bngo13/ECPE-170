import argparse

vowels = ["a","e","i","o","u"]

key = "ifyay ayay ordway eginsbay ithway ayay owelvay , ustjay asyay otay ethay endyay"
aaa = "ifyay ayay ordway eginsbay ithway ayay owelvay , ustjay asyay otay ethay endyay"

parser = argparse.ArgumentParser()
parser.add_argument('--input')
parser.add_argument('--output')


args = parser.parse_args()

f = open(str(args.input), "r")
data = f.read().lower()
data = data[:-1]

input_sentence = data.split(" ", -1)
output_sentence = ""
print(input_sentence)

def check_vowel(input_letter):
    for vowel in vowels:
        if input_letter == vowel:
                return True

    print(input_letter)
    return False

for input_word in input_sentence:
    suffix = "ay"
    prefix = ""
    i = 0
    for input_letter in input_word:
        if check_vowel(input_letter) == False:
            i = i + 1
        else:
            break
    if i == 0:
        prefix = input_word
        suffix = "y" + suffix
    elif i == len(input_word):
        prefix = input_word[-1]
        suffix = input_word[:-1] + suffix
    else:
        prefix = input_word[i:]
        suffix = input_word[:i] + suffix
    output_sentence = output_sentence + prefix + suffix + " "

output_sentence = output_sentence[:-1]
print(output_sentence)

outfile = open("output.txt", 'w')
outfile.write(output_sentence)
outfile.flush()
outfile.close()
