import sys
import json

if sys.version_info[0] < 3:
    input = raw_input

## Format of instructions:
## (mnemonic, syntax, mode, opcode, bytes, mpu cycles)

def translate_instructions(raw, ins_set):
    instruction_dict = {}
    for instruction in ins_set:
        # Creating a mapping from opcode to instruction
        instruction_dict[instruction[3][1:].upper()] = instruction
    output_str = ""
    bytes_left = 0

    raw = raw.upper()
    if " " in raw.strip() and max(len(t) for t in raw.split())==2:
        raw = raw.split() # If space split
    else:
        raw = [raw[i:i+2] for i in range(0,len(raw),2)] # If conjoined

    is_indexed = False
    for byte in raw:
        if bytes_left > 0:
            output_str += byte
            bytes_left -= 1
            if bytes_left == 0 and is_indexed:
                output_str += ",X"
                is_indexed = False
        else:
            output_str += "\n" + instruction_dict[byte][0]
            bytes_left = instruction_dict[byte][4]-1
            if instruction_dict[byte][2] == "IMM":
                output_str += " #$"
            elif instruction_dict[byte][2] == "DIR":
                output_str += " $"
            elif instruction_dict[byte][2] == "EXT":
                output_str += " $"
            elif instruction_dict[byte][2] == "IDX":
                output_str += " $"
                is_indexed = True
            elif instruction_dict[byte][2] == "REL":
                output_str += " $"

    return output_str[1:]
        

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
    print()
    print("Instruction set loaded!")
    for attr in ["name","version","source"]:
        if attr in instruction_info:
            print("%s: %s" % (attr[0].upper()+attr[1:], instruction_info[attr]))
    instruction_set = instruction_info["instruction_set"]
    print("%d instructions" % len(instruction_set))
    print()
    print("Input raw: ")
    raw_program = input()
    print(translate_instructions(raw_program, instruction_set))


if __name__ == "__main__":
    if len(sys.argv) > 1: # Command line arg mode
        print("Command line argument mode not yet implemented!")
        sys.exit(0)
    else: # Interactive mode
        interactive_mode()
