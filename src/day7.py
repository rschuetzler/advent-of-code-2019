import csv
import itertools

from ship.intcode import Intcode

if __name__ == "__main__":
    memory = []
    with open("day7/input.txt") as file:
        csv_reader = csv.reader(file, delimiter=",")
        for row in csv_reader:
            memory = [int(i) for i in row]

    # initialize amps
    amps = []
    for i in range(5):
        amps.append(Intcode(memory))

    # Day 7, part 1
    # phases = [0, 1, 2, 3, 4]
    # max_thrust = 0
    # for phase_setting in itertools.permutations(phases):
    #     phase_setting = list(phase_setting)
    #     input_signal = 0
    #     for amp in amps:
    #         amp.set_inputs([phase_setting.pop(0), input_signal])
    #         output_signal = amp.run_intcode()
    #         input_signal = output_signal
    #         amp.reboot()

    #     max_thrust = max(max_thrust, output_signal)
    # print(max_thrust)

    # Day 7, part 2 - feedback mode
    phases = range(5, 10)
    max_thrust = 0
    for phase_setting in itertools.permutations(phases):
        # Reset all amps

        phase_setting_list = list(phase_setting)
        for amp in amps:
            amp.reboot()
            amp.add_input(phase_setting_list.pop(0))

        input_signal = 0

        while not amps[4].is_halted():
            for amp in amps:
                amp.add_input(input_signal)
                output_signal = amp.start()
                input_signal = output_signal
        print(phase_setting, amps[4].last_output)

        max_thrust = max(max_thrust, amps[4].last_output)
    print(max_thrust)
