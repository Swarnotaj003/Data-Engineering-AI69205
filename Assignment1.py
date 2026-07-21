import random
from queue import PriorityQueue

# ASSIGNMENT 1
# Write python program for the following problems. 
# Given an array of real numbers, find out the mean, median and the mode of the largest k elements from the array.  
# You must not sort the array to do this, as sorting takes unnecessarily longer time. 
# You generate the array of numbers randomly in your code. 


# APPROACH 1
# Use min heap to store k largest elements. 
# Then use the heap to compute the stats.
# Time complexity - O(n log k)

def getKLargest(arr, k):
    minHeap = PriorityQueue()
    for num in arr:
        minHeap.put(num)
        # if heap is full, evict the smallest element
        if minHeap.qsize() > k:
            minHeap.get()
            
    return minHeap
    
def computeKLargestStatistics1(arr, k):
    mean = 0
    median = 0
    mode = 0
    kLargest = getKLargest(arr, k)
    
    # to store frequency of each element
    count = {}    
    
    while not kLargest.empty():
        num = kLargest.get()
        # print(num)
        mean += num     # accumulate sum
        
        # check for median
        if k % 2 == 1:
            # middle element for odd k
            if kLargest.qsize() == k // 2:
                median = num
        else:
            # average of middle two for even k
            if kLargest.qsize() == k // 2:
                left = num
            elif kLargest.qsize() == k // 2 - 1:
                right = num
                median = (left + right)/ 2
            
        # populate the frequency map
        count[num] = count.get(num, 0) + 1 
    
    # compute mean
    mean = mean / k
    
    # find the mode
    maxCount = 0
    for num in count.keys():
        if count[num] > maxCount:
            mode = num
            maxCount = count[num]
    if maxCount == 1:
        mode = None
        
    return mean, median, mode


# APPROACH 2
# Use quick select to find k largest elements.
# Then use quick select again to find the median.
# Time complexity - Expected O(n + k)

def quickSelect(arr, low, high, idx):
    # base case of recursion
    if low >= high:
        return arr[low]
    
    # choose a random pivot
    randomPivot = random.randint(low, high)
    arr[randomPivot], arr[high] = arr[high], arr[randomPivot]
    pivot = arr[high]   
    i = low     # to track the position of the pivot in sorted order
    
    for j in range(low, high):
        # move smaller elements to the left
        if arr[j] <= pivot:
            arr[i], arr[j] = arr[j], arr[i]
            i += 1
            
    # assign pivot to its correct position i
    # greater elements remain to its right
    arr[i], arr[high] = arr[high], arr[i]
    
    # the selected pivot is the threshold
    if i == idx:
        return arr[i]   
    # pivot is too small
    if i > idx:
        return quickSelect(arr, low, i - 1, idx)
    # pivot is too large
    return quickSelect(arr, i + 1, high, idx)

def computeKLargestStatistics2(arr, k):
    mean = 0
    median = 0
    mode = 0
    n = len(arr)
    
    # find threhold to filter out k largest numbers 
    # OR find the (n - k)th smallest number
    threshold = quickSelect(arr.copy(), 0, n - 1, n - k)
    
    # collect k largest numbers
    kLargest = [num for num in arr if num > threshold]
    remaining = k - len(kLargest)
    for num in arr:
        if num == threshold and remaining > 0:
            kLargest.append(num)
            remaining -= 1
    
    # to store frequency of each element
    count = {} 
    
    # compute mean
    for num in kLargest:
        # print(num)
        mean += num
        # populate the frequency map
        count[num] = count.get(num, 0) + 1 
    mean = mean / k
        
    # find the mode
    maxCount = 0
    for num in count.keys():
        if count[num] > maxCount:
            mode = num
            maxCount = count[num]
    if maxCount == 1:
        mode = None
    
    # find the median
    if k % 2 == 1:
        # middle element for odd k
        median = quickSelect(kLargest.copy(), 0, k - 1, k // 2)
    else:
        # average of middle two for even k
        left = quickSelect(kLargest.copy(), 0, k - 1, k // 2 - 1)
        right = quickSelect(kLargest.copy(), 0, k - 1, k // 2)
        median = (left + right)/ 2
    
    return mean, median, mode
    

# MAIN CODE
n = 25
k = 7
arr = [random.randint(0, 99) for _ in range(n)]
print(arr)

# mean, median, mode = computeKLargestStatistics1(arr, k)
mean, median, mode = computeKLargestStatistics2(arr, k)

print('Mean =', mean)
print('Median =', median)
print('Mode =', mode)