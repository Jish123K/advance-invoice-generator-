def test_update_product(authorized_client, test_products):

    data = {

        "product_name": "savon",

        "quantity_init": 32,

        "quantity_left": 452,

        "id": test_products[[0].id

}

res = authorized_client.put(f"/products/{test_products[0].id}", json=data)

assert res.status_code == 200

product = schemas.ProductOut(**res.json())

assert product.product_name == data["product_name"]

assert product.quantity_init == data["quantity_init"]

assert product.quantity_left == data["quantity_left"]
