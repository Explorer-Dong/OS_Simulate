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
            self.length += self.next.length
            space = self.next
            self.next = space.next
            self.next.prev = self
            space.next = None
            space.prev = None
            del space
        if self.prev.isFree():
            self.length += self.prev.length
            space = self.prev
            self.prev = space.prev
            self.prev.next = self
            space.prev = None
            space.next = None
            del space

    def isSatisfied(self, length):
        return self.isFree() and self.length >= length


class FirstFit(object):
    def __init__(self, maxLength=1024*1024):
        self.head = Space(length=-1)
        self.tail = Space(length=-1)
        space = Space(length=maxLength)
        space.prev = self.head
        space.next = self.tail
        self.head.next = space
        self.tail.prev = space

    def allocate(self, length, job):
        space = self.head.next
        while space is not self.tail:
            if space.isSatisfied(length):
                space.allocate(length, job)
                return
            space = space.next

    def free(self, job):
        space = self.head.next
        while space is not self.tail:
            if space.job == job:
                break
            space = space.next
        if space is self.tail:
            return 1, "Job not found"
        space.free()
        return 0, "Success"

    def print_space_list(self):
        space = self.head.next
        while space is not self.tail:
            print(
                "Start Address: {}, Length: {}, Job: {}, Status: {}".format(
                    space.start_address, space.length, space.job, space.status
                )
            )
            space = space.next


if __name__ == "__main__":
    first_fit = FirstFit()
    first_fit.allocate(10, "Job1")
    first_fit.allocate(5, "Job2")
    first_fit.allocate(3, "Job3")
    first_fit.allocate(7, "Job4")
    first_fit.print_space_list()
    print('-'*50)
    first_fit.free("Job2")
    first_fit.free("Job3")
    first_fit.print_space_list()
