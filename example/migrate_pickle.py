import os
import pickle


# --- Custom Unpickler that remaps old module paths ---
class RenameUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        # Add your old→new mappings here
        if module == "DG" and name == "Node":
            from masterrtl.vlg2ir.directed_graph_node import DirectedGraphNode

            return DirectedGraphNode
        # Example: remap another class
        if module == "DG" and name == "Graph":
            from masterrtl.vlg2ir.directed_graph import DirectedGraph

            return DirectedGraph
        # Fallback to default behavior
        return super().find_class(module, name)


def load_with_remap(path):
    with open(path, "rb") as f:
        return RenameUnpickler(f).load()


def save_with_new(path, obj):
    with open(path, "wb") as f:
        pickle.dump(obj, f)


# --- Batch conversion ---
input_dir = "/home/jarmatag/repos/MasterRTL/example/module/TinyRocket_init_tr"
output_dir = "/home/jarmatag/repos/MasterRTL/example/module/TinyRocket_init_tr_converted"
os.makedirs(output_dir, exist_ok=True)

for fname in os.listdir(input_dir):
    if fname.endswith(".pkl"):
        in_path = os.path.join(input_dir, fname)
        out_path = os.path.join(output_dir, fname)

        print(f"Converting {in_path} -> {out_path}")
        obj = load_with_remap(in_path)
        save_with_new(out_path, obj)
