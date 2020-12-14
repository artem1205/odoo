# -*- coding: utf-8 -*-
import math
from odoo import api, fields, models, _


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.depends('product_uom_qty')
    def choose_carton(self):
        """

    :param quantity: takes number of items as an argument
    :return: return number of needed cartons

    """
        small_cap, meidum_cap, large_cap = 3, 6, 9
        small, medium, large, collective = 0, 0, 0, 0
        quantity = self.product_uom_qty

        while quantity > 0:
            large = quantity // large_cap
            quantity = (quantity % large_cap)
            if quantity > meidum_cap:
                large += 1
                quantity = 0
            medium = quantity // meidum_cap
            quantity = (quantity % meidum_cap)
            if quantity > small_cap:
                medium += 1
                quantity = 0
            elif quantity == 0:
                break
            else:
                small += 1
                quantity = 0
        collective += math.ceil((large + small + medium) / 3)

        return small, medium, large, collective



