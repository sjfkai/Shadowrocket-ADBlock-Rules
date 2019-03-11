# -*- coding: utf-8 -*-

import re
import time


# confs names in template/ and ../
# except sr_head and sr_foot
confs_names = [
    'surge',
]


def getRulesStringFromFile(path, kind):
    file = open(path, 'r', encoding='utf-8')
    contents = file.readlines()
    ret = ''

    for content in contents:
        content = content.strip('\r\n')
        if not len(content):
            continue

        if content.startswith('#'):
            ret += content + '\n'
        else:
            prefix = 'DOMAIN-SUFFIX'
            if re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', content):
                prefix = 'IP-CIDR'
                if '/' not in content:
                    content += '/32'
            elif '.' not in content:
                prefix = 'DOMAIN-KEYWORD'

            ret += prefix + ',%s,%s\n' % (content, kind)

    return ret



# make values
values = {}

values['build_time'] = time.strftime("%Y-%m-%d %H:%M:%S")

values['top500_proxy']  = getRulesStringFromFile('resultant/top500_proxy.list', 'GFW')
values['top500_direct'] = getRulesStringFromFile('resultant/top500_direct.list', 'CHINA')

values['ad'] = getRulesStringFromFile('resultant/ad.list', 'ADS')

values['manual_direct'] = getRulesStringFromFile('manual_direct.txt', 'CHINA')
values['manual_proxy']  = getRulesStringFromFile('manual_proxy.txt', 'GFW')
values['manual_reject'] = getRulesStringFromFile('manual_reject.txt', 'ADS')

values['gfwlist'] = getRulesStringFromFile('resultant/gfw.list', 'GFW') \
                  + getRulesStringFromFile('manual_gfwlist.txt', 'GFW')


# make confs
for conf_name in confs_names:
    file_template = open('template/'+conf_name+'.txt', 'r', encoding='utf-8')
    template = file_template.read()

    file_output = open('../'+conf_name+'.conf', 'w', encoding='utf-8')

    marks = re.findall(r'{{(.+)}}', template)

    for mark in marks:
        template = template.replace('{{'+mark+'}}', values[mark])

    file_output.write(template)
