import csv

from ship.intcode import Intcode

if __name__ == "__main__":
    memory = []
    with open("day9/input.txt") as file:
        csv_reader = csv.reader(file, delimiter=",")
        for line in csv_reader:
            memory.extend(int(i) for i in line)
    puter = Intcode(memory)
    print(puter.run_until_halt())
