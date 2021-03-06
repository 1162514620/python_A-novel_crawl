import requests
import httpx
import asyncio
import bs4
import re
import tkinter as tk
from tkinter import filedialog

#网页下载
def open_url(url):

    #伪造访问身份验证文件
    headers = {'User-Agent': 'my custom user agent', 'Cookie': 'haha'}
    #访问到该网页
    res = requests.get(url, headers=headers)
    #返回获取到的网页
    return res

#获取下一章的网址
def find_next(res):
    #以html的方式进行解析
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    N = soup.find("a", class_="next")
    return "https://www.biqugeu.net"+N.attrs['href']

#获取当前页章节名和正文内容
def Access_content(res):

    #以html的方式进行解析获取到的网页内容
    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    content=[]
    N = soup.find_all("div", class_="bookname")
    #将获取到的章节名写到content中
    for each in N:
        content .append(each.h1.text)
        print("正在爬取  %s  的内容\n"%each.h1.text)
    #得到小说内容的TXT文本部分
    T = soup.find_all("div", id="content")
    #将获取到的内容写到content中
    for each in T:
        content .append(each.text)

    return content

#获取文件夹路径
def Access_directory():

    #打开绘图部件
    root = tk.Tk()
    #隐藏绘图部件
    root.withdraw()
    #获得选择好的文件夹
    return filedialog.askdirectory()

def main():

    result = []
    # 输入第一章的网址
    host = input("请输入第一章的网址：")
    #获得小说名称
    novel_name = input("小说名称为：")
    #获取文件夹路径
    Folderpath = Access_directory()
    
    while (1):
        try:
            #打开网页
            res = open_url(host)
            #将获得的内容添加到result的末尾
            result.extend(Access_content(res))
            #获得下一章的网址
            host = find_next(res)
        except:
            break

    #写入TXT文件
    with open(Folderpath+'\\'+novel_name+'.txt', "w", encoding="utf-8") as f:
        for each in result:
            f.write(each)

if __name__ == "__main__":
    main()

