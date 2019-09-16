from src import Generator, split as split_req, Writer
# from src.parsers import split as split_req
# from src.writer import Writer

if __name__ == "__main__":
    gen = Generator()
    wr = Writer()
    output_file_name = input("Enter File Name: ")
    [reqs, variable] = split_req(input())
    # print(reqs)
    wr.open_file(output_file_name)
    for req in reqs:
        if req == ';':
            print()
            wr.write_new_line()
            continue
        arg = gen.parse_request(req)
        # print(arg)
        data = gen.generate(**arg)
        wr.write(data)
        print(data, end='', sep=' ')
        if arg.get('var_name', False) is not False:
            gen.variables[arg['var_name']] = data
        


