infile = "input.txt"

running_total = 0


def calculate_fuel(mass: int) -> int:
    fuel = (mass // 3) - 2
    if fuel <= 0:
        return 0
    else:
        return fuel + calculate_fuel(fuel)


with open(infile) as input:
    for line in input:
        running_total += calculate_fuel(int(line))
        print(running_total)
