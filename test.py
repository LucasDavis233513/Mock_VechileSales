def extract_and_remove(testLst, indToRemove):
    extractedEle = []
    newLst = []

    for tup in testLst:
        extracted = tuple(tup[i] for i in indToRemove)
        new = tuple(tup[i] for i in range(len(tup)) if i not in indToRemove)

        extractedEle.append(extracted)
        newLst.append(new)

    return extractedEle, newLst

testLst = [(5, 6, 7, 4, 5, 6, 7), (7, 2, 4, 6, 7, 8, 9), (6, 6, 7, 2, 3, 4, 4), (6, 10, 8, 3, 2, 5, 10)]
indToRemove = [0, 5, 6]

print(testLst)

extractedEle, newLst = extract_and_remove(testLst, indToRemove)

print(extractedEle)

print(newLst)