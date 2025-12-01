import re

import networkx as nx
import numpy as np

from .directed_graph import DirectedGraph

STD_DATA = {
    "area_seq": {
        "DFF": 4.522,
    },
    "area_comb": {
        "And": 1.064,
        "Land": 1.064,
        "Xor": 1.596,
        "Xnor": 1.596,
        "Uxor": 1.596,
        "Or": 1.064,
        "Unor": 0.798,
        "Lor": 1.064,
        "Uor": 1.064,
        "Unot": 0.798,
        "Ulnot": 0.798,
        "Uand": 1.064,
        "Cond": 1.862,
        "Eq": 0,
        "Concat": 0,
        "Plus": 4.256,
        "Minus": 4.256,
        "Uminus": 4.256,
        "Repeat": 0,
        "Divide": 40,
        "Mod": 35,
        "Times": 37.5,
        "Than": 0,
        "Sra": 3,
        "Sla": 3,
        "Sll": 3,
        "Srl": 3,
        "Case": 1.862,
        "Mux": 1.862,
        "LessThan": 35,
        "GreaterThan": 35,
        "LessEq": 35,
        "GreaterEq": 35,
    },
    "stat_pwr": {
        "DFF": 0.07911,
        "And": 0.02507,
        "Land": 0.02507,
        "Xor": 0.03616,
        "Xnor": 0.03616,
        "Uxor": 0.03616,
        "Or": 0.02269,
        "Unor": 0.01282,
        "Lor": 0.02269,
        "Uor": 0.02269,
        "Unot": 0.106,
        "Ulnot": 0.106,
        "Uand": 0.02269,
        "Cond": 0.03593,
        "Eq": 0,
        "Concat": 0,
        "Plus": 0.07576,
        "Minus": 0.07576,
        "Uminus": 0.07576,
        "Repeat": 0,
        "Divide": 0.1,
        "Mod": 0.1,
        "Times": 0.1,
        "Than": 0,
        "Sra": 0.03,
        "Sla": 0.03,
        "Sll": 0.03,
        "Srl": 0.03,
        "Case": 0.03593,
        "Mux": 0.03593,
        "LessThan": 0.3,
        "GreaterThan": 0.3,
        "LessEq": 0.3,
        "GreaterEq": 0.3,
    },
    "dyn_pwr": {
        "DFF": 3.1,
        "And": 3.1,
        "Or": 3.1,
        "Ulnot": 1.8,
        "Unot": 1.8,
        "Xor": 2.45,
        "Concat": 0,
        "Mux": 2.6,
        "Cond": 2.6,
    },
    "dyn_pwr_all": {
        "DFF": 3.98,
        "And": 5.2,
        "Land": 1.064,
        "Xor": 2.43,
        "Xnor": 2.43,
        "Uxor": 2.43,
        "Or": 2.71,
        "Unor": 1.74,
        "Lor": 2.71,
        "Uor": 2.71,
        "Unot": 4.61,
        "Ulnot": 4.61,
        "Uand": 2.71,
        "Cond": 3.38,
        "Eq": 0,
        "Concat": 0,
        "Plus": 4.95,
        "Minus": 4.95,
        "Uminus": 4.95,
        "Repeat": 0,
        "Divide": 40,
        "Mod": 35,
        "Times": 37.5,
        "Than": 0,
        "Sra": 3,
        "Sla": 3,
        "Sll": 3,
        "Srl": 3,
        "Case": 3.38,
        "Mux": 3.38,
        "LessThan": 35,
        "GreaterThan": 35,
        "LessEq": 35,
        "GreaterEq": 35,
    },
    "timing": {
        "freq": 2,
        "clk_unc": 0.05,
        "lib_setup": 0.032,
        "input_delay": 0,
        "output_delay": 0,
        "DFF": 0.1187,
        "And": 0.0496,
        "Or": 0.0323,
        "Ulnot": 0.0328,
        "Unot": 0.0328,
        "Mux": 0.0498,
        "Cond": 0.0498,
        "Xor": 0.0882,
        "Concat": 0,
    },
}


