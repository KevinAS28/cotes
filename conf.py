class Conf:
    def __init__(self, filename, separator="=", comment="#"):
        self.configuration = {}
        self.filename = filename
        self.separator = separator
        self.comment=comment
        self.read()
        
    def read(self):
        with open(self.filename, "r") as read:
            buffer = read.read()
        conf0 = buffer.split("\n")
    
        for conf in conf0:
            conflist = conf.split(self.separator, 1)

            if (len(conflist)!=2): #error configuration, pass it
                continue

            if (conflist[0]==self.comment): #if commented, pass it
                continue
            self.configuration[conflist[0]] = conflist[1]
    
    def write(self):
        buffer = ""
        for key in self.configuration:
            buffer+="{}={}\n".format(key, self.configuration[key])

        with open(self.filename, "w+") as write:
            write.write(buffer)

    def getVal(self, key):
        return self.configuration[key]

    def getKey(self, val):
        values = self.configuration.values
        if (val in values):
            index = values.index(val)
            return self.configuration[self.configuration.keys[index]]
        else:
            raise IndexError("Conf.getKey(): value not found")
    
    def setVal(self, key, val):
        self.configuration[key] = val
    
