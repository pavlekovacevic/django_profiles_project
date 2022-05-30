from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from profiles_api.views import UserLoginApiView

client = APIClient()

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
            
            response = client.post("/api/login/", data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

# def test_get_list_all_users(), getting all users from db
    def test_get_list_all_users(self):
        response = self.client.get("/api/profile/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# def test_add_status_to_profile(), validated user can add status to his own profile
    def test_add_status_to_profile(self):
        response = client.post('/api/profile/', data={
            'email': 'pavle@test.com',
            'name': 'Pavle',
            'password': 'password' 
        })

        response = client.post('/api/login/', data={
            'username': 'pavle@test.com',
            'password': 'password'
        })

        client.credentials(HTTP_AUTHORIZATION='Token ' + response.json()['token'])

        response = client.post('/api/feed/', data={
            'status_text': 'Hello World'
        })
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

# def test_add_status_to_profile_forbidden_user(), validated user tries to add profile to other user id so req is interupted
    def test_add_status_to_profile_forbidden_user(self):
        response = client.post('/api/profile/', data={
            'email': 'test@test.com',
            'name': 'test',
            'password': 'password' 
        })
        
        response = client.post('/api/login/', data={
            'username': 'test@test.com',
            'password': 'password'
        })
        
        client.credentials(HTTP_AUTHORIZATION='Token ' + 'joqwbfoqb2131982312')
        
        response = client.post('/api/feed/', data={
            'status_text': 'Hello World'
        })
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

# def_get_feed_all_users(), user is logged in and can see all feed
    def test_get_feed_all_users(self):
        response = self.client.post('/api/profile/', data={
            'email': 'pavle@test.com',
            'name': 'Pavle',
            'password': 'password' 
        })
        
        
        response = self.client.post('/api/login/', data={
            'username': 'pavle@test.com',
            'password': 'password'
        })
        
        client.credentials(HTTP_AUTHORIZATION='Token ' + response.json()['token'])

        response = self.client.get("/api/profile/")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# def get_feed_all_users_user_forbidden(), user does not have a valid token so is unable to see feed
    def test_get_feed_user_forbidden(self):
        response = client.get("/api/feed/")
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

# def test_patch_profile(), user is tryign to change their profile
    def test_patch_profile(self):
        response = self.client.post('/api/profile/', data={
            'email': 'pavle@test.com',
            'name': 'Pavle',
            'password': 'password' 
        })
        user_id = response.json()['id']
        
        response = self.client.post('/api/login/', data={
            'username': 'pavle@test.com',
            'password': 'password'
        })
        
        client.credentials(HTTP_AUTHORIZATION='Token ' + response.json()['token'])
        
        response = client.patch(f"/api/profile/{user_id}/", data={
            'name':'TestName'
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)

# def test_patch_profile_forbidden_user(), user tries to change other users profile
    def test_patch_profile_forbidden_user(self):
        response = self.client.post('/api/profile/', data={
            'email': 'pavle@test.com',
            'name': 'Pavle',
            'password': 'password' 
        })
        
        response1 = self.client.post('/api/profile/', data={
            'email': 'test@test.com',
            'name': 'test',
            'password': 'password' 
        })

        fake_id = response1.json()['id']

        response = self.client.post('/api/login/', data={
            'username': 'pavle@test.com',
            'password': 'password'
        })
        
        client.credentials(HTTP_AUTHORIZATION='Token ' + response.json()['token'])
        
        response = client.patch(f"/api/profile/{fake_id}/", data={
            'name':'TestName'
        })

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
# def test_delete_profile(), user is tryign to delete their profile
    def test_delete_profile(self):
        response = self.client.post('/api/profile/', data={
            'email': 'pavle@test.com',
            'name': 'Pavle',
            'password': 'password' 
        })
        user_id = response.json()['id']
        
        response = self.client.post('/api/login/', data={
            'username': 'pavle@test.com',
            'password': 'password'
        })
        
        client.credentials(HTTP_AUTHORIZATION='Token ' + response.json()['token'])
        
        response = client.delete(f"/api/profile/{user_id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
# def test_delete_profile_forbidden_user(), user tries to delete other users profile
    def test_delete_profile_forbidden_user(self):
        response = self.client.post('/api/profile/', data={
                'email': 'pavle@test.com',
                'name': 'Pavle',
                'password': 'password' 
            })
            
        response1 = self.client.post('/api/profile/', data={
            'email': 'test@test.com',
            'name': 'test',
            'password': 'password' 
        })

        fake_id = response1.json()['id']

        response = self.client.post('/api/login/', data={
            'username': 'pavle@test.com',
            'password': 'password'
        })
        
        client.credentials(HTTP_AUTHORIZATION='Token ' + response.json()['token'])
        
        response = client.patch(f"/api/profile/{fake_id}/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)