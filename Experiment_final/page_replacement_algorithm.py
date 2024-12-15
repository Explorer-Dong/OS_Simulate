class PageReplacementAlgorithm:
    def __init__(self, size):
        self.size = size

    def replace_page(self, memory, page_to_load, page_table, val):
        pass


class FIFO(PageReplacementAlgorithm):
    def __init__(self, size):
        super().__init__(size)
        self.queue = []

    def replace_page(self, memory, page_to_load, page_table, val):
        if page_to_load in self.queue:
            return None

        if len(self.queue) == self.size:
            page_to_replace = self.queue[0]
            page_table['page'][page_to_replace] = None
            self.queue.pop(0)
        
        idx = len(self.queue)
        # print(idx)
        self.queue.append(page_to_load)
        page_table['page'][page_to_load] = page_table['data'][idx]
        
        memory[page_table['page'][page_to_load]] = val
        self.update(page_table)

    def update(self, page_table):
        for i in range(len(self.queue)):
            page_table['page'][self.queue[i]] = page_table['data'][i]


class LRU(PageReplacementAlgorithm):
    def __init__(self, size):
        super().__init__(size)
        self.order = []

    def replace_page(self, memory, page_to_load, page_table, val):
        if page_to_load not in self.order:
            if len(self.order) == self.size:
                page_to_replace = self.order[0]
                page_table['page'][page_to_replace] = None
                self.order.pop(0)

        else:
            idx = self.order.index(page_to_load)
            page_table['page'][idx] = None
            self.order.pop(idx)

        
        idx = len(self.order)
        self.order.append(page_to_load)
        page_table['page'][page_to_load] = page_table['data'][idx]

        memory[page_table['page'][page_to_load]] = val
        self.update(page_table)

    def update(self, page_table):
        for i in range(len(self.order)):
            page_table['page'][self.order[i]] = page_table['data'][i]