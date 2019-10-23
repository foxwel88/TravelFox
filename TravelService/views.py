import datetime
import json
from django.shortcuts import HttpResponse

from TravelService.models import Log
from TravelService.service.plan_service import PlanService
from TravelService.service.user_service import UserService
import logging

logger = logging.getLogger('django')


def test_connect(request):
    return HttpResponse("ok")


def wx_login(request):
    post_json_str = request.body.decode('UTF-8')
    post_json = json.loads(post_json_str)

    wx_code = post_json['wx_code']

    login_res = UserService.wx_login(wx_code)

    log = Log(log_method='wx_login', log_data=post_json_str)
    log.save()
    return HttpResponse(json.dumps(login_res))


def wx_register(request):
    post_json_str = request.body.decode('UTF-8')
    post_json = json.loads(post_json_str)
    print(post_json)

    wx_code = post_json['wx_code']
    user_name = post_json['user_name']
    user_icon = post_json['user_icon']

    register_res = UserService.wx_register(wx_code, user_name, user_icon)

    log = Log(log_method='wx_login', log_data=post_json_str)
    log.save()
    return HttpResponse(json.dumps(register_res))


def get_plan_list(request):

    post_json_str = request.body.decode('UTF-8')
    post_json = json.loads(post_json_str)

    user_id = int(post_json['user_id'])

    plan_list_json_str = PlanService.get_plan_list(user_id)

    log = Log(log_user_id=user_id, log_method='get_plan_list', log_data=post_json_str)
    log.save()
    return HttpResponse(plan_list_json_str)


def get_plan(request):
    post_json_str = request.body.decode('UTF-8')
    post_json = json.loads(post_json_str)

    plan_id = int(post_json['plan_id'])

    plan_json_str = PlanService.get_plan(plan_id)

    log = Log(log_method='get_plan', log_data=post_json_str)
    log.save()
    return HttpResponse(plan_json_str)


def add_plan(request):
    post_json_str = request.body.decode('UTF-8')
    post_json = json.loads(post_json_str)
    print(post_json)

    user_id = int(post_json['user_id'])
    plan_name = post_json['plan_name']
    plan_start_date = datetime.datetime.strptime(post_json['plan_start_date'], "%Y-%m-%d")
    plan_end_date = datetime.datetime.strptime(post_json['plan_end_date'], "%Y-%m-%d")
    plan_share = post_json['plan_share']
    plan_place1 = post_json['plan_place1']
    plan_place2 = post_json['plan_place2']

    plan_json_str = PlanService.add_plan(user_id, plan_name, plan_start_date, plan_end_date, plan_share,
                                         plan_place1, plan_place2)

    log = Log(log_user_id=user_id, log_method='add_plan', log_data=post_json_str)
    log.save()
    return HttpResponse(plan_json_str)


def get_plan_item_list(request):
    post_json_str = request.body.decode('UTF-8')
    post_json = json.loads(post_json_str)

    user_id = int(post_json['user_id'])
    plan_id = int(post_json['plan_id'])

    plan_item_list_str = PlanService.get_plan_item_list(user_id, plan_id)
    log = Log(log_user_id=user_id, log_method='get_plan_item_list', log_data=post_json_str)
    log.save()
    return HttpResponse(plan_item_list_str)


def add_plan_item(request):
    post_json_str = request.body.decode('UTF-8')
    post_json = json.loads(post_json_str)

    user_id = int(post_json['user_id'])
    plan_id = int(post_json['plan_id'])
    plan_item_type = post_json['plan_item_type']
    plan_item_date = datetime.datetime.strptime(post_json['plan_item_date'], "%Y-%m-%d")
    plan_item_json = post_json['plan_item_json']

    prev_plan_item_id = int(post_json['prev_plan_item_id'])

    plan_item_list_str = PlanService.add_plan_item(user_id, plan_id, plan_item_type, plan_item_date,
                                                   plan_item_json, prev_plan_item_id)

    log = Log(log_user_id=user_id, log_method='add_plan_item', log_data=post_json_str)
    log.save()
    return HttpResponse(plan_item_list_str)


def modify_plan_item(request):
    post_json_str = request.body.decode('UTF-8')
    post_json = json.loads(post_json_str)
    print(post_json)

    user_id = int(post_json['user_id'])
    plan_item_id = int(post_json['plan_item_id'])
    plan_item_json = post_json['plan_item_json']

    plan_item_list_str = PlanService.modify_plan_item(user_id, plan_item_id, plan_item_json)

    log = Log(log_user_id=user_id, log_method='modify_plan_item', log_data=post_json_str)
    log.save()
    return HttpResponse(plan_item_list_str)


def move_plan_item(request):
    post_json_str = request.body.decode('UTF-8')
    post_json = json.loads(post_json_str)
    print(post_json)

    user_id = int(post_json['user_id'])
    plan_id = int(post_json['plan_id'])
    plan_item_id = int(post_json['plan_item_id'])
    plan_item_date = datetime.datetime.strptime(post_json['plan_item_date'], "%Y-%m-%d")
    prev_plan_item_id = int(post_json['prev_plan_item_id'])

    plan_item_list_str = PlanService.move_plan_item(user_id, plan_id, plan_item_id, plan_item_date, prev_plan_item_id)

    log = Log(log_user_id=user_id, log_method='move_plan_item', log_data=post_json_str)
    log.save()
    return HttpResponse(plan_item_list_str)


def del_plan_item(request):
    post_json_str = request.body.decode('UTF-8')
    post_json = json.loads(post_json_str)

    user_id = int(post_json['user_id'])
    plan_item_id = int(post_json['plan_item_id'])

    plan_item_list_str = PlanService.del_plan_item(user_id, plan_item_id)

    log = Log(log_user_id=user_id, log_method='del_plan_item', log_data=post_json_str)
    log.save()
    return HttpResponse(plan_item_list_str)


def del_share(request):
    post_json_str = request.body.decode('UTF-8')
    post_json = json.loads(post_json_str)

    user_id = int(post_json['user_id'])
    plan_id = int(post_json['plan_id'])

    result = PlanService.del_share(user_id, plan_id)

    log = Log(log_user_id=user_id, log_method='del_share', log_data=post_json_str)
    log.save()
    return HttpResponse(result)


def get_plan_item(request):
    post_json_str = request.body.decode('UTF-8')
    post_json = json.loads(post_json_str)

    user_id = int(post_json['user_id'])
    plan_item_id = int(post_json['plan_item_id'])

    plan_item_str = PlanService.get_plan_item(user_id, plan_item_id)

    log = Log(log_user_id=user_id, log_method='get_plan_item', log_data=post_json_str)
    log.save()
    return HttpResponse(plan_item_str)


def add_share(request):
    post_json_str = request.body.decode('UTF-8')
    post_json = json.loads(post_json_str)

    user_id = int(post_json['user_id'])
    plan_id = int(post_json['plan_id'])
    share_type = post_json['share_type']
    print("add_share:" + str(user_id) + " " + str(plan_id) + " " + str(share_type))

    result = PlanService.add_share(user_id, plan_id, share_type)

    log = Log(log_user_id=user_id, log_method='add_share', log_data=post_json_str)
    log.save()
    return HttpResponse(result)


def index(request):
    return HttpResponse("hello world")
