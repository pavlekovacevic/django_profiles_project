from email.headerregistry import ContentTypeHeader
from urllib import request
from wsgiref import headers
from django.http import HttpRequest
from django.test import TestCase, Client
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from profiles_api.serializers import UserProfileSerializer
from django.contrib.auth import get_user_model
from profiles_api.views import UserLoginApiView
# Create your tests here.
client = Client()
User = get_user_model()

class MyTestCase(APITestCase,UserLoginApiView):
# def test_create_user(), all data is valid and user is created
    def test_create_user(self):
        data1 = {
            'email':'kovacevicpavle14@gmail.com',
            'name':'Pavle',
            'password':'password'
        }
        response = self.client.post("/api/profile/", data1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
# def test_create_user_invalid_data(), data is not valid and the req is interupted
    def test_create_user_invalid_data(self):
        data = {
            'email':1,
            'name':'Pavle',
            'password':'password'
        }
        response = self.client.post("/api/profile/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
# def test_create_user_already_in_db(), user tries to signup but the profile is already created
    def test_create_user_already_in_db(self):
        data1 = {
            'email':'kovacevicpavle14@gmail.com',
            'name':'Pavle',
            'password':'password'
        }
        response = self.client.post("/api/profile/", data1)

        data = {
            'email':'kovacevicpavle14@gmail.com',
            'name':'Pavle',
            'password':'password'
        }
        response = self.client.post("/api/profile/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

# def test_user_login(), correct credentials and user gets a token, request continues
    def test_user_login(self):
        # response = self.client.post("/api/profile/", data={
        #     'email':"kovacevicpavle14@gmail.com",
        #     'name':'Pavle',
        #     'password':'password'
        # })

        # response = self.client.post("api/login/",  data={
        #     'username':"kovacevicpavle14@gmail.com",
        #     'password':'password'
        # })

        # self.assertEqual(response.status_code, status.HTTP_200_OK)

        # TODO: Uporedi gornji i donji kod, zasto ne radi gornji

        data1={
            'email':"John@gmail.com",
            'name':'Pavle',
            'password':'password'
        }

        response = self.client.post("/api/profile/", data1)

        data2={
            'username':"John@gmail.com",
            'password':'password'
        }
        # import pdb;pdb.set_trace()
        response = self.client.post("/api/login/", data2)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        

# def test_user_login_forbidden_user(), credentials not correct user does not get a token
    def test_user_login_forbidden_user(self):
        data = {
            'email':"John@gmail.com",
            'name':'Pavle',
            'password':'password'
        }
        response = self.client.post("/api/login/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# def test_user_login_invalid_data(), form is not fullfiled and user cant log in
    def test_user_login_invalid_data(self):
            data = {
                'email':1,
                'name':'Pavle',
                'password':'password'
            }
            response = self.client.post("/api/login/", data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
# def test_get_list_all_users(), getting all users from db
    def test_get_list_all_users(self):
        response = self.client.get("/api/profile/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
# def test_add_status_to_profile(), validated user can add status to his own profile
    def test_add_status_to_profile(self):
        # data1={
        #     'email':"John@gmail.com",
        #     'name':'Pavle',
        #     'password':'password'
        # }

        response = self.client.post("/api/profile/", data={
            'email':"John@gmail.com",
            'name':'Pavle',
            'password':'password'
        })

        # data2={
        #     'username':"John@gmail.com",
        #     'password':'password'
        # }
        
        response = self.client.post("/api/login/", data={
            'username':"John@gmail.com",
            'password':'password'
        })

        # import pdb;pdb.set_trace()

        # self.assertEqual(response.status_code, status.HTTP_200_OK)

        auth_headers = {
            'Authorization': 'Bearer ' + response.json()['token']
        }

        # import pdb;pdb.set_trace()

        response = self.client.post("/api/feed/", content_type='application/json', data={
            'status_text':'Hello world!'
        }, headers=auth_headers)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

# def test_add_status_to_profile_forbidden_user(), validated user tries to add profile to other user id so req is interupted
# def_get_feed_all_users(), user is logged in and can see all feed
# def get_feed_all_users_user_forbidden(), user does not have a valid token so is unable to see feed
# def test_put_profile(), user is tryign to change their profile
# def test_put_profile_forbidden_user(), user tries to change other users profile
# def test_patch_profile(), user is tryign to change their profile
# def test_patch_profile_forbidden_user(), user tries to change other users profile
# def test_delete_profile(), user is tryign to delete their profile
# def test_delete_profile_forbidden_user(), user tries to delete other users profile