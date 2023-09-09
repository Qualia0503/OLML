import requests
from lxml import etree
import random
import smtplib
from email.mime.text import MIMEText
from email.header import Header


def get_data(url, num):
    # 解析格式与基础信息
    path = ['//*[@id="TopstoryContent"]/div/div/div[2]/section/div[2]/a',
            '//*[@id="pl_top_realtimehot"]/table/tbody/tr/td[2]/a']
    web_name = ["知乎热榜",
                "微博热搜"]
    pre = ['',
           'https://s.weibo.com/']
    get_title = ['/h2/text()','/text()']
    get_link = ['/@href',
                '/@href']

    # 获取网页
    headers = {
        'cookie' : '_zap=cd4e46ef-046c-4ac4-bec9-a4ceebbe61e9; d_c0="ABBZob93kRKPTujfUEHSZsDGA3Or-XP2Jbk=|1611779821"; _xsrf=c3efbd4a-f067-4987-9f88-9fa00ad99c74; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1611779824,1611780198,1612601197; captcha_session_v2="2|1:0|10:1612601196|18:captcha_session_v2|28:YzBmNWVyMmRzcG9zZGtsMjY4bDA=|77934fcc04c05daf95820ee72c36d45f61ee29bdc09ac2a952adca8f60986c4d"; SESSIONID=dzXDzBqcnYy6lksHFvqaJfGTSU24M0m6if6mFk4ld6q; JOID=UlAUCk5l98ditSHvA2zKmaafUXMQCYSXKsprl2gOprdc1U-UQgmh3Qu4IO4HAloZ1-XcWPMzbpED4tBAg1gQ60g=; osd=VVgSBU1i_8FttibnBWPJnq6ZXnAXAYKYKc1jkWcNob9a2kyTSg-u3gywJuEEBVIf2ObbUPU8bZYL5N9DhFAW5Es=; l_n_c=1; o_act=login; ref_source="other_https://www.zhihu.com/signin?next=/hot"; r_cap_id="NDZhNTgwYzZlMWRkNGU3NDhmMGQ5OWIxMTBiNmY0NDg=|1612601203|87363e6326c64a52a37522116052bd5a3e72aa0f"; cap_id="OTlhOTEwN2UwMDhmNDFhN2FkNDc0NzdkYmY4OWVhYjg=|1612601203|65556d70e1f9ca3205c76dd3988bcfa16debedb0"; l_cap_id="NTU1ZjJiMjI0MmI2NDNlNGI2MjcyYmVmN2UzYWVhZjE=|1612601203|5b2e13fabc4c8c0c2799b822e3c899a3dfde18d3"; n_c=1; captcha_ticket_v2="2|1:0|10:1612601227|17:captcha_ticket_v2|244:eyJhcHBpZCI6IjIwMTIwMzEzMTQiLCJyZXQiOjAsInRpY2tldCI6InQwM2owNWdXOW10TGdublgydlFSaWQ2VnV5dmg5SFFKZlZsVm96a3Bjd3ZPOFpwdGhiN2VvOXF1X2VqLUNGcVl3VWZ5OG1UeHhhYlhZTUg3SGQwLTRuZWVHcTZWamROdFBvYURYZ1VjTVdkdHVabWdUcDQxWkNraWcqKiIsInJhbmRzdHIiOiJAWkczIn0=|2be273676cf7f4ac916b60186d285240c989edafd0d11725f09079660d75d75a"; z_c0="2|1:0|10:1612601290|4:z_c0|92:Mi4xSXdBckFBQUFBQUFBRUZtaHYzZVJFaWNBQUFDRUFsVk55dVJGWUFDOWVZbXRBT1hCUHFJNkdGY2Z5NW9ZLVBRZjFB|9fb1ea92b3598b21a2f83b8ce50f1f819c8a50ff911627c6c91933775d3d990c"; tshl=; tst=h; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1612601292; KLBRSID=c450def82e5863a200934bb67541d696|1612604884|1612601196',
        'User-Agent': 'Mozilla%d/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36' % random.randint(
            55, 100),
    }
    r = requests.get(url, headers=headers)
    # print(r.status_code)
    html = etree.HTML(r.text)       # 调用HTML类初始化，构造XPath解析对象

    # 获取数据
    titles = html.xpath(path[num] + get_title[num])
    links = html.xpath(path[num] + get_link[num])

    # num==1是微博，由于微博的会出现推荐的话题，这里将其舍去
    if num == 1:
        error = 'javascript:void(0);'
        for j in range(20):
            if links[j] == error:
                del links[j]
                del titles[j]

    # 将前10个结果存到res里
    res = web_name[num] + "\n"
    for i in range(10):
        res = res + str(i+1) + " " + titles[i] + "\n" + pre[num] + links[i] + "\n\n"
    return res

#
def send_email(text):
    # 初始信箱设置
    from_addr = '317327783@qq.com'  # 发件人邮箱（需要开启smtp服务）
    password = 'esyfkpzkhunsbica'  # 邮箱密钥
    recipients = 'qualia0503@gmail.com','3626309546@qq.com' # 收件人邮箱
    # recipients = '317327783@qq.com','quzheng1983@outlook.com' # 收件人邮箱
    # to_addr =", ".join(recipients)  # 收件人邮箱
    smtp_server = 'smtp.qq.com'

    # 邮件内容
    msg = MIMEText(text, 'plain', 'utf-8')
    msg['From'] = Header(from_addr)
    # msg['To'] = to_addr
    msg['To'] = ", ".join(recipients)
    msg['Subject'] = Header('知乎微博热门话题')

    # 开启发信服务，这里使用的是加密传输
    server = smtplib.SMTP_SSL(smtp_server)
    server.connect(smtp_server, 465)
    server.login(from_addr, password)
    server.sendmail(from_addr, recipients, msg.as_string())

    # 关闭服务器
    server.quit()


# 爬取url
url = ['https://www.zhihu.com/hot',
        'https://s.weibo.com/top/summary',]
n = len(url)
res = ""
for i in range(n):
    res = res + get_data(url[i], i) + "\n\n"
print(res)

# 发送邮件
send_email(res)

