def read_ascii(filename):
    """
    Fonction pour lire les fichiers positions .ascii de BigDFT
    :param filename: nom du fichier à lire
    :return: positions atomiques, éléments, spin, unités
    :return: geocode, type de coordonnées, dimensions de la cellule
    """

    data_pos = []
    data_element = []
    data_spin = []
    cell_dims = []
    coord = "absolute"

    with open(filename, "r") as f:

        for line in f:
            l = line.split()

            if not line[0] == "#":
                if len(l) >= 4:
                    data_pos.append([float(l[0]), float(l[1]), float(l[2])])
                    data_element.append(l[3])
                    if len(l) == 4:
                        data_spin.append(0)
                    elif len(l) == 6:
                        data_spin.append(int(l[5][0]))
                    else:
                        raise Exception("A line is not recognized:\n" + line)
                elif len(l) == 3:
                    for dim in l:
                        cell_dims.append(float(dim))
                else:
                    raise Exception("A line is not recognized:\n" + line)

            elif l[0] == "#keyword:":
                if l[1] in [
                    "atomicd0",
                    "atomic",
                    "bohr",
                    "bohrd0",
                    "angstroem",
                    "angstroemd0",
                ]:
                    units = l[1]
                elif l[1] in ["surface", "periodic", "freeBC"]:
                    geocode = l[1]
                elif l[1] == "reduced":
                    coord = "reduced"
                else:
                    raise Exception("Keyword not recognized")

    return data_pos, data_element, data_spin, units, geocode, coord, cell_dims
