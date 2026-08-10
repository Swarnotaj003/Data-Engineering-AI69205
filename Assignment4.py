"""
ASSIGNMENT 4

You are given a text file with a set of sentences (one sentence in one line). Your
goal is to produce dictionary of the following form generated from the file (one
line for one word).
word, total count, number of lines with the word

You must make sure the words are sorted based on descending order of total
frequency. You need to use heap data structure to achieve this goal. In other
words, you repeatedly insert words into a heap one by one. Once you finished
reading the file, you need to produce the sorted list (descending order) of words
based on word count.

When you are getting words from the lines, the word splitting must happen in
any non-alphanumeric character. All words must be in lowercase.
The data file is shared in the moodle.

Input format: Your program will take the file with the sentences as the input.
Output: It will produce output on screen.

Important note: You must not use any inbuilt library such as python dictionary.
If you use any other data structure that has higher time complexity than heap,
you will get 50% credit.
"""

class MaxHeap:
    def __init__(self, capacity):
        self.capacity = capacity
        self.idx = 0
        # arr stores [word, total count, no. of lines with the word] element
        self.arr = [[] for _ in range(capacity)] 

    def size(self):
        return self.idx  

    def parent(self, i):
        return (i - 1) // 2

    def left(self, i):
        return 2 * i + 1

    def right(self, i):
        return 2 * i + 2

    def swap(self, i, j):
        self.arr[i], self.arr[j] = self.arr[j], self.arr[i]
 
    def maxHeapify(self, i):
        max = i
        left = self.left(i)
        right = self.right(i)
        # compare based on total word count
        if left < self.idx and self.arr[left][1] > self.arr[max][1]:
            max = left
        if right < self.idx and self.arr[right][1] > self.arr[max][1]:
            max = right
        if max != i:
            self.swap(max, i)
            self.maxHeapify(max)   

    def insert(self, word, count, lines):
        if self.idx >= self.capacity:
            raise OverflowError("Max heap is full!")
        self.arr[self.idx] = [word, count, lines]
        self.idx += 1
        i = self.idx - 1
        # bubble up to maintain heap property
        while i > 0 and self.arr[self.parent(i)][1] < self.arr[i][1]:
            p = self.parent(i)
            self.swap(i, p)
            i = p

    def peekMax(self):
        if self.idx == 0:
            raise IndexError("Max heap is empty")
        maxVal = self.arr[0]
        return maxVal

    def extractMax(self):
        if self.idx == 0:
            raise IndexError("Max heap is empty")
        maxVal = self.arr[0]
        self.swap(0, self.idx - 1)
        self.idx -= 1
        self.maxHeapify(0)
        return maxVal


class HashMap:
    def __init__(self, capacity):
        self.n = 0
        self.capacity = capacity
        # map[hash(word) % capacity] = ["word", total count, no. of lines with the word]
        self.map = [[] for _ in range(capacity)]

    def compute_hash(self, key):
        p = 31
        mod = 1e9 + 7
        pow = 1
        hash_val = 0
        for ch in key:
            char_val = ord(ch) - ord('a') + 1
            hash_val = (hash_val + char_val * pow) % mod
            pow = (pow * p) % mod
        return int(hash_val)

    def get_id(self, key):
        # calculate hash address
        idx = self.compute_hash(key) % self.capacity
        return idx

    def contains_key(self, key):
        idx = self.get_id(key)
        return len(self.map[idx]) > 0

    def put(self, key, count = 1, lines = 0):
        if self.n >= self.capacity:
            raise OverflowError('HashMap is full!')
        idx = self.get_id(key)
        # use linear probing to handle collision
        while len(self.map[idx]) > 0:
            idx = (idx + 1) % self.capacity
        # insert in the empty slot
        self.map[idx] = [key, count, lines]
        self.n += 1

    def get(self, key):
        idx = self.get_id(key)
        if not self.contains_key(key):
            raise KeyError('Key not found!')
        return self.map[idx]

    def increment(self, key, val_idx):
        """
        val_idx = 1 => update word count
        val_idx = 2 => update lines count
        """ 
        if val_idx != 1 and val_idx != 2:
            raise ValueError('val_idx must be 1 or 2!')
        if not self.contains_key(key):
            raise KeyError('Key not found!')
        idx = self.get_id(key)
        self.map[idx][val_idx] += 1


class Solution:
    def build_dictionary(filename):
        """
        Method to build dictionary of words from a text file
        """
        hashmap = HashMap(capacity=5000)    # to store count and lines of each unique word
        maxheap = MaxHeap(capacity=5000)    # to maintain ordering of words by word count
        dictionary = []                     # to store all the words in descending order of word count

        # read the file and count words using hash-map
        with open(filename, 'r') as file:
            for line in file:
                # replace all non-alphanumeric chars by '$'
                processed_line = ''
                for i in range(len(line)):
                    if line[i].isalnum():
                        processed_line += line[i]
                    else:
                        processed_line += '$'
                line = processed_line

                # split the line by '$'
                words = line.split('$')

                # convert words into lowercase & ignore empty words
                processed_words = []
                for word in words:
                    if len(word) == 0:
                        continue
                    word = word.lower()
                    processed_words.append(word)
                words = processed_words

                # populate the hashmap for counting
                for word in words:
                    word = word.lower()
                    if not hashmap.contains_key(word):
                        hashmap.put(word)
                    else:
                        hashmap.increment(word, 1)  # incerement word count by 1
                for word in set(words):
                    word = word.lower()
                    hashmap.increment(word, 2)      # incerement line count of each by 1

        # insert words from hash-map into max-heap
        for word_count in hashmap.map:
            if len(word_count) == 0:
                continue
            word, count, lines = word_count
            maxheap.insert(word, count, lines)

        # vacate the max heap and insert into dictionary in order
        while maxheap.size() > 0:
            dictionary.append(maxheap.extractMax())

        return dictionary


if __name__ == '__main__':
    dictionary = Solution.build_dictionary('files/data-assgn-4.txt')

    print("DICTIONARY OF WORDS")
    for i in range(len(dictionary)):
        word, count, lines = dictionary[i]
        print(f"{i}\t\t Word: {word}\t\t Total count: {count}\t\t No. of lines with the word: {lines}")
    print("\nNumber of unique words =", len(dictionary))
