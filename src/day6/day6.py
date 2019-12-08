def find_steps_to_com(orbits, planet):

    for orbit in orbits:
        if orbit[1] == planet:
            if orbit[0] == "COM":
                return 1
            else:
                return 1 + find_steps_to_com(orbits, orbit[0])
    raise ValueError(f"Planet {planet} has no orbit")


def generate_planet_path_to_com(orbits, planet):
    for orbit in orbits:
        if orbit[1] == planet:
            if orbit[0] == "COM":
                yield "COM"
            else:
                yield orbit[0]
                yield from generate_planet_path_to_com(orbits, orbit[0])


def find_planet_path_to_com(orbits, planet):

    path = [p for p in generate_planet_path_to_com(orbits, planet)]
    path.insert(0, planet)
    return path


def find_path_between_planets(orbits, planet1, planet2):
    path1_to_com = find_planet_path_to_com(orbits, planet1)
    path2_to_com = find_planet_path_to_com(orbits, planet2)

    common_planet = ""
    # Find the closest common planet
    if planet2 in path1_to_com:
        return path1_to_com[: path1_to_com.index(planet2)]
    else:
        for planet in path1_to_com:
            if planet in path2_to_com:
                common_planet = planet
                break

    path1_to_common = path1_to_com[: path1_to_com.index(common_planet) + 1]
    path2_to_common = path2_to_com[: path2_to_com.index(common_planet)]
    print(common_planet)

    return path1_to_common + path2_to_common[::-1]


orbit_strings = []
orbits = []  # List of lists, [orbited, orbiter]
planets = set()
with open("input.txt") as file:
    for line in file:
        orbit_strings.append(line.strip())
    for orbit in orbit_strings:
        orbit = orbit.split(sep=")")
        orbits.append(orbit)
        planets.add(orbit[0])
        planets.add(orbit[1])
planets.remove("COM")

# Calculate checksum, probably super slow
# total_steps = 0
# for planet in planets:
#     steps = find_steps_to_com(orbits, planet)
#     total_steps += steps
# print(total_steps)

# Test path to COM
path = find_planet_path_to_com(orbits, "XVQ")
# print(path)

# -3 accounts for the fact that the first two steps in the path are your current
# location, so you don't need to transfer those, and the last step is the destination.
# Since the goal is to orbit the same planet as the destination, not to orbit the
# destination, that's where we can stop.
print(len(find_path_between_planets(orbits, "YOU", "SAN")) - 3)
