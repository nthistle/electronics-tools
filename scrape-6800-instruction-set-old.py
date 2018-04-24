import requests
import sys

url = "http://www.electronics.dit.ie/staff/tscarff/6800/Instructions/instructions.htm"

req = requests.get(url)
raw_text = None
if req.ok:
    print("Fetched Instruction Set with Status Code %d" % req.status_code)
    raw_text = req.text.replace("<!--mstheme--></font><pre>","")
else:
    print("Error fetching URL '%s'" % url)
    sys.exit(1)

instruction_set = []
dat = raw_text.split("\n")

headers = [x.strip() for x in dat[27].replace("<b>","").replace("</b>","").split("|")]
cc_key = dat[28].split("|")[8]
last_operation = None
scrape_ranges = [(30,95),(101,112),(118,133),(139,147),(153,161)]
start_index = 30

mode_split = chr(183)
empty_cc = chr(149)


for scrape in scrape_ranges:
    for idx in range(*scrape):
        row = [x.strip() for x in dat[idx].split("|")]
        if len(row[0]) > 0:
            last_operation = row[0]
        # (mnemonic, word desc, op desc, modes {}, condition codes {})
        modes = {}
        cond_codes = {}
        operation = (row[1], last_operation, row[7], modes, cond_codes)
        for i in range(2, 7):
            mode = [x.strip() for x in row[i].split(mode_split)]
            if len(mode[0]) > 0:
                # this mode actually exists
                modes[headers[i]] = (mode[0], int(mode[1], 16), int(mode[2], 16))
        for i, val in enumerate(row[8]):
            if val != empty_cc:
                cond_codes[cc_key[i]] = val
        instruction_set.append(operation)
            
        
