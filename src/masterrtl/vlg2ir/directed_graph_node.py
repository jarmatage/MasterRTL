import re


class DirectedGraphNode:
    def __init__(self, name, type, width: None, father: None):
        self.name = name
        self.type = type
        self.width = width
        self.father = father
        self.path: list[str] = []
        self.tr: float | None = None
        self.t1 = 0.5

    def update_width(self, width):
        self.width = width

    def update_delay(self, delay):
        self.delay = delay

    def update_fanout(self, fanout):
        self.fanout = fanout

    def update_feature(self, feat):
        self.feat = feat

    def update_AT(self, AT_delay, path, visited=False):
        if visited:
            # self.AT = max(self.AT-self.delay, AT_delay) + self.delay
            if self.AT - self.delay < AT_delay:
                self.AT = AT_delay
                self.path = path

        else:
            self.AT = AT_delay + self.delay
            path_copy = path.copy()
            path_copy.append(self.name)
            self.path = path_copy

    def update_AT_transformer(self, AT_delay, path, fanout_num, visited=False):
        if visited:
            # self.AT = max(self.AT-self.delay, AT_delay) + self.delay
            if self.AT - self.delay < AT_delay:
                self.AT = AT_delay
                self.path = path

        else:
            self.AT = AT_delay + self.delay
            path_copy = path.copy()
            path_copy.append(self.name)
            self.path = path_copy

    def finish_AT(self):
        if self.path[-1] != self.name:
            self.path.append(self.name)
            self.AT += self.delay
        p_s = re.sub(r"_CK_$", "", self.path[-1])
        p_s = re.sub(r"_Q_$", "", p_s)
        p_e = re.sub(r"_CK_$", "", self.path[0])
        p_e = re.sub(r"_Q_$", "", p_e)
        pair = (p_s, p_e)

        return pair, self.path, self.AT

    def add_tr(self, tr):
        self.tr = tr

    def add_t1(self, t1):
        self.t1 = t1

    def __repr__(self):
        return self.name
