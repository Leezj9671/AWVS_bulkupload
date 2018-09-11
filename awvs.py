# 用于AWVS11地址的批量上传、删除和开始扫描
import re
import json
import requests

from config import AcunetixConfig

base_url = AcunetixConfig.base_url
headers = {
    'X-Auth': AcunetixConfig.api_key,
    'Content-type': 'application/json; charset=utf8'
}
requests.urllib3.disable_warnings()

def upload(file_path):
    '''
    从txt文件批量上传，文件名作为描述名
    '''
    with open(file_path) as fp:
        description = re.findall('(\w+).txt', file_path)[0]
        targets = fp.readlines()
        for target in targets:
            data = {
                "address": target.strip(), 
                "description": description,
                "criticality": '10'
            }
            resp = requests.post(base_url + '/api/v1/targets', json=data, headers=headers, verify=False).json()
            try:
                print('{} added'.format(resp['address']))
            except:
                print('{} add failed'.format(target))

def deleteAllTargets():
    targets = requests.get(base_url + '/api/v1/targets', headers=headers, verify=False).json()['targets']
    for target in targets:
        requests.delete(base_url + '/api/v1/targets/{}'.format(target['target_id']), headers=headers, verify = False)
        print('deleted {}'.format(target['address']))

def showAll():
    print('*'*20 + 'ALL Targets'+ '*'*20)
    targets = requests.get(base_url + '/api/v1/targets', headers=headers, verify=False).json()['targets']
    for target in targets:
        print(target["address"])

def scanAll():
    targets = requests.get(base_url + '/api/v1/targets', headers=headers, verify=False).json()['targets']
    for target in targets:
        data = {
            "target_id": target['target_id'],
            "profile_id": "11111111-1111-1111-1111-111111111111",
            "schedule":
                {
                    "disable": False,
                    "start_date": None,
                    "time_sensitive": False
                }
        }
        resp = requests.post(base_url + '/api/v1/scans', json=data, headers=headers, verify=False)
        print('start scan: {}'.format(target['address']))

def deletsAllScans():
    scans = requests.get(base_url + '/api/v1/scans', headers=headers, verify=False).json()['scans']
    print(scans)
    for target in scans:
        requests.delete(base_url + '/api/v1/scans/{}'.format(target['scan_id']), headers=headers, verify = False)
        print('deleted {}'.format(target['target']['address']))

# upload('test.txt')
# showAll()
# scanAll()
deleteAllTargets()
# deletsAllScans()
