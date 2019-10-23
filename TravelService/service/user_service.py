import datetime
import json

import requests

from TravelService.models import TravelUser, TravelShare, TravelPlan

import TravelService.wechat_data as wx

from django.db import connection

class UserService:

    @staticmethod
    def wx_login_request(wx_code):
        url = "https://api.weixin.qq.com/sns/jscode2session?appid=" + wx.app_id + \
              "&secret=" + wx.app_secret_id + "&js_code=" + wx_code + "&grant_type=authorization_code"
        response = requests.get(url).text
        wx_res = json.loads(response)
        return wx_res

    @staticmethod
    def get_user(user_name):
        try:
            travel_user = TravelUser.objects.get(user_name=user_name)
            return {"flag": "1", "travel_user": travel_user}
        except TravelUser.DoesNotExist:
            return {"flag": "0"}

    @staticmethod
    def wx_login(wx_code):
        wx_res = UserService.wx_login_request(wx_code)

        if "errcode" in wx_res.keys():
            return {"flag": "-1"}

        wx_open_id = wx_res['openid']
        try:
            travel_user = TravelUser.objects.get(user_wechat=wx_open_id)
            return {"flag": "1", "travel_user": travel_user.get_json()}
        except TravelUser.DoesNotExist:
            return {"flag": "0"}

    @staticmethod
    def wx_register(wx_code, user_name, user_icon):
        wx_res = UserService.wx_login_request(wx_code)

        if "errcode" in wx_res.keys():
            return {"flag": "-1"}

        wx_open_id = wx_res['openid']
        travel_user = TravelUser()
        travel_user.user_wechat = wx_open_id
        travel_user.user_name = user_name
        travel_user.user_icon = user_icon
        travel_user.save()

        travel_plan = TravelPlan()

        travel_plan.plan_name = '北京的旅行计划示例'

        travel_plan.plan_startDate = datetime.datetime.strptime('2019-01-01', "%Y-%m-%d")
        travel_plan.plan_endDate = travel_plan.plan_startDate
        travel_plan.plan_user_id = travel_user.id
        travel_plan.plan_user = travel_user
        travel_plan.plan_share = 'public'
        travel_plan.plan_place1 = '北京'
        travel_plan.plan_place2 = '北京'
        travel_plan.save()

        travel_plan.plan_createTime = datetime.datetime.strptime('2000-01-01', "%Y-%m-%d")
        travel_plan.save()

        ex_plan_id = travel_plan.id
        print(ex_plan_id)

        travel_share = TravelShare(share_type='x', share_plan=travel_plan, share_user=travel_user)
        travel_share.save()

        cursor = connection.cursor()
        sql = "insert into TravelService_travelplanitem (planItem_date, planItem_type, planItem_json, planItem_order, planItem_plan_id) SELECT planItem_date, planItem_type, planItem_json, planItem_order, " + str(ex_plan_id) + " AS planItem_plan_id FROM TravelService_travelplanitem where planItem_plan_id = 7"
        cursor.execute(sql)

        return {"flag": "1", "travel_user": travel_user.get_json()}
