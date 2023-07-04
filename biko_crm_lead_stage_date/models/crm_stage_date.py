from odoo import fields, models


class CrmLeadStageDate(models.Model):
    _name = "crm.stage.date"
    _description = "CRM Stage change date"

    change_date = fields.Datetime(string="Change Date", required=True)
    stage_id = fields.Many2one("crm.stage", string="Stage", required=True)
    lead_id = fields.Many2one("crm.lead", string="Lead", required=True)
