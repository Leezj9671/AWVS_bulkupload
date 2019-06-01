# 用于AWVS11地址的批量上传、删除和开始扫描
# 相关配置于config.py中修改
import os
import re
import json
import requests

from config import AcunetixConfig

base_url = AcunetixConfig.base_url
targets_url = base_url + '/api/v1/targets'
scans_url = base_url + '/api/v1/scans'
groups_url = base_url + 'api/v1/target_groups'
headers = {
    'X-Auth': AcunetixConfig.api_key,
    'Content-type': 'application/json; charset=utf8'
}
# 关闭错误提示
requests.urllib3.disable_warnings()


class Target(object):
    '''Targets相关操作'''

    def upload(self, file_path):
        '''从txt文件批量上传，以文件名作为描述名

        :param file_path: 需要上传的地址文件路径
        '''
        with open(file_path) as fp:
            basename = os.path.basename(file_path)
            description = os.path.splitext(basename)[0]
            targets = fp.readlines()
            for target in targets:
                if not target:
                    continue
                data = {
                    "address": target.strip(),
                    "description": description,
                    "criticality": '10'
                }
                resp = requests.post(targets_url,
                                    json=data, headers=headers, verify=False).json()
                try:
                    print('[+]Added: {}'.format(resp['address']))
                except:
                    print('[x]Add failed: {}'.format(target))

    def deleteOneTarget(self, target_id):
        '''删除一个target

        Args:
            target_id: 删除target的id
        '''
        resp = requests.get(targets_url + '/' + target_id, headers=headers, verify=False)
        if resp == 200:
            print('[√]Delete target success: {}'.target_id)
            return True
        else:
            return False

    def deleteAllTargets(self):
        '''删除所有Targets'''
        targets = requests.get(targets_url,
                            headers=headers, verify=False).json()['targets']
        print('[-]Current Targets: ', targets)
        for target in targets:
            requests.delete(targets_url + target['target_id'], headers=headers, verify=False)
            print('[!]Deleted {}'.format(target['address']))


    def showAll(self):
        '''展示所有Targets'''
        print('\n[-]ALL Targets:')
        targets = requests.get(targets_url, headers=headers, verify=False).json()['targets']
        for target in targets:
            print(target['target_id'], target["address"])
        print('\n')


    def addGroup(group_name, group_description):
        '''增加targets组

        Args:
            group_name: 组名
            group_description: 该组描述

        Returns:
            group_id: 添加的组ID
        '''
        data = {
            'name': group_name,
            'description': group_description
        }
        resp = requests.get(targets_url, data=data, headers=headers, verify=False)
        if resp.status_code == 201:
            #成功创建
            print('[√]Group {} added')
            return  resp.json()['']
        else:
            #409 冲突
            print('[!]{}'.format(resp.json()['message']))
            return None

    def scanAll():
        '''对所有Targets进行扫描'''
        targets = requests.get(targets_url,
                            headers=headers, verify=False).json()['targets']
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
            resp = requests.post(scans_url,
                                json=data, headers=headers, verify=False)
            print('[√]Start scan: {}'.format(target['address']))


class Scan(object):
    '''扫描相关操作'''

    def getAllScans(self):
        '''获取所有扫描任务

        Returns:
            scans<list>:
        '''
        scans = requests.get(scans_url, headers=headers, verify=False).json()['scans']
        print('[√]Get current Scans: ', scans)
        return scans


    def getScanID(self, target_id=None, ):
        scans  = response.get(scans_url, scanner_id)
        for scan in scans['scans']:
            if scan['target_id'] == target_id:
                scan_id = scan['scan_id']
                return scan_id


    def deletsAllScans():
        '''删除所有扫描'''
        scans = requests.get(scans_url, headers=headers, verify=False).json()['scans']
        try:
            for target in scans:
                requests.delete(scans_url + target['scan_id'], headers=headers, verify=False)
                print('[!]Deleted {}'.format(target['target']['address']))
        except:
            print('[-]Scans delete ERROR!')
            return False
        return True


if __name__ == "__main__":
    targets = Target()
    scans = Scan()

    targets.deleteAllTargets()
    targets.deletsAllScans()
    # 上传urlstxt的所有地址
    targets.upload('urls.txt')
    targets.showAll()

    scans.ScanscanAll()
