from core import print_open_endpoints
from endpoint.webhook_endpoint import app

if __name__ == '__main__':
    # 设置配置项来指定 IP 地址和端口号
    app.config['HOST_IP'] = '0.0.0.0'
    app.config['HOST_PORT'] = 5000
    # 获取配置项中的 IP 地址和端口号
    ip_address = app.config['HOST_IP']
    port = app.config['HOST_PORT']
    print_open_endpoints()
    # 启动 Flask 应用
    app.run(host=ip_address, port=port)
