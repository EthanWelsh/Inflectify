import re
from datetime import datetime


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


def get_date_string(date_info):
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

    if date_info.day and date_info.month and date_info.year != 1900:
        day = number_string(str(date_info.day), ordinal=True)
        year = year_string(date_info.year)
        return "{month} {day}, {year}".format(day=day, month=month[date_info.month], year=year)
    elif date_info.day and date_info.month:
        day = number_string(str(date_info.day), ordinal=True)
        return "{month} {day}".format(day=day, month=month[date_info.month])
    elif date_info.month and date_info.year != 1900:
        year = year_string(date_info.year)
        return "{month} {year}".format(year=year, month=month[date_info.month])


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
    }

    new_sentence = []
    for word in sentence:
        word = str.lower(word)
        new_sentence += [abbrev.get(word, word)]

    return new_sentence


def year_string(numerical_year):
    year_str = str(numerical_year)

    start = year_str[:2]
    ending = year_str[2:]

    if re.match('\d\d00', year_str):
        return number_string(start) + ' ' + 'hundred'
    elif re.match('2000', year_str):
        return 'Two Thousand'
    elif re.match('200[1-9]', year_str):
        return number_string(year_str[:3]+'0') + ' and ' + number_string(year_str[3])
    elif re.match('\d\d0[1-9]', year_str):
        return number_string(start) + ' oh ' + number_string(ending)
    else:
        return number_string(start) + ' ' + number_string(ending)


def year(sentence):
    year_regex = re.compile('^((1[5-9]\d\d)|(20\d\d))$')

    new_sentence = []

    for word in sentence:
        if year_regex.match(word):
            new_sentence += [year_string(word)]
        else:
            new_sentence += [word]

    return new_sentence


def date(sentence):
    month_names = '(?:january|february|march|april|may|june|july|august|september|october|november|december)'

    date_formats = [
        ('\d{1,2}\/\d{1,2}\/\d{4}', '%m/%d/%Y'),  # mm/dd/yyyy
        ('\d{1,2}\/\d{1,2}\/\d{2}', '%m/%d/%y'),  # mm/dd/yy
        ('{month_names}\s+\d{{1,2}}\s+\d{{4}}'.format(month_names=month_names), '%B %d %Y'),  # january 3 2015
        ('{month_names}\s+\d{{4}}'.format(month_names=month_names), '%B %Y'),  # january 1980
        ('{month_names}\s+[123]\d'.format(month_names=month_names), '%B %d'),  # january 30
        ('{month_names}\s+[4-9]\d'.format(month_names=month_names), '%B %y'),  # january 79
    ]

    sentence_str = ' '.join(sentence)
    sentence_str = sentence_str.lower()

    # Remove commas
    sentence_str = sentence_str.replace(',', '')

    for regex, pattern in date_formats:
        for match in re.findall(regex, sentence_str):
            date_tuple = datetime.strptime(match, pattern)
            sentence_str = sentence_str.replace(match, get_date_string(date_tuple))

    return sentence_str.split()


def ordinal(sentence):
    sentence_str = ' '.join(sentence)
    sentence_str = sentence_str.lower()

    ordinal_regex = re.compile('(\d+)(st|nd|rd|th)')

    for number, ordinal_ending in ordinal_regex.findall(sentence_str):
        sentence_str = sentence_str.replace(number+ordinal_ending, number_string(number, ordinal=True))

    return sentence_str.split()


def money(sentence):

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
        else:
            sentence.remove(index)
            sentence[index] = number_string(first, money=True)

    if len(match_indexes) > 1:
        return money(str(sentence).split())

    return str(sentence).split()


def fraction(sentence):
    fraction_regex = re.compile('[\d]+\\\/[\d]+')
    match_indexes = []

    for index, word in enumerate(sentence):
        if fraction_regex.match(word):
            match_indexes += [index]

    number_regex = re.compile('[\d]+')

    sentence = Sentence(sentence)

    if match_indexes:

        index = match_indexes[0]
        prev = sentence.adjacent_word(index, -1)

        if number_regex.match(prev):
            sentence.insert(index, -1, 'and')
            index += 1

        num, den = sentence[index].split('\/')
        sentence[index] = fractions(numerator=num, denominator=den)

    if len(match_indexes) > 1:
        return fraction(str(sentence).split())

    return sentence


def percent(sentence):
    percent_regex = re.compile('%')

    match_indexes = []

    for index, word in enumerate(sentence):
        if percent_regex.match(word):
            match_indexes += [index]

    for index in match_indexes:
        sentence[index] = 'Percent'

    return sentence


def number(sentence):
    number_regex = re.compile('^([0-9]+[.]*[0-9]*)$')
    match_indexes = []

    for index, word in enumerate(sentence):
        if number_regex.match(word):
            match_indexes += [index]

    for index in match_indexes:
        sentence[index] = number_string(sentence[index])

    return sentence


def clean(sentence):
    sentence_str = ' '.join(sentence)
    sentence_str = sentence_str.replace('-', ' ')
    sentence_str = sentence_str.replace('$', ' $ ')

    return sentence_str.split()


def time(sentence):
    time_regex = re.compile('\d{1,2}:\d\d')
    match_indexes = []

    for index, word in enumerate(sentence):
        if time_regex.match(word):
            match_indexes += [index]

    for index in match_indexes:
        hours, minutes = sentence[index].split(':')
        sentence[index] = number_string(hours) + ' ' + number_string(minutes)

    return sentence


def main():
    #with open('hw1_corpus.txt', 'r') as sample_text:
    with open('hw1_samplein.txt', 'r') as sample_text:
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
        sentence = number(sentence)
        sentence = time(sentence)

        print(' '.join(sentence))


if __name__ == '__main__':
    main()
