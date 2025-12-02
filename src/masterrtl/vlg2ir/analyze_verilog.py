import os
import time

from masterrtl.pyverilog.vparser.parser import parse  # type: ignore

from .ast_analyzer import ASTAnalyzer


def analyze_verilog(
    filelist: list[str],
    design_name: str,
    cmd: str = "sog",
    out_path: str | None = None,
    include_paths: list[str] | None = None,
    define_macros: list[str] | None = None,
):
    """
    Analyze Verilog files and convert to graph representation.

    Args:
        filelist: List of Verilog file paths to analyze
        design_name: Name of the design
        cmd: Command type ('ast' for word-level, 'sog' for bit-level)
        out_path: Directory path for output files
        include_paths: List of include paths for preprocessing
        define_macros: List of macro definitions for preprocessing
    """
    start_time = time.perf_counter()

    if include_paths is None:
        include_paths = []
    if define_macros is None:
        define_macros = []

    # Validate files exist
    for f in filelist:
        if not os.path.exists(f):
            raise OSError(f"file not found: {f}")

    if not filelist:
        raise ValueError("No Verilog files provided")

    # Parse Verilog
    ast, directives = parse(
        filelist, preprocess_include=include_paths, preprocess_define=define_macros
    )

    print("Verilog2AST Finish!")

    # Analyze AST
    ast_analysis = ASTAnalyzer(ast)
    ast_analysis.AST2Graph(ast)

    g = ast_analysis.graph

    # Save graph
    g.graph2pkl(design_name, cmd, out_path)

    elapsed = time.perf_counter() - start_time
    print(f"Analysis completed in {elapsed:.2f}s")
