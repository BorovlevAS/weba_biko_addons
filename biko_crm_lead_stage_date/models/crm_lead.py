from odoo import fields, models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    lead_stage_date_ids = fields.One2many(
        comodel_name="crm.stage.date",
        inverse_name="lead_id",
        string="Stage change date",
    )

    def _create_history_record(self, stage_id):
        history_link = self.env["crm.stage.date"].search(
            [("stage_id", "=", stage_id), ("lead_id", "=", self.id)]
        )

        if not history_link:
            history_link = self.env["crm.stage.date"].create(
                {
                    "change_date": fields.Datetime.now(),
                    "stage_id": stage_id,
                    "lead_id": self.id,
                }
            )
        else:
            history_link.write(
                {
                    "change_date": fields.Datetime.now(),
                }
            )

        return history_link

    def write(self, vals):
        if "stage_id" in vals:
            stage_id = vals["stage_id"]
            history_link = self._create_history_record(stage_id)
            vals.update({"lead_stage_date_ids": [(4, history_link.id)]})

        return super().write(vals)

    def create(self, vals):
        lead = super().create(vals)
        stage_id = lead.stage_id
        lead.update(
            {
                "lead_stage_date_ids": [
                    (
                        0,
                        0,
                        {
                            "change_date": fields.Datetime.now(),
                            "stage_id": stage_id.id,
                        },
                    )
                ]
            }
        )
        return lead
