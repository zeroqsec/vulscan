
def fileLoadPaylaod(filePath) -> list:
    '''
    load file and output file content as a list
    :param filePath:
    :return:type<list>
    '''
    with open(filePath,mode='r',encoding='utf-8') as f:
        return f.readlines()

