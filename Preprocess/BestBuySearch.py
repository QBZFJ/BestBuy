import csv

rating_path = "..\\rating.csv"
threshold = 5
filename = "csvout"

# testDataSet_path = "..\\test.csv"
# trainDataSet_path = "..\\train.csv"

idsetcounttemp = 1
skusetcounttemp = 1
idsetcountnumber = 0
skusetcountnumber = 0
recurlist = []

# Document Read
def getCompleteList(path):
    file = open(path, encoding='utf-8')
    reader = csv.reader(file)
    completelist = []
    for rows in reader:
        completelist.append(rows)
    file.close()
    return completelist

# Process Threshold
def getRating(list):
    global recurlist
    useridlist = dict()
    skulist = dict()
    for rows in list:
        if rows[0] not in useridlist:
            useridlist[rows[0]] = 1
        else:
            useridlist[rows[0]] += 1

        if rows[1] not in skulist:
            skulist[rows[1]] = 1
        else:
            skulist[rows[1]] += 1
    deluseridlist = dellistthresholddeduction(useridlist)
    delskulist = dellistthresholddeduction(skulist)
    returnlist = ratingfinallist(list, deluseridlist, delskulist)
    recurlist = returnlist
    return returnlist

def thresholdcheck(list):
    global idsetcountnumber
    global idsetcounttemp
    global skusetcountnumber
    global skusetcounttemp
    global recurlist
    temp = []
    while True:
        if skusetcounttemp == skusetcountnumber and idsetcounttemp == idsetcountnumber:
            break
        skusetcountnumber = skusetcounttemp
        idsetcountnumber = idsetcounttemp
        if recurlist:
            temp = getRating(recurlist)
        else:
            temp = getRating(list)

    return temp

#Query SKU count
def getQuerySKUCount(path):
    file = open(path, encoding='utf-8')
    reader = csv.reader(file)
    dataSKUCount = dict()
    for rows in reader:
        if rows[1] not in dataSKUCount:
            dataSKUCount[rows[1]] = 1
        else:
            dataSKUCount[rows[1]] += 1
    file.close()
    thresholddeduction(dataSKUCount)
    # print(len(dataSKUCount))
    dataSKUCount = sorted(dataSKUCount.items(), key=lambda x: x[1], reverse=True)
    return dataSKUCount

#Query User count
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
    thresholddeduction(dataUserCount)
    # print(len(dataUserCount))
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
    thresholddeduction(dataUserQuery)

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

def thresholddeduction(dict):
    global threshold
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

def dellistthresholddeduction(dict):
    global threshold
    print(len(dict))
    dellist = set()
    for k,v in dict.items():
        if isinstance(v, list):
            if len(v) > threshold:
                dellist.add(k)
        else:
            if v > threshold:
                dellist.add(k)
    print(len(dellist))
    return dellist

def ratingfinallist(list, idlist, skulist):
    global idsetcounttemp
    global skusetcounttemp
    ratinglist = []
    for delid in list:
        if delid[0] in idlist and delid[1] in skulist:
            ratinglist.append(delid)
    idset = set()
    skuset = set()
    for i in ratinglist:
        if i[0] not in idset:
            idset.add(i[0])
        if i[1] not in skuset:
            skuset.add(i[1])
    idsetcounttemp = len(idset)
    skusetcounttemp = len(skuset)
    return ratinglist


def printfunction(list):
    for i in list:
        print(i)

def toCSV(list, name):
    with open(name + '.csv', 'w', newline='') as f:
        for i in list:
            w = csv.writer(f)
            w.writerow(i)

def start(list):
    finalresult = []
    finalresult = thresholdcheck(list)
    return finalresult


# printfunction(getQuerySKUCount(trainDataSet_path)[:101])
# printfunction(getEachUserQuery(trainDataSet_path)[:101])
# printfunction(getXBoxSampleQuery(trainDataSet_path)[:101])

# toCSV(getQueryUserCount(trainDataSet_path), "getQueryUserCount")
# toCSV(getQuerySKUCount(trainDataSet_path), "getQuerySKUCount")

toCSV(start(getCompleteList(rating_path)), filename)