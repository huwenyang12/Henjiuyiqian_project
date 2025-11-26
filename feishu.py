import json
import requests
from requests_toolbelt import MultipartEncoder


class FeiShu(object):

    webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/f8b618bc-5c42-4434-9389-8a307f4d0aec"

    def get_token(self):
    	# 调用机器人的地址 如有更改 可查看飞书文档
        url = 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal'
        headers = {'content-type': 'application/json; charset=utf-8'}
        data = {'app_id': 'cli_a362e6124a38900e',
                'app_secret': '7IvedN0e4g0fNupJlZ04GfNJ2xCrLRV1'}
        token = requests.post(url, headers=headers, json=data).json()['tenant_access_token']
        print(token)
        return token

    def upload_feishu_image(self, image_file):
        url = "https://open.feishu.cn/open-apis/im/v1/images"
        form = {'image_type': 'message',
                'image': (open(image_file, 'rb'))}  # 需要替换具体的path 
        multi_form = MultipartEncoder(form)
        token = self.get_token()
        headers = {
            'Authorization': 'Bearer {}'.format(token),  ## 获取tenant_access_token, 需要替换为实际的token
        }
        headers['Content-Type'] = multi_form.content_type
        response = requests.request("POST", url, headers=headers, data=multi_form)
        print(response.headers['X-Tt-Logid'])  # for debug or oncall
        return json.loads(response.content)

    def send_feishu_image(self,image_file, web_hook):
        response = self.upload_feishu_image(image_file)
        img_key = response['data']['image_key']
        header = {
            "Content-Type": "application/json;charset=UTF-8"
        }
        message_body = {
            			"msg_type": "image",
           				 "content": {'image_key': img_key}
						}

        ChatRob = requests.post(url=web_hook, data=json.dumps(message_body), headers=header)
        opener = ChatRob.json()

        if opener["StatusMessage"] == "success":
            print(u"%s 通知消息发送成功！" % opener)
        else:
            print(u"通知消息发送失败，原因：{}".format(opener))
        return opener

    def send_feishu_message(self, url, message):
        payload_message = {
            "msg_type": "text",
            "content": {
                "text": message
            }
        }
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=json.dumps(payload_message))
        return response

    def send_message(self, message):
        return self.send_feishu_message(self.webhook_url, message)

    def send_image(self, image_file):
        return self.send_feishu_image(image_file, self.webhook_url)

