class Node:

    def __init__(self, value=None):
        self.value = value
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def get_value(self):
        return self.value

    def __hash__(self):
        return hash(self.value)