from src import Generator, split as split_req, Writer

if __name__ == "__main__":
    gen = Generator()
    wr = Writer()
    output_file_name = input("Enter File Name: ")
    [reqs, variable] = split_req(input())
    wr.open_file(output_file_name)
    for req in reqs:
        arg = gen.parse_request(req)
        data = gen.generate(**arg)
        wr.write(data)
        print(data, end='', sep=' ')
        


