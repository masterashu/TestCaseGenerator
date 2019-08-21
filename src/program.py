from generators import Generator
from parsers import split as split_req

if __name__ == "__main__":
    gen = Generator()
    [reqs, variable] = split_req(input())
    for req in reqs:
        if req == ';':
            print()
            continue
        arg = gen.parse_request(req)
        print(gen.generate(**arg))


