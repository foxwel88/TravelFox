import datetime
import json

from django.test import TestCase

from TravelService.models import TravelPlan, TravelShare
from TravelService.models import TravelUser
from TravelService.service.plan_service import PlanService


class ServiceTest(TestCase):
    def setUp(self):
        user = TravelUser()
        user.user_email = 'cttony1997@126.com'
        user.user_name = 'foxwel88'
        user.user_phone = '13236551908'
        user.save()
        self.user_id = user.id

        user2 = TravelUser()
        user2.user_email = 'cttony18997@126.com'
        user2.user_name = 'foxwel8888'
        user2.user_phone = '132365518908'
        user2.save()
        self.user2_id = user2.id

        self.plan_id = 0
        self.service = PlanService()

    def test_add_plan(self):
        travel_plan_str = self.service.add_plan(self.user_id, "new plan", datetime.date(2014, 8, 12),
                                                datetime.date(2014, 8, 24), 'public')
        travel_plan_dict = json.loads(travel_plan_str)
        print(travel_plan_str)
        travel_plan = TravelPlan.objects.get(id=travel_plan_dict['plan_id'])
        self.plan_id = travel_plan.id
        self.assertEqual(travel_plan.id, travel_plan_dict['plan_id'])
        self.assertEqual(travel_plan.plan_name, "new plan")
        self.assertEqual(travel_plan.plan_share, "public")

    def test_get_plan_list(self):
        self.service.add_plan(self.user_id, "new plan1", datetime.date(2014, 8, 12),
                              datetime.date(2014, 8, 24), 'public')
        self.service.add_plan(self.user_id, "new plan2", datetime.date(2014, 8, 12),
                              datetime.date(2014, 8, 24), 'public')
        self.service.add_plan(self.user2_id, "new plan3", datetime.date(2014, 8, 12),
                              datetime.date(2014, 8, 24), 'public')
        print(TravelShare.objects.all())
        print(self.service.get_plan_list(self.user_id))


class PlanItemTest(TestCase):
    def setUp(self):

        self.service = PlanService()
        user = TravelUser()
        user.user_email = 'cttony1997@126.com'
        user.user_name = 'foxwel88'
        user.user_phone = '13236551908'
        user.save()
        self.user_id = user.id

        travel_plan_str = self.service.add_plan(self.user_id, "new plan", datetime.date(2014, 8, 12),
                                                datetime.date(2014, 8, 24), 'public')
        travel_plan_dict = json.loads(travel_plan_str)
        self.plan_id = travel_plan_dict['plan_id']

    def test_add_plan_item(self):
        print("haha")
        plan_item_list = json.loads(self.service.add_plan_item(self.user_id, self.plan_id, 'flight', datetime.date(2014, 8, 13), 'haha', -1))
        print(plan_item_list)
        plan_item_list = json.loads(self.service.add_plan_item(self.user_id, self.plan_id, 'hotel', datetime.date(2014, 8, 14), 'haha', plan_item_list[0]['plan_item_id']))
        print(plan_item_list)
        plan_item_list = json.loads(self.service.add_plan_item(self.user_id, self.plan_id, 'bus', datetime.date(2014, 8, 15), 'haha', plan_item_list[1]['plan_item_id']))
        print(plan_item_list)
        plan_item_list = json.loads(self.service.add_plan_item(self.user_id, self.plan_id, 'school', datetime.date(2014, 8, 14), 'haha', plan_item_list[1]['plan_item_id']))
        print(plan_item_list)
        plan_item_list = json.loads(self.service.add_plan_item(self.user_id, self.plan_id, 'flight', datetime.date(2014, 8, 13), 'haha', plan_item_list[0]['plan_item_id']))
        print(plan_item_list)
