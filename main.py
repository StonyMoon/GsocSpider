from pyquery import PyQuery
import requests
import pickle


class Organization:
    def __init__(self, name, url, technologies):
        self.name = name
        self.url = url
        self.technologies = technologies


        # 打开url返回内容


def open_url(url, try_time=2):
    # 设置请求头
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
    }
    try:
        re = requests.get(url, headers=headers)
    except Exception:
        if try_time > 0:
            return open_url(url, try_time - 1)
        print('网页:', url, '抓取失败')
        return None
    else:
        return re.text


# 返回organization的url
def get_organization():
    url = 'https://summerofcode.withgoogle.com/archive/2017/organizations/'
    response = open_url(url)
    soup = PyQuery(response)
    soup = soup('.organization-card__link')
    for each in soup.items():
        yield 'https://summerofcode.withgoogle.com' + each.attr('href')


# 通过organization的url返回technology的列表
def get_technologies(url):
    l = []
    response = open_url(url)
    soup = PyQuery(response)
    soup = soup('.organization__tag')
    for each in soup.items():
        l.append(each.text())
    return l


# 返回并且储存一个dict,key为technology，value为organization
# d的key是organization，value是technologies的列表
def save_organization():
    organizations = get_organization()
    all_technologies = []
    d = {}
    result = {}
    for each in organizations:
        print('抓取%s中', each)
        technologies_list = get_technologies(each)
        d[each] = technologies_list
        all_technologies += technologies_list
    all_technologies = list(set(all_technologies))
    for technology in all_technologies:
        result[technology] = []
        for organization_url in d.keys():
            if technology in d[organization_url]:
                result[technology].append(organization_url)
    with open('data.pkl', 'wb') as output:
        pickle.dump(result, output)
    return result


# 通过technology来搜索
def search_by_technology(d, technology):
    try:
        for each in d[technology]:
            print(each)
    except Exception:
        print('不存在这个technology')


with open('data.pkl', 'rb') as f:
    di = pickle.load(f)

while True:
    cmd = input()
    if cmd == 't':
        for t in di.keys():
            print(t)
    else:
        search_by_technology(di, cmd)