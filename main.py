class Number:
    def __init__(self, number):
        self.number = number

    def __str__(self):
        return self.trillions(self.number)

    def small(self, number):
        return {1: 'One', 2: 'Two', 3: 'Three', 4: 'Four', 5: 'Five', 6: 'Six',
                7: 'Seven', 8: 'Eight', 9: 'Nine', 10: 'Ten', 11: 'Eleven',
                12: 'Twelve', 13: 'Thirteen', 14: 'Fourteen', 15: 'Fifteen',
                16: 'Sixteen', 17: 'Seventeen', 18: 'Eighteen', 19: 'Nineteen'}[number]

    def decades(self, number):
        if number < 20:
            return self.small(number)

        ret = {20: 'Twenty', 30: 'Thirty', 40: 'Forty', 50: 'Fifty', 60: 'Sixty',
               70: 'Seventy', 80: 'Eighty', 90: 'Ninety'}[(number // 10) * 10]

        remainder = number % 10

        if remainder > 0:
            ret += ' ' + self.small(remainder)
        return ret

    def hundreds(self, number):
        if number < 100:
            return self.decades(number)

        ret = self.small(number // 100) + ' Hundred'

        if number % 100 > 0:
            ret += ' ' + self.decades(number % 100)

        return ret

    def thousands(self, number):
        if number < 1000:
            return self.hundreds(number)

        thousands = number // 1000
        ret = self.hundreds(thousands) + ' Thousand'

        remainder = number % 1000
        if remainder > 0:
            ret += ' ' + self.hundreds(remainder)

        return ret

    def millions(self, number):
        if number < 1000000:
            return self.thousands(number)

        millions = number // 1000000
        ret = self.hundreds(millions) + ' Million'

        remainder = number % 1000000
        if remainder > 0:
            ret += ' ' + self.thousands(remainder)

        return ret

    def billions(self, number):
        if number < 1000000000:
            return self.millions(number)

        billions = number // 1000000000
        ret = self.hundreds(billions) + ' Billion'

        remainder = number % 1000000000
        if remainder > 0:
            ret += ' ' + self.millions(remainder)

        return ret

    def trillions(self, number):
        if number < 1000000000000:
            return self.billions(number)

        trillions = number // 1000000000000
        ret = self.hundreds(trillions) + ' Million'

        remainder = number % 1000000000
        if remainder > 0:
            ret += ' ' + self.billions(remainder)

        return ret


def main():
    with open('hw1_samplein.txt', 'r') as sample_text:
        sentences = [line for line in sample_text]

    print(sentences)


if __name__ == '__main__':
    main()
