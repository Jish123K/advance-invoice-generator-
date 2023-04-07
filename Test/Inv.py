from app import schemas

from flask_testing import TestCase

class MyTest(TestCase):

    

    def create_app(self):

        app = create_app()

        app.config['TESTING'] = True

        return app

    def setUp(self):

        db.create_all()

        # Create some test data

    def tearDown(self):

        db.session.remove()

        db.drop_all()

    def test_get_all_invoices(self):

        res = self.client.get('/invoices/')

        self.assertEqual(res.status_code, 200)

    def test_unauthorized_get_all_invoices(self):

        res = self.client.get('/invoices/')

        self.assertEqual(res.status_code, 401)

    def test_unauthorized_get_one_invoice(self):

        res = self.client.get(f'/invoices/{test_invoices[0].id}')

        self.assertEqual(res.status_code, 401)

    def test_get_one_invoice_not_exist(self):

        res = self.client.get('/invoices/456478955')

        self.assertEqual(res.json.get('detail'), 'invoice with id: 456478955 was not found')

        self.assertEqual(res.status_code, 404)

    def test_get_one_invoice(self):

        res = self.client.get(f'/invoices/{test_invoices[0].id}')

        product = schemas.InvoiceOut(**res.json)

        self.assertEqual(product.id, test_invoices[0].id)

        self.assertEqual(product.reference, test_invoices[0].reference)

    def test_unauthorized_delete_invoice(self):

        res = self.client.delete(f'/invoices/{test_invoices[0].id}')

        self.assertEqual(res.status_code, 401)

    def test_authorize_delete_invoices(self):

        res = self.client.delete(f'/invoices/{test_invoices[0].id}')

        self.assertEqual(res.status_code, 204)

    def test_authorize_delete_non_existing(self):

        res = self.client.delete('/invoices/3456')

        self.assertEqual(res.json.get('detail'), 'invoice with id: 3456 does not exist')

        self.assertEqual(res.status_code, 404)

    def test_update_invoice(self):

        h = 200000

        c = 4500

        data = {

            "reference": "savon_de_merde",

            "value_net": h,

            "actual_payment": h

        }

        res = self.client.put(f'/invoices/{test_invoices[0].id}', json=data)

        updated_product = schemas.InvoiceCreate(**res.json)

        self.assertEqual(res.status_code, 200)

        self.assertEqual(updated_product.reference, data['reference'])

        self.assertEqual(updated_product.actual_payment, h)

