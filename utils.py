def write_file(filename, list):
        with open(filename, 'w') as wf:
            for point in list:
                for coord in point:
                    wf.write(str(coord) + " ")
                wf.write("\n")
