import json
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
data_path = os.path.join(BASE_DIR, "data.json")

KEY = 172

with open(os.path.join(BASE_DIR, "data.json"), "r", encoding="utf-8") as f:
    data = json.load(f)

text = json.dumps(
    data,ensure_ascii=False,indent=4)
encrypted = bytes(b ^ KEY for b in text.encode("utf-8"))

with open("data.dat", "wb") as f:
    f.write(encrypted)
