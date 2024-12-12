class Space(object):
    def __init__(
        self, start_address=0, length=0, job=None, status="Free",
    ):
        self.start_address = start_address
        self.length = length
        self.job = job
        self.status = status
        self.prev = None
        self.next = None

    def isFree(self):
        return self.status == "Free"

    def isAllocated(self):
        return self.status == "Allocated"

    def allocate(self, length, job):
        if length > self.length:
            print("Not enough space available")
            return None
        new_space = Space(
            start_address=self.start_address,
            length=length,
            job=job,
            status="Allocated",
        )
        self.prev.next = new_space
        new_space.prev = self.prev
        self.prev = new_space
        new_space.next = self
        self.start_address += length
        self.length -= length
        return new_space

    def free(self):
        self.status = "Free"
        self.job = None
        if self.next.isFree():
            # 将下一个结点合并到当前结点
            self.length += self.next.length
            self.next = self.next.next
            self.next.prev = self
        if self.prev.isFree():
            # 将上一个结点合并到当前结点
            self.length += self.prev.length
            self.prev = self.prev.prev
            self.prev.next = self

    def isSatisfied(self, length):
        return self.isFree() and self.length >= length
