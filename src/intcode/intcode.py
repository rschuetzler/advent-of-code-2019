import csv


class Intcode(object):
    def __init__(self, memory):
        self.memory = memory
        # self.memory[1] = noun
        # self.memory[2] = verb
        self.current_address = 0
        self.num_params = {
            1: 3,  # Addition: arg1, arg2, location
            2: 3,  # Multiplication: arg1, arg2, location
            3: 1,  # Input: location
            4: 1,  # Output: location
            5: 2,  # Jump-if-true: bool, value
            6: 2,  # Jump-if-false: bool, value
            7: 3,  # less than: val1, val2, position
            8: 3,  # equals: val1, val2, position
            99: 0,  # End
        }

    def step(self, instruction):
        self.current_address += self.num_params[instruction] + 1
        # print(f"Stepping to {self.current_address}")

    def convert_opcodes_to_addresses(self, opcodes):
        addresses = []
        for offset, op in enumerate(opcodes):
            op_address = self.current_address + offset + 1
            if op == 0:
                addresses.append(self.memory[op_address])
            elif op == 1:
                addresses.append(op_address)

        return addresses

    def parse_instruction(self, parameter: int):
        op_codes = []
        if parameter < 100:  # Default opcode of zero of none specified
            op_codes = [0 for x in range(self.num_params[parameter])]
            instruction = parameter
        else:
            op_string = str(parameter)
            instruction = int(op_string[-2:])
            code_string = op_string[:-2]
            op_codes = []
            for code_char in code_string[::-1]:
                op_codes.append(int(code_char))

        # print(f"Address: {self.current_address}")
        # print(f"Instruction: {instruction}")
        # print(op_codes)

        if len(op_codes) < self.num_params[instruction]:  # Pad out opcodes to num args
            for i in range(len(op_codes), self.num_params[instruction]):
                op_codes.append(0)

        op_addresses = self.convert_opcodes_to_addresses(op_codes)

        return instruction, op_addresses

    def add(self, op_addresses):
        arg1 = self.memory[op_addresses[0]]
        arg2 = self.memory[op_addresses[1]]

        self.memory[op_addresses[2]] = arg1 + arg2
        # return op_addresses[2]

    def multiply(self, op_addresses):
        arg1 = self.memory[op_addresses[0]]
        arg2 = self.memory[op_addresses[1]]

        self.memory[op_addresses[2]] = arg1 * arg2
        # return op_addresses[2]

    def input(self, op_addresses):
        input_value = int(input("Enter an input: "))
        self.memory[op_addresses[0]] = input_value

        # return op_addresses[0]

    def output(self, op_addresses):
        print(self.memory[op_addresses[0]])
        # return -1

    def jump_if_true(self, op_addresses):
        if self.memory[op_addresses[0]] != 0:
            self.current_address = self.memory[op_addresses[1]]
            return -1
        else:
            return

    def jump_if_false(self, op_addresses):
        if self.memory[op_addresses[0]] == 0:
            self.current_address = self.memory[op_addresses[1]]
            return -1
        else:
            return

    def less_than(self, op_addresses):
        arg1 = self.memory[op_addresses[0]]
        arg2 = self.memory[op_addresses[1]]
        if arg1 < arg2:
            self.memory[op_addresses[2]] = 1
        else:
            self.memory[op_addresses[2]] = 0

    def equals(self, op_addresses):
        arg1 = self.memory[op_addresses[0]]
        arg2 = self.memory[op_addresses[1]]
        if arg1 == arg2:
            self.memory[op_addresses[2]] = 1
        else:
            self.memory[op_addresses[2]] = 0

    def do_action(self, instruction, op_addresses):
        actions = {
            1: self.add,
            2: self.multiply,
            3: self.input,
            4: self.output,
            5: self.jump_if_true,
            6: self.jump_if_false,
            7: self.less_than,
            8: self.equals,
        }
        action_value = actions[instruction](op_addresses)
        if action_value == -1:
            pass
        else:
            self.step(instruction)

    def run_intcode(self):

        instruction, op_addresses = self.parse_instruction(
            self.memory[self.current_address]
        )
        while instruction != 99:
            # print(f"{instruction}: {op_addresses}")
            self.do_action(instruction, op_addresses)
            instruction, op_addresses = self.parse_instruction(
                self.memory[self.current_address]
            )

        return


if __name__ == "__main__":
    memory = []

    with open("input.txt") as file:
        csv_reader = csv.reader(file, delimiter=",")
        for row in csv_reader:
            memory = [int(i) for i in row]
            # print(memory)
    goal_value = 19690720

    # for noun in range(1, 100):
    #     for verb in range(1, 100):
    #         if run_intcode(memory[:], STEP, noun, verb) == goal_value:
    #             print((100 * noun) + verb)

