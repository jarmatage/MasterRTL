import json
import pickle
import time

import networkx as nx

from masterrtl.vlg2ir.directed_graph import DirectedGraph
from masterrtl.vlg2ir.graph_processor import GraphProcessor
from masterrtl.vlg2ir.graph_stat import cal_timing

from .train_path_rfr import train_rfr


def run_one_design(design_name, cmd, out_path):
    folder_dir = "../../example/timing_dag"
    with open(f"{folder_dir}/{design_name}_{cmd}.pkl", "rb") as f:
        graph = pickle.load(f)
    with open(f"{folder_dir}/{design_name}_{cmd}_node_dict_init.pkl", "rb") as f:
        node_dict = pickle.load(f)
    graph = nx.to_dict_of_lists(graph)

    g = DirectedGraph()
    g.init_graph(graph, node_dict)
    graphProc = GraphProcessor(g)
    start_time = time.perf_counter()

    ### ---- load the path-level model 'rfr' ---- ###
    # with open('/home/coguest5/MasterRTL/ML_model/saved_model/rfr_model.pkl', 'rb') as f:
    #         rfr = pickle.load(f)
    rfr = train_rfr()
    ######################################################################

    sta_result = graphProc.Graph_STA(rfr, design_name)
    if sta_result is None:
        raise AssertionError(f"STA failed for {design_name}")
    delay_list_all, wns_list = sta_result
    end_time = time.perf_counter()
    runtime = round((end_time - start_time), 2)
    print(f"Timing STA Runtime of {design_name}: {runtime} seconds")

    feat_timing = cal_timing(delay_list_all)
    wns_pred = feat_timing[0]
    tns_pred = feat_timing[1]
    print(f"Predicted WNS: {wns_pred}")
    print(f"Predicted TNS: {tns_pred}")

    with open(f"{out_path}/{design_name}_{cmd}_vec_timing.json", "w") as f:
        json.dump(feat_timing, f)

    print(design_name + " Finish!")
