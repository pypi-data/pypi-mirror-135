# python-nacos-client
- pip3 install py-nacos-client
- 可按照代码库中microservice.yaml文件进行注册服务配置
- adapter_server中主要方法instance = load_active_content() 返回为加载yaml转换成一个当前服务实例对象，需要传入文件绝对路径
- nacos_client.init(instance) 初始化实例，自动注册，心跳，注销
- 项目入口引入并执行以上内容

# 项目中使用
- nacos_client.get_client() 全局获取客户端实例
- nacos_client.get_random_provider(server_name) 权重ip，传参目标服务名
- nacos_client.load_balance_client_avr(server_name) 轮询ip，传参目标服务名
- nacos_client.add_regist(instance) 手动注册指定实例
- nacos_client.remove_ins(instance) 手动注销指定实例
- nacos_client.stop() 手动退出: 注销当前已注册的全部实例（多端口也算一个可用实例）
- @nacos_client.client_warpper装饰器改变一个函数的内容为返回一个ip

```python
# 可参照init文件内入口使用
# ----logger 用法
# 当前为终端输出，项目下指定路径与输出格式即可输出到文件中

# import logging
# _format =logging.Formatter(
# fmt='[%(asctime)s]-[%(name)s]-[line:%(lineno)d] -%(levelname)-4s: %(message)s',
# datefmt='%Y-%m_%d %H:%M:%S',
# )
# _handler = logging.handlers.TimedRotatingFileHandler("/var/..")
# _handler.setFormat(_format)
# _handler.setLevel("INFO")




# @nacos_client.client_warpper(client.get_random_provider, "hbase-agent")
#     def a():
#         pass
```