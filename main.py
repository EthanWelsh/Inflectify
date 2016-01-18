from numbers import number_string
import re


def main():
    with open('hw1_samplein.txt', 'r') as sample_text:
        sentences = [[word for word in line.split()] for line in sample_text]

    number_regex = re.compile('^[0-9]+$')

    for sentence in sentences:
        for word in sentence:
            if number_regex.match(word):
                print(number_string(word), end=' ')
            else:
                print(word, end=' ')
        print()


if __name__ == '__main__':
    main()
