#!/usr/bin/env python3
"""
Example script showing how to use the refactored MasterRTL functions programmatically.

This script demonstrates:
1. Feature extraction for area, power, and timing
2. Model training
3. Model inference

For command-line usage, see REFACTORING.md
"""

import pickle
from pathlib import Path


def example_area_extraction():
    """Extract area features for a design."""
    from masterrtl.feature_extract.area import run_one_design

    design_name = "TinyRocket"
    cmd = "sog"
    input_dir = "example/sog"
    output_dir = "example/feature"

    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    print(f"Extracting area features for {design_name}...")
    run_one_design(design_name, cmd, input_dir, output_dir)
    print(f"✓ Area features saved to {output_dir}/{design_name}_{cmd}_vec_area.json")


def example_power_extraction():
    """Extract power features for a design."""
    from masterrtl.feature_extract.graph_power import run_one_design

    design_name = "TinyRocket"
    cmd = "sog"
    feat_dir = "example/feature"
    toggle_rate_dir = "example/verilog/toggle_rate"
    output_dir = "example/feature"

    print(f"Extracting power features for {design_name}...")
    run_one_design(design_name, cmd, feat_dir, toggle_rate_dir, output_dir)
    print(f"✓ Power features saved to {output_dir}/{design_name}_{cmd}_vec_pwr.json")


def example_timing_extraction():
    """Extract timing features for a design."""
    from masterrtl.feature_extract.feature_extra_graph_STA import run_one_design

    design_name = "TinyRocket"
    cmd = "sog"
    timing_dag_dir = "example/timing_dag"
    output_dir = "example/feature"

    print(f"Extracting timing features for {design_name}...")
    run_one_design(design_name, cmd, timing_dag_dir, output_dir)
    print(f"✓ Timing features saved to {output_dir}/{design_name}_{cmd}_vec_timing.json")


def example_delay_preprocessing():
    """Preprocess delay propagation for a design."""
    from masterrtl.preproc.delay_propagation import run_one_design

    design_name = "TinyRocket"
    cmd = "sog"
    input_dir = "example/sog"
    output_dir = "example/timing_dag"

    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    print(f"Processing delay propagation for {design_name}...")
    run_one_design(design_name, cmd, input_dir, output_dir)
    print(f"✓ Delay propagation completed. Output: {output_dir}")


def example_model_training():
    """Train a PPA estimation model."""
    from masterrtl.ml_model.preprocess import load_data
    from masterrtl.ml_model.train import train

    design_name = "TinyRocket"
    ppa_type = "Area"  # Can be: Area, TNS, WNS, Power
    feat_dir = "example/feature/"
    label_dir = "example/label/"
    model_dir = "example/saved_model/"

    # Create model directory if it doesn't exist
    Path(model_dir).mkdir(parents=True, exist_ok=True)

    print(f"Training {ppa_type} model for {design_name}...")

    # Load data
    x, y = load_data(ppa_type, design_name, feat_dir, label_dir)
    print(f"  Loaded {len(x)} training samples")

    # Train model
    trained_model = train(x, y)

    # Save model
    model_path = Path(model_dir) / f"xgboost_{ppa_type}_model.pkl"
    with open(model_path, "wb") as f:
        pickle.dump(trained_model, f)

    print(f"✓ Model trained and saved to {model_path}")


def example_model_inference():
    """Run PPA estimation inference on a design."""
    from masterrtl.ml_model.preprocess import load_data

    design_name = "TinyRocket"
    ppa_type = "Area"  # Can be: Area, TNS, WNS, Power
    feat_dir = "example/feature/"
    label_dir = "example/label/"
    model_path = "example/saved_model/xgboost_Area_model.pkl"

    print(f"Running {ppa_type} inference for {design_name}...")

    # Load model
    with open(model_path, "rb") as f:
        model = pickle.load(f)

    # Load test data
    x_test, y_test = load_data(ppa_type, design_name, feat_dir, label_dir)

    # Run prediction
    y_pred = model.predict(x_test)

    print(f"  Predicted {ppa_type}: {y_pred[0]:.6f}")
    if len(y_test) > 0:
        print(f"  Actual {ppa_type}: {y_test[0]:.6f}")
        error = abs(y_pred[0] - y_test[0]) / y_test[0] * 100
        print(f"  Relative error: {error:.2f}%")

    print("✓ Inference completed")


def example_custom_design():
    """Example showing how to use the functions with a custom design."""

    # Configuration for your custom design
    design_name = "MyCustomProcessor"
    input_dir = "my_designs/MyCustomProcessor/sog"
    output_dir = "my_designs/MyCustomProcessor/features"

    # Create output directory
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    print(f"\nExample: Processing custom design '{design_name}'")
    print(f"  Input directory: {input_dir}")
    print(f"  Output directory: {output_dir}")

    # Note: This will fail if the input files don't exist
    # Uncomment to run with your actual design files:
    # extract_area(design_name, cmd, input_dir, output_dir)

    print("  (Skipped - input files don't exist)")


if __name__ == "__main__":
    print("=" * 70)
    print("MasterRTL Refactored API Examples")
    print("=" * 70)

    print("\n1. Feature Extraction Examples:")
    print("-" * 70)

    # Uncomment the examples you want to run:
    # Note: These require the example files to exist

    # example_area_extraction()
    # example_power_extraction()
    # example_timing_extraction()

    print("\n2. Preprocessing Examples:")
    print("-" * 70)

    # example_delay_preprocessing()

    print("\n3. Model Training Example:")
    print("-" * 70)

    # example_model_training()

    print("\n4. Model Inference Example:")
    print("-" * 70)

    # example_model_inference()

    print("\n5. Custom Design Example:")
    print("-" * 70)

    example_custom_design()

    print("\n" + "=" * 70)
    print("Note: Uncomment the function calls in this script to run examples")
    print("Make sure the required input files exist before running")
    print("=" * 70)
