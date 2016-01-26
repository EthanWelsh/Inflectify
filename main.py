#!/usr/bin/python3

import re
import sys

from numbers import number_string, fractions


class Sentence:
    def __init__(self, sentence):
        self.sentence = sentence

    def adjacent_word(self, index, offset=1):
        if 0 <= index + offset < len(self.sentence):
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


def get_date_string(day=None, month=None, year=None):
    month_dict = {1: 'January',
                  2: 'February',
                  3: 'March',
                  4: 'April',
                  5: 'May',
                  6: 'June',
                  7: 'July',
                  8: 'August',
                  9: 'September',
                  10: 'October',
                  11: 'November',
                  12: 'December'}

    if day and month and year:
        day = number_string(str(day), ordinal=True)
        year = year_string(year)
        return "{month} {day}, {year}".format(day=day, month=month_dict[month], year=year)
    elif day and month:
        day = number_string(str(day), ordinal=True)
        return "{month} {day}".format(day=day, month=month_dict[month])
    elif month and year:
        year = year_string(year)
        return "{month} {year}".format(year=year, month=month_dict[month])


def year_string(numerical_year):
    year_str = str(numerical_year)

    if len(year_str) == 2:
        if int(year_str) <= 16:
            year_str = '20' + year_str
        else:
            year_str = '19' + year_str

    start = year_str[:2]
    ending = year_str[2:]

    if re.match('2000', year_str):
        return 'Two Thousand'
    elif re.match('\d\d00', year_str):
        return number_string(start) + ' ' + 'hundred'
    elif re.match('200[1-9]', year_str):
        return number_string(year_str[:3] + '0') + ' and ' + number_string(year_str[3])
    elif re.match('\d\d0[1-9]', year_str):
        return number_string(start) + ' oh ' + number_string(ending)
    else:
        return number_string(start) + ' ' + number_string(ending)


def numeral_to_int(numeral_string):
    numeral_map = (('M',  1000),
                   ('CM', 900),
                   ('D',  500),
                   ('CD', 400),
                   ('C',  100),
                   ('XC', 90),
                   ('L',  50),
                   ('XL', 40),
                   ('X',  10),
                   ('IX', 9),
                   ('V',  5),
                   ('IV', 4),
                   ('I',  1))

    result = 0
    index = 0
    for numeral, integer in numeral_map:
        while numeral_string[index:index+len(numeral)] == numeral:
            result += integer
            index += len(numeral)
    return result


def abbreviations(sentence):

    try:
        abbrev = {
            'jan.': 'January',
            'feb.': 'February',
            'mar.': 'March',
            'apr.': 'April',
            'may.': 'May',
            'jun.': 'June',
            'jul.': 'July',
            'aug.': 'August',
            'sep.': 'September',
            'sept.': 'September',
            'oct.': 'October',
            'nov.': 'November',
            'dec.': 'December',
            'etc...': 'etcetera',
            'u.s.': 'United States',
            'u.s.a.': 'United States of America',
            'u.k.': 'United Kingdom',
            'mr.': 'Mister',
            'mrs.': 'Miss',
            'dr.': 'Doctor',
            'gov.': 'Governor',
            'sen.': 'Senator',
            'inc.': 'incorporated',
            'vs.': 'verse',
            'jr.': 'junior',
            'EST': 'Eastern Standard Time'
        }

        new_sentence = []
        for word in sentence:
            if str.lower(word) in abbrev:
                new_sentence += [abbrev.get(str.lower(word))]
            else:
                new_sentence += [word]

        return new_sentence
    except:
        return sentence

def roman_numeral(sentence):
    try:
        numeral_regex = re.compile('^[MCDXLIV]+$')

        new_sentence = []
        for word in sentence:
            if numeral_regex.match(word):
                numeral_string = numeral_regex.search(word).group()
                new_sentence += [str(numeral_to_int(numeral_string.upper()))]
            else:
                new_sentence += [word]

        return new_sentence
    except:
        return sentence


