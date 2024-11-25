def selection_sort(arr):
    arrayLength = len(arr)
    for i in range(arrayLength):
        minimumIndex = i
        for j in range(i + 1, arrayLength):
            if arr[j] < arr[minimumIndex]:
                minimumIndex = j
        arr[i], arr[minimumIndex] = arr[minimumIndex], arr[i]
    return arr

arr = [64, 25, 12, 22, 11]
newArr = selection_sort(arr)
print(type(newArr))
