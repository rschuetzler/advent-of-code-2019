import csv

from intcode.intcode import Intcode

if __name__ == "__main__":
    memory = []
    with open("day5/input.txt") as file:
        csv_reader = csv.reader(file, delimiter=",")
        for row in csv_reader:
            memory = [int(i) for i in row]
    intcode = Intcode(memory)
    intcode.run_intcode()