def distance(sentence):
    try:
        year_regex = re.compile('(\d+)\'(\d+)\"')

        new_sentence = []

        for word in sentence:
            if year_regex.match(word):
                feet, inches = year_regex.search(word).groups()

                if int(feet) == 1:
                    new_sentence += ['One foot']
                else:
                    new_sentence += [number_string(feet) + ' feet']

                new_sentence += ['and']

                if int(inches) == 1:
                    new_sentence += ['One inch']
                else:
                    new_sentence += [number_string(inches) + ' inches ']
            else:
                new_sentence += [word]

        return new_sentence
    except:
        return sentence


def ratio(sentence):
    try:
        year_regex = re.compile('^\d+:\d+$')

        new_sentence = []

        for word in sentence:
            if year_regex.match(word):
                first, second = word.split(':')
                new_sentence += [number_string(first) + ' to ' + number_string(second)]
            else:
                new_sentence += [word]

        return new_sentence
    except:
        return sentence


def year(sentence):
    try:
        year_regex = re.compile('^((1[5-9]\d\d)|(20\d\d))s?$')

        new_sentence = []

        for word in sentence:
            if year_regex.match(word):
                if word[len(word) - 1] == 's':
                    if word[-3:-1] == '10':
                        new_sentence += [year_string(word[:4]) + 's']
                    else:
                        new_sentence += [year_string(word[:4])[:-1] + 'ies']
                else:
                    new_sentence += [year_string(word)]
            else:
                new_sentence += [word]

        return new_sentence
    except:
        return sentence


def date(sentence):
    try:
        month_number_dict = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6, 'july': 7,
                             'august': 8, 'september': 9, 'october': 10, 'november': 11, 'december': 12}
        month_names = '(?:january|february|march|april|may|june|july|august|september|october|november|december)'

        sentence_str = ' '.join(sentence)

        # Remove commas
        sentence_str = sentence_str.replace(',', '')

        # 12/01/2016
        match = re.search('(\d{1,2})\/(\d{1,2})\/(\d{2,4})', sentence_str, flags=re.IGNORECASE)
        if match:
            month, day, year = match.groups()
            sentence_str = sentence_str.replace(match.group(), get_date_string(month=int(month), day=day, year=year))

        # january 1 2016
        match = re.search('({month_names})\s+(\d{{1,2}})\s+(\d{{4}})'.format(month_names=month_names), sentence_str, flags=re.IGNORECASE)
        if match:
            month, day, year = match.groups()
            sentence_str = sentence_str.replace(match.group(),
                                                get_date_string(month=month_number_dict[str.lower(month)], day=day, year=year))

        # january 1980
        match = re.search('({month_names})\s+(\d{{4}})'.format(month_names=month_names), sentence_str, flags=re.IGNORECASE)
        if match:
            month, year = match.groups()
            sentence_str = sentence_str.replace(match.group(), get_date_string(month=month_number_dict[str.lower(month)], year=year))

        # january 25
        match = re.search('({month_names})\s+([123]\d)'.format(month_names=month_names), sentence_str, flags=re.IGNORECASE)
        if match:
            month, day = match.groups()
            sentence_str = sentence_str.replace(match.group(), get_date_string(month=month_number_dict[str.lower(month)], day=day))

        # january 79
        match = re.search('({month_names})\s+([4-9]\d)'.format(month_names=month_names), sentence_str, flags=re.IGNORECASE)
        if match:
            month, year = match.groups()
            sentence_str = sentence_str.replace(match.group(), get_date_string(month=month_number_dict[str.lower(month)], year=year))

        return sentence_str.split()
    except:
        return sentence

def ordinal(sentence):
    try:
        sentence_str = ' '.join(sentence)

        ordinal_regex = re.compile('(\d+)(st|nd|rd|th)', flags=re.IGNORECASE)

        for number, ordinal_ending in ordinal_regex.findall(sentence_str):
            sentence_str = sentence_str.replace(number + ordinal_ending, number_string(number, ordinal=True))

        return sentence_str.split()
    except:
        return sentence


def money(sentence):
    try:
        money_regex = re.compile('[$]')
        match_indexes = []

        for index, word in enumerate(sentence):
            if money_regex.match(word):
                match_indexes += [index]

        sentence = Sentence(sentence)

        if match_indexes:
            index = match_indexes[0]
            first = sentence.adjacent_word(index, offset=1)
            second = sentence.adjacent_word(index, offset=2)

            if 'illion' in second:
                sentence.insert(index, offset=2, word='Dollars')
                sentence.remove(index)
            elif '\/' in second:
                sentence.insert(index, offset=3, word='Dollar')
                sentence.remove(index)
            else:
                sentence.remove(index)
                sentence[index] = number_string(first, money=True)

        if len(match_indexes) > 1:
            return money(str(sentence).split())

        return str(sentence).split()
    except:
        return sentence


def fraction(sentence):
    try:
        fraction_regex = re.compile('[\d]+\\\/[\d]+')
        number_regex = re.compile('\d+')

        match_indexes = []

        for index, word in enumerate(sentence):
            if fraction_regex.match(word):
                match_indexes += [index]

        sentence = Sentence(sentence)

        if match_indexes:

            index = match_indexes[0]
            prev_word = sentence.adjacent_word(index, -1)

            if number_regex.match(prev_word):
                sentence.insert(index, -1, 'and')
                index += 1

            num, den = sentence[index].split('\/')
            sentence[index] = fractions(numerator=num, denominator=den)

        if len(match_indexes) > 1:
            return fraction(str(sentence).split())

        return sentence
    except:
        return sentence


def percent(sentence):
    try:
        percent_regex = re.compile('%')

        match_indexes = []

        for index, word in enumerate(sentence):
            if percent_regex.match(word):
                match_indexes += [index]

        for index in match_indexes:
            sentence[index] = 'Percent'

        return sentence
    except:
        return sentence


def number(sentence):
    try:
        number_regex = re.compile('^([0-9]+[.]*[0-9]*)$')
        match_indexes = []

        for index, word in enumerate(sentence):
            if number_regex.match(word):
                match_indexes += [index]

        for index in match_indexes:
            sentence[index] = number_string(sentence[index])

        return sentence
    except:
        return sentence


def clean(sentence):
    try:
        sentence_str = ' '.join(sentence)
        sentence_str = sentence_str.replace('-', ' ')
        sentence_str = sentence_str.replace('$', ' $ ')

        return sentence_str.split()
    except:
        return sentence


def time(sentence):
    try:
        time_regex = re.compile('\d{1,2}:\d\d')
        match_indexes = []

        for index, word in enumerate(sentence):
            if time_regex.match(word):
                match_indexes += [index]

        for index in match_indexes:
            hours, minutes = sentence[index].split(':')
            sentence[index] = number_string(hours) + ' ' + number_string(minutes)

        return sentence
    except:
        return sentence


def main():
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
    else:
        print('Please enter a filename to Inflectify!')
        return -1

    with open(file_name, 'r') as sample_text:
        sentences = [Sentence([word for word in line.split()]) for line in sample_text]

    for sentence in sentences:
        sentence = clean(sentence)
        sentence = abbreviations(sentence)
        sentence = ordinal(sentence)
        sentence = date(sentence)
        sentence = money(sentence)
        sentence = fraction(sentence)
        sentence = percent(sentence)
        sentence = year(sentence)
        sentence = roman_numeral(sentence)
        sentence = number(sentence)
        sentence = time(sentence)
        sentence = ratio(sentence)
        sentence = distance(sentence)

        print(' '.join(sentence))


if __name__ == '__main__':
    main()
