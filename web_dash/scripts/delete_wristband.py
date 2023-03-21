import logging, time, json, argparse

def readWristbandCodes(file):
    valid_codes = []
    f = open(file)
    wristbandCodes = json.load(f)
    for i in wristbandCodes:
        valid_codes.append(i)
    return valid_codes

wristband_file = "/home/pi/HighlightReel/core/res/wristband_codes.json"
current_wristbands = readWristbandCodes(wristband_file)
parser = argparse.ArgumentParser()
parser.add_argument('wristband_to_delete')
args = parser.parse_args()
print(type(current_wristbands[0]))
print(int(args.wristband_to_delete))

if int(args.wristband_to_delete) in current_wristbands:
    current_wristbands.remove(int(args.wristband_to_delete))
    json_object = json.dumps(current_wristbands)
    with open(wristband_file, "w") as outfile:
        outfile.write(json_object)
exit()