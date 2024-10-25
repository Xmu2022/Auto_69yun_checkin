
# -*- coding: utf-8 -*-

import requests
import zipfile
import os
import sys
import subprocess
import asyncio


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


async def run_main_program(main_program_path):
    """运行主程序（异步处理）"""
    print(f"开始运行主程序: {main_program_path}")
    result = subprocess.run([sys.executable, main_program_path], capture_output=True, text=True)
    if result.returncode == 0:
        print("主程序运行成功！")
    else:
        print(f"主程序运行失败，返回码: {result.returncode}")
        print(f"错误输出: {result.stderr}")  # 输出错误信息


async def main():
    url = "https://69yun69.com/download/scripts/69tools.zip"  # 这是更新的代码的 URL
    zip_file_path = "69tools.zip"
    extract_to = "."  # 解压路径
    main_program = "main.py"  # 替换为实际的入口文件名
    execute_path = '69tools'  # 执行路径

    if download_file(url, zip_file_path):
        unzip_file(zip_file_path, extract_to)
        main_program_path = os.path.join(execute_path, main_program)

        # 检查主程序文件是否存在再运行
        if os.path.isfile(main_program_path):
            await run_main_program(main_program_path)  # 异步运行主程序
        else:
            print(f"主程序文件不存在: {main_program_path}")
    else:
        print("下载文件失败，请检查网络或文件地址。")


if __name__ == "__main__":
    asyncio.run(main())  # 异步调用主函数
