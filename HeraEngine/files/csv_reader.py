
class CSV():
    def read(self,input_file="result.txt"):
        coordinates = []
        with open(input_file, "r") as file:
            for line in file:
                x, y = map(int, line.strip().split(";"))
                coordinates.append((x, y))
        return coordinates