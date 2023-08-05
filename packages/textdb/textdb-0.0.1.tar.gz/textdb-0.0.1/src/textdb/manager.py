class TextDB:
    def __init__(self, filename):
        self.filename = filename
        self.dataDict = {}

    def read(self):
        with open(self.filename, "rb") as file:
            data = file.read().decode('utf-8')
            data = data.replace("\r", "")
            rows = data.split("\n")
            print(rows)

            for row in rows:
                if row != "":
                    row = row.split(":")

                    self.dataDict[row[0]] = row[1]

            file.close()

        return self.dataDict

    def write(self, name, value):
        with open(self.filename, "a") as file:
            file.write(f"\n{name}:{value}")

            file.close()

    def deleteAll(self):
        with open(self.filename, 'w') as file:
            file.close()
