from urllib import parse,request
import json

import requests

get_plan_list = {"user_id": "7"}
add_plan = {"user_id": "7", "plan_name": "测试plan", "plan_start_date": "2018-09-20", "plan_end_date": "2018-09-28", "plan_share": "private"}
get_plan = {"plan_id": "2", "user_id": "7"}
add_plan_item = {"user_id": "7", "plan_id": "2", "plan_item_type": "flight", "plan_item_date": "2018-09-20", "plan_item_json": {"filght_id": "CA232", "flight_time": "2018-09-20 22:10:00"}, "prev_plan_item_id": "1"}
get_plan_item_list = {"user_id": "7", "plan_id": "2"}
del_plan_item = {"user_id": "7", "plan_item_id": "6"}

headers = {
    "Content-Type": "application/json; charset=UTF-8",
    "Referer": "http://jinbao.pinduoduo.com/index?page=5",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
    }

url = 'http://127.0.0.1:8000/travel_fox/get_plan_list/'
response = requests.post(url, data=json.dumps(get_plan_list), headers=headers).text
print(response)
