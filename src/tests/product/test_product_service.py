import uuid


class TestProductService:
    async def _create_product(self, client, manager_id,
                              name, price, description):
        # 创建一个产品
        response = await client.post('/service/v1/product',
                                     json={
                                         'manager_id': manager_id,
                                         'name': name,
                                         'price': price,
                                         'description': description
                                     })
        assert response.status == 200
        json_result = await response.json()
        assert json_result['ok']

        return json_result['result']['product_id']

    async def test_create_product(self, client):
        url = '/service/v1/product'

        manager_id = str(uuid.uuid4())
        price = 1.1
        response = await client.post(url,
                                     json={
                                         'manager_id': manager_id,
                                         'name': '产品1',
                                         'price': price,
                                         'description': '产品1的介绍'
                                     })
        assert response.status == 200

        json_result = await response.json()
        assert json_result['ok']

        product = json_result['result']
        assert product['manager_id'] == manager_id
        assert product['name'] == '产品1'
        price1 = format(product['price'], '.1f')
        assert price1 == str(price)
        assert product['description'] == '产品1的介绍'

        error_response = await client.post(url,
                                           json={
                                               'manager_id': manager_id,
                                               'name': '产品1',
                                               'price': price,
                                               'description': '产品1的介绍'
                                           })
        assert error_response.status == 200
        error_result = await error_response.json()

        assert error_result['error_type'] == 'product_already_exist'
        assert error_result['message'] == '产品名需要唯一'

    async def test_list_products(self, client):
        """测试列出产品"""
        manager_id = str(uuid.uuid4())
        price = 1.1
        # 创建3个产品
        await self._create_product(client, manager_id, '1', price, '1')
        await self._create_product(client, manager_id, '2', price, '2')
        await self._create_product(client, manager_id, '3', price, '3')

        response = await client.get('/service/v1/products')
        assert response.status == 200

        json_result = await response.json()
        assert json_result['ok']

        products = json_result['result']['products']
        assert len(products) == 3

    async def test_list_products_by_manager(self, client):
        manager1_id = str(uuid.uuid4())
        price = 1.1
        # 创建3个产品
        await self._create_product(client, manager1_id, '1', price, '1')
        await self._create_product(client, manager1_id, '2', price, '2')
        await self._create_product(client, manager1_id, '3', price, '3')

        # 另一个管理员
        manager2_id = str(uuid.uuid4())
        await self._create_product(client, manager2_id, '4', price, '4')

        # 按管理员ID查询
        response1 = await client.get(
            f'/service/v1/product/manager/{manager1_id}')
        assert response1.status == 200
        json_result1 = await response1.json()
        assert json_result1['ok']

        products = json_result1['result']['products']
        assert products[0]['manager_id'] == manager1_id
        price1 = format(products[0]['price'], '.1f')
        assert price1 == str(price)
        assert len(products) == 3

        response2 = await client.get(
            f'/service/v1/product/manager/{manager2_id}')
        json_result2 = await response2.json()
        products = json_result2['result']['products']
        assert products[0]['manager_id'] == manager2_id
        price2 = format(products[0]['price'], '.1f')
        assert price2 == str(price)
        assert len(products) == 1

    async def test_delete_product(self, client):
        manager_id = str(uuid.uuid4())
        price = 1.1
        product_id = await self._create_product(client,
                                                manager_id, '1', price, '1')
        await self._create_product(client, manager_id, '2', price, '2')
        await self._create_product(client, manager_id, '3', price, '3')

        # 创建3个产品
        response1 = await client.get(
            f'/service/v1/product/manager/{manager_id}')
        json_result1 = await response1.json()
        assert len(json_result1['result']['products']) == 3

        # 删除
        url = f'/service/v1/product/{product_id}'
        response2 = await client.delete(url, json={
            'manager_id': manager_id,
        })
        assert response2.status == 200
        json_result2 = await response2.json()
        assert json_result2['ok']

        response3 = await client.get(
            f'/service/v1/product/manager/{manager_id}')
        json_result3 = await response3.json()
        assert len(json_result3['result']['products']) == 2

    async def test_update_product(self, client):
        manager_id = str(uuid.uuid4())
        price = 1.1
        price1 = 1.2
        product_id = await self._create_product(client,
                                                manager_id, '1', price, '1')
        response = await client.put(f'/service/v1/product/{product_id}',
                                    json={
                                        'manager_id': manager_id,
                                        'name': 'new',
                                        'price': price1,
                                        'description': 'new'
                                    })
        assert response.status == 200
        json_result = await response.json()
        assert json_result['ok']

        assert json_result['result']['name'] == 'new'
        price2 = format(json_result['result']['price'], '.1f')
        assert price2 == str(price1)
        assert json_result['result']['description'] == 'new'
