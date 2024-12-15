from space import Space
from first_fit import FirstFit


class NextFit(FirstFit):
    def __init__(self, maxLength=1024 * 1024):
        super().__init__(maxLength=maxLength)
        self.now_space: Space = self.head.next  # 上一次查询结束指向的空间

    def allocate(self, length, job):
        search_all = self.now_space == self.head.next
        while self.now_space != self.tail:
            if self.now_space.isSatisfied(length):
                self.now_space.allocate(length, job)
                return
            self.now_space = self.now_space.next
        if not search_all:
            self.now_space = self.head.next
            self.allocate(length, job)


if __name__ == "__main__":
    # 注意：暂不支持立刻释放刚刚申请的内存空间
    next_fit = NextFit(20)
    next_fit.allocate(7, 'Job1')
    next_fit.print_space_list()

    next_fit.allocate(4, 'Job2')
    next_fit.print_space_list()

    next_fit.free('Job1')
    next_fit.print_space_list()

    next_fit.allocate(5, 'Job3')
    next_fit.print_space_list()
