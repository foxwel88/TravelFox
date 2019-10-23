import json

from TravelService.models import TravelPlan, TravelUser, TravelPlanItem, TravelShare


class PlanService:

    @staticmethod
    def get_plan_list(user_id):
        plan_query_list = TravelShare.objects.filter(share_user_id=user_id).order_by('-share_plan__plan_createTime')
        plan_list = []
        for cur_travel_share in plan_query_list:
            plan_list.append(cur_travel_share.share_plan.get_json())
        return json.dumps(plan_list, ensure_ascii=False)

    @staticmethod
    def add_plan(user_id, plan_name, plan_start_date, plan_end_date, plan_share, plan_place1, plan_place2):
        travel_plan = TravelPlan(plan_name=plan_name,plan_share=plan_share, plan_user_id=user_id,
                                 plan_place1=plan_place1, plan_place2=plan_place2)
        travel_plan.plan_user = TravelUser.objects.get(id=user_id)
        travel_plan.plan_startDate = plan_start_date
        travel_plan.plan_endDate = plan_end_date
        travel_plan.save()

        PlanService.add_share(user_id, travel_plan.id, 'x')
        return json.dumps(travel_plan.get_json(), ensure_ascii=False)



    @staticmethod
    def get_plan(plan_id):
        try:
            travel_plan = TravelPlan.objects.get(id=plan_id)
        except TravelPlan.DoesNotExist:
            return "wrong"

        return json.dumps(travel_plan.get_json(), ensure_ascii=False)

    @staticmethod
    def add_share(user_id, plan_id, share_type):
        travel_share = TravelShare.objects.filter(share_plan_id=plan_id, share_user_id=user_id)
        if len(travel_share) != 0:
            return "exist"

        travel_plan = TravelPlan.objects.get(id=plan_id)
        travel_user = TravelUser.objects.get(id=user_id)

        if travel_user is None or travel_plan is None:
            return "wrong"

        travel_share = TravelShare(share_user=travel_user, share_plan=travel_plan, share_type=share_type)
        travel_share.save()
        return 'success'

    @staticmethod
    def get_plan_item_list(user_id, plan_id):
        travel_plan = TravelPlan.objects.get(id=plan_id)
        if travel_plan.plan_share == 'private':
            travel_share = TravelShare.objects.filter(share_plan_id=plan_id, share_user_id=user_id)
            if len(travel_share) == 0:
                return "wrong"

        plan_item_query_list = TravelPlanItem.objects.filter(planItem_plan_id=plan_id).order_by('planItem_order')
        plan_item_list = []
        for cur_travel_plan_item in plan_item_query_list:
            plan_item_list.append(cur_travel_plan_item.get_json())

        return json.dumps(plan_item_list, ensure_ascii=False)

    @staticmethod
    def add_plan_item(user_id, plan_id, plan_item_type, plan_item_date, plan_item_json, prev_plan_item_id):
        try:
            travel_plan = TravelPlan.objects.get(id=plan_id)
            travel_user = TravelUser.objects.get(id=user_id)
        except TravelUser.DoesNotExist:
            return "wrong"

        if travel_user is None or travel_plan is None:
            return "wrong"

        if travel_plan.plan_user_id != travel_user.id:
            if TravelShare.objects.get(share_user_id=user_id, share_plan_id=plan_id) is None:
                return "wrong"

        plan_item_order = -1
        plan_item_list = TravelPlanItem.objects.filter(planItem_plan_id=plan_id).order_by('planItem_order')

        # 前序item_id==-1 表明新的item放在第一个
        if prev_plan_item_id == -1:
            if len(plan_item_list) == 0:
                plan_item_order = 1000
            else:
                plan_item_order = (0 + plan_item_list[0].planItem_order) / 2.0
        else:
            for i in range(len(plan_item_list)):
                if plan_item_list[i].id == prev_plan_item_id:
                    if i == (len(plan_item_list) - 1):
                        plan_item_order = plan_item_list[i].planItem_order + 1000
                    else:
                        plan_item_order = (plan_item_list[i].planItem_order + plan_item_list[
                            i + 1].planItem_order) / 2.0
                    break

        # 找不到这个前序item_id
        if plan_item_order == -1:
            return "wrong"

        print(json.dumps(plan_item_json, ensure_ascii=False))
        travel_plan_item = TravelPlanItem(planItem_plan_id=plan_id, planItem_type=plan_item_type,
                                          planItem_json=json.dumps(plan_item_json, ensure_ascii=False), planItem_order=plan_item_order)
        travel_plan_item.planItem_date = plan_item_date
        travel_plan_item.save()

        return PlanService.get_plan_item_list(user_id, plan_id)

    @staticmethod
    def move_plan_item(user_id, plan_id, plan_item_id, plan_item_date, prev_plan_item_id):
        try:
            travel_plan = TravelPlan.objects.get(id=plan_id)
            travel_user = TravelUser.objects.get(id=user_id)
            travel_plan_item = TravelPlanItem.objects.get(id=plan_item_id)

            if travel_user is None or travel_plan is None or travel_plan_item is None:
                return "wrong"

            if travel_plan.plan_user_id != travel_user.id:
                if TravelShare.objects.get(share_user_id=user_id, share_plan_id=plan_id) is None:
                    return "wrong"

        except TravelUser.DoesNotExist:
            return "wrong"
        except TravelPlan.DoesNotExist:
            return "wrong"
        except TravelPlanItem.DoesNotExist:
            return "wrong"
        except TravelShare.DoesNotExist:
            return "wrong"

        plan_item_order = -1
        plan_item_list = TravelPlanItem.objects.filter(planItem_plan_id=plan_id).order_by('planItem_order')

        # 前序item_id==-1 表明新的item放在第一个
        if prev_plan_item_id == -1:
            if len(plan_item_list) == 0:
                plan_item_order = 1000
            else:
                plan_item_order = (0 + plan_item_list[0].planItem_order) / 2.0
        else:
            for i in range(len(plan_item_list)):
                if plan_item_list[i].id == prev_plan_item_id:
                    if i == (len(plan_item_list) - 1):
                        plan_item_order = plan_item_list[i].planItem_order + 1000
                    else:
                        plan_item_order = (plan_item_list[i].planItem_order + plan_item_list[
                            i + 1].planItem_order) / 2.0
                    break

        # 找不到这个前序item_id
        if plan_item_order == -1:
            return "wrong"

        travel_plan_item.planItem_date = plan_item_date
        travel_plan_item.planItem_order = plan_item_order
        travel_plan_item.save()

        return PlanService.get_plan_item_list(user_id, plan_id)

    @staticmethod
    def del_plan_item(user_id, plan_item_id):
        travel_plan_item = TravelPlanItem.objects.get(id=plan_item_id)
        travel_plan = travel_plan_item.planItem_plan
        travel_user = TravelUser.objects.get(id=user_id)
        if travel_plan_item is None or travel_user is None or travel_plan is None:
            return "wrong"

        if travel_plan.plan_user_id != travel_user.id:
            if TravelShare.objects.get(user_id=user_id, plan_id=travel_plan.id) is None:
                return "wrong"

        travel_plan_item.delete()
        return PlanService.get_plan_item_list(user_id, travel_plan.id)

    @staticmethod
    def del_share(user_id, plan_id):
        travel_share = TravelShare.objects.filter(share_plan_id=plan_id, share_user_id=user_id)
        if len(travel_share) == 0:
            return "wrong"

        for item in travel_share:
            item.delete()

        return "success"

    @staticmethod
    def get_plan_item(user_id, plan_item_id):
        travel_plan_item = TravelPlanItem.objects.get(id=plan_item_id)
        travel_plan = travel_plan_item.planItem_plan
        travel_user = TravelUser.objects.get(id=user_id)
        if travel_plan_item is None or travel_user is None or travel_plan is None:
            return "wrong"

        if travel_plan.plan_user_id != travel_user.id:
            if TravelShare.objects.get(user_id=user_id, plan_id=travel_plan.id) is None:
                return "wrong"

        return json.dumps(travel_plan_item.get_json(), ensure_ascii=False)

    @staticmethod
    def modify_plan_item(user_id, plan_item_id, plan_item_json):
        travel_plan_item = TravelPlanItem.objects.get(id=plan_item_id)
        travel_plan = travel_plan_item.planItem_plan
        travel_user = TravelUser.objects.get(id=user_id)
        if travel_plan_item is None or travel_user is None or travel_plan is None:
            return "wrong"

        if travel_plan.plan_user_id != travel_user.id:
            if TravelShare.objects.get(user_id=user_id, plan_id=travel_plan.id) is None:
                return "wrong"

        travel_plan_item.planItem_json = json.dumps(plan_item_json, ensure_ascii=False)
        travel_plan_item.save()
        return PlanService.get_plan_item_list(user_id, travel_plan.id)

