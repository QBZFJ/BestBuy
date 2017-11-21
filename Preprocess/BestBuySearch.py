import csv

testDataSet_path = "..\\test.csv"
trainDataSet_path = "..\\train.csv"

#Query count for each user
def getQueryUserCount(path):
    file = open(path, encoding='utf-8')
    reader = csv.reader(file)
    dataUserCount = dict()
    for rows in reader:
        if rows[0] not in dataUserCount:
            dataUserCount[rows[0]] = 1
        else:
            dataUserCount[rows[0]] += 1
    file.close()
    thresholddeduction(dataUserCount, 5)

    dataUserCount = sorted(dataUserCount.items(), key=lambda x: x[1], reverse=True)
    return dataUserCount

#Query item for each user
def getEachUserQuery(path):
    file = open(path, encoding='utf-8')
    reader = csv.reader(file)
    dataUserQuery = dict()
    for rows in reader:
        if rows[0] not in dataUserQuery:
            dataUserQuery[rows[0]] = [rows[3]]
        else:
            dataUserQuery[rows[0]].append(rows[3])
    file.close()
    thresholddeduction(dataUserQuery, 5)

    dataUserQuery = sorted(dataUserQuery.items(), key=lambda x: len(x[1]), reverse=True)
    return dataUserQuery

#Query for each SKU
def getXBoxSampleQuery(path):
    file = open(path, encoding='utf-8')
    reader = csv.reader(file)
    queryItemCount = dict()
    for rows in reader:
        query = rows[3].replace(" ","").replace("_","").replace("-","").lower()
        if query not in queryItemCount:
            queryItemCount[query] = {rows[1]:1}
        elif rows[1] not in queryItemCount[query]:
            queryItemCount[query][rows[1]] = 1
        else:
            queryItemCount[query][rows[1]] += 1
    file.close()
    queryItemCount = sorted(queryItemCount.items(), key=lambda x: len(x[1]), reverse=True)
    return queryItemCount

def thresholddeduction(dict, threshold):
    dellist = []
    for k,v in dict.items():
        if isinstance(v, list):
            if len(v) <= threshold:
                dellist.append(k)
        else:
            if v <= threshold:
                dellist.append(k)
    for delitem in dellist:
        del dict[delitem]
    return dict

def printfunction(list):
    for i in list:
        print(i)

# printfunction(getQueryUserCount(trainDataSet_path)[:101])
# printfunction(getEachUserQuery(trainDataSet_path)[:101])
printfunction(getXBoxSampleQuery(trainDataSet_path)[:101])