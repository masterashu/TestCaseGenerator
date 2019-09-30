from src import Generator, split as split_req, Writer
from sys import argv
# from src.parsers import split as split_req
# from src.writer import Writer
    
def main():
    if len(argv) != 3:
        print("Usage: python3 clProgram.py outputFileName schemaInQuotes")
        if len(argv) < 3:
            print("Too few arguments provided.")
        else:
            print("Too many arguments provided. Hint: Did you forget to put the schema in quotes?")
        return -1


    gen = Generator()
    wr = Writer()
    output_file_name = argv[1]
    [reqs, variable] = split_req(argv[2])
    #print(reqs)
    wr.open_file(output_file_name)
    for req in reqs:
        if req == ';':
            print()
            wr.write_new_line()
            continue
        arg = gen.parse_request(req)
        #print(arg)
        data = gen.generate(**arg)
        wr.write(data)
        print(data, end='', sep=' ')
        if arg.get('var_name', False) is not False:
            gen.variables[arg['var_name']] = data

if __name__ == "__main__":
    main()
    


