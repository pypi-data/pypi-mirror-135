******：
******、******：
    1、******，******app_key、token
    2、******app_key、token******headers******，******
    3、******：headers["appkey"]******headers["token"]
******、demo******：
    1、******，******uid、token
    2、******uid、token******headers******，******
    3、******：headers["uid"]******headers["token"]

******、******
    ******：
        1、******business_id，bind_device_id******":"******，******app_key=business_id:bind_device_id
        2、******app_key******aes32******，******token
        3、******app_key******token******headers******，******
        4、******：headers["appkey"]******headers["token"]
    ******：
        1、******alipay_id，bind_device_id******":"******，******app_key=alipay_id:bind_device_id
        2、******app_key******aes32******，******token
        3、******app_key******token******headers******，******
        4、******：headers["appkey"]******headers["token"]

******、api******:
    1、app_key: ******key，******headers******appkey
    2、******,token：
        1）、******ip******IP******
        2）、******POST******k=v******
        3）、******key******，******，******'&'******；******str="a=1&b=2&c=3"
        4）、******str******secret_key******aes******（AES-256(32******)、ECB******），******sign=AES(secret_key, str)
        5）、******sign******secret_key******HMAC-MD5，******，******token。token=hmac.HMAC(secret_key, sign).hexdigest()
        6）、******token******headers******
        7）、******body******application/x-******-form-urlencoded******post******
    3、******：headers["appkey"]******headers["token"]

******、******：
    demo******，******。******，******POST******。
        ******：
            {
                "pay_channel_code": "DemoCardPay",
                "company_id": "******ID",
                "psd_order_id": "******",
                "demo_order_id": "demo******ID",
                "order_amount": "******",
                "fact_amount": '******',
                "reward_amount": '******',
                "order_type": '******',
                "timestamp": "******",
                "state": "******" # 3 ****** -1 ******
            }
        ******：
            {
                "msg": "success"
            }



******、******：
    1、******、******
        from libs import helps
        from config.permission_conf import *

        @helps.params(ANONYMOUS_PERMISSION)	# 0 ******
        @helps.params(LOGIN_PERMISSION) # 1 ******

        ******，******，self.company（******）******self.member（******），
        ******，******，******、******；******，******handler******
    2、******api
        from libs import helps

        @helps.api()

******、******
    1、mq_start.py：******（******，******）
    2、works/mq******：******1******，******（******）。******：xxx_worker.py
    3、order_work_start.py（******，******，******）


******、******40******，5******5******，****** ******。
   ******：****** * ******（******）* 60（******）* ******