import copy


def get_r_values(cell_states_dict):
    r_values_dict = copy.deepcopy(cell_states_dict)

    for x, y in cell_states_dict:
        cell_r_value = 0

        for y_pos in range(-1, 2):
            for x_pos in range(-1, 2):
                if not (x_pos == 0 and y_pos == 0):
                    try:
                        cell_r_value += cell_states_dict[x+x_pos, y+y_pos]
                    except KeyError:
                        pass

        r_values_dict[x, y] = cell_r_value

    return r_values_dict


def get_next_gen(cell_states_dict):
    new_gen = copy.deepcopy(cell_states_dict)
    r_values = get_r_values(cell_states_dict)

    for x, y in cell_states_dict:

        # Case 1: Cell is alive
        if cell_states_dict[x, y] == 1:
            if not 2 <= r_values[x, y] <= 3:
                new_gen[x, y] = 0

        # Case 2: Cell is dead
        else:
            if r_values[x, y] == 3:
                new_gen[x, y] = 1

    return new_gen


def print_dict(dictionary):
    start_y = 0
    for x, y in dictionary:
        print(("\n" if y != start_y else "") + str(dictionary[x, y]), end=" ")
        start_y = y
    print()
