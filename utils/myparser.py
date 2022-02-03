import sys

def parseInputFile():

    try:
        input_fileName = sys.argv[1]
    except IndexError:
        print("WARNING: No input file name found, assuming it is 'input'")
        input_fileName = 'input'

    # ~~~~ Parse input
    inpt = {}
    try:
        f = open( input_fileName )
    except FileNotFoundError:
        print("ERROR: Input file " + input_fileName + " not found")
        sys.exit()
    data = f.readlines()
    for line in data:
        if ':' in line:
            key, value = line.split(":")
            inpt[key.strip()] = value.strip()
    f.close()
   
    return inpt
