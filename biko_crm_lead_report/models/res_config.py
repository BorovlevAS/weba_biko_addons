from odoo import api, fields, models


class ResConfig(models.TransientModel):
    _inherit = "res.config.settings"

    stage_figure_out_id = fields.Many2one("crm.stage", string="Tender figure out")
    stage_subcontract_id = fields.Many2one("crm.stage", string="Tender subcontract")
    stage_offer_id = fields.Many2one("crm.stage", string="Offer was sent")

    init_project_id = fields.Many2one("crm.stage", string="Init project")

    get_prepay_id = fields.Many2one("crm.stage", string="Advance payment")

    def _get_value(self, param_name):
        IrConfigParam = self.env["ir.config_parameter"].sudo()
        param_id = IrConfigParam.get_param(f"biko_crm_lead_report.{param_name}")
        if param_id:
            param = self.env["crm.stage"].sudo().browse(int(param_id))
            if param:
                return {
                    f"{param_name}": param.id,
                }
        else:
            return ""

    @api.model
    def get_values(self):
        res = super().get_values()

        value = self._get_value("stage_figure_out_id")
        if value:
            res.update(value)

        value = self._get_value("stage_subcontract_id")
        if value:
            res.update(value)

        value = self._get_value("stage_offer_id")
        if value:
            res.update(value)

        value = self._get_value("init_project_id")
        if value:
            res.update(value)

        value = self._get_value("get_prepay_id")
        if value:
            res.update(value)

        return res

    def set_values(self):
        # pylint: disable=missing-return
        super().set_values()
        IrConfigParam = self.env["ir.config_parameter"].sudo()
        IrConfigParam.set_param(
            "biko_crm_lead_report.stage_figure_out_id",
            self.stage_figure_out_id.id,
        )
        IrConfigParam.set_param(
            "biko_crm_lead_report.stage_subcontract_id",
            self.stage_subcontract_id.id,
        )
        IrConfigParam.set_param(
            "biko_crm_lead_report.stage_offer_id",
            self.stage_offer_id.id,
        )
        IrConfigParam.set_param(
            "biko_crm_lead_report.init_project_id",
            self.init_project_id.id,
        )
        IrConfigParam.set_param(
            "biko_crm_lead_report.get_prepay_id",
            self.get_prepay_id.id,
        )
