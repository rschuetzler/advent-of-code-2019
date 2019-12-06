import csv

VALID_OPCODES = (1, 2, 99)
STEP = 4


def run_intcode(memory, step, noun, verb):
    memory[1] = noun
    memory[2] = verb

    i = 0
    while (instruction := memory[i]) != 99:
        arg1 = memory[memory[i + 1]]
        arg2 = memory[memory[i + 2]]

        if instruction not in VALID_OPCODES:
            raise ValueError(
                f"Invalid Opcode: {instruction}\nNoun: {noun}\nVerb: {verb}"
            )
        if instruction == 1:  # Add
            memory[memory[i + 3]] = arg1 + arg2
            i += STEP
        elif instruction == 2:
            memory[memory[i + 3]] = arg1 * arg2
            i += STEP

    return memory[0]


if __name__ == "__main__":
    memory = []

    with open("input.txt") as file:
        csv_reader = csv.reader(file, delimiter=",")
        for row in csv_reader:
            memory = [int(i) for i in row]
            # print(memory)
    goal_value = 19690720

    for noun in range(1, 100):
        for verb in range(1, 100):
            if run_intcode(memory[:], STEP, noun, verb) == goal_value:
                print((100 * noun) + verb)

