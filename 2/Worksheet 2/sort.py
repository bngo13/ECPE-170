def loadFile():
    infile = open("data.txt")
    data = []
    # Append Data
    for a in infile:
        data.append(int(a[:-1]))
    return data


def bubbleSort(data):
    for i in range(0, len(data) - 1):
        for j in range(0, len(data) - i - 1):
            if data[j] > data[j + 1]:
                temp = data[j]
                data[j] = data[j + 1]
                data[j + 1] = temp
    return data


def insertSort(data):
    key = 0
    j = 0
    for i in range(0, len(data)):
        key = data[i]
        j = i - 1

        while j >= 0 and data[j] > key:
            data[j + 1]  = data[j]
            j -= 1
        data[j + 1] = key

    return data

def main():
    data = loadFile()
    insertData = data
    print("Insert Sort:")
    print(insertSort(insertData))

    bubbleData = data
    print("Bubble Sort:")
    print(bubbleSort(insertData))



if __name__ == "__main__":
    main()
