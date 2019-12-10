def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def produce_layers(image, dimensions):
    layer_size = dimensions[0] * dimensions[1]
    layers = list(chunks(image, layer_size))
    return layers


def verify_image(image, dimensions):
    layers = produce_layers(image, dimensions)
    min_layer = [dimensions[0] * dimensions[1]]
    for layer in layers:
        zeros = len([z for z in layer if z == 0])
        if zeros < min_layer[0]:
            min_layer = [
                zeros,
                len([o for o in layer if o == 1]),
                len([t for t in layer if t == 2]),
            ]
    return min_layer[1] * min_layer[2]


def produce_image(in_array, dimensions):
    layers = produce_layers(in_array, dimensions)
    flat_image = [2 for x in range(dimensions[0] * dimensions[1])]
    for index, pixel in enumerate(flat_image):
        for layer in layers:
            if layer[index] < 2:
                flat_image[index] = layer[index]
                break

    image = list(chunks(flat_image, dimensions[0]))
    for line in image:
        print(line)


if __name__ == "__main__":
    dimensions = (25, 6)
    with open("input.txt") as file:
        in_str = file.readline().strip()
        in_array = [int(char) for char in in_str]
    print(verify_image(in_array, dimensions))

    produce_image(in_array, dimensions)

