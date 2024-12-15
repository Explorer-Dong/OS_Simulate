from space import Space


class FirstFit(object):
    def __init__(self, maxLength=1024 * 1024):
        self.head = Space(status='NULL')
        self.tail = Space(status='NULL')
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
        space: Space = self.head.next
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
        print('-' * 50)

    def tolist(self):
        space = self.head.next
        result = []
        while space is not self.tail:
            result.append((space.start_address, space.length, space.job, space.status))
            space = space.next
        return result


if __name__ == "__main__":
    first_fit = FirstFit(20)

    first_fit.allocate(10, "Job1")
    first_fit.print_space_list()

    first_fit.allocate(8, "Job2")
    first_fit.print_space_list()

    first_fit.free("Job1")
    first_fit.print_space_list()

    first_fit.allocate(5, "Job3")
    first_fit.print_space_list()
