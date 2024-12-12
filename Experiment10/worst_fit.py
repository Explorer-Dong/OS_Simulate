from space import Space
from first_fit import FirstFit

class WorstFit(FirstFit):
    def __init__(self, maxLength=1024*1024):
        super().__init__(maxLength=maxLength)
    
    def allocate(self, length, job):
        space: Space = self.head.next
        target_space: Space = None
        while space is not self.tail:
            if space.isSatisfied(length):
                if target_space is None or space.length > target_space.length:
                    target_space = space
            space = space.next
        if target_space:
            target_space.allocate(length, job)

if __name__ == "__main__":
    worst_fit = WorstFit(20)
    
    worst_fit.allocate(6, "Job1")
    worst_fit.print_space_list()

    worst_fit.allocate(7, "Job2")
    worst_fit.print_space_list()
    
    worst_fit.free("Job1")
    worst_fit.print_space_list()

    worst_fit.allocate(5, "Job3")
    worst_fit.print_space_list()
