# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class CrmLeadProduct(models.Model):
    _inherit = 'crm.lead.product'

    biko_currency_id = fields.Many2one(
        related="lead_id.company_currency",
        depends=["lead_id.company_currency"],
        store=True,
        string="Currency",
        readonly=True,
    )

    biko_price_subtotal = fields.Monetary(
        compute="_compute_amount",
        string="Subtotal",
        currency_field="biko_currency_id",
        readonly=True,
        store=True,
    )
    biko_price_tax = fields.Float(
        compute="_compute_amount", string="Total Tax", readonly=True, store=True
    )
    biko_price_total = fields.Monetary(
        compute="_compute_amount",
        string="Total",
        currency_field="biko_currency_id",
        readonly=True,
        store=True,
    )
    
    @api.depends("qty", "price_unit", "tax_id")
    def _compute_amount(self):
        """
        Compute the amounts of the TI line.
        """
        for line in self:
            price = line.price_unit
            taxes = line.tax_id.compute_all(
                price,
                line.lead_id.company_currency,
                line.qty,
                product=line.product_id,
                partner=line.lead_id.partner_id,
            )
            line.update(
                {
                    "biko_price_tax": sum(
                        t.get("amount", 0.0) for t in taxes.get("taxes", [])
                    ),
                    "biko_price_total": taxes["total_included"],
                    "biko_price_subtotal": taxes["total_excluded"],
                }
            )

