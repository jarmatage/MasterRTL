import subprocess

from .clean_verilog import clean_verilog

SOG_YOSYS_SCRIPT = [
    "proc",
    "flatten",
    "opt",
    "fsm",
    "opt",
    "memory",
    "opt",
    "techmap",
    "opt",
]


def generate_sog(design: str, verilog_files: list[str], out_dir: str) -> None:
    cmd: list[str] = []
    for file in verilog_files:
        cmd.append(f"read_verilog {file}")
    cmd.extend(SOG_YOSYS_SCRIPT)
    cmd.append(f"write_verilog {out_dir}/{design}_sog.v")

    subprocess.run(["yosys", "-p", "; ".join(cmd)], check=True)
    clean_verilog(f"{out_dir}/{design}_sog.v")
