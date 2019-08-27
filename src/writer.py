class Writer:
    def __init__(self):
        # self.buffer = []
        self.output_file = None
        
    def open_file(self, file_name):
        self.output_file = open(file_name, 'w')

    def write_new_line(self):
        self.output_file.write('\n')

    def write(self, data):
        if type(data) is str:
            self.output_file.write(data)
        elif type(data) is int:
            self.output_file.write(str(data))
        elif type(data) is list:
            self.output_file.write(' '.join(map(str, data)))
        self.output_file.write(' ')
    
    def close(self):
        self.output_file.close()


if __name__ == "__main__":
    writer = Writer()
    writer.open_file('a.txt')
    writer.write(73)
    writer.write('73')
    writer.write_new_line()
    writer.write([2,5,6,31])
