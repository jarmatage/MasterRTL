"""Command-line interface for MasterRTL."""

from pathlib import Path

import click


@click.group()
@click.version_option()
def cli():
    """MasterRTL: Pre-Synthesis PPA Estimation Framework for RTL Designs."""
    pass


@cli.group()
def feature():
    """Feature extraction commands."""
    pass


@cli.group()
def preproc():
    """Preprocessing commands."""
    pass


@cli.group()
def model():
    """ML model commands."""
    pass


@cli.group()
def yosys():
    """Yosys synthesis and processing commands."""
    pass


@feature.command(name="area")
@click.option(
    "--design-name",
    required=True,
    help="Name of the design",
)
@click.option(
    "--cmd",
    default="sog",
    help="Command type (default: sog)",
)
@click.option(
    "--input-dir",
    required=True,
    type=click.Path(exists=True, file_okay=False),
    help="Directory containing input pickle files",
)
@click.option(
    "--output-dir",
    required=True,
    type=click.Path(file_okay=False),
    help="Output directory for feature JSON files",
)
def extract_area(design_name, cmd, input_dir, output_dir):
    """Extract area features from a design."""
    from masterrtl.feature_extract.area import run_one_design

    Path(output_dir).mkdir(parents=True, exist_ok=True)
    run_one_design(design_name, cmd, input_dir, output_dir)
    click.echo(f"Area features extracted to {output_dir}")


@feature.command(name="power")
@click.option(
    "--design-name",
    required=True,
    help="Name of the design",
)
@click.option(
    "--cmd",
    default="sog",
    help="Command type (default: sog)",
)
@click.option(
    "--feat-dir",
    required=True,
    type=click.Path(exists=True, file_okay=False),
    help="Directory containing feature JSON files",
)
@click.option(
    "--toggle-rate-dir",
    required=True,
    type=click.Path(exists=True, file_okay=False),
    help="Directory containing toggle rate JSON files",
)
@click.option(
    "--output-dir",
    required=True,
    type=click.Path(file_okay=False),
    help="Output directory for feature JSON files",
)
def extract_power(design_name, cmd, feat_dir, toggle_rate_dir, output_dir):
    """Extract power features from a design."""
    from masterrtl.feature_extract.graph_power import run_one_design

    Path(output_dir).mkdir(parents=True, exist_ok=True)
    run_one_design(design_name, cmd, feat_dir, toggle_rate_dir, output_dir)
    click.echo(f"Power features extracted to {output_dir}")


@feature.command(name="timing")
@click.option(
    "--design-name",
    required=True,
    help="Name of the design",
)
@click.option(
    "--cmd",
    default="sog",
    help="Command type (default: sog)",
)
@click.option(
    "--timing-dag-dir",
    required=True,
    type=click.Path(exists=True, file_okay=False),
    help="Directory containing timing DAG pickle files",
)
@click.option(
    "--output-dir",
    required=True,
    type=click.Path(file_okay=False),
    help="Output directory for feature JSON files",
)
def extract_timing(design_name, cmd, timing_dag_dir, output_dir):
    """Extract timing features from a design using STA."""
    from masterrtl.feature_extract.feature_extra_graph_STA import run_one_design

    Path(output_dir).mkdir(parents=True, exist_ok=True)
    run_one_design(design_name, cmd, timing_dag_dir, output_dir)
    click.echo(f"Timing features extracted to {output_dir}")


@feature.command(name="module-power")
@click.option(
    "--bench",
    required=True,
    help="Name of the benchmark",
)
@click.option(
    "--design-name",
    required=True,
    help="Name of the design",
)
@click.option(
    "--design-hier-json",
    required=True,
    type=click.Path(exists=True, dir_okay=False),
    help="Path to design hierarchy JSON file",
)
@click.option(
    "--module-dir",
    required=True,
    type=click.Path(exists=True, file_okay=False),
    help="Directory containing module pickle files",
)
@click.option(
    "--power-dag-dir",
    required=True,
    type=click.Path(exists=True, file_okay=False),
    help="Directory containing power DAG pickle files",
)
@click.option(
    "--output-dir",
    required=True,
    type=click.Path(file_okay=False),
    help="Output directory for feature JSON files",
)
def extract_module_power(
    bench, design_name, design_hier_json, module_dir, power_dag_dir, output_dir
):
    """Extract module-level power features."""
    from masterrtl.feature_extract.module_power import run_all_hier

    Path(output_dir).mkdir(parents=True, exist_ok=True)
    run_all_hier(bench, design_name, design_hier_json, module_dir, power_dag_dir, output_dir)
    click.echo(f"Module power features extracted to {output_dir}")


