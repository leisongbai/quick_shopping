from tests.docs import api_docs


class ProfileApi:
    @classmethod
    async def create_profile(cls, client, user_id):
        url = '/v1/profile'
        await client.post(url,
                          json={
                              'user_id': user_id,
                              'nickname': 'tester',
                          })


class TestProfileApi:
    @api_docs(title='创建个人资料',
              path='v1/profile',
              method='POST',
              body={
                  'user_id(必填)': '用户id',
                  'nickname(必填)': '用户昵称',
                  'gender': '性别',
                  'role_id': '角色id'
              })
    async def test_create_profile(self, client):
        account_id = '123456789@qq.com'
        # 获取验证码
        response = await client.post('/service/v1/account/send_code',
                                     json={'account_id': account_id})
        assert response.status == 200
        json_result = await response.json()
        validate_token = json_result['result']['validate_token']
        validate_code = json_result['result']['validate_code']

        url = '/v1/account'
        response = await client.post(url,
                                     json={
                                         'account_id': account_id,
                                         'password': '123456789@qq.com',
                                         'validate_token': validate_token,
                                         'validate_code': validate_code,
                                     })
        assert response.status == 200
        response = await client.post('/v1/login',
                                     json={
                                         'account_id': '123456789@qq.com',
                                         'password': '123456789@qq.com'
                                     })
        assert response.status == 200
        json_result = await response.json()
        user_id = json_result['result']['user_id']
        url = '/v1/profile'

        response = await client.post(url,
                                     json={
                                         'user_id': user_id,
                                         'nickname': 'tester',
                                         'gender': 0,
                                         'role_id': 'MANAGER'
                                     })

        assert response.status == 200

        json_result = await response.json()
        assert json_result['ok']
        return {'正确响应': json_result}

    @api_docs(title='获取个人资料', path='/v1/profile/{user_id}', method='GET')
    async def test_get_profile(self, client):
        account_id = '123456789@qq.com'
        # 获取验证码
        response = await client.post('/service/v1/account/send_code',
                                     json={'account_id': account_id})
        assert response.status == 200
        json_result = await response.json()
        validate_token = json_result['result']['validate_token']
        validate_code = json_result['result']['validate_code']

        url = '/v1/account'
        response = await client.post(url,
                                     json={
                                         'account_id': account_id,
                                         'password': '123456789@qq.com',
                                         'validate_token': validate_token,
                                         'validate_code': validate_code,
                                     })
        assert response.status == 200
        response = await client.post('/v1/login',
                                     json={
                                         'account_id': '123456789@qq.com',
                                         'password': '123456789@qq.com'
                                     })
        assert response.status == 200
        json_result = await response.json()
        user_id = json_result['result']['user_id']

        url = '/v1/profile'
        response = await client.post(url,
                                     json={
                                         'user_id': user_id,
                                         'nickname': 'tester',
                                         'gender': 0,
                                         'role_id': 'MANAGER'
                                     })
        assert response.status == 200

        response = await client.get(f'/v1/profile/{user_id}')
        assert response.status == 200
        json_result = await response.json()
        assert json_result['ok']

        profile = json_result['result']
        assert profile['user_id'] == user_id
        assert profile['nickname'] == 'tester'
        assert profile['gender'] == 0
        assert profile['avatar'] == ''
        assert profile['role_id'] == 'MANAGER'
        return {'正确响应': json_result}

    @api_docs(title='更新个人资料',
              path='/v1/profile/{user_id}',
              method='PUT',
              body={
                  'nickname': '昵称',
                  'gender': '性别',
                  'user_id': '用户id',
                  'avatar': '头像'
              })
    async def test_update_profile(self, client):
        account_id = '123456789@qq.com'
        # 获取验证码
        response = await client.post('/service/v1/account/send_code',
                                     json={'account_id': account_id})
        assert response.status == 200
        json_result = await response.json()
        validate_token = json_result['result']['validate_token']
        validate_code = json_result['result']['validate_code']

        url = '/v1/account'
        response = await client.post(url,
                                     json={
                                         'account_id': account_id,
                                         'password': '123456789@qq.com',
                                         'validate_token': validate_token,
                                         'validate_code': validate_code,
                                     })
        assert response.status == 200
        response = await client.post('/v1/login',
                                     json={
                                         'account_id': '123456789@qq.com',
                                         'password': '123456789@qq.com'
                                     })

        assert response.status == 200
        json_result = await response.json()
        print(json_result)
        user_id = json_result['result']['user_id']
        token = json_result['result']['token']

        url = '/v1/profile'
        response = await client.post(url,
                                     json={
                                         'user_id': user_id,
                                         'nickname': 'tester',
                                         'gender': 1,
                                         'role_id': 'MANAGER'
                                     })

        assert response.status == 200

        response = await client.get(f'/service/v1/profile/{user_id}')
        assert response.status == 200
        json_result = await response.json()

        profile = json_result['result']
        assert profile['nickname'] == 'tester'
        assert profile['gender'] == 1

        # 更新 profile
        response3 = await client.put(f'/v1/profile/{user_id}',
                                     json={
                                         'nickname': 'tester2',
                                         'gender': 0
                                     },
                                     headers={'Authorization': token})
        assert response3.status == 200
        json_result1 = await response3.json()
        # 再次查询
        response2 = await client.get(f'/service/v1/profile/{user_id}')
        assert response2.status == 200
        json_result2 = await response2.json()

        new_profile = json_result2['result']
        assert new_profile['nickname'] == 'tester2'
        assert new_profile['gender'] == 0
        return {'正确响应': json_result1}

    @api_docs(title='获取所有商家',
              path='/v1/profile/user/manager',
              method='GET',
              body={})
    async def test_query_managers(self, client):
        account_id = '123456789@qq.com'
        # 获取验证码
        response = await client.post('/service/v1/account/send_code',
                                     json={'account_id': account_id})
        assert response.status == 200
        json_result = await response.json()
        validate_token = json_result['result']['validate_token']
        validate_code = json_result['result']['validate_code']

        url = '/v1/account'
        response = await client.post(url,
                                     json={
                                         'account_id': account_id,
                                         'password': '123456789@qq.com',
                                         'validate_token': validate_token,
                                         'validate_code': validate_code,
                                     })
        assert response.status == 200
        response = await client.post('/v1/login',
                                     json={
                                         'account_id': '123456789@qq.com',
                                         'password': '123456789@qq.com'
                                     })

        assert response.status == 200
        json_result = await response.json()
        user_id = json_result['result']['user_id']

        url = '/v1/profile'
        response = await client.post(url,
                                     json={
                                         'user_id': user_id,
                                         'nickname': 'tester',
                                         'gender': 1,
                                         'role_id': 'MANAGER'
                                     })

        assert response.status == 200
        assert json_result['ok']

        response1 = await client.get(f'/v1/profile/{user_id}')
        assert response1.status == 200
        response2 = await client.get('/v1/profile/user/manager')
        assert response2.status == 200
        json_result2 = await response2.json()
        return {'正确响应': json_result2}
