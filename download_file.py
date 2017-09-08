import requests
import re
import urllib
import os

def gethtml(req, re1, url):
    r = req.get(url)
    html = r.content.decode('utf-8')
    re_content = re1.findall(html)
    try:
        re_content.remove('../')
    except:
        pass
    return re_content, html


if __name__ == "__main__":
    limit = r"href=\"(.+?)\""
    url_list = [""]#website
    req = requests.session()
    re1 = re.compile(limit)
    root_url_len = len(url_list[0])
    save_root_path = ""

    while(url_list):
        url = url_list[0]
        if url[-1]=="/":
            re_content, htmlcontent= gethtml(req, re1, url)
            if re_content:
                if re_content[0][-1] == "/":
                    url_list = url_list + list(map(lambda x: url + x, re_content))  
                    url_list.remove(url)
                    # print(url_list)
                else:
                    url_list.remove(url)
                    # print url
                    for name in re_content:
                        dir_name = url[root_url_len:].replace("/","\\")
                        if save_root_path:
                            pass
                        else:
                            save_root_path = os.getcwd()
                        full_dir_path = save_root_path+"\\"+dir_name
                        if not os.path.exists(full_dir_path):
                            os.makedirs(full_dir_path)
                        #urllib.urlretrieve(url+name,full_dir_path+name)
                        print 'download... ' + url+name
            else:
                break
        else:
            url_list.remove(url)
            name = url[url.rfind('/')+1:]
            dir_name = url[root_url_len:url.rfind('/')+1].replace("/","\\")
            if save_root_path:
                pass
            else:
                save_root_path = os.getcwd()
            full_dir_path = save_root_path+"\\"+dir_name
            if not os.path.exists(full_dir_path):
                os.makedirs(full_dir_path)
            urllib.urlretrieve(url,full_dir_path+name)
            print 'download... ' + url
            
    print 'download suceess'
