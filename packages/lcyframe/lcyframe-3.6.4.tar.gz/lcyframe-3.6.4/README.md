# 基于 tornado 框架封装


一、使用方法：把包拷贝到你项目根目录下

    1、开启一个服务：
        app = LcyFrame(port, handler_path_list, **kwargs)
        app.run()

    2、worker.py: 消息队列服务。请指定一个存放消费者的文件夹worker，把方法文件放里面
    3、crontab: 给予tornado实现的定时任务。请指定一个存放需要执行的方法的文件夹crontab，把方法文件放里面
    4、token 基于AES设计，
    5、header 必填字段: uid、token

二、该框架集成：
    redis
    mongo
    mysql:
        # 一波操作准确无误后，需要手动commit，让其他事务可见；中间出问题，需要手动rollback回滚
        from lcyframe.libs.singleton import MySqlCon
        mysql = MySqlCon.get_connection(**{"password": ""})
        try:
            s = mysql.insert("insert into alipay(zname, zpassword) values('13282920751', '33232')")
            s = mysql.insert("insert into alipay(zname, zpassword) values(%s, %s)", ['13282920751', '33232'])
            s = mysql.insert("insert into alipay(zname, zpassword) values('13282920751', '33232')", commit=True)
            d = mysql.find("select * from alipay")
            raise Exception("程序逻辑500错误等流程错误中断，回滚")
        except:
            mysql.rollback()
        finally:
            mysql.commit()
    ssdb
    nsq:
        1、在配置文件设置配置，主进程启动时，自动注册所有生产者事件。
          nsq_config:     # 发布订阅队列配置
          lookupd_http_addresses: "127.0.0.1:4161"
          nsqd_tcp_addresses: ["127.0.0.1:4150"]
          producer_dir:
            - producer/nsq
          workers_dir:
            - works/nsq
        2、定义生产者：on_create_user
            class PubLishUser(WriteNsq):
                topic = "test".lower()
                __events__ = ("on_create_user", )
        3、定义消费者：on_create_user
            @MqttTask(topic="test", channel="channel2")
            class ExampleEvent2(ReadNsq, BaseModel):
                @classmethod
                def on_create_user(cls, **msg):
                    print msg, "channel2"
                    return msg
        4、三种调用方式：
            一、
            from producer.nsq import pub_user
            pub_user.PubLishUser().on_create_user({"a": 1})
            二、系统自动加载，不能与方法一同时使用
            self.application.nsq.PubLishUser.on_create_user({"a": 1})
            三、原生方法
            self.application.nsq.pub("topic", json.dumps(kw))
            
        5、启动消费者服务：
            w = NsqWorker(**config)
            w.start()
    消息队列：
        # mq调用方法
        # self.application.mq.put({"event": "up", "a": 1})

        # nsq调用方法
        # self.application.nsq.pub("test", '{"event": "on_create_user", "uid": 0}')
        # from producer.nsq import user
        # user.PublishUser().on_create_user({"uid": 0})
        self.application.nsq.NsqEvent.on_create_user({"uid": 0})

        # mqtt调用方法,2种方法不可同时使用，否则会抢占链接
        # from producer.mqtt import user
        # user.MqttEvent().on_create_user({"a": "mqtt_test"})
        self.application.mqtt.MqttEvent.on_create_user({"a": "mqtt_test"})

    工具集函数
    handler通用方法
    module通用方法

三、支持以packages的方式安装到环境内



四、API参数与返回规则

- name: "demo"  # API handler 类名
  apis: "/demo"
  description: 样例
  method:
    post:
        summary: 添加
        description: 测试post
        parameters:
          - name: str
            in: query
            description: 手机号
            required: false
            type: string
            regex: ^(0|86|17951)?(13[0-9]|15[012356789]|17[0-8]|18[0-9]|14[57])[0-9]{8}$
          - name: int
            in: query
            description: 整形
            required: true
            type: integer
            allow: [1,2]
          - name: float
            in: query
            description: 浮点型
            required: true
            type: float
            allowed: [1.0,2.0]
          - name: json
            in: query
            description: json格式
            required: true
            type: json
            allowed: []
          - name: form-data
            in: form-data
            description: 位置：body_json，参数放在body内，以multipart/form-data方式，json格式。json类型的参数，设为非必须时，需提供默认值
            required: false
            type: json
            default: []
          - name: form-data2
            in: form-data
            description: 位置：body_json，参数放在body内，以multipart/form-data方式，json格式。json类型的参数，设为非必须时，需提供默认值
            required: false
            type: string
          - name: www-form
            in: www-form
            description: 位置：body_form，参数放在body表单内，以multipart/x-www-form-urlencoded方式提交。手机号正则限定
            required: false
            type: string
          - name: excel
            in: form-data
            description: 上传文件，参数放在body内，以multipart/form-data方式提交;excel=self.params["excel"]
            required: false
            type: file
        responses:
            name: 名称
            sex: 姓名
            bool_type: true|bool
            num: 1.2|float
            dict:     # 字典
              a: [1,2]   #
              b: [{"key": 1}]
            list:     # 列表
              - item_x:
                - key_1: value_1  # 字典
                  key_2: value_2
                - key_3: value_3
                  key_4: value_4
              - item_y: value_y


    get:
        summary: 查看
        description: 测试get
        parameters:

          - name: a
            in: path
            description: 角色id
            required: true
            type: integer
          - name: b
            in: query
            description: 供应商id
            required: false
            type: string
          - name: d
            in: path
            description: 城市全拼列表
            required: false
            type: int
            allowed: [1,2]

- apis: "/user_list"
  name: "userlist"  # API handler 类名
  description: 用户列表
  method:
    post:
        summary: 添加
        description: 测试post
        parameters:
          - name: a
            in: path
            description: 角色id
            required: true
            type: integer
          - name: b
            in: query
            description: 供应商id
            required: false
            type: string
          - name: c
            in: body
            description: 手机号
            required: false
            type: string
            regex: ^(0|86|17951)?(13[0-9]|15[012356789]|17[0-8]|18[0-9]|14[57])[0-9]{8}$
          - name: d
            in: path
            description: 城市全拼列表
            required: false
            type: int
            allowed: [1,2]
          - name: pic
            in: file
            description: 文件
            required: false
            type: file
        responses:
            name: 名称
            sex: 姓名
            dict:     # 字典
              a: 1
              b:
              - a: 1
              - b: 2
            list:     # 列表
              - a:
                - x: x  # 字典
                  xx: xx
                - x: x
                  xx: xx
              - b: 2


    get:
        summary: 查看
        description: 测试get
        parameters:

          - name: a
            in: path
            description: 角色id
            required: true
            type: integer
          - name: b
            in: query
            description: 供应商id
            required: false
            type: string
          - name: d
            in: path
            description: 城市全拼列表
            required: false
            type: int
            allowed: [1,2]
