from HeraEngine.types.Vec2 import Vec2

class BmpReader():
    def __init__(self):
        pass

    def read_file(self,path):

        data = []

        with open(path,"r") as file:
            data = file.read().split(";")

        size = Vec2(data[0],data[1])
        data.pop(0)
        data.pop(0)

        for i in range(len(data)):
            data[i] = int(data[i])

        return size, data
