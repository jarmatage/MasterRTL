class DirectedGraphSubNode:
    def __init__(self, name, type, width: int | None = None, delay: int = 0):
        self.name = name
        self.type = type
        self.width: int = 1 if width is None else width
        self.delay = delay

    def update_width(self, width):
        self.width = width

    def __repr__(self):
        return self.name
