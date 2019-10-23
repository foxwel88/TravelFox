import datetime
import json
import TravelService.service.img_service as img

from django.db import models


class Log(models.Model):
    log_time = models.DateTimeField(auto_now_add=True)
    log_user_id = models.IntegerField(blank=True, null=True)
    log_user_name = models.CharField(max_length=50, blank=True, null=True)
    log_ip = models.CharField(max_length=50, blank=True, null=True)
    log_method = models.CharField(max_length=50, blank=True, null=True)
    log_data = models.CharField(max_length=10086, blank=True, null=True)
    log_desc = models.CharField(max_length=50, blank=True, null=True)


class TravelUser(models.Model):
    user_name = models.CharField(max_length=20)
    user_icon = models.CharField(max_length=250, blank=True, null=True)
    user_phone = models.CharField(max_length=20, blank=True, null=True, unique=True)
    user_email = models.CharField(max_length=50, blank=True, null=True, unique=True)
    user_wechat = models.CharField(max_length=100,blank=True, null=True,  unique=True)
    def get_json(self):
        return {'user_id': self.id, 'user_name': self.user_name, 'user_wechat': self.user_wechat,
                'user_email': self.user_email, 'user_icon': self.user_icon}


class TravelPlan(models.Model):
    plan_user = models.ForeignKey('TravelUser', on_delete=models.SET_NULL, null=True)
    plan_name = models.CharField(max_length=20)
    plan_createTime = models.DateTimeField(auto_now_add=True)
    plan_startDate = models.DateTimeField()
    plan_endDate = models.DateTimeField()
    plan_place1 = models.CharField(max_length=50, blank=True, null=True)
    plan_place2 = models.CharField(max_length=50, blank=True, null=True)
    plan_pic = models.CharField(max_length=50, blank=True, null=True)
    # 分享类型:private, public
    plan_share = models.CharField(max_length=20)

    def get_json(self):
        return {'plan_id': self.id, 'plan_name': self.plan_name, 'plan_user_id': self.plan_user_id,
                'plan_createTime': datetime.datetime.strftime(self.plan_createTime, '%Y-%m-%d %H:%M:%S'),
                'plan_startDate': datetime.datetime.strftime(self.plan_startDate, '%Y-%m-%d'),
                'plan_endDate': datetime.datetime.strftime(self.plan_endDate, '%Y-%m-%d'),
                'plan_share': self.plan_share,
                'plan_place1': self.plan_place1,
                'plan_place2': self.plan_place2,
                'plan_pic': img.get_img_path(self.plan_pic, self.plan_place1, self.plan_place2),
                'user_name': self.plan_user.user_name,
                'user_icon': self.plan_user.user_icon}


class TravelPlanItem(models.Model):
    planItem_plan = models.ForeignKey('TravelPlan', on_delete=models.CASCADE)
    planItem_date = models.DateTimeField()
    planItem_type = models.CharField(max_length=20)
    planItem_json = models.TextField()
    planItem_order = models.FloatField()

    def get_json(self):
        print(self.planItem_json)
        return {'plan_item_id': self.id, 'plan_id': self.planItem_plan_id,
                'plan_item_date': datetime.datetime.strftime(self.planItem_date, '%Y-%m-%d'),
                'plan_item_type': self.planItem_type,
                'plan_item_json': json.loads(self.planItem_json),
                'planItem_order': self.planItem_order,
                'date_flag': ""}


class TravelShare(models.Model):
    share_plan = models.ForeignKey('TravelPlan', on_delete=models.CASCADE)
    share_user = models.ForeignKey('TravelUser', on_delete=models.CASCADE)
    # 分享类型:R,W,X
    share_type = models.CharField(max_length=20)
