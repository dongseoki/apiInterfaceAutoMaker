import json
import os
def getApiMethods(apiDatas, key):
    return list(apiDatas[key].keys())

def getApiName(apiDatas, key, apiMN):
    apiItem = apiDatas[key][apiMN]
    if 'summary' in apiItem:
        return apiItem['summary']
    else :
        return key

def getApiDesc(apiDatas, key, apiMN):
    apiItem = apiDatas[key][apiMN]
    if 'description' in apiItem:
        return apiItem['description']
    else :
        return ''

def printAPIInterface(relPath, fileName):
    f = open(relPath+'/' +fileName, encoding='utf8')
    data =json.load(f)
    apiDatas = data['paths']
    for key in sorted(list(data['paths'].keys())):
        # print(key)
        apiMethodList = getApiMethods(apiDatas, key)
        for apiMN in apiMethodList:
            apiName = getApiName(apiDatas, key, apiMN)
            apiDesc = getApiDesc(apiDatas, key, apiMN)
            print('{}\t{}\t{}\t{}\t{}'.format(fileName.split('.')[0], apiName, apiMN, apiDesc, key))


relPath = './jsonDatas'
file_list = os.listdir(relPath)
for file_name in file_list:
    printAPIInterface(relPath, file_name)