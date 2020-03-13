from urllib.parse import urlparse
import aiofiles
import asyncio
import re
q=asyncio.Queue()
async def url_montage(url,dir_dict=None,file_dict=None):
    if '.' not in urlparse(url)[2].split('/')[-1]:  # 是目录或者无后缀文件名，直接拼接
        if dir_dict:
            async with aiofiles.open(dir_dict) as paths:
                async for path in paths:
                    q.put_nowait(url + path.rstrip('\n'))
        if file_dict:
            async with aiofiles.open(file_dict) as paths:
                async for path in paths:

                    q.put_nowait(url + path.rstrip('\n'))

def queue_put(urls_file, dir_dict='./dict/list.txt', filenames_dict=None):
    urls_list = get_urls(urls_file)
    paths = get_url_path(urls_list, dir_dict, filenames_dict)
    for url_path in paths:
        q.put_nowait(url_path)

def get_urls(url_file):
    urls_list = set()
    f = open(url_file, 'r', encoding='UTF-8')
    for i in f.readlines():
        if re.search(r'=>>', i):
            i = re.search(r'(.*)=>>(.*)', i).group(1)
            if i.endswith('/'):
                pass
            else:
                i = i + '/'
            if i.startswith('https://') | i.startswith('http://'):
                pass
            else:
                i = 'http://' + i
        else:
            if i.startswith('https://') | i.startswith('http://'):
                pass
            else:
                i = 'http://' + i
        urls_list.add(i.strip('\n').strip())
    f.close()
    return urls_list

def get_url_path(urls,path_file,filenames_dict):
    if path_file:
        with open(path_file, 'r', encoding='utf-8') as paths:
            for url in urls:
                for path in paths:
                    yield url + path.rstrip('\n')

    if filenames_dict:
        with open(filenames_dict, 'r', encoding='utf-8') as paths:
            for url in urls:
                for path in paths:
                    yield url + path.rstrip('\n')