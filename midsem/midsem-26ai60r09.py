from queue import PriorityQueue

class MedianOfDataStream:
    def __init__(self):
        self.max_heap = PriorityQueue()     # stores values < current median
        self.min_heap = PriorityQueue()     # stores values >= current median

    def print_medians(self, filename):
        """
        Method to fetch median of an incoming data stream.
        Time complexity: O(n * log n); n = size of stream.
        """
        with open(filename, 'r') as file:
            curr_median = None
            print("Value\t\tMedian")

            for line in file:
                vals = line.split(',')
                for val in vals:
                    val = int(val.strip())

                    # insert current value into one of the heaps
                    if curr_median is None:
                        curr_median = val
                        self.min_heap.put(curr_median)
                        # display output
                        print(f"{val}\t\t{curr_median:.1f}")
                        continue                    # skip 1st iteration
                    elif val < curr_median:
                        self.max_heap.put(-val)     # max heap is simulated by negating values
                    else:
                        self.min_heap.put(val)

                    # maintain the size conditions between the heaps
                    if self.max_heap.qsize() > self.min_heap.qsize():
                        temp = -self.max_heap.get()
                        self.min_heap.put(temp)
                    elif self.max_heap.qsize() + 1 < self.min_heap.qsize():
                        temp = self.min_heap.get()
                        self.max_heap.put(-temp)

                    # fetch the current median
                    if self.max_heap.qsize() == self.min_heap.qsize():
                        curr_median = (-self.max_heap.queue[0] + self.min_heap.queue[0]) / 2
                    else:                                                
                        curr_median = self.min_heap.queue[0]

                    # display output
                    print(f"{val}\t\t{curr_median:.1f}")
    

if __name__ == "__main__":
    filename = input("Enter input file path of data stream: ")
    mds = MedianOfDataStream()
    try:
        mds.print_medians(filename)
    except Exception as e:
        print(e)