def binarySearch(arr,target):
    low = 0
    high = len(arr)-1
    mid = 0 

    while low <= high:
        mid = (low+high)//2
        if arr[mid] > target:
            high = mid - 1
        elif arr[mid] < target:
            low = mid + 1
        else:
            return mid
    
    return -1

def BinarySearch(arr,target,low,high):
    while low <= high:
        mid = (low+high)//2
        if arr[mid] == target:
            return mid
        elif arr[mid] > target:
            return BinarySearch(arr,target,low,mid-1)
        elif arr[mid] < target:
            return BinarySearch(arr,target,mid+1,high)


arr = [4,2,45,6,45,643,654]
arr.sort()
res1 = binarySearch(arr,654)
res2 = BinarySearch(arr,654,0,len(arr))
print(res1,res2)
