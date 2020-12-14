# -*- coding: utf-8 -*-

from odoo.tests import TransactionCase


class TestSaleOrderLine(TransactionCase):
    def test_sale_order_line(self):
        self.test_product = self.env['product.product'].create({
            'name': 'Product A for carton boXes',
            'standard_price': 1000.0,
            'list_price': 1000.0,
            'type': 'consu',
            'uom_id': self.env.ref('uom.product_uom_unit').id,
            'uom_po_id': self.env.ref('uom.product_uom_unit').id,
            'invoice_policy': 'delivery',
            'expense_policy': 'no',
            'service_type': 'manual',
            'taxes_id': False,
        })
        self.test_order = self.env['sale.order'].create({
            'partner_id': self.env.ref('base.res_partner_1').id,
            'order_line': [
                (0, False, {
                    'product_id': self.test_product.id,
                    'name': 'Product A for carton boXes',
                    'price_unit': 100.0,
                    'product_uom_qty': 30,
                }),
            ],
        })
        print(self.test_order.order_line.choose_carton())
        self.assertEqual(self.test_order.order_line.choose_carton(), (1, 0, 3, 2),
                         'something went wrong, check the given instruction')
