import requests
import zipfile
import os
import sys
import subprocess


def download_file(url, local_path):
    """通过 HTTPS 下载文件"""
    print(f"开始下载文件: {url}")
    response = requests.get(url, verify=False)
    if response.status_code == 200:
        with open(local_path, "wb") as file:
            file.write(response.content)
        print(f"文件下载成功，保存至: {local_path}")
        return True
    else:
        print(f"下载失败，状态码: {response.status_code}，请检查 URL 或网络连接。")
        return False


def unzip_file(zip_path, extract_to):
    """解压缩 ZIP 文件"""
    print(f"开始解压缩文件: {zip_path}")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"文件解压成功，已解压到: {extract_to}")


def run_main_program(main_program_path):
    """运行主程序"""
    print(f"开始运行主程序: {main_program_path}")
    result = subprocess.run([sys.executable, main_program_path], capture_output=True, text=True)
    if result.returncode == 0:
        print("主程序运行成功！")
    else:
        print(f"主程序运行失败，返回码: {result.returncode}")
        print(f"错误输出: {result.stderr}")  # 输出错误信息

def main():
    url = "https://69yun69.com/download/scripts/69tools.zip"  # 这是更新的代码的 URL
    zip_file_path = "69tools.zip"
    extract_to = "."  # 解压路径
    main_program = "main.py"  # 替换为实际的入口文件名
    execute_path = '69tools' # 执行路径
    if download_file(url, zip_file_path):
        unzip_file(zip_file_path, extract_to)
        main_program_path = os.path.join(execute_path, main_program)

    
        #     # 获取当前工作目录
        # current_directory = os.getcwd()
        # print(f"当前工作目录: {current_directory}")
        
        # # 检查共享对象文件的详细信息
        # file_path = "69tools/checkin_69_auto.cpython-38-x86_64-linux-gnu.so"
        # try:
        #     file_info = subprocess.check_output(['ls', '-l', file_path], text=True)
        #     print(f"文件详细信息:\n{file_info}")
        # except subprocess.CalledProcessError as e:
        #     print(f"错误: {e}")

        
        
        # 检查主程序文件是否存在再运行
        if os.path.isfile(main_program_path):
            run_main_program(main_program_path)
        else:
            print(f"主程序文件不存在: {main_program_path}")
    else:
        print("下载文件失败，请检查网络或文件地址。")


if __name__ == "__main__":
    main()
