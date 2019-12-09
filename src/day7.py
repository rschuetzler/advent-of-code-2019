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

    phases = [0, 1, 2, 3, 4]
    max_thrust = 0
    for phase_setting in itertools.permutations(phases):
        phase_setting = list(phase_setting)
        input_signal = 0
        for amp in amps:
            amp.set_inputs([phase_setting.pop(0), input_signal])
            output_signal = amp.run_intcode()
            input_signal = output_signal
            amp.reboot()

        max_thrust = max(max_thrust, output_signal)
    print(max_thrust)
