from numbers import number_string

def main():
    with open('hw1_samplein.txt', 'r') as sample_text:
        sentences = [line for line in sample_text]

    print(sentences)
    print(number_string(1, True))

if __name__ == '__main__':
    main()
