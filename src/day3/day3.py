import csv


def run_wire(wire):
    directions = {"U": [0, -1], "D": [0, 1], "L": [-1, 0], "R": [1, 0]}

    locations = []
    current_location = (0, 0)
    locations.append(current_location)
    for run in wire:
        move = directions[run[0]]
        for i in range(1, run[1] + 1):
            current_location = tuple(sum(x) for x in zip(current_location, move))
            locations.append(current_location)
    return locations


def intersections(wire1, wire2):
    return set(wire1).intersection(wire2)


def calculate_manhattan_distance(point: tuple):
    return abs(point[0]) + abs(point[1])


def calculate_wire_distance(wires: list, point: tuple):
    dist1 = wires[0].index(point)
    dist2 = wires[1].index(point)
    return dist1 + dist2


if __name__ == "__main__":
    wires = []
    with open("input.txt") as file:
        csv_reader = csv.reader(file, delimiter=",")
        for row in csv_reader:
            wires.append(row)
    for wire_num, runs in enumerate(wires):
        for run_num, run in enumerate(runs):
            direction = run[:1]
            length = int(run[1:])
            wires[wire_num][run_num] = (direction, length)

    runs = []
    for wire in wires:
        runs.append(run_wire(wire))
    intersections = intersections(runs[0], runs[1])
    intersections.remove((0, 0))

    print(min([calculate_manhattan_distance(x) for x in intersections]))
    print(min([calculate_wire_distance(runs, x) for x in intersections]))

