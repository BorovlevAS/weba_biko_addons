# flake8: noqa
# pylint: skip-file
import uuid

from odoo import _, fields, models
from odoo.exceptions import ValidationError


class StockMovesWizard(models.TransientModel):
    _name = "biko.cons.report.wizard"
    _description = "Consolidated report wizard"

    company_id = fields.Many2one(
        "res.company",
        string="Company",
        default=lambda self: self.env.user.company_id.id,
    )
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")

    def check_date_range(self):
        if self.end_date < self.start_date:
            raise ValidationError(_("End Date should be greater than Start Date."))

    def fill_report_data(self, unique_id):
        tender_figure_out_id = 6
        tender_subcontract_id = 7
        send_offer_id = 32
        init_project_id = 35
        get_prepay_id = 36

        leads_figure_out_count = self.env["crm.stage.date"].search_count(
            [
                ("change_date", ">=", self.start_date),
                ("change_date", "<=", self.end_date),
                ("stage_id", "=", tender_figure_out_id),
            ],
        )
        leads_subcontractor_count = self.env["crm.stage.date"].search_count(
            [
                ("change_date", ">=", self.start_date),
                ("change_date", "<=", self.end_date),
                ("stage_id", "=", tender_subcontract_id),
            ],
        )
        lead_offer_ids = (
            self.env["crm.stage.date"]
            .search(
                [
                    ("change_date", ">=", self.start_date),
                    ("change_date", "<=", self.end_date),
                    ("stage_id", "=", send_offer_id),
                ],
            )
            .mapped("lead_id")
        )
        leads_offers_count = len(lead_offer_ids)
        leads_offer_sum = sum([lead.expected_revenue for lead in lead_offer_ids])
        lead_offer_avg = leads_offer_sum / (
            leads_offers_count if leads_offers_count > 0 else 0
        )

        lead_init_project_sum = sum(
            self.env["crm.stage.date"]
            .search(
                [
                    ("change_date", ">=", self.start_date),
                    ("change_date", "<=", self.end_date),
                    ("stage_id", "=", init_project_id),
                ],
            )
            .mapped("lead_id")
            .mapped("expected_revenue")
        )

        lead_prepay_sum = sum(
            self.env["crm.stage.date"]
            .search(
                [
                    ("change_date", ">=", self.start_date),
                    ("change_date", "<=", self.end_date),
                    ("stage_id", "=", get_prepay_id),
                ],
            )
            .mapped("lead_id")
            .mapped("x_advance_pay")
        )

        lead_lost_sum = sum(
            self.env["crm.lead"]
            .with_context(active_test=False)
            .search(
                [
                    ("date_closed", ">=", self.start_date),
                    ("date_closed", "<=", self.end_date),
                    ("probability", "=", 0),
                    ("active", "=", False),
                ],
            )
            .mapped("expected_revenue")
        )

        print(".....")

    def open_report(self):
        self.check_date_range()

        unique_id = uuid.uuid4().hex
        self.fill_report_data(unique_id)

        action = {
            "name": _(
                "Consolidated report ({start_date:%d-%m-%Y} - {end_date:%d-%m-%Y})"
            ).format(start_date=self.start_date, end_date=self.end_date),
            "type": "ir.actions.act_window",
            "view_mode": "pivot",
            "view_type": "pivot",
            "res_model": "biko.consolidated.report",
            "view_id": self.env.ref(
                "biko_crm_lead_report.biko_consolidated_report_pivot"
            ).id,
            "domain": [("uid", "=", unique_id)],
        }

        return action