@feature.command(name="slack-calibration")
@click.option(
    "--design-name",
    required=True,
    help="Name of the design",
)
@click.option(
    "--node-dict-dir",
    required=True,
    type=click.Path(exists=True, file_okay=False),
    help="Directory containing node dictionary pickle files",
)
@click.option(
    "--pred-slack-dir",
    required=True,
    type=click.Path(exists=True, file_okay=False),
    help="Directory containing predicted slack JSON files",
)
@click.option(
    "--output-dir",
    required=True,
    type=click.Path(file_okay=False),
    help="Output directory for calibrated WNS files",
)
@click.option(
    "--dc-rpt-dir",
    type=click.Path(exists=True, file_okay=False),
    help="Optional directory containing DC timing reports for validation",
)
@click.option(
    "--cmd",
    default="rtlil",
    help="Command type (default: rtlil)",
)
def extract_slack_calibration(
    design_name, node_dict_dir, pred_slack_dir, output_dir, dc_rpt_dir, cmd
):
    """Calibrate predicted slack values and extract WNS."""
    from masterrtl.feature_extract.pred_slack_calibration import run_one_design

    Path(output_dir).mkdir(parents=True, exist_ok=True)
    pred_median_rf, mul_wns_lst = run_one_design(
        design_name, node_dict_dir, pred_slack_dir, output_dir, dc_rpt_dir, cmd
    )
    click.echo(f"Predicted median WNS: {pred_median_rf:.6f}")
    click.echo(f"Multiple WNS estimates: {mul_wns_lst}")
    click.echo(f"Calibrated WNS saved to {output_dir}")


@preproc.command(name="delay")
@click.option(
    "--design-name",
    required=True,
    help="Name of the design",
)
@click.option(
    "--cmd",
    default="sog",
    help="Command type (default: sog)",
)
@click.option(
    "--input-dir",
    required=True,
    type=click.Path(exists=True, file_okay=False),
    help="Directory containing input pickle files",
)
@click.option(
    "--output-dir",
    required=True,
    type=click.Path(file_okay=False),
    help="Output directory for processed files",
)
def preprocess_delay(design_name, cmd, input_dir, output_dir):
    """Process delay propagation for a design."""
    from masterrtl.preproc.delay_propagation import run_one_design

    Path(output_dir).mkdir(parents=True, exist_ok=True)
    run_one_design(design_name, cmd, input_dir, output_dir)
    click.echo(f"Delay propagation completed. Output: {output_dir}")


@preproc.command(name="toggle-rate")
@click.option(
    "--bench",
    required=True,
    help="Name of the benchmark",
)
@click.option(
    "--design-hier-json",
    required=True,
    type=click.Path(exists=True, dir_okay=False),
    help="Path to design hierarchy JSON file",
)
@click.option(
    "--module-dir",
    required=True,
    type=click.Path(exists=True, file_okay=False),
    help="Directory containing module pickle files",
)
@click.option(
    "--init-tr-dir",
    required=True,
    type=click.Path(exists=True, file_okay=False),
    help="Directory containing initial toggle rate files",
)
@click.option(
    "--output-dir",
    required=True,
    type=click.Path(file_okay=False),
    help="Output directory for processed files",
)
def preprocess_toggle_rate(bench, design_hier_json, module_dir, init_tr_dir, output_dir):
    """Process toggle rate propagation for a design module."""
    from masterrtl.preproc.tr_propagate import run_all_hier

    Path(output_dir).mkdir(parents=True, exist_ok=True)
    run_all_hier(bench, design_hier_json, module_dir, init_tr_dir, output_dir)
    click.echo(f"Toggle rate propagation completed. Output: {output_dir}")


@model.command(name="train")
@click.option(
    "--design-name",
    required=True,
    help="Name of the design",
)
@click.option(
    "--ppa-type",
    required=True,
    type=click.Choice(["Area", "TNS", "WNS", "Power"], case_sensitive=False),
    help="PPA metric type to train",
)
@click.option(
    "--feat-dir",
    required=True,
    type=click.Path(exists=True, file_okay=False),
    help="Directory containing feature JSON files",
)
@click.option(
    "--label-dir",
    required=True,
    type=click.Path(exists=True, file_okay=False),
    help="Directory containing label JSON files",
)
@click.option(
    "--output-dir",
    required=True,
    type=click.Path(file_okay=False),
    help="Output directory for trained model",
)
def train_model(design_name, ppa_type, feat_dir, label_dir, output_dir):
    """Train a PPA estimation model."""
    import pickle

    from masterrtl.ml_model.preprocess import load_data
    from masterrtl.ml_model.train import train

    Path(output_dir).mkdir(parents=True, exist_ok=True)

    x, y = load_data(ppa_type, design_name, feat_dir, label_dir)
    trained_model = train(x, y)

    model_path = Path(output_dir) / f"xgboost_{ppa_type}_model.pkl"
    with open(model_path, "wb") as f:
        pickle.dump(trained_model, f)

    click.echo(f"Model trained and saved to {model_path}")


