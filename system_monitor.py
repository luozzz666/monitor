# _*_ coding:utf-8 _*_

from email.mime.text import MIMEText
import smtplib
import logging
import json
import os,sys,time,json,socket,time
import psutil


loglevel=logging.basicConfig(
    level=logging.INFO,
    format = "[%(asctime)s] - [%(levelname)s] %(message)s",
    filename=r'/root/sysmonitor.log'
    )

def sendmail(subject,content):
    msg_from='xxx@qq.com'
    passwd='xxx'
    msg_to='xxx@qq.com,xxx@qq.com'
    msg = MIMEText(content)
    msg['Subject'] = subject
    msg['From'] = msg_from
    msg['To'] = msg_to
    try:
        s=smtplib.SMTP_SSL("smtp.qq.com",465)
        s.login(msg_from, passwd)
        s.sendmail(msg_from, msg_to.split(","), msg.as_string())
        logging.info('%s ---> %s 发送成功' %(msg_from,msg_to))
    except s.SMTPException,e:
        logging.error('%s ---> %s 发送失败' %(msg_from,msg_to))
    finally:
        s.quit()


def getbaseinfo():
    msg=[]
    hostname=socket.gethostname()
    hostnameinfo = "hostname:%s" %hostname
    ip=socket.gethostbyname(hostname)
    ipinfo="ip:%s" %ip
    nowtime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    timeinfo="time:%s" %nowtime 
    msg.append(hostnameinfo)
    msg.append(ipinfo)
    msg.append(timeinfo)
    return msg

def judge(project,size):
    if size > 80:
        subject="Problem:The usage of %s is to large"  %project
        cpuinfo="The %s usage is:%s" %(project,size)
        msg=getbaseinfo()
        msg.append(cpuinfo)
        content="\n".join(str(i) for i in msg)
        sendmail(subject,content)

def cpuinfo():
    cpu_count=psutil.cpu_count()
    cpu_count=psutil.cpu_count(logical=False)
    cpu_usage=psutil.cpu_percent(2)
    logging.info("Problem:The cpu usage is %s,it is to large" %cpu_usage)
    judge("cpu",cpu_usage)



def meminfo():
    memdata=psutil.virtual_memory()
    totalmem=memdata.total/1024/1024
    availablemem=memdata.available/1024/1024
    usagemem=int(memdata.percent)
    freemem=int(100-memdata.percent)
    logging.info("Problem:The mem usage is %s,it is to large" %usagemem)
    judge("mem",usagemem)
    

def diskinfo():
    path='/'
    uagedisk=psutil.disk_usage(path).percent
    logging.info("Problem:The disk usage is %s,it is to large" %uagedisk)
    judge("disk",uagedisk)

cpuinfo()
meminfo()
diskinfo()

