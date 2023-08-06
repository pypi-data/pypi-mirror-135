class TextDB:
    def __init__(self, filename):
        self.filename = filename
        self.dataDict = {}
        self.dataList = []

    def read(self):
        with open(self.filename, "rb") as file:
            data = file.read().decode('utf-8')
            data = data.replace("\r", "")
            rows = data.split("\n")

            for row in rows:
                if row != "":
                    row = row.split(":")

                    self.dataDict[row[0]] = row[1]
                    self.dataList.append([row[0], row[1]])

            file.close()

        return self.dataDict

    def write(self, name, value):
        with open(self.filename, "a") as file:
            file.write(f"\n{name}:{value}")

            file.close()

    def delete(self, name):
        for i in range(len(self.dataList)):
            if self.dataList[i][0] == name:
                self.dataList.pop(i)
                break
        self.deleteAll()
        for row in self.dataList:
            self.write(row[0], row[1])
        self.read()


    def deleteAll(self):
        with open(self.filename, 'w') as file:
            file.close()
