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
# file_list = os.listdir(relPath)
file_list = ['common-api.json',
             'banner-api.json',
             'board-api.json',
             'category-api.json',
             'common-api2.json',
             'consulting-api.json',
             'contents-api.json',
             'counseling-api.json',
             'coupon-api.json',
             'logging-api.json',
             'login2-api.json',
             'mailing-api.json',
             'mavatar-api.json',
             'mbody-api.json',
             'mcloth-api.json',
             'mface-api.json',
             'mhair-api.json',
             'micecontents-api.json',
             'mregion-api.json',
             'mshoes-api.json',
             'mypage-api.json',
             'order-api.json',
             'popup-api.json',
             'projectinfo-api.json',
             'projectinfo2-api.json',
             'quiz-api.json',
             'session-api.json',
             'stat2-api.json',
             'statistics-api.json',
             'subscribe-api.json',
             'survey2-api.json',
             'user-api.json',
             'goods-api.json',
             'inquiry-api.json']
for file_name in file_list:
    printAPIInterface(relPath, file_name)