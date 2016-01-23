import re
from time import strptime

from numbers import number_string, fractions


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

        sentence = abbreviations(sentence)
        sentence = date(sentence)

        if contains_money(sentence):
            sentence = money(Sentence(sentence))
        if contains_fraction(sentence):
            sentence = fraction(sentence)
        if contains_percent(sentence):
            sentence = percent(sentence)
        # if contains_number(sentence):
        #    sentence = number(sentence)

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


def year(setence):
    year_regex = re.compile('[12]\d{3}')
    pass


def get_date_string(datetime):
    month = {1: 'January',
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

    if datetime.tm_mday and datetime.tm_mon and datetime.tm_year:
        day = number_string(str(datetime.tm_mon), ordinal=True)
        year = str(datetime.tm_year)
        year = number_string(year[:2]) + ' ' + number_string(year[2:])
        return "{month} {day}, {year}".format(day=day, month=month[datetime.tm_mon], year=year)
    elif datetime.tm_mday and datetime.tm_mon:
        day = number_string(str(datetime.tm_mon), ordinal=True)
        return "{month} {day}".format(day=day, month=month[datetime.tm_mon])
    elif datetime.tm_mon and datetime.tm_year:
        year = str(datetime.tm_year)
        year = number_string(year[:2]) + ' ' + number_string(year[2:])
        return "{month} {year}".format(year=year, month=month[datetime.tm_mon])


def abbreviations(sentence):

    abbrev = {
        'jan.': 'January',
        'feb.': 'February',
        'mar.': 'March',
        'apr.': 'April',
        'may.': 'May',
        'jun.': 'June',
        'jul.': 'July',
        'aug.': 'August',
        'sept.': 'September',
        'oct.': 'October',
        'nov.': 'November',
        'dec.': 'December',
        'etc...': 'etcetera',
        'u.s.': 'United States',
        'u.s.a.': 'United States of America',
        'u.k.': 'United Kingdom',
        'mr.':'Mister',
        'mrs.':'Miss',
        'dr.':'Doctor',
        'gov.':'Governor',
        'sen.':'Senator',
        'inc.':'incorporated',
        'vs.':'verse',
        'jr.':'junior',
    }

    new_sentence = []
    for word in sentence:
        word = str.lower(word)
        new_sentence += [abbrev.get(word, word)]

    return new_sentence


def date(sentence):

    # @formatter:off
    date_formats = [
        ('\d{1,2}\/\d{1,2}\/\d{4}',                                                 '%m/%d/%Y'),    # mm/dd/yyyy
        ('\d{1,2}\/\d{1,2}\/\d{2}',                                                 '%m/%d/%y'),    # mm/dd/yy
        ('(?:january|february|march|april|may|june|july|august)\s+\d{1,2}\s+\d{4}', '%B %d %Y'),    # january 3 2015
        ('(?:jan|feb|mar|apr|may|jun|jul|aug)\s+\d{1,2}\s+\d{4}',                   '%b %d %Y'),    # jan 3 2015
        ('(?:january|february|march|april|may|june|july|august)\s+\d{4}',           '%B %Y'),       # january 1980
        ('(?:jan|feb|mar|apr|may|jun|jul|aug)\s+\d{4}',                             '%b %Y'),       # jan 1980
        ('(?:january|february|march|april|may|june|july|august)\s+\d{1}',           '%B %d'),       # january 3
        ('(?:jan|feb|mar|apr|may|jun|jul|aug)\s+\d{1}',                             '%b %d'),       # jan 3
    ]
    # @formatter:on

    sentence_str = ' '.join(sentence)
    sentence_str = sentence_str.lower()

    # Remove Ordinals
    ordinal_regex = re.compile('(?<=[0-9])(?:st|nd|rd|th)')
    sentence_str = re.sub(ordinal_regex, '', sentence_str)

    # Remove commas
    sentence_str = sentence_str.replace(',', '')
    sentence_str = sentence_str.replace('.', '/')
    sentence_str = sentence_str.replace('-', '/')

    for regex, pattern in date_formats:
        for match in re.findall(regex, sentence_str):
            date_tuple = strptime(match, pattern)
            sentence_str = sentence_str.replace(match, get_date_string(date_tuple))

    return sentence_str.split()


def money(sentence):
    indexes = contains_money(sentence)

    for index in indexes:

        first = sentence.adjacent_word(index, offset=1)
        second = sentence.adjacent_word(index, offset=2)

        if 'illion' in second:
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
