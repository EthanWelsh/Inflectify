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


def main():
    with open('hw1_samplein.txt', 'r') as sample_text:
        sentences = [Sentence([word for word in line.split()]) for line in sample_text]

    for sentence in sentences:

        sentence = date(sentence)

        if contains_money(sentence):
            sentence = money(sentence)
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
        day = number_string(datetime.tm_mon, ordinal=True)
        year = str(datetime.tm_year)
        year = number_string(year[:2]) + ' ' + number_string(year[2:])
        return "{month} {day}, {year}".format(day=day, month=month[datetime.tm_mon], year=year)
    elif datetime.tm_mday and datetime.tm_mon:
        day = number_string(datetime.tm_mon, ordinal=True)
        return "{month} {day}".format(day=day, month=month[datetime.tm_mon])
    elif datetime.tm_mon and datetime.tm_year:
        year = str(datetime.tm_year)
        year = number_string(year[:2]) + ' ' + number_string(year[2:])
        return "{month} {year}".format(year=year, month=month[datetime.tm_mon])


def date(sentence):
    regex_format_dict = {
        '\d{1,2}\/\d{1,2}\/\d{2}': '%d/%m/%y',  # dd/mm/yy
        '\d{1,2}\/\d{1,2}\/\d{4}': '%d/%m/%Y',  # dd/mm/yyyy
        '(jan|feb|mar|apr|may|jun|jul|aug)\s+\d{1}': '',  # jan 3
        '(jan|feb|mar|apr|may|jun|jul|aug)\s+\d{4}': '',  # jan 1980
        '(jan|feb|mar|apr|may|jun|jul|aug)\s+\d{1,2}\s+\d{4}': '%b %d %y'  # jan 3 2015
    }

    numerical_date = re.compile('\d{1,2}[.-/]\d{1,2}[.-/](\d{4}|\d{2})')
    written_date = re.compile(
            '(jan(uary)?|feb(uary)?|mar(ch)?|apr(il)|may|jun(e)?|jul(y)?|aug(ust)?)\s\d+.?.?\s?(\d{2}|\d{4})?\s')

    sentence_str = ' '.join(sentence)
    sentence_str = sentence_str.lower()

    matches = []
    numerical_groups = numerical_date.match(sentence_str)
    if numerical_groups:
        for match in numerical_groups.groups():
            # Change (-|.) to /
            matches += [re.sub('[-.]', '/', sentence_str)]

    for match in matches:
        for regex, pattern in regex_format_dict.items()






    """

    written_groups = written_date.match(sentence_str)
    if written_groups:
        for match in written_groups.groups():
            # Change January to -> Jan
            for full, abbreviation in [('january', 'jan'), ('february', 'feb'), ('march', 'mar'), ('april', 'apr'),
                                   ('may', 'may'), ('june', 'jun'), ('july', 'jul'), ('august', 'aug'),
                                   ('september', 'sep'), ('october', 'oct'), ('november', 'nov'), ('december', 'dec')]:
                date = re.sub(full, abbreviation, match)

            # Remove st, nd, rd, th
            date = re.sub('(st|nd|rd|th)', '', date)


    return sentence


        # Change January to -> Jan
        for full, abbreviation in [('january', 'jan'), ('february', 'feb'), ('march', 'mar'), ('april', 'apr'),
                                   ('may', 'may'), ('june', 'jun'), ('july', 'jul'), ('august', 'aug'),
                                   ('september', 'sep'), ('october', 'oct'), ('november', 'nov'), ('december', 'dec')]:
            date = re.sub(full, abbreviation, match)

        # Remove st, nd, rd, th
        date = re.sub('(st|nd|rd|th)', '', date)
        matches += (match, date)


    return sentence
    """


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
