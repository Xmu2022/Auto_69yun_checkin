#################### V2 ################
# -*- coding: utf-8 -*-

import aiohttp
from bs4 import BeautifulSoup
import json
import re
import asyncio

domains = ["69yun69.com"]

def load_credentials(filepath):
    """从文件中加载用户凭据"""
    credentials = []
    with open(filepath, "r", encoding="utf-8") as file:
        for line in file:
            email, passwd = line.strip().split(',')
            credentials.append((email, passwd))
    return credentials

def convert_mb_to_gb(mb_value):
    """将MB转换为GB，并保留两位小数"""
    if mb_value.endswith("MB"):
        mb = float(mb_value.replace("MB", "").strip())
        gb = mb / 1024
        return f"{gb:.2f}GB"
    return mb_value

async def auto_checkin(domain, email, passwd):
    login_url = f"https://{domain}/auth/login"
    checkin_url = f"https://{domain}/user/checkin"
    user_info_url = f"https://{domain}/user"

    async with aiohttp.ClientSession() as session:
        # 模拟登录请求
        login_data = {
            "email": email,
            "passwd": passwd,
            "code": ""
        }
        headers = {
            "Referer": "; auto"
        }

        async with session.post(login_url, data=login_data, headers=headers, ssl=False) as login_response:
            # 检查是否登录成功
            if login_response.status != 200:
                return None

        # 模拟签到请求
        async with session.post(checkin_url, headers=headers, ssl=False) as checkin_response:
            checkin_response_text = await checkin_response.text()

        # 登录成功后获取用户信息页面
        async with session.get(user_info_url, headers=headers, ssl=False) as user_info_response:
            user_info_text = await user_info_response.text()

    print("user_info_text:", user_info_text)  # 打印原始 HTML 内容

    # 使用 BeautifulSoup 解析 HTML 并提取套餐级别
    soup = BeautifulSoup(user_info_text, 'html.parser')

    # 根据具体的 HTML 结构，定位并提取套餐级别信息
    package_level_div = soup.find('div', class_='card-body pt-2 pl-5 pr-3 pb-1')
    if package_level_div:
        package_level_text = package_level_div.find('p', class_='text-dark-50')
        package_level = package_level_text.get_text(strip=True).split(':')[0].strip() if package_level_text else "N/A"
    else:
        package_level = "N/A"
    print('package_level:', package_level)

    username_match = re.search(r"name: '([^']*)'", user_info_text)
    expire_date_match = re.search(r"Class_Expire': '([^']*)'", user_info_text)
    traffic_match = re.search(r"Unused_Traffic': '([^']*)'", user_info_text)

    username = username_match.group(1) if username_match else "N/A"
    expire_date = expire_date_match.group(1) if expire_date_match else "N/A"
    traffic = convert_mb_to_gb(traffic_match.group(1)) if traffic_match else "N/A"

    checkin_result_json = json.loads(checkin_response_text)

    # 判断签到状态
    if checkin_result_json.get("ret") == 0:
        message = f"🎉 签到结果 🎉\n\n 您似乎已经签到过了...😅\n\n🔑 用户名: {username}\n📅 套餐到期时间: {expire_date}\n📊 剩余流量: {traffic}\n🏆 套餐级别: {package_level}"
    elif checkin_result_json.get("ret") == 1:
        message = f"🎉 签到结果 🎉\n\n ✅ 签到成功！\n尊贵的 🌟 {package_level}，您获得了 {checkin_result_json.get('traffic')} 流量. 🎊\n\n🔑 用户名: {username}\n📅 套餐到期时间: {expire_date}\n📊 剩余流量: {traffic}\n🏆 套餐级别: {package_level}"
    else:
        message = f"🎉 签到结果 🎉\n\n 签到失败! 😅\n\n{checkin_response_text}\n🔑 用户名: {username}\n📅 套餐到期时间: {expire_date}\n🏆 剩余流量: {traffic}\n🏆 套餐级别: {package_level}"

    return message.strip()

async def main():
    credentials = load_credentials("credentials.txt")  # 读取凭据文件
    for email, passwd in credentials:
        for domain in domains:
            print(f"Checking in for {email} with domain {domain}")
            checkin_result = await auto_checkin(domain, email, passwd)
            if checkin_result:
                print(checkin_result)
                break
            else:
                print('签到失败!')

if __name__ == "__main__":
    asyncio.run(main())
