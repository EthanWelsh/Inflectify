class Number:
    def __init__(self, number):
        self.number = number

    def __str__(self):
        if self.number <= 19:
            return self.small(self.number)
        elif self.number < 100:
            return self.decades(self.number)
        elif self.number < 1000:
            return self.hundreds(self.number)
        elif self.number < 1000000:
            return self.thousands(self.number)

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
            ret += '-' + self.small(remainder)
        return ret

    def hundreds(self, number):

        if number < 100:
            return self.decades(number)

        ret = self.small(number//100) + '-' + 'Hundred'

        if number % 100 > 0:
            ret += '-' + self.decades(number % 100)

        return ret

    def thousands(self, number):

        if number < 1000:
            return self.hundreds(number)

        thousands = number // 1000

        if thousands > 0:
            ret = self.hundreds(thousands)

        ret += '-Thousand'

        remainder = number % 1000

        if remainder > 0:
            ret += '-' + self.hundreds(remainder)

        return ret

    def millions(self, number):
        return ''

    def billions(self, number):
        return ''

    def trillions(self, number):
        return ''


def main():
    '''
    sentences = []
    with open('hw1_samplein.txt', 'r') as sample_text:
        sentences = [line for line in sample_text]

    print(sentences)
    '''

    print('1:' + str(Number(1)))
    print('10:' + str(Number(10)))
    print('11:' + str(Number(11)))
    print('19:' + str(Number(19)))
    print('20:' + str(Number(20)))
    print('21:' + str(Number(21)))
    print('91:' + str(Number(91)))
    print('100:' + str(Number(100)))
    print('101:' + str(Number(101)))
    print('111:' + str(Number(111)))
    print('120:' + str(Number(120)))
    print('190:' + str(Number(190)))
    print('213:' + str(Number(213)))
    print('999:' + str(Number(999)))
    print('1000:' + str(Number(1000)))
    print('1001:' + str(Number(1001)))
    print('1013:' + str(Number(1013)))
    print('1073:' + str(Number(1073)))
    print('1173:' + str(Number(1173)))
    print('10173:' + str(Number(10173)))
    print('103173:' + str(Number(103173)))





if __name__ == '__main__':
    main()
