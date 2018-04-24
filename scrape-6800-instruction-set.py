import requests, sys, re, json

name = "6800 Instruction Set Scraper, Neil Thistlethwaite"
version = "0.1"
url = "http://www.8bit-era.cz/6800.html"
output_json = "6800-instruction-set.json"

req = requests.get(url)
raw_text = None
if req.ok:
    print("Fetched Instruction Set with Status Code %d" % req.status_code)
    raw_text = req.text
else:
    print("Error fetching URL '%s'" % url)
    sys.exit(1)

instruction_set = []
dat = raw_text.split("\n")[174:371]

last_main = ""

## Format of instructions:
## (mnemonic, syntax, mode, opcode, bytes, mpu cycles)

for line in dat:
    info = re.sub(r"!+","\n",
           re.sub("<a.+?>|<tr>|<td.*?>|</a>|</td>|</tr>","!",
                  re.sub(r"\s+"," ",
                  re.sub("<a.+?>|</a>"," ", line))
                  ).replace("\t","").strip()
           ).split("\n")[1:7]

    ## 'Last Main' keeps track of the leading header from previous rows
    if len(info[0].strip()) > 0:
        last_main = info[0].strip()
        
    ## We want to turn "ADD A" and "ADD B" under syntax into "ADDA" and "ADDB" for mnemonics
    syntax = info[1].strip()
    main = last_main
    if syntax[:len(last_main)] == last_main and len(syntax) > len(last_main) + 1 and syntax[len(last_main)] == " " and syntax[len(last_main)+1] in "AB":
        main = last_main + syntax[len(last_main)+1]
    instruction_set.append((main, syntax, info[2].strip(), info[4].strip(), int(info[3].strip()), int(info[5].strip())))

print("Instruction Set page parsed")

header_info = {"name":name, "version":version, "source":url, "instruction_set":instruction_set}

with open(output_json,"w") as f:
    f.write(json.dumps(header_info))

print("Instruction Set dumped to JSON file: %s" % output_json)
