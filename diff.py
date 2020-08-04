import os
from pathlib import Path
import urllib.request
import sys
import json
from itertools import takewhile
from distutils.util import strtobool

def levenshteinDistance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1
    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]

REPORT_URL = "https://raw.githubusercontent.com/Totenfehler/toktrak/other/reports/{}.csv"
MAP_URL = "https://raw.githubusercontent.com/Totenfehler/toktrak/other/map.json"

args = list(sys.argv)
if len(args) != 3:
	sys.exit("Invalid Args: requires username path/to/dir/")
prg,name,dirpath = args
dirpath = Path(dirpath)
if not dirpath.exists() or not dirpath.is_dir():
	sys.exit("No such directory: " + str(dirpath))
print("Fetching Name Mapping...")
name_map = json.loads(urllib.request.urlopen(MAP_URL).read().decode("utf-8"))
if name not in name_map:
	deltas = [(key,levenshteinDistance(name,key)) for key in name_map]
	deltas.sort(key=lambda x:x[1])
	close = [i[0] for i in deltas][:3]
	print("Unknown username: " + name)
	print("Did you mean: {}?".format(", ".join(close)))
	sys.exit()
uid = name_map[name]
url = REPORT_URL.format(uid)
print("Fetching Post Records for", name, uid)
body = urllib.request.urlopen(url).read()
table = [row.split(",") for row in body.decode("utf-8").strip().split("\n")[1:]]
table = [(pid,saved == "Y") for pid,saved in table]
saved_remote = {pid for pid,saved in table}
print("Scanning post directory...")
saved_local = set()
for fname in os.listdir(dirpath):
	p = dirpath / Path(fname)
	if p.suffix not in (".mp4", ".webm"):
		print("Skipping non-video file", fname)
		continue
	pid = "".join(takewhile(str.isdigit, p.stem))
	if not pid.isdigit():
		print("Skipping non-numeric file prefix", fname)
		continue
	saved_local.add(pid)
print("Local:   {} posts".format(len(saved_local)))
print("Remote:  {} posts".format(len(saved_remote)))
print("Missing: {} posts".format(len(saved_remote-saved_local)))
print("Private: {} posts".format(len(saved_local-saved_remote)))
print("Print {} missing/private post ids?".format(len(saved_remote-saved_local) + len(saved_local-saved_remote)))
response = input()
if strtobool(response):
	missing = list(sorted(saved_remote-saved_local))
	private = list(sorted(saved_local-saved_remote))
	print("=======Missing=======")
	print("\n".join(missing))
	print("=======Private=======")
	print("\n".join(private))