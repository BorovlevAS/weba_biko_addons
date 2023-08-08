from odoo import fields, models


class ConsolidatedLeadReport(models.Model):
    _name = "biko.consolidated.report"
    _description = "Consolidated report on leads"
    _order = "line_group, line_order"

    uid = fields.Char(readonly=True)
    company_id = fields.Many2one("res.company", string="Company", readonly=True)

    line_group = fields.Selection(
        selection=[
            ("00_tenders", "ТЕНДЕРА"),
            ("01_commercial", "КОМЕРЦІЙНІ ПРОПОЗИЦІЇ"),
            ("03_money", "ГРОШІ"),
            ("04_calls", "ДЗВІНКИ"),
        ],
    )

    line_order = fields.Integer()
    line_caption = fields.Char()
    line_value = fields.Float()
