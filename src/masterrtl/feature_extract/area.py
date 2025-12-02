import json
import pickle

from masterrtl.vlg2ir.directed_graph import DirectedGraph
from masterrtl.vlg2ir.graph_stat import cal_oper


def run_one_design(design_name, cmd, input_dir, out_path):
    """Extract area features from a design.

    Args:
        design_name: Name of the design
        cmd: Command type (e.g., 'sog')
        input_dir: Directory containing the input pickle files
        out_path: Output directory for feature JSON files
    """
    print("Current Design:", design_name)
    with open(f"{input_dir}/{design_name}_{cmd}.pkl", "rb") as f:
        graph = pickle.load(f)
    with open(f"{input_dir}/{design_name}_{cmd}_node_dict.pkl", "rb") as f:
        node_dict = pickle.load(f)
    g = DirectedGraph()
    g.init_graph(graph, node_dict)
    feat_vec = cal_oper(g)
    vec_name = out_path + f"/{design_name}_{cmd}_vec_area.json"
    with open(vec_name, "w") as f:
        json.dump(feat_vec, f)
