#!/bin/bash

masterrtl yosys generate-sog \
    --design-name Rocket \
    --output-dir results \
    verilog/TinyRocket/plusarg_reader.v \
    verilog/TinyRocket/chipyard.TestHarness.TinyRocketConfig.top.v

masterrtl yosys analyze-verilog \
    --design-name Rocket \
    --output-dir results/ \
    results/Rocket_sog.v

masterrtl preproc delay \
    --design-name Rocket \
    --input-dir results/ \
    --output-dir results/timing_dag/

masterrtl preproc toggle-rate \
    --bench chipyard \
    --design-hier-json design_hier.json \
    --module-dir module/TinyRocket/ \
    --init-tr-dir module/TinyRocket_init_tr/ \
    --output-dir results/power_dag/
