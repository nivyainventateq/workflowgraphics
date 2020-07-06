import json
import pandas as pd
import os

def convertjson():

    result =[]
    with open('media/temp.json') as f:
        data = f.readlines()
    for line in data:
        result.append(json.loads(line))

    return result


def saveJsonfiles(filename):
    df = pd.read_excel('media/'+str(filename))
    df = df.dropna()
    if os.path.isfile('media/temp.json'):
        os.remove('media/temp.json')
    df.to_json('media/temp.json', orient='records', lines=True)
    return True