@model.command(name="infer")
@click.option(
    "--design-name",
    required=True,
    help="Name of the design",
)
@click.option(
    "--ppa-type",
    required=True,
    type=click.Choice(["Area", "TNS", "WNS", "Power"], case_sensitive=False),
    help="PPA metric type to predict",
)
@click.option(
    "--feat-dir",
    required=True,
    type=click.Path(exists=True, file_okay=False),
    help="Directory containing feature JSON files",
)
@click.option(
    "--label-dir",
    required=True,
    type=click.Path(exists=True, file_okay=False),
    help="Directory containing label JSON files",
)
@click.option(
    "--model-path",
    required=True,
    type=click.Path(exists=True, dir_okay=False),
    help="Path to trained model pickle file",
)
def infer_model(design_name, ppa_type, feat_dir, label_dir, model_path):
    """Run PPA estimation inference on a design."""
    import pickle

    from masterrtl.ml_model.preprocess import load_data

    with open(model_path, "rb") as f:
        model = pickle.load(f)

    x_test, y_test = load_data(ppa_type, design_name, feat_dir, label_dir)
    y_pred = model.predict(x_test)

    click.echo(f"Predicted {ppa_type}: {y_pred[0]:.6f}")
    if len(y_test) > 0:
        click.echo(f"Actual {ppa_type}: {y_test[0]:.6f}")
        error = abs(y_pred[0] - y_test[0]) / y_test[0] * 100
        click.echo(f"Relative error: {error:.2f}%")


@yosys.command(name="generate-sog")
@click.argument(
    "verilog_files",
    nargs=-1,
    type=click.Path(exists=True, dir_okay=False),
    required=True,
    metavar="VERILOG_FILE",
)
@click.option(
    "--design-name",
    required=True,
    help="Name of the design",
)
@click.option(
    "--output-dir",
    required=True,
    type=click.Path(file_okay=False),
    help="Output directory for SOG Verilog file",
)
def generate_sog_cmd(design_name, verilog_files, output_dir):
    """Generate Simple Operator Graph (SOG) from Verilog files using Yosys."""
    from masterrtl.yosys.generate_sog import generate_sog

    Path(output_dir).mkdir(parents=True, exist_ok=True)

    click.echo(f"Generating SOG for design '{design_name}'...")
    click.echo(f"Input files: {', '.join(verilog_files)}")

    generate_sog(design_name, list(verilog_files), output_dir)

    output_file = Path(output_dir) / f"{design_name}_sog.v"
    click.echo(f"SOG generated and saved to {output_file}")


@yosys.command(name="analyze-verilog")
@click.argument(
    "verilog_files",
    nargs=-1,
    type=click.Path(exists=True, dir_okay=False),
    required=True,
    metavar="VERILOG_FILE",
)
@click.option(
    "--design-name",
    required=True,
    help="Name of the design",
)
@click.option(
    "--cmd",
    default="sog",
    type=click.Choice(["ast", "sog"], case_sensitive=False),
    help="Command type: 'ast' for word-level, 'sog' for bit-level (default: sog)",
)
@click.option(
    "--output-dir",
    type=click.Path(file_okay=False),
    help="Output directory for graph pickle files (default: current directory)",
)
@click.option(
    "--include-path",
    multiple=True,
    type=click.Path(exists=True, file_okay=False),
    help="Include paths for preprocessing (can be specified multiple times)",
)
@click.option(
    "--define",
    multiple=True,
    help="Macro definitions for preprocessing (can be specified multiple times)",
)
def analyze_verilog_cmd(verilog_files, design_name, cmd, output_dir, include_path, define):
    """Analyze Verilog files and convert to graph representation.

    This command parses Verilog files and creates a graph representation that can be
    used for feature extraction and PPA estimation. The graph is saved as pickle files.
    """
    from masterrtl.vlg2ir.analyze_verilog import analyze_verilog

    if output_dir:
        Path(output_dir).mkdir(parents=True, exist_ok=True)

    click.echo(f"Analyzing Verilog files for design '{design_name}'...")
    click.echo(f"Mode: {cmd.upper()} ({'word-level AST' if cmd == 'ast' else 'bit-level SOG'})")
    click.echo(f"Input files: {', '.join(verilog_files)}")

    if include_path:
        click.echo(f"Include paths: {', '.join(include_path)}")
    if define:
        click.echo(f"Macro definitions: {', '.join(define)}")

    analyze_verilog(
        filelist=list(verilog_files),
        design_name=design_name,
        cmd=cmd,
        out_path=output_dir,
        include_paths=list(include_path) if include_path else None,
        define_macros=list(define) if define else None,
    )

    output_location = output_dir if output_dir else "current directory"
    click.echo(f"Graph representation saved to {output_location}")
    click.echo(f"Files: {design_name}_{cmd}.pkl, {design_name}_{cmd}_node_dict.pkl")


if __name__ == "__main__":
    cli()
