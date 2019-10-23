#coding:utf-8
#用于web状态码监测并报警
#version:0.6
#实现状态码获取
#修改为Python3支持
#增加网页状态码持续监控和报警条件(报警条件为一分钟内有三次状态码非200)0.
#优化代码结构
#优化网页不能访问的状态监测
#完成报警内容推送
#类封装
#多web监测(多任务)
#修复对ssl监测的支持


from multiprocessing import Process
import requests
import time
import client


class Monitor():
    
    def __init__(self,url):
        self.url = url
        self.threshold = 0
        self.time_con = []
        self.statu_code = ''

    def get_code(self,url):
        '''获取url状态码'''
        header={
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Mobile Safari/537.36'   
        }

        #response = requests.request('GET',self.url,headers=header)
        
        try:
            response = requests.request('GET',self.url,stream=True,headers=header)

        #如果证书认证失败则去掉验证
        except requests.exceptions.SSLError:
            #调试不支持证书认证的网址
            #print(self.url +" "+"without cert")
            requests.urllib3.disable_warnings()
            response = requests.request('GET',self.url,stream=True,headers=header,verify=False)


        
        return response.status_code

    def monitor_web(self,url):
        '''网页状态监测'''
        while True:
            ###抓取的睡眠时间
            time.sleep(3)
            #self.statu_code = self.get_code(self.url)
            
            try:
                self.statu_code = self.get_code(self.url)


            except requests.exceptions.ConnectionError:
                #print(self.statu_code)
                print(self.url +" 连接被拒绝")
                return "连接被拒绝"
                break
        
            if self.statu_code != 200:
                print("----网络出错----")
                print(self.statu_code)
                return self.statu_code
                break
            else:
                pass
    

    def baojin(self):
        '''报警'''
        #global threshold
        #global time_con
        if self.threshold >= 4:
            time_difference = max(self.time_con) - min(self.time_con)
            print(time_difference)
            if time_difference <= 60:
                
                ###报警
                print('报警!!!!!!!'+" "+self.url)
                client.send_msg("%s 网页不能访问,statu_code = %s"% (self.url,self.statu_code))
                self.threshold = 0
                self.time_con = []
                time.sleep(10)
            else:
                #global threshold
                self.threshold = 0
                self.time_con = []
        else:
            pass


def run_proc(web_name,url):

    web_name = Monitor(url)
    while True:
        
        print(web_name.url+"监测中")
        web_name.statu_code = web_name.monitor_web(url)
        web_name.threshold+=1
        web_name.time_con.append(time.time())
        web_name.baojin()
        
        
def main(name,url):
    name = Process(target=run_proc,args=(name,url))
    name.start()

if __name__ == "__main__":

    main('web1','https://baidu.com')
   
    
    






