import requests

# 定义接口的URL
url = 'http://localhost:8888/pdf_parse'

# 读取要上传的PDF文件
# pdf_file_path = '1506.02640v5.pdf'
pdf_file_path = '经济月报2023.6.pdf'

# 准备请求的文件和数据
files = {
    'pdf_file': open(pdf_file_path, 'rb')
}
data = {
    'parse_method': 'auto',
    'model_json_path': None,  # 如果有路径，替换为实际路径
    'is_json_md_dump': True,
    'output_dir': 'output'
}

# 发送POST请求
response = requests.post(url, files=files, data=data)

# 处理响应
if response.status_code == 200:
    print('成功解析PDF:', response.json()['images'])
else:
    print('请求失败，状态码:', response.status_code)
    print('响应内容:', response.text)
