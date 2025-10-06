class History:
    def __init__(self, max_items=50):
        self.items = []
        self.max_items = max_items

    def add(self, expr, result):
        self.items.append(f"{expr} = {result}")
        if len(self.items) > self.max_items:
            self.items.pop(0)

    def get_all(self):
        return self.items.copy()

    def clear(self):
        self.items.clear()