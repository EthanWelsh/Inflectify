class Number:
    def __init__(self, number, ordinal):
        self.number = number
        self.ordinal = ordinal

    def __str__(self):
        return self.trillions(self.number, self.ordinal)

    def small(self, number, ordinal=False):

        number_words = {1: 'One', 2: 'Two', 3: 'Three', 4: 'Four', 5: 'Five', 6: 'Six',
                        7: 'Seven', 8: 'Eight', 9: 'Nine', 10: 'Ten', 11: 'Eleven',
                        12: 'Twelve', 13: 'Thirteen', 14: 'Fourteen', 15: 'Fifteen',
                        16: 'Sixteen', 17: 'Seventeen', 18: 'Eighteen', 19: 'Nineteen'}

        special_ordinals = {1: 'First', 2: 'Second', 3: 'Third', 5: 'Fifth', 8: 'Eighth', 9: 'Ninth'}

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


def main():
    with open('hw1_samplein.txt', 'r') as sample_text:
        sentences = [line for line in sample_text]

    print(sentences)

    print('1: ', str(Number(1, ordinal=True)))
    print('2: ', str(Number(2, ordinal=True)))
    print('3: ', str(Number(3, ordinal=True)))
    print('4: ', str(Number(4, ordinal=True)))
    print('5: ', str(Number(5, ordinal=True)))
    print('6: ', str(Number(6, ordinal=True)))
    print('7: ', str(Number(7, ordinal=True)))
    print('8: ', str(Number(8, ordinal=True)))
    print('9: ', str(Number(9, ordinal=True)))
    print('10: ', str(Number(10, ordinal=True)))
    print('11: ', str(Number(11, ordinal=True)))
    print('12: ', str(Number(12, ordinal=True)))
    print('13: ', str(Number(13, ordinal=True)))
    print('14: ', str(Number(14, ordinal=True)))
    print('15: ', str(Number(15, ordinal=True)))
    print('16: ', str(Number(16, ordinal=True)))
    print('17: ', str(Number(17, ordinal=True)))
    print('18: ', str(Number(18, ordinal=True)))
    print('19: ', str(Number(19, ordinal=True)))
    print('20: ', str(Number(20, ordinal=True)))
    print('21: ', str(Number(21, ordinal=True)))
    print('22: ', str(Number(22, ordinal=True)))
    print('23: ', str(Number(23, ordinal=True)))
    print('24: ', str(Number(24, ordinal=True)))
    print('25: ', str(Number(25, ordinal=True)))
    print('26: ', str(Number(26, ordinal=True)))
    print('27: ', str(Number(27, ordinal=True)))
    print('28: ', str(Number(28, ordinal=True)))
    print('29: ', str(Number(29, ordinal=True)))
    print('30: ', str(Number(30, ordinal=True)))
    print('31: ', str(Number(31, ordinal=True)))
    print('100: ', str(Number(100, ordinal=False)))
    print('131: ', str(Number(131, ordinal=True)))
    print('999: ', str(Number(999, ordinal=True)))
    print('1000: ', str(Number(1000, ordinal=True)))
    print('10001: ', str(Number(10001, ordinal=True)))
    print('100000: ', str(Number(100000, ordinal=True)))
    print('1000000: ', str(Number(1000000, ordinal=True)))
    print('10000000: ', str(Number(10000000, ordinal=True)))
    print('100000000: ', str(Number(100000000, ordinal=True)))
    print('1000000000: ', str(Number(1000000000000, ordinal=True)))


if __name__ == '__main__':
    main()
