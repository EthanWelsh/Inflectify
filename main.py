import re

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

    if day and month_dict and year:
        day = number_string(str(day), ordinal=True)
        year = year_string(year)
        return "{month} {day}, {year}".format(day=day, month=month_dict[month], year=year)
    elif day and month_dict:
        day = number_string(str(day), ordinal=True)
        return "{month} {day}".format(day=day, month=month_dict[month])
    elif month_dict and year:
        year = year_string(year)
        return "{month} {year}".format(year=year, month=month_dict[month])


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

    if len(year_str) == 2:
        if int(year_str) <= 16:
            year_str = '20' + year_str
        else:
            year_str = '19' + year_str

    start = year_str[:2]
    ending = year_str[2:]

    if re.match('\d\d00', year_str):
        return number_string(start) + ' ' + 'hundred'
    elif re.match('2000', year_str):
        return 'Two Thousand'
    elif re.match('200[1-9]', year_str):
        return number_string(year_str[:3] + '0') + ' and ' + number_string(year_str[3])
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
    month_number_dict = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6, 'july': 7,
                         'august': 8, 'september': 9, 'october': 10, 'november': 11, 'december': 12}
    month_names = '(?:january|february|march|april|may|june|july|august|september|october|november|december)'

    sentence_str = ' '.join(sentence)
    sentence_str = sentence_str.lower()

    # Remove commas
    sentence_str = sentence_str.replace(',', '')

    # 12/01/2016
    match = re.search('(\d{1,2})\/(\d{1,2})\/(\d{2,4})', sentence_str)
    if match:
        month, day, year = match.groups()
        sentence_str = sentence_str.replace(match.group(), get_date_string(month=int(month), day=day, year=year))

    # january 1 2016
    match = re.search('({month_names})\s+(\d{{1,2}})\s+(\d{{4}})'.format(month_names=month_names), sentence_str)
    if match:
        month, day, year = match.groups()
        sentence_str = sentence_str.replace(match.group(), get_date_string(month=month_number_dict[month], day=day, year=year))

    # january 1980
    match = re.search('({month_names})\s+(\d{{4}})'.format(month_names=month_names), sentence_str)
    if match:
        month, year = match.groups()
        sentence_str = sentence_str.replace(match.group(), get_date_string(month=month_number_dict[month], year=year))

    # january 25
    match = re.search('({month_names})\s+([123]\d)'.format(month_names=month_names), sentence_str)
    if match:
        month, day = match.groups()
        sentence_str = sentence_str.replace(match.group(), get_date_string(month=month_number_dict[month], day=day))

    # january 79
    match = re.search('({month_names})\s+([4-9]\d)'.format(month_names=month_names), sentence_str)
    if match:
        month, year = match.groups()
        sentence_str = sentence_str.replace(match.group(), get_date_string(month=month_number_dict[month], year=year))

    return sentence_str.split()


def ordinal(sentence):
    sentence_str = ' '.join(sentence)
    sentence_str = sentence_str.lower()

    ordinal_regex = re.compile('(\d+)(st|nd|rd|th)')

    for number, ordinal_ending in ordinal_regex.findall(sentence_str):
        sentence_str = sentence_str.replace(number + ordinal_ending, number_string(number, ordinal=True))

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
