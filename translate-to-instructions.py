import sys
import json

def interactive_mode():
    default_file = "6800-instruction-set.json"
    instruction_set_filename = input("Instruction Set Filename? [%s] " % default_file)
    if len(instruction_set_filename) == 0:
        instruction_set_filename = default_file
    try:
        with open(instruction_set_filename) as f:
            instruction_info = json.loads(f.read())
    except:
        print("Error reading file or parsing JSON!")
        sys.exit(1)
    print("Instruction set loaded!")
    for attr in ["name","version","source"]:
        if attr in instruction_info:
            print("%s: %s" % (attr[0].upper()+attr[1:], instruction_info[attr]))
    instruction_set = instruction_info["instruction_set"]


if __name__ == "__main__":
    if len(sys.argv) > 1: # Command line arg mode
        print("Command line argument mode not yet implemented!")
        sys.exit(0)
    else: # Interactive mode
        interactive_mode()
