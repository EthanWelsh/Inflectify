from numbers import number_string, fractions
import re


class Sentence():
    def __init__(self, sentence):
        self.sentence = sentence

    def adjacent_word(self, index, offset=1):
        if 0 < index + offset < len(self.sentence):
            return self.sentence[index + offset]
        else:
            return ''

    def remove(self, index):
        del self.sentence[index]

    def insert(self, index, offset, word):
        self.sentence.insert(index + offset + 1, word)

    def __iter__(self):
        return self.sentence.__iter__()

    def __getitem__(self, item):
        return self.sentence.__getitem__(item)

    def __setitem__(self, key, value):
        return self.sentence.__setitem__(key, value)

    def __str__(self):
        return ' '.join(self.sentence)


def main():
    with open('hw1_samplein.txt', 'r') as sample_text:
        sentences = [Sentence([word for word in line.split()]) for line in sample_text]

    for sentence in sentences:
        if contains_money(sentence):
            sentence = money(sentence)
        if contains_fraction(sentence):
            sentence = fraction(sentence)
        if contains_percent(sentence):
            sentence = percent(sentence)
        if contains_number(sentence):
            sentence = number(sentence)

        print(' '.join(sentence))


def contains_money(sentence):
    money_regex = re.compile('[$]')
    match_indexes = []

    for index, word in enumerate(sentence):
        if money_regex.match(word):
            match_indexes += [index]

    return match_indexes


def contains_number(sentence):
    number_regex = re.compile('^[0-9]+[.]*[0-9]*$')
    match_indexes = []

    for index, word in enumerate(sentence):
        if number_regex.match(word):
            match_indexes += [index]

    return match_indexes


def contains_fraction(sentence):
    fraction_regex = re.compile('[\d]+\\\/[\d]+')
    match_indexes = []

    for index, word in enumerate(sentence):
        if fraction_regex.match(word):
            match_indexes += [index]

    return match_indexes


def contains_percent(sentence):
    percent_regex = re.compile('%')

    match_indexes = []

    for index, word in enumerate(sentence):
        if percent_regex.match(word):
            match_indexes += [index]

    return match_indexes


def money(sentence):
    monetary_amounts = {'thousand', 'million', 'billion', 'trillion'}
    indexes = contains_money(sentence)

    for index in indexes:

        first = sentence.adjacent_word(index, offset=1)
        second = sentence.adjacent_word(index, offset=2)

        if second in monetary_amounts:
            sentence.insert(index, offset=2, word='Dollars')
            sentence.remove(index)
        else:
            sentence.remove(index)
            sentence[index] = number_string(first, money=True)

    return sentence


def fraction(sentence):
    indexes = contains_fraction(sentence)
    number_regex = re.compile('[\d]+')

    for index in indexes:
        prev = sentence.adjacent_word(index, -1)

        if number_regex.match(prev):
            sentence.insert(index, -1, 'and')
            index += 1

        num, den = sentence[index].split('\/')
        sentence[index] = fractions(numerator=num, denominator=den)

    return sentence


def percent(sentence):
    indexes = contains_percent(sentence)

    for index in indexes:
        sentence[index] = 'Percent'

    return sentence


def number(sentence):
    indexes = contains_number(sentence)

    for index in indexes:
        sentence[index] = number_string(sentence[index])

    return sentence

if __name__ == '__main__':
    main()
