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
    cmd = [f"read_verilog {file}" for file in verilog_files]
    cmd.append(f"hierarchy -check -top {design}")
    cmd.extend(SOG_YOSYS_SCRIPT)
    cmd.append(f"write_verilog {out_dir}/{design}_sog.v")

    with open(f"{out_dir}/sog.ys", "w") as f:
        for arg in cmd:
            f.write(f"{arg}\n")

    subprocess.run(["yosys", f"{out_dir}/sog.ys"], check=True)
    clean_verilog(f"{out_dir}/{design}_sog.v")