def cal_oper(g: DirectedGraph):
    g_nx: nx.DiGraph[str] = nx.DiGraph(g.graph)
    g.get_all_nodes2()
    seq_set = set()
    comb_set = set()
    type_set = set()
    seq_num, comb_num, io_num, fanout_sum = 0, 0, 0, 0
    and_num, or_num, not_num, xor_num, mux_num = 0, 0, 0, 0, 0
    seq_area, comb_area, stat_pwr, dyn_pwr = 0, 0, 0, 0
    for name, node in g.node_dict.items():
        if not g_nx.has_node(name):
            continue
        type = node.type
        width = node.width
        type_set.add(type)
        # if type in ['Reg', 'Pointer', 'Partselect']:
        if type in ["Reg"]:
            seq_set.add(name)
            fanout_sum += g_nx.in_degree(name)
            seq_num += width
            seq_area += STD_DATA["area_seq"]["DFF"] * width
            stat_pwr += STD_DATA["stat_pwr"]["DFF"] * width
            dyn_pwr += STD_DATA["dyn_pwr"]["DFF"] * width
        elif type in ["Operator", "UnaryOperator", "Concat", "Repeat"]:
            comb_set.add(name)
            comb_num += width
            op_temp = re.findall(r"([A-Z][a-z]*)(\d+)", name)
            op = op_temp[0][0]
            if op in STD_DATA["area_comb"].keys():
                comb_area += STD_DATA["area_comb"][op] * width
                stat_pwr += STD_DATA["stat_pwr"][op] * width
                dyn_pwr += STD_DATA["dyn_pwr"][op] * width
            else:
                print(op)
                raise AssertionError

            if op in ["And"]:
                and_num += 1
            elif op in ["Or"]:
                or_num += 1
            elif op in ["Ulnot", "Unot"]:
                not_num += 1
            elif op in ["Xor"]:
                xor_num += 1
            elif op in ["Cond", "Mux"]:
                mux_num += 1

        elif type in ["Output", "Input", "Inout"]:
            io_num += width
        elif type in ["Constant", "Wire", "Partselect", "Pointer", "Inout"]:
            pass
        else:
            print(type)
            raise AssertionError
    # ----- comb area -------
    seq_area = round(seq_area, 0)
    comb_area = round(comb_area, 0)
    total_area = seq_area + comb_area
    stat_pwr = round(stat_pwr, 0)
    dyn_pwr = round(dyn_pwr, 0)
    total_pwr = stat_pwr + dyn_pwr
    print(f"f0: #. DFF bits: {seq_num}")
    print(f"f1: #. fanout: {fanout_sum}")
    print(f"f2: #. IO bits: {io_num}")
    print(f"f3: #. AND: {and_num}")
    print(f"f4: #. OR: {or_num}")
    print(f"f5: #. NOT: {not_num}")
    print(f"f6: #. XOR: {xor_num}")
    print(f"f7: #. MUX: {mux_num}")
    print(f"f8: est. seq. area: {seq_area}")
    print(f"f9: est. comb. area: {comb_area}")
    print(f"f10: est. total area: {total_area}")
    print(f"f11: est. stat. pwr: {stat_pwr}")
    print(f"f12: est. dyn. pwr: {dyn_pwr}")
    print(f"f13: est. total pwr: {total_pwr}\n")

    ### 14 features
    feat_vec = [
        seq_num,
        fanout_sum,
        io_num,
        and_num,
        or_num,
        not_num,
        xor_num,
        mux_num,
        seq_area,
        comb_area,
        total_area,
        stat_pwr,
        dyn_pwr,
        total_pwr,
    ]
    return feat_vec


def cal_timing_type(delay_list, path_type):
    delay_sum = np.array(delay_list)

    if path_type == "rr":
        input_delay_array = np.zeros(delay_sum.shape)
        output_delay_array = np.zeros(delay_sum.shape)
    elif path_type == "ir":
        input_delay_array = np.ones(delay_sum.shape) * STD_DATA["timing"]["input_delay"]
        output_delay_array = np.zeros(delay_sum.shape)
    elif path_type == "ro":
        input_delay_array = np.zeros(delay_sum.shape)
        output_delay_array = np.ones(delay_sum.shape) * STD_DATA["timing"]["output_delay"]
    elif path_type == "io":
        input_delay_array = np.ones(delay_sum.shape) * STD_DATA["timing"]["input_delay"]
        output_delay_array = np.ones(delay_sum.shape) * STD_DATA["timing"]["output_delay"]

    require_time = (
        1 / STD_DATA["timing"]["freq"]
        - STD_DATA["timing"]["clk_unc"]
        - STD_DATA["timing"]["lib_setup"]
    )
    require_time_array = np.ones(delay_sum.shape) * require_time - output_delay_array
    arrival_time_array = delay_sum + input_delay_array
    slack_array = require_time_array - arrival_time_array
    slack_array[slack_array > 0] = 0
    return slack_array


def cal_timing(delay_list_all):
    slack_array_total = cal_timing_type(delay_list_all, "rr")
    tns = np.sum(slack_array_total)
    wns = np.min(slack_array_total)

    feat_vec = [wns, tns]
    print("calculated tns:", tns)
    print("calculated wns:", wns)
    return feat_vec
