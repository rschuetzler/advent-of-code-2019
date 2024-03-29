import csv


class Intcode(object):
    def __init__(self, memory, inputs=[]):
        self.memory = memory[:]
        self.start_memory = memory[:]
        self.inputs = inputs
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
            9: 1,  # adjust relative base: val
            99: 0,  # End
        }
        self.relative_base = 0
        self.status = 0  # 0: ready, 1: paused, -1: halted
        self.last_output = 0

    def halt(self, *args):
        self.status = -1

    def pause(self):
        self.status = 1

    def start(self):
        if not self.is_halted():
            self.status = 0
            return self.run_intcode()
        else:
            raise ValueError("Program is halted")

    def is_halted(self):
        return self.status == -1

    def reboot(self):
        self.memory = self.start_memory[:]
        self.current_address = 0
        self.status = 0
        self.last_output = 0
        self.inputs = []

    def reset_with_input(self, inputs):
        self.reboot()
        self.inputs = inputs

    def set_inputs(self, inputs):
        self.inputs = inputs

    def add_input(self, input_value):
        self.inputs.append(input_value)

    def pad(self, address):
        if address >= len(self.memory):
            for _ in range(len(self.memory), address + 1):
                self.memory.append(0)

    def write(self, address, value):
        if address < 0:
            raise ValueError(f"Address {address} out of bounds")
        self.pad(address)
        self.memory[address] = value

    def read(self, address):
        self.pad(address)
        return self.memory[address]

    def step(self, instruction):
        self.current_address += self.num_params[instruction] + 1
        # print(f"Stepping to {self.current_address}")

    def convert_opcodes_to_addresses(self, opcodes):
        addresses = []
        # print(self.memory)
        # print(f"Relative address: {self.relative_base}")
        # print(f"Current address: {self.current_address}")
        # print(f"Opcodes: {opcodes}")
        for offset, op in enumerate(opcodes):
            op_address = self.current_address + offset + 1
            if op == 0:
                addresses.append(self.read(op_address))
            elif op == 1:
                addresses.append(op_address)
            elif op == 2:
                addresses.append(self.relative_base + self.read(op_address))
        # print(f"Addresses: {addresses}")
        return addresses

    def parse_instruction(self, parameter: int):
        op_codes = []
        if parameter == 99:
            op_codes = []
            instruction = parameter
        elif parameter < 99:  # Default opcode of zero of none specified
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
            for _ in range(len(op_codes), self.num_params[instruction]):
                op_codes.append(0)

        op_addresses = self.convert_opcodes_to_addresses(op_codes)

        return instruction, op_addresses

    def add(self, op_addresses):
        arg1 = self.read(op_addresses[0])
        arg2 = self.read(op_addresses[1])

        self.write(op_addresses[2], arg1 + arg2)
        # return op_addresses[2]

    def multiply(self, op_addresses):
        arg1 = self.read(op_addresses[0])
        arg2 = self.read(op_addresses[1])

        self.write(op_addresses[2], arg1 * arg2)
        # return op_addresses[2]

    def get_input(self, op_addresses):
        if self.inputs:
            input_value = self.inputs.pop(0)
        else:
            input_value = int(input("Enter an input: "))
        self.write(op_addresses[0], input_value)

        # return op_addresses[0]

    def output(self, op_addresses):
        # print(self.memory[op_addresses[0]])
        self.status = 1
        self.last_output = self.read(op_addresses[0])
        print(self.last_output)
        return self.read(op_addresses[0])
        # return -1

    def jump_if_true(self, op_addresses):
        if self.read(op_addresses[0]) != 0:
            self.current_address = self.read(op_addresses[1])
            return -1
        else:
            return

    def jump_if_false(self, op_addresses):
        if self.read(op_addresses[0]) == 0:
            self.current_address = self.read(op_addresses[1])
            return -1
        else:
            return

    def less_than(self, op_addresses):
        arg1 = self.read(op_addresses[0])
        arg2 = self.read(op_addresses[1])
        if arg1 < arg2:
            self.write(op_addresses[2], 1)
        else:
            self.write(op_addresses[2], 0)

    def equals(self, op_addresses):
        arg1 = self.read(op_addresses[0])
        arg2 = self.read(op_addresses[1])
        if arg1 == arg2:
            self.write(op_addresses[2], 1)
        else:
            self.write(op_addresses[2], 0)

    def modify_relative_base(self, op_addresses):
        arg = self.read(op_addresses[0])
        self.relative_base += arg

    def do_action(self, instruction, op_addresses):
        actions = {
            1: self.add,
            2: self.multiply,
            3: self.get_input,
            4: self.output,
            5: self.jump_if_true,
            6: self.jump_if_false,
            7: self.less_than,
            8: self.equals,
            9: self.modify_relative_base,
            99: self.halt,
        }
        action_value = actions[instruction](op_addresses)
        if action_value == -1:
            pass
        else:
            self.step(instruction)
            return action_value

    def run_intcode(self):
        output = 0

        while self.status == 0:
            # print(f"{instruction}: {op_addresses}")
            # print(
            #     f"Current address: {self.current_address},",
            #     f"value: {self.read(self.current_address)}",
            # )
            # print(f"Relative base: {self.relative_base}")
            # print(self.memory)
            instruction, op_addresses = self.parse_instruction(
                self.read(self.current_address)
            )
            output = self.do_action(instruction, op_addresses)

        return self.last_output

    def run_until_halt(self):
        output = []
        while not self.is_halted():
            thisout = self.start()
            if not output or output[-1] != thisout:
                output.append(thisout)
        return output


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

