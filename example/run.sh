#!/bin/bash

echo "Process RTL"
masterrtl yosys generate-sog \
    --design-name Rocket \
    --output-dir results \
    verilog/TinyRocket/plusarg_reader.v \
    verilog/TinyRocket/chipyard.TestHarness.TinyRocketConfig.top.v
