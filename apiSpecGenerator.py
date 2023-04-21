import json
import os


def printByDepth(element, dataType, description, depth):
    priDepth = '    ' * depth + ' - '
    priVal = '{}\t{}\t{}\t{}'.format(element, dataType, 'O', description)
    print(priDepth + priVal)


def parseSchemaPath(refValue):
    # refValue = '#/components/schemas/ErrorResponse'
    return refValue.split('/')[3]


def printRequestParameter(uri, apiMN, apiDatas):
    print()
    print('request parameter print begin : {} {}'.format(uri, apiMN))
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
    print('request parameter print end : {} {}'.format(uri, apiMN))
    print()


# schValDic
def printResponseByDepth(refKeyOnlyDict, schValDic, depth=0):
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
    refValue = refKeyOnlyDict['$ref']  # '#/components/schemas/ErrorResponse'
    schName = parseSchemaPath(refValue)
    schVal = schValDic[schName]
    # schVal ex
    # {'type': 'object',
#   'properties': {'httpStatus': {'type': 'integer', 'format': 'int32'},
#    'errorMessage': {'type': 'string'},
#    'detailMessage': {'type': 'string'},
    # }
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


def printApiSpec(relPath, fileName):
    f = open(relPath+'/' + fileName, encoding='utf8')
    data = json.load(f)
    apiDatas = data['paths']
    for key in sorted(list(data['paths'].keys())):
        # print(key)
        apiMethodList = getApiMethods(apiDatas, key)
        for apiMN in apiMethodList:
            apiName = getApiName(apiDatas, key, apiMN)
            apiDesc = getApiDesc(apiDatas, key, apiMN)
            print('{}\t{}\t{}\t{}\t{}'.format(
                fileName.split('.')[0], apiName, apiMN, apiDesc, key))
            print('api spec begin')
            try:
                printRequestParameter(key, apiMN, apiDatas)
            except:
                print('api spec request error occured', apiName, key)

            try:
                for statusCode in apiDatas[key][apiMN]['responses'].keys():
                    if statusCode not in ['401', '404', '400', '500']:
                        print('uri: {}, method: {}, stCode: {}, respone REsult begin'.format(
                            key, apiMN, statusCode))
                        printResponseByDepth(apiDatas[key][apiMN]['responses'][statusCode]['content']['application/json']['schema'],
                                             data['components']['schemas'])
                        print('uri: {}, method: {}, stCode: {}, respone REsult END'.format(
                            key, apiMN, statusCode))

                print('api spec end')
            except:
                print('api spec response result error occured', apiName, key)
            print()
            print('-' * 50)
            print()


relPath = './jsonDatas'
file_list = os.listdir(relPath)
for file_name in file_list:
    printApiSpec(relPath, file_name)

# printApiSpec('./jsonDatas', 'banner-api.json')
