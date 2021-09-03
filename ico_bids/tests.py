import json
from datetime import datetime, timedelta
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from ico_bids.models import Token, Bid
from ico_bids.tasks import allocate_token

# Create your tests here.

class TokenAllocationTestCase(APITestCase):
    """
        Token Allocation Test
    """
    def __init__(self, *nargs, **kwargs):
        super().__init__(*nargs, **kwargs)
        self.maxDiff = None

    @classmethod
    def setUpClass(cls):
        super(TokenAllocationTestCase, cls).setUpClass()

        user1 = User.objects.create(**{
            'email': 'user1@example.com',
            'username': 'user1',
            'password': 'ico_pwd',
            'first_name': 'user1',
            'last_name': 'ico'
        })
        user2 = User.objects.create(**{
            'email': 'user2@example.com',
            'username': 'user2',
            'password': 'ico_pwd',
            'first_name': 'user2',
            'last_name': 'ico'
        })
        user3 = User.objects.create(**{
            'email': 'user3@example.com',
            'username': 'user3',
            'password': 'ico_pwd',
            'first_name': 'user3',
            'last_name': 'ico'
        })
        user4 = User.objects.create(**{
            'email': 'user4@example.com',
            'username': 'user4',
            'password': 'ico_pwd',
            'first_name': 'user4',
            'last_name': 'ico'
        })
        user5 = User.objects.create(**{
            'email': 'user5@example.com',
            'username': 'user5',
            'password': 'ico_pwd',
            'first_name': 'user5',
            'last_name': 'ico'
        })

        current_time = datetime.now()
        start_time = current_time - timedelta(hours=2)
        end_time = current_time - timedelta(hours=1)
        token1 = Token.objects.create(**{
            'name': 'token1',
            'start_time': start_time.time(),
            'end_time': end_time.time(),
            'available_token': 100
        })

        bid1 = Bid.objects.create(**{
            'user': user1,
            'token': token1,
            'number_of_token': 150,
            'bid_price': 25,
        })
        bid1.created_at = datetime.now() - timedelta(hours=1, minutes=30)
        bid1.save()

        bid2 = Bid.objects.create(**{
            'user': user2,
            'token': token1,
            'number_of_token': 140,
            'bid_price': 25,
        })
        bid2.created_at = datetime.now() - timedelta(hours=1, minutes=30)
        bid2.save()

        bid3 = Bid.objects.create(**{
            'user': user3,
            'token': token1,
            'number_of_token': 15,
            'bid_price': 30,
        })
        bid3.created_at = datetime.now() - timedelta(hours=1, minutes=30)
        bid3.save()

        bid4 = Bid.objects.create(**{
            'user': user4,
            'token': token1,
            'number_of_token': 12,
            'bid_price': 27,
        })
        bid4.created_at = datetime.now() - timedelta(hours=1, minutes=30)
        bid4.save()

        bid5 = Bid.objects.create(**{
            'user': user5,
            'token': token1,
            'number_of_token': 12,
            'bid_price': 20
        })
        bid5.created_at = datetime.now() - timedelta(hours=1, minutes=30)
        bid5.save()

        allocate_token()

    def test_successfull_allocation(self):
        url = reverse('successfull-bid')
        response = self.client.get(url)
        response_json = json.loads(response.content)
        for obj in response_json:
            obj.pop('created_at')
            obj.pop('updated_at')
        expected_result = [
            {
                "id": 3,
                "number_of_token": 15,
                "bid_price": 30,
                "alloted_tokens": 15,
                "status": "SUCCESS",
                "user": 3,
                "token": 1,
            },
            {
                "id": 4,
                "number_of_token": 12,
                "bid_price": 27,
                "alloted_tokens": 12,
                "status": "SUCCESS",
                "user": 4,
                "token": 1,
            },
            {
                "id": 1,
                "number_of_token": 150,
                "bid_price": 25,
                "alloted_tokens": 37,
                "status": "SUCCESS",
                "user": 1,
                "token": 1,
            },
            {
                "id": 2,
                "number_of_token": 140,
                "bid_price": 25,
                "alloted_tokens": 36,
                "status": "SUCCESS",
                "user": 2,
                "token": 1,
            }
        ]
        self.assertJSONEqual(json.dumps(response_json), expected_result)


    def test_failed_allocation(self):
        url = reverse('failed-bid')
        response = self.client.get(url)
        response_json = json.loads(response.content)
        for obj in response_json:
            obj.pop('created_at')
            obj.pop('updated_at')
        expected_result = [
            {
                "id": 5,
                "number_of_token": 12,
                "bid_price": 20,
                "alloted_tokens": 0,
                "status": "FAILED",
                "user": 5,
                "token": 1,
            }
        ]
        self.assertJSONEqual(json.dumps(response_json), expected_result)
