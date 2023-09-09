import requests
from lxml import etree
import json
from email.message import Message
import smtplib
from threading import Timer


class Weibo:

    # 初始化 （发件人邮箱，发件人邮箱密码，收件人邮箱）

    def __init__(self, sender, password, receiver):
        self.sender = sender
        self.password = password
        self.receiver = receiver
        # 处理爬取的信息

    def handle(self):
        url = "http://s.weibo.com/top/summary?cate=homepage"
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.5; rv:10.0.1) Gecko/20100101 Firefox/10.0.1 SeaMonkey/2.7.1"}
        response = requests.get(url, headers=headers)
        result = response.text
        html = etree.HTML(result)

        # html内容
        content = html.xpath("//script/text()")[-2]
        # 得到网页的字典数据,利用json解析

        start = content.find("(")
        substr = content[start + 1:-1]
        dict_data = json.loads(substr)

        # 解析出来的html数据
        html_data = etree.HTML(dict_data["html"])
        # 热搜榜排名

        order = html_data.xpath("//tr/td[1]/span/em/text()")

        # 热搜榜标题

        title = html_data.xpath("//tr/td[2]/div/p/a/text()")

        # 热搜榜链接

        url = html_data.xpath("//tr/td[2]/div/p/a/@href")

        # 热搜榜访问量

        view = html_data.xpath("//tr/td[3]/p/span/text()")

        return title, url

    # 发送邮件，这里直接用html方式发送

    def sendEmail(self):

        t, u = self.handle()

        html_content = '''

            <html>

                <body>

                    <a href=" ''' + 'http://s.weibo.com' + u[0] + ' ">' + t[0] + '''</a></p><br>

                    <a href=" ''' + 'http://s.weibo.com' + u[1] + ' ">' + t[1] + '''</a></p><br>

                    <a href=" ''' + 'http://s.weibo.com' + u[2] + ' ">' + t[2] + '''</a></p><br>

                    <a href=" ''' + 'http://s.weibo.com' + u[3] + ' ">' + t[3] + '''</a></p><br>

                    <a href=" ''' + 'http://s.weibo.com' + u[4] + ' ">' + t[4] + '''</a></p><br>

                    <a href=" ''' + 'http://s.weibo.com' + u[5] + ' ">' + t[5] + '''</a></p><br>

                    <a href=" ''' + 'http://s.weibo.com' + u[6] + ' ">' + t[6] + '''</a></p><br>

                    <a href=" ''' + 'http://s.weibo.com' + u[7] + ' ">' + t[7] + '''</a></p><br>

                    <a href=" ''' + 'http://s.weibo.com' + u[8] + ' ">' + t[8] + '''</a></p><br>

                    <a href=" ''' + 'http://s.weibo.com' + u[9] + ' ">' + t[9] + '''</a></p><br>

                </body>

            </html>

        '''

        msg = Message()

        # 邮件标题

        msg["Subject"] = "微博实时热搜"

        # 邮件发送者

        msg["From"] = self.sender

        # 邮件接受者

        msg["To"] = self.receiver

        # 邮件内容格式

        msg.set_type("text/html")

        # 邮件内容

        msg.set_payload(html_content, 'utf-8')

        try:

            smtp = smtplib.SMTP_SSL('smtp.qq.com', 465)

            smtp.login(self.sender, self.password)

            smtp.sendmail(self.sender, self.receiver, msg.as_string())

            smtp.quit()

            print("发送成功！")

        except smtplib.SMTPException:

            print("发送失败")

    # 每隔半小时发送邮件（定时任务）

    def run_task(self):

        self.sendEmail()

        task = Timer(1800, self.run_task)

        task.start()


if __name__ == '__main__':
    w = Weibo("317327783@qq.com", "esyfkpzkhunsbica", "317327783@qq.com")

    task = Timer(1, w.run_task)

    task.start()
