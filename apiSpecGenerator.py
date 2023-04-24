import json
import os
import sys
import traceback

global apNum
apNum = 1


def printByDepth(element, dataType, description, depth):
    priDepth = '    ' * depth + ' - '
    priVal = '{}\t{}\t{}\t{}'.format(element, dataType, 'O', description)
    print(priDepth + priVal)


def parseSchemaPath(refValue):
    # refValue = '#/components/schemas/ErrorResponse'
    return refValue.split('/')[3]


def printRequestParameter(uri, apiMN, apiDatas, schValDic):
    # print()
    # print('request parameter print begin : {} {}'.format(uri, apiMN))
    if 'parameters' in apiDatas[uri][apiMN]:
        for paramItem in apiDatas[uri][apiMN]['parameters']:
            try:
                element = paramItem['name']
                dataType = paramItem['schema']['type']
                if paramItem['required'] == True:
                    mandatory = 'O'
                else:
                    mandatory = 'X'
                if 'description' in paramItem:
                    desc = paramItem['description']
                else:
                    desc = ''
                print(' - {}\t{}\t{}\t{}'.format(element, dataType, mandatory, desc))
            except:
                print('error occured name : {}, value : {}'.format(
                    paramItem['name'], paramItem))
    if 'requestBody' in apiDatas[uri][apiMN]:
        if 'application/json' in apiDatas[uri][apiMN]['requestBody']['content']:
            schemaRealValDit = apiDatas[uri][apiMN]['requestBody']['content']['application/json']['schema']
        if 'multipart/form-data' in apiDatas[uri][apiMN]['requestBody']['content']:
            schemaRealValDit = apiDatas[uri][apiMN]['requestBody']['content']['multipart/form-data']['schema']
        if 'items' in schemaRealValDit:
            if '$ref' in schemaRealValDit['items']:
                printResponseByDepth({
                    '$ref': schemaRealValDit['items']['$ref']
                }, schValDic)
        if '$ref' in schemaRealValDit:
            printResponseByDepth({
                '$ref': schemaRealValDit['$ref']
            }, schValDic)
    # print('request parameter print end : {} {}'.format(uri, apiMN))
    # print()


# schValDic
def printResponseByDepth(refKeyOnlyDict, schValDic, depth=0):
    if depth >= 7:
        print('depth is too deep')
        return
    # schValDic
    # ex)
    #     {'ErrorResponse': {'type': 'object',
    #   'properties': {'httpStatus': {'type': 'integer', 'format': 'int32'},
    #    'errorMessage': {'type': 'string'},
    #    'detailMessage': {'type': 'string'},
    #    'errors': {'type': 'array',
    #     'items': {'$ref': '#/components/schemas/FieldError'}}}},
    #  'FieldError': {'type': 'object',
    #   'properties': {'field': {'type': 'string'},
    #    'value': {'type': 'string'},
    #    'reason': {'type': 'string'}}},
    #  'RegistTbBannerReq': {'required': ['delYn', 'dspCnt'],
    #   'type': 'object',
    #   'properties': {'projectCd': {'type': 'string',
    #     'description': '프로젝트코드',
    #     'nullable': True,
    #     'example': 'BCWW'},
    #    'siteId': {'type': 'integer',
    #     'description': '사이트ID',
    #     'format': 'int32',
    #     'nullable': True},
    #    'bannerLocCd': {'type': 'string',
    #     'description': '배너위치코드(BLC)',
    #     'nullable': True,
    #     'example': 'BLC004'},
    #    'imgPath': {'type': 'string',
    if '$ref' in refKeyOnlyDict:
        refValue = refKeyOnlyDict['$ref']  # '#/components/schemas/ErrorResponse'
        schName = parseSchemaPath(refValue)
        schVal = schValDic[schName]
        if 'properties' in schVal:
            for propertyName in schVal['properties'].keys():
                propertyValueDict = schVal['properties'][propertyName]
                element = propertyName
                if 'type' in propertyValueDict:
                    dataType = propertyValueDict['type']
                elif '$ref' in propertyValueDict:
                    dataType = 'Object'
                else:
                    dataType = '_'
                if 'description' in propertyValueDict:
                    description = propertyValueDict['description']
                else:
                    description = '_'
                printByDepth(element, dataType, description, depth)
                if 'items' in propertyValueDict:
                    if '$ref' in propertyValueDict['items']:
                        printResponseByDepth({
                            '$ref': propertyValueDict['items']['$ref']
                        }, schValDic, depth+1)
                if '$ref' in propertyValueDict:
                    printResponseByDepth({
                        '$ref': propertyValueDict['$ref']
                    }, schValDic, depth+1)
    if 'items' in refKeyOnlyDict:
        dataType = 'array'
        printByDepth('_', dataType, '_', depth)
        if '$ref' in refKeyOnlyDict['items']:
            printResponseByDepth({
                '$ref': refKeyOnlyDict['items']['$ref']
            }, schValDic, depth+1)
        return;
    # schVal ex
    # {'type': 'object',
#   'properties': {'httpStatus': {'type': 'integer', 'format': 'int32'},
#    'errorMessage': {'type': 'string'},
#    'detailMessage': {'type': 'string'},
    # }


def getApiMethods(apiDatas, key):
    return list(apiDatas[key].keys())


def getApiName(apiDatas, key, apiMN):
    apiItem = apiDatas[key][apiMN]
    if 'summary' in apiItem:
        return apiItem['summary']
    else:
        return key


