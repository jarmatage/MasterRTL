import re
from pathlib import Path


def clean_verilog(file):
    path = Path(file)
    tmp = path.with_suffix(path.suffix + ".tmp")
    path.rename(tmp)
    with tmp.open("r") as fin, path.open("w") as fout:
        for line in fin:
            line = re.sub(r"\(\*(.*)\*\)", "", line)
            if line.strip():
                fout.writelines(line)
    tmp.unlink()
