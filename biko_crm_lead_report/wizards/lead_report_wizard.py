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
    manager_ids = fields.Many2many("res.users", string="Salespersons")
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")

    def check_date_range(self):
        if self.end_date < self.start_date:
            raise ValidationError(_("End Date should be greater than Start Date."))

    def _add_report_line(
        self, unique_id, line_group, line_order, line_caption, line_value
    ):
        self.env["biko.consolidated.report"].create(
            {
                "uid": unique_id,
                "company_id": self.company_id.id,
                "line_group": line_group,
                "line_order": line_order,
                "line_caption": line_caption,
                "line_value": line_value,
            }
        )

    def _get_stage_from_param(self, param_name):
        value = self.env["ir.config_parameter"].sudo().get_param(param_name, 0)
        return int(value)

    def _generate_domain(self, stage_id):
        domain = [
            ("change_date", ">=", self.start_date),
            ("change_date", "<=", self.end_date),
            ("stage_id", "=", stage_id),
        ]

        if self.manager_ids:
            domain += [("lead_id.user_id", "in", self.manager_ids.ids)]

        return domain

    def fill_report_data(self, unique_id):
        tender_figure_out_id = self._get_stage_from_param(
            "biko_crm_lead_report.stage_figure_out_id"
        )
        tender_subcontract_id = self._get_stage_from_param(
            "biko_crm_lead_report.stage_subcontract_id"
        )
        send_offer_id = self._get_stage_from_param(
            "biko_crm_lead_report.stage_offer_id"
        )
        init_project_id = self._get_stage_from_param(
            "biko_crm_lead_report.init_project_id"
        )
        get_prepay_id = self._get_stage_from_param("biko_crm_lead_report.get_prepay_id")

        domain = self._generate_domain(tender_figure_out_id)

        leads_figure_out_count = self.env["crm.stage.date"].search_count(
            domain,
        )

        self._add_report_line(
            unique_id,
            "00_tenders",
            0,
            "1.1. Кількість опрацьованих листів з тендерами",
            leads_figure_out_count,
        )

        domain = self._generate_domain(tender_subcontract_id)

        leads_subcontractor_count = self.env["crm.stage.date"].search_count(
            domain,
        )
        self._add_report_line(
            unique_id,
            "00_tenders",
            1,
            "1.2. Кількість тендерів на субпідряд",
            leads_subcontractor_count,
        )

        domain = self._generate_domain(send_offer_id)

        lead_offer_ids = (
            self.env["crm.stage.date"]
            .search(
                domain,
            )
            .mapped("lead_id")
        )

        leads_offers_count = len(lead_offer_ids)
        self._add_report_line(
            unique_id,
            "01_commercial",
            2,
            "2.1. Кількість відправленних КП",
            leads_offers_count,
        )

        leads_offer_sum = sum([lead.expected_revenue for lead in lead_offer_ids])
        self._add_report_line(
            unique_id,
            "01_commercial",
            3,
            "2.2. Сума з відправленних КП",
            leads_offer_sum,
        )

        lead_offer_avg = (
            (leads_offer_sum / leads_offers_count) if leads_offers_count > 0 else 0
        )

        self._add_report_line(
            unique_id,
            "01_commercial",
            4,
            "2.3. Середній чек КП",
            lead_offer_avg,
        )

        domain = self._generate_domain(init_project_id)

        lead_init_project_sum = sum(
            self.env["crm.stage.date"]
            .search(
                domain,
            )
            .mapped("lead_id")
            .mapped("expected_revenue")
        )
        self._add_report_line(
            unique_id,
            "03_money",
            5,
            "3.1. Сума підписаних договорів",
            lead_init_project_sum,
        )

        domain = self._generate_domain(get_prepay_id)

        lead_prepay_sum = sum(
            self.env["crm.stage.date"]
            .search(
                domain,
            )
            .mapped("lead_id")
            .mapped("x_advance_pay")
        )
        self._add_report_line(
            unique_id,
            "03_money",
            6,
            "3.2. Сума авансів",
            lead_prepay_sum,
        )

        domain = [
            ("date_closed", ">=", self.start_date),
            ("date_closed", "<=", self.end_date),
            ("probability", "=", 0),
            ("active", "=", False),
        ]

        if self.manager_ids:
            domain += [("user_id", "in", self.manager_ids.ids)]

        lead_lost_sum = sum(
            self.env["crm.lead"]
            .with_context(active_test=False)
            .search(
                domain,
            )
            .mapped("expected_revenue")
        )
        self._add_report_line(
            unique_id,
            "",
            7,
            "4. Сума провалених угод",
            lead_lost_sum,
        )

    def open_report(self):
        self.check_date_range()

        unique_id = uuid.uuid4().hex
        self.fill_report_data(unique_id)

        action = {
            "name": _("Consolidated report ({start_date} - {end_date})").format(
                start_date=self.start_date, end_date=self.end_date
            ),
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
