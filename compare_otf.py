import json
import os
from pprint import pprint


class OTFHelper(object):
    @staticmethod
    def get_unique_identifier(item):
        if item['Backend Type'].endswith('_APKU'):
            return item['Name'] + item['Backend Type'][:-5]
        else:
            return item['Name'] + item['Backend Type'][:-4]


dir_path = os.path.dirname(os.path.realpath(__file__))
pdt_application = 'APK'

with open(dir_path + r'\uat.json') as data_file:
    uat = {OTFHelper.get_unique_identifier(item): item for item in
           filter(lambda x: x['Application Server'] == '', json.load(data_file))}

with open(dir_path + '\pdt.json') as data_file:
    pdt = {OTFHelper.get_unique_identifier(item): item for item in
           filter(lambda x: x['Application Server'] == '', json.load(data_file))}

diff = []
for key, uat_value in uat.items():
    if key not in pdt:
        print(key)
    else:
        pdt_value = pdt[key]
        if pdt_value['Value'] != uat_value['Value']:
            otf_var = {'OLD': pdt_value['Value'], 'NAME': uat_value['Name'], 'APPLICATION': pdt_application, 'AS': 0,
                       'PEAK': 0, 'PHASE': 'PDT', 'NEW': uat_value['Value'], 'DU': uat_value['Backend Type'][: -5]}
            diff.append(otf_var)

with open(dir_path + r'\result.json', 'w') as outfile:
    json.dump(diff, outfile, indent=4)
