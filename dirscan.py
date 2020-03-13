# -*- coding:utf-8 -*-  
#====#====#====#====
#QQ:664763775 
#FileName: *.py  
#Version:1.0.0 
#auther:Da13 
#====#====#====#====

import requests
import asyncio
import parser
import aiohttp
import sys
from lib.urls import url_montage,queue_put,q
from urllib.parse import urlparse
import random
from tenacity import retry, stop_after_attempt
import time

user_agent_list = ['Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36',
                       'Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36',
                       'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:17.0) Gecko/20100101 Firefox/17.0.6',
                       'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36',
                       'Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36']


header = {
            'Accept': '*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'User-Agent': random.choice(user_agent_list),
        }
f= open("result.txt","a",encoding="UTF-8")



async def parse_url(session,q,ext):

    while not q.empty():
        url = q.get_nowait()
        try:
            file = "dict/" + ext + "_file.txt"

            random_url = get_random_url(url)
            result,text=await get_req(session,url)
            if result.status ==200 and result is not None:
                if "404.css" in text or "404.js" in text or "404.html" in text or "404" in text or "not found" in text or "error" in text:
                    print("[*]" + "200" + "==>" + url+"不存在")

                else:
                    random_res,random_text  = await get_req(session,random_url)
                    if text==random_text or random_res is  None or random_res.status==200:


                        print("[*]" + "404" + "==>" + url + "不存在")
                    else:

                        await url_montage(url, dir_dict='./dict/list.txt', file_dict=file)
                        f.write("[*]"+str(result.status)+"==>"+url+'\n')
                        print("[*]"+str(result.status)+"==>"+url)
            elif result.status == 403:


                random_res,random_text = await get_req(session,random_url)

                if random_res.status==404:
                    f.write("[*]" + str(result.status) + "==>" + url + '\n')
                    print("[*]" + str(result.status) + "==>" + url)
                    await url_montage(url, dir_dict='./dict/list.txt', file_dict=file)

            elif result.status in [301,302]:
                random_res,random_text = await get_req(session, random_url)
                if random_res.status in [301,302] or random_res is None or random_text == text:

                    print("[*]" + "302" + "==>" + url + "不存在")
                else:
                    f.write("[*]" + str(result.status) + "==>" + url+'\n')
                    print("[*]" + str(result.status) + "==>" + url)
            elif result.status in [401,405]:
                f.write("[*]" + str(result.status) + "==>" + url+'\n')
                print("[*]" + str(result.status) + "==>" + url+"存在认证")
            else:
                #pass
                print("[*]" + str(result.status) + "==>" + url)
        except Exception as e:
            print("[*]" + url+"解析错误")

@retry(stop=stop_after_attempt(4))
async def get_req(session, url):

    try:

        response = await session.get(url, allow_redirects=False, headers = header,timeout=3)
        text = await response.text()
        return response,text
    except Exception as e:

        return None
        #with open('异常处理.txt', 'a+', encoding='utf-8') as f:
        #    f.write("处理异常"+url+'\n')

async def start(q,ext):


    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:  # 创建session
        tasks = []
        for _ in range(50):
            task = parse_url(session, q,ext)
            tasks.append(task)
        await asyncio.wait(tasks)
def get_random_url(root_url):
    if '.' not in urlparse(root_url)[2].split('/')[-1]:
        str=root_url.split('/')[-2]+'/'
        random_url = root_url.replace(str,'')+'ssss/'
    else:
        random_url=root_url.rstrip(root_url.split('/')[-1])+'sssss.php'
    return random_url



if __name__ == '__main__':

    requests.packages.urllib3.disable_warnings()
    time1=time.time()
    parser.add_argument("--target", type=str, help="target urls file.")
    parser.add_argument("--ext", type=str, help="target ext")
    if len(sys.argv) == 1:
        sys.argv.append("-h")
    args = parser.parse_args()
    urls_file = args.target
    ext = args.ext
    queue_put(urls_file)

    asyncio.run(start(q,ext))
    f.close()
    print(time.time()-time1)

