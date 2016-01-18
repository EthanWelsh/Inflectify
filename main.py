from numbers import number_string, fractions
import re


def main():
    with open('hw1_samplein.txt', 'r') as sample_text:
        sentences = [[word for word in line.split()] for line in sample_text]

    number_regex = re.compile('^[0-9]+$')
    fraction_regex = re.compile('[\d]+\\\/[\d]+')

    for sentence in sentences:
        for word in sentence:
            if fraction_regex.match(word):
                num, den = word.split('\\/')
                print(fractions(num, den), end=' ')
            elif number_regex.match(word):
                print(number_string(word), end=' ')
            else:
                print(word, end=' ')
        print()


if __name__ == '__main__':
    main()
