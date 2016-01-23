class Number:
    def __init__(self, number, ordinal):
        self.number = number
        self.ordinal = ordinal

    def __str__(self):
        return self.trillions(self.number, self.ordinal)

    def small(self, number, ordinal=False):

        number_words = {0: 'Zero', 1: 'One', 2: 'Two', 3: 'Three', 4: 'Four', 5: 'Five', 6: 'Six',
                        7: 'Seven', 8: 'Eight', 9: 'Nine', 10: 'Ten', 11: 'Eleven',
                        12: 'Twelve', 13: 'Thirteen', 14: 'Fourteen', 15: 'Fifteen',
                        16: 'Sixteen', 17: 'Seventeen', 18: 'Eighteen', 19: 'Nineteen'}

        special_ordinals = {1: 'First', 2: 'Second', 3: 'Third', 5: 'Fifth', 8: 'Eighth', 9: 'Ninth', 12: 'Twelfth'}

        if ordinal:
            return special_ordinals.get(number, number_words[number] + 'th')
        else:
            return number_words[number]

    def decades(self, number, ordinal=False):
        if number < 20:
            return self.small(number, ordinal)

        decade_words = {20: 'Twenty', 30: 'Thirty', 40: 'Forty', 50: 'Fifty', 60: 'Sixty',
                        70: 'Seventy', 80: 'Eighty', 90: 'Ninety'}
        decade_number = (number // 10) * 10

        prefix = decade_words[decade_number]
        remainder = number % 10

        if remainder > 0:
            return prefix + ' ' + self.small(remainder, ordinal)
        elif ordinal:
            return prefix + 'th'
        else:
            return prefix

    def hundreds(self, number, ordinal=False):
        if number < 100:
            return self.decades(number, ordinal)

        prefix = number // 100
        remainder = number % 100

        ret = self.small(prefix) + ' Hundred'

        if remainder > 0:
            ret += ' ' + self.decades(remainder, ordinal)
        elif ordinal:
            ret += 'th'

        return ret

    def thousands(self, number, ordinal=False):
        if number < 1000:
            return self.hundreds(number, ordinal)

        prefix = self.hundreds(number // 1000)
        remainder = number % 1000

        if remainder > 0:
            return prefix + ' Thousand ' + self.hundreds(remainder, ordinal)
        elif ordinal:
            return prefix + ' Thousandth'

        return prefix + ' Thousand'

    def millions(self, number, ordinal=False):
        if number < 1000000:
            return self.thousands(number, ordinal)

        millions = number // 1000000
        ret = self.hundreds(millions) + ' Million'

        remainder = number % 1000000

        if remainder > 0:
            ret += ' ' + self.thousands(remainder)
        else:
            ret += 'th'

        return ret

    def billions(self, number, ordinal=False):
        if number < 1000000000:
            return self.millions(number, ordinal)

        billions = number // 1000000000
        ret = self.hundreds(billions) + ' Billion'

        remainder = number % 1000000000
        if remainder > 0:
            ret += ' ' + self.millions(remainder)
        else:
            ret += 'th'

        return ret

    def trillions(self, number, ordinal=False):
        if number < 1000000000000:
            return self.billions(number, ordinal)

        trillions = number // 1000000000000
        ret = self.hundreds(trillions) + ' Trillion'

        remainder = number % 1000000000
        if remainder > 0:
            ret += ' ' + self.billions(remainder)
        else:
            ret += 'th'

        return ret


def read_digits(number):
    return ' '.join([number_string(digit) for digit in str(number)])


def number_string(number, ordinal=False, money=False):
    if '.' in number:
        integer, decimal = str(number).split('.')

        if money:

            return '{dollars} Dollars and {cents} Cents'.format(dollars=number_string(integer), cents=number_string(decimal))
        else:
            return '{integer} Point {decimal}'.format(integer=number_string(integer), decimal=read_digits(decimal))
    else:
        integer = str(Number(int(number), ordinal))

        if money:
            return '{dollars} Dollars'.format(dollars=integer)
        else:
            return integer


def fractions(numerator, denominator):

    num = number_string(numerator)
    den = number_string(denominator, ordinal=True)

    if int(numerator) > 1:
        if int(denominator) == 2:
            return '{} Halves'.format(num, den)
        else:
            return '{} {}s'.format(num, den)
    else:
        if int(denominator) == 2:
            return '{} Half'.format(num)
        else:
            return '{} {}s'.format(num, den)