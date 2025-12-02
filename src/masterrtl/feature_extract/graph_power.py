import json


def run_one_design(design_name, cmd, feat_dir, toggle_rate_dir, out_path):
    """Extract power features from a design.

    Args:
        design_name: Name of the design
        cmd: Command type (e.g., 'sog')
        feat_dir: Directory containing feature JSON files
        toggle_rate_dir: Directory containing toggle rate JSON files
        out_path: Output directory for feature JSON files
    """
    with open(f"{feat_dir}/{design_name}_{cmd}_vec_area.json") as f:
        feat_vec = json.load(f)

    with open(f"{toggle_rate_dir}/{design_name}_tc_sum_all.json") as f:
        tr_sum = json.load(f)
        feat_vec.append(tr_sum)

    with open(f"{toggle_rate_dir}/{design_name}_tc_avr_all.json") as f:
        tr_avr = json.load(f)
        feat_vec.append(tr_avr)

    ### ---- load the prediction of module level power 'pred_pwr' ---- ###
    pred_pwr = 0
    ######################################################################

    feat_vec.append(pred_pwr)

    print(feat_vec)
    vec_name = out_path + f"/{design_name}_{cmd}_vec_pwr.json"
    with open(vec_name, "w") as f:
        json.dump(feat_vec, f)
