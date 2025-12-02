import json

import numpy as np

bench_type = "timing"
feat_type = "feat_timing"


def load_data(label_tpe, design_name, feat_dir, label_dir):
    """Load data for model inference.

    Args:
        label_tpe: Type of label (Area, TNS, WNS, Power)
        design_name: Name of the design
        feat_dir: Directory containing feature JSON files
        label_dir: Directory containing label JSON files
    """
    if label_tpe == "Area":
        return load_data_area(label_tpe, design_name, feat_dir, label_dir)
    elif label_tpe in ["TNS", "WNS"]:
        return load_data_timing(label_tpe, design_name, feat_dir, label_dir)
    elif label_tpe == "Power":
        return load_data_power(label_tpe, design_name, feat_dir, label_dir)
    raise ValueError(f"Unknown label type: {label_tpe}")


def load_data_area(label_tpe, design_name, feat_dir, label_dir):
    """Load area data for a design.

    Args:
        label_tpe: Type of label
        design_name: Name of the design
        feat_dir: Directory containing feature JSON files
        label_dir: Directory containing label JSON files
    """

    with open(f"{feat_dir}{design_name}_sog_vec_area.json") as f:
        feat_design_lst = json.load(f)
    test_feat_lst = []
    test_feat_lst.extend(feat_design_lst)

    with open(f"{label_dir}{design_name}.json") as f:
        label_dct = json.load(f)
    label = label_dct[label_tpe]
    test_label_lst = [label]

    test_x = np.array(test_feat_lst).reshape(1, -1)
    test_y = np.array(test_label_lst)

    return test_x, test_y


def load_data_timing(label_tpe, design_name, feat_dir, label_dir):
    """Load timing data for a design.

    Args:
        label_tpe: Type of label (TNS or WNS)
        design_name: Name of the design
        feat_dir: Directory containing feature JSON files
        label_dir: Directory containing label JSON files
    """

    with open(f"{feat_dir}{design_name}_sog_vec_timing.json") as f:
        feat_timing_lst = json.load(f)
    with open(f"{feat_dir}{design_name}_sog_vec_area.json") as f:
        feat_design_lst = json.load(f)
    test_feat_lst = []
    test_feat_lst.extend(feat_design_lst)
    test_feat_lst.extend(feat_timing_lst)

    with open(f"{label_dir}{design_name}.json") as f:
        label_dct = json.load(f)
    label = label_dct[label_tpe]
    test_label_lst = [label]

    test_x = np.array(test_feat_lst).reshape(1, -1)
    test_y = np.array(test_label_lst)

    return test_x, test_y


def load_data_power(label_tpe, design_name, feat_dir, label_dir):
    """Load power data for a design.

    Args:
        label_tpe: Type of label
        design_name: Name of the design
        feat_dir: Directory containing feature JSON files
        label_dir: Directory containing label JSON files
    """

    with open(f"{feat_dir}{design_name}_sog_vec_pwr.json") as f:
        feat_design_lst = json.load(f)
    test_feat_lst = []
    test_feat_lst.extend(feat_design_lst)

    with open(f"{label_dir}{design_name}.json") as f:
        label_dct = json.load(f)
    label = label_dct[label_tpe]
    test_label_lst = [label]

    test_x = np.array(test_feat_lst).reshape(1, -1)
    test_y = np.array(test_label_lst)

    return test_x, test_y


def draw_fig_kf(title, y_pred, y_test, method, train_test):
    pass
