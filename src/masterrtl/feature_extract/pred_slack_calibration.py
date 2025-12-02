import json
import pickle
import re

import matplotlib.pyplot as plt
import numpy as np


def get_wns_median_based_on_scale(pred_lst, seq_num):
    seq_num = seq_num / 1000  ### k
    sorted_pred_lst = sorted(pred_lst, reverse=True)
    # print(sorted_pred_lst)
    # exit()
    if seq_num <= 3:
        idx = round(len(sorted_pred_lst) * 0.1)
    elif 3 < seq_num <= 5:
        idx = round(len(sorted_pred_lst) * 0.5)
    elif seq_num > 5:
        idx = round(len(sorted_pred_lst) * 0.9)
    ret_wns = sorted_pred_lst[idx]
    print("Pred Final WNS: ", ret_wns)
    return ret_wns


def get_mul_wns(pred_lst):
    sorted_pred_lst = sorted(pred_lst, reverse=True)

    idx = round(len(sorted_pred_lst) * 0.1)
    ret_wns1 = sorted_pred_lst[idx]
    idx = round(len(sorted_pred_lst) * 0.5)
    ret_wns2 = sorted_pred_lst[idx]
    idx = round(len(sorted_pred_lst) * 0.9)
    ret_wns3 = sorted_pred_lst[idx]
    ret_lst = [ret_wns1, ret_wns2, ret_wns3]
    return ret_lst


def get_seq_num(node_dict):
    seq_num, comb_num, total_num = 0, 0, 0
    for node in node_dict.values():
        type = node.type
        width = node.width
        if type in ["Reg"]:
            seq_num += width
        elif type in ["Operator", "UnaryOperator", "Concat", "Repeat"]:
            comb_num += width
    total_num = seq_num + comb_num
    return seq_num, total_num


def get_dc_lst_from_dir(design_name, vec_len, dc_rpt_dir):
    """Load DC timing report slack values.

    Args:
        design_name: Name of the design
        vec_len: Number of slack values to return
        dc_rpt_dir: Directory containing DC timing reports
    """
    slack_lst = []
    with open(f"{dc_rpt_dir}/{design_name}.rpt") as f:
        lines = f.readlines()
    for line in lines:
        slk = re.findall(r"(\s*)slack(\s*)\((\w+)\)(\s*)(.*)", line, re.IGNORECASE)
        slk2 = re.findall(
            r"(\s*)slack(\s*)\(VIOLATED: increase significant digits\)(\s*)(.*)",
            line,
            re.IGNORECASE,
        )
        if "slack" in line:
            if slk:
                slack = float(slk[0][-1])
                slack_lst.append(slack)
            elif slk2:
                slack = float(slk2[0][-1])
                slack_lst.append(slack)
            else:
                print(line)

    ret_lst = slack_lst[:vec_len]
    return ret_lst


def draw_fig(dc_lst, pred_lst_rf, pred_lst_trans, design_name):
    plt.clf()
    plt.hist(dc_lst, alpha=1, label="DC")
    plt.hist(pred_lst_rf, alpha=0.4, label="Random Forest")
    plt.hist(pred_lst_trans, alpha=0.4, label="Transformer")
    plt.legend(loc="upper left")
    plt.savefig(f"/data/user/AST_analyzer/histogram/fig/{design_name}.png", dpi=300)


def run_one_design(
    design_name,
    node_dict_dir,
    pred_slack_dir,
    output_dir,
    dc_rpt_dir=None,
    cmd="rtlil",
    max_seq: int = 0,
    min_seq: int = 1000000000000,
):
    """Run slack calibration for a design.

    Args:
        design_name: Name of the design
        node_dict_dir: Directory containing node dictionary pickle files
        pred_slack_dir: Directory containing predicted slack JSON files
        output_dir: Output directory for calibrated WNS files
        dc_rpt_dir: Optional directory containing DC timing reports for validation
        cmd: Command type (default: rtlil)
        max_seq: Maximum sequence number (default: 0)
        min_seq: Minimum sequence number (default: 1000000000000)
    """
    save_list_all = []
    with open(f"{node_dict_dir}/{design_name}_{cmd}_node_dict_init.pkl", "rb") as f:
        node_dict = pickle.load(f)
    seq_num, total_num = get_seq_num(node_dict)
    print(seq_num)
    max_seq = max(seq_num, max_seq)
    min_seq = min(seq_num, min_seq)

    vec_len = seq_num * 0.02
    if vec_len > 1000:
        vec_len = 1000
    elif vec_len < 10:
        vec_len = 100
    else:
        vec_len = round(vec_len)

    with open(f"{pred_slack_dir}/{design_name}_rf.json") as f:
        pred_slack_lst_rf = json.load(f)

    vec_len = min([vec_len, len(pred_slack_lst_rf)])
    pred_slack_lst_rf = pred_slack_lst_rf[:vec_len]

    print("Pred Median WNS: ", np.median(pred_slack_lst_rf))
    pred_median_rf = get_wns_median_based_on_scale(pred_slack_lst_rf, seq_num)

    # If DC report directory is provided, validate predictions
    if dc_rpt_dir:
        dc_slack_lst = get_dc_lst_from_dir(design_name, vec_len, dc_rpt_dir)
        print("Real WNS: ", max(dc_slack_lst))
        dc_wns = min(dc_slack_lst)
        pred_mean_rf = np.mean(pred_slack_lst_rf)
        save_lst = [dc_wns, pred_median_rf, pred_mean_rf]
        save_list_all.append(save_lst)

    # Save calibrated WNS
    with open(f"{output_dir}/{design_name}_rf.json", "w") as f:
        json.dump([pred_median_rf], f)

    mul_wns_lst = get_mul_wns(pred_slack_lst_rf)
    with open(f"{output_dir}/{design_name}_rf_mul.json", "w") as f:
        json.dump(mul_wns_lst, f)

    return pred_median_rf, mul_wns_lst


def run_all(
    design_json,
    bench,
    node_dict_dir,
    pred_slack_dir,
    output_dir,
    dc_rpt_dir=None,
    design_name=None,
):
    """Run slack calibration for all designs in a benchmark.

    Args:
        design_json: Path to design JSON file
        bench: Benchmark name
        node_dict_dir: Directory containing node dictionary pickle files
        pred_slack_dir: Directory containing predicted slack JSON files
        output_dir: Output directory for calibrated WNS files
        dc_rpt_dir: Optional directory containing DC timing reports
        design_name: Optional specific design name to process
    """
    with open(design_json) as f:
        design_data = json.load(f)
        bench_data = design_data[bench]
    for k in bench_data:
        if design_name:
            if k == design_name:
                print("Current Design:", k)
                run_one_design(k, node_dict_dir, pred_slack_dir, output_dir, dc_rpt_dir)
        else:
            print("Current Design:", k)
            run_one_design(k, node_dict_dir, pred_slack_dir, output_dir, dc_rpt_dir)
