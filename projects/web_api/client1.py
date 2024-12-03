import requests
import os
import base64

# 定义接口的URL
url = 'http://localhost:5004/pdf_parse'

# 读取要上传的PDF文件
pdf_file_path = '经济月报2023.3.pdf'

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
    response_data = response.json()
    images = response_data.get('images', [])
    md_content = response_data.get('md_content', '')

    # 创建output和images文件夹
    output_dir = data['output_dir']
    images_dir = os.path.join(output_dir, "images")
    os.makedirs(images_dir, exist_ok=True)

    # 保存images字段中的内容到images文件夹中
    for image in images:
        base64_data = image['base64']
        try:
            # 如果base64_data包含逗号，假设它是data URI格式并去掉前缀
            if ',' in base64_data:
                base64_data = base64_data.split(',')[1]
            image_data = base64.b64decode(base64_data)
            image_path = os.path.join(images_dir, image['name'])
            with open(image_path, 'wb') as img_file:
                img_file.write(image_data)
            print(f"Saved image: {image_path}")
        except (IndexError, ValueError) as e:
            print(f"Error decoding image {image['name']}: {e}")

    # 将md_content写入一个Markdown文件
    md_file_path = os.path.join(output_dir, 'output.md')
    with open(md_file_path, 'w') as md_file:
        md_file.write(md_content)
    print(f"Markdown content saved to {md_file_path}")

else:
    print('请求失败，状态码:', response.status_code)
    print('响应内容:', response.text)
