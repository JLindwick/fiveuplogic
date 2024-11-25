def insertionSort(arr):
    arrayLength = len(arr)  
    if arrayLength <= 1:
        return  
    for i in range(1, arrayLength):  
        myValue = arr[i]  
        j = i-1
        while j >= 0 and myValue < arr[j]: 
            arr[j+1] = arr[j]  
            j -= 1
        arr[j+1] = myValue  
  

arr = [12, 11, 13, 5, 6]
insertionSort(arr)
print(arr)