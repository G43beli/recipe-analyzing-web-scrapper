import json as j
from urllib.request import urlopen, Request

def load_json(path):
    try:
        with open(path) as jsonFile:
            jsonObject = j.load(jsonFile)
            jsonFile.close()
            return jsonObject
    except:
        return dict()

def save_json(data_json, path):
    with open(path, 'w') as outfile:
        j.dump(data_json, outfile)

def load_proxies(headers, from_storage=False):
    path = 'storage/proxies.json'
    try:
        if from_storage:
            data_json = load_json(path)
            return get_ips_from_json(data_json)
        else:
            ips = []
            speed_params = ['fast', 'medium']
            for param in speed_params:
                url = f'https://proxylist.geonode.com/api/proxy-list?limit=50&page=1&sort_by=lastChecked&sort_type=desc&google=true&filterUpTime=100&speed={param}&protocols=https'
                request = Request(url, None, headers)
                response = urlopen(request)
                data_json = j.loads(response.read())
                save_json(data_json, path)
                ips.extend(get_ips_from_json(data_json))
            return ips
    except Exception as ex:
        print('Proxy loading failed:', ex)
        return []

def get_ips_from_json(data_json):
    ips = []
    if 'data' in data_json:
        for ip_config in data_json['data']:
            ips.append(ip_config['ip'] + ":" + ip_config['port'])
    return ips