def getApiDesc(apiDatas, key, apiMN):
    apiItem = apiDatas[key][apiMN]
    if 'description' in apiItem:
        return apiItem['description']
    else:
        return ''


def replaceWithUnder(value):
    return value.replace('/', '_').replace('*', '+')


def makeAPSpecDirPath(uri, apiMN):
    global apNum
    path = './apiSpecGeneratorResult/' + 'AP_' + \
        str(apNum).zfill(3) + '_' + replaceWithUnder(uri) + '_' + apiMN
    return path


def printAPIMeta(fileName, apiName, apiMN, apiDesc, key):
    print('{}\n{}\n{}\n{}\n{}'.format(
        fileName.split('.')[0], apiName, apiMN, apiDesc, key))


def printApiSpec(relPath, fileName):
    f = open(relPath+'/' + fileName, encoding='utf8')
    data = json.load(f)
    apiDatas = data['paths']
    for key in sorted(list(data['paths'].keys())):
        uri = key

        # print(key)
        apiMethodList = getApiMethods(apiDatas, key)
        for apiMN in apiMethodList:
            fileToErrorDic[file_name]['apiSubCnt'] += 1
            global apNum
            if (apNum == 451):
                apNum += 10
            createDirectory = makeAPSpecDirPath(uri, apiMN)
            if not os.path.exists(createDirectory):
                os.makedirs(createDirectory)
            apNum += 1

            apiName = getApiName(apiDatas, key, apiMN)
            apiDesc = getApiDesc(apiDatas, key, apiMN)
            original_stdout = sys.stdout
            with open(createDirectory + '/api_meta_info.txt', 'w', encoding='utf8') as f:
                # Change the standard output to the file we created.
                sys.stdout = f
                printAPIMeta(fileName, apiName, apiMN, apiDesc, key)
                sys.stdout = original_stdout  # Reset the standard output to its original value
            # print('api spec begin')
            original_stdout = sys.stdout
            with open(createDirectory + '/api_request_parameter.txt', 'w', encoding='utf8') as f:
                # Change the standard output to the file we created.
                sys.stdout = f
                try:
                    printRequestParameter(
                        key, apiMN, apiDatas, data['components']['schemas'])
                except:
                    print('api spec request error occured', apiName, key)
                    print(traceback.format_exc())
                    fileToErrorDic[file_name]['errReqCnt'] += 1
                    fileToErrorDic[file_name]['errReqList'].append(
                        createDirectory)
                sys.stdout = original_stdout  # Reset the standard output to its original value
            with open(createDirectory + '/api_response_parameter.txt', 'w', encoding='utf8') as f:
                # Change the standard output to the file we created.
                sys.stdout = f
                try:
                    for statusCode in apiDatas[key][apiMN]['responses'].keys():
                        if statusCode not in ['401', '404', '400', '500']:
                            print('uri: {}, method: {}, stCode: {}, respone REsult begin'.format(
                                key, apiMN, statusCode))
                            if 'content' in apiDatas[key][apiMN]['responses'][statusCode]:
                                printResponseByDepth(apiDatas[key][apiMN]['responses'][statusCode]['content']['application/json']['schema'],
                                                     data['components']['schemas'])
                                print('uri: {}, method: {}, stCode: {}, respone REsult END'.format(
                                    key, apiMN, statusCode))

                    print('api spec end')
                except:
                    print('api spec response result error occured', apiName, key)
                    print(traceback.format_exc())
                    fileToErrorDic[file_name]['errResCnt'] += 1
                    fileToErrorDic[file_name]['errResList'].append(
                        createDirectory)
                sys.stdout = original_stdout  # Reset the standard output to its original value
            # print()
            # print('-' * 50)
            # print()


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
global fileToErrorDic
fileToErrorDic = {}

# dir = './apiSpecGeneratorResult'
# for f in os.listdir(dir):
#     os.remove(os.path.join(dir, f))

for file_name in file_list:
    fileToErrorDic[file_name] = {
        'apiSubCnt': 0,
        'errReqCnt': 0,
        'errResCnt': 0,
        'errReqList': [],
        'errResList': []
    }
    printApiSpec(relPath, file_name)

# printApiSpec('./jsonDatas', 'banner-api.json')

totalErrReqCnt = 0
totalErrResCnt = 0


def printErrorInfo(file_name, errorInfo):
    print('file_name: ', file_name)
    print('apiSubCnt: ', errorInfo['apiSubCnt'])
    print('errReqCnt: ', errorInfo['errReqCnt'])
    print('errReqPercent: ',
          errorInfo['errReqCnt'] / errorInfo['apiSubCnt'] * 100)
    print('errResCnt: ', errorInfo['errResCnt'])
    print('errResPercent: ',
          errorInfo['errResCnt'] / errorInfo['apiSubCnt'] * 100)
    print('errReqList: ', errorInfo['errReqList'])
    print('errResList: ', errorInfo['errResList'])
    print('-'*50)


for file_name in file_list:
    printErrorInfo(file_name, fileToErrorDic[file_name])
    totalErrReqCnt += fileToErrorDic[file_name]['errReqCnt']
    totalErrResCnt += fileToErrorDic[file_name]['errResCnt']

print('totalErrReqCnt: ', totalErrReqCnt)
print('totalErrResCnt: ', totalErrResCnt)
