import logging
from odoo import fields, models, api

_logger = logging.getLogger(__name__)

try:
    from num2words import num2words
except ImportError as err:
    _logger.debug(err)


class CrmLead(models.Model):
    _inherit = "crm.lead"

    biko_amount_untaxed = fields.Monetary(
        string="Untaxed Amount",
        store=True,
        readonly=True,
        compute="_compute_amount_all",
        tracking=5,
        currency_field="company_currency",
    )
    biko_amount_tax = fields.Monetary(
        string="Taxes",
        store=True,
        readonly=True,
        compute="_compute_amount_all",
        currency_field="company_currency",
    )
    biko_amount_total = fields.Monetary(
        string="Total",
        store=True,
        readonly=True,
        compute="_compute_amount_all",
        tracking=4,
        currency_field="company_currency",
    )
    
    biko_currency_name = fields.Char(
        # store=True,
        # readonly=True,
        compute='_compute_biko_currency_name', )
    biko_currency_cent_name = fields.Char(
        # store=True,
        # readonly=True,
        compute='_compute_biko_currency_name', )    
    biko_amount_ukr_text = fields.Char(
        # store=True,
        # readonly=True,
        compute='_compute_biko_amount_ukr_text', )    
    biko_amount_untaxed_ukr_text = fields.Char(
        # store=True,
        # readonly=True,
        compute='_compute_biko_amount_untaxed_ukr_text', )    
    biko_taxed_ukr_text = fields.Char(
        # store=True,
        # readonly=True,
        compute='_compute_biko_taxed_ukr_text', )
    
    @api.depends("lead_product_ids.biko_price_total")
    def _compute_amount_all(self):
        """
        Compute the total amounts of the SO.
        """
        for lead in self:
            amount_untaxed = amount_tax = 0.0
            for line in lead.lead_product_ids:
                amount_untaxed += line.biko_price_subtotal
                amount_tax += line.biko_price_tax
            lead.update(
                {
                    "biko_amount_untaxed": amount_untaxed,
                    "biko_amount_tax": amount_tax,
                    "biko_amount_total": amount_untaxed + amount_tax,
                }
            )

    def _compute_biko_amount_ukr_text(self):
        for obj in self:
            obj.biko_amount_ukr_text = '{} {} {:0>2} {}'.format(
                num2words(int(obj.biko_amount_total), lang='uk'),
                self.biko_currency_name,
                round(100 * (obj.biko_amount_total - int(obj.biko_amount_total))),
                self.biko_currency_cent_name,
            ).capitalize()
            
    def _compute_biko_amount_untaxed_ukr_text(self):
        for obj in self:
            obj.biko_amount_untaxed_ukr_text = '{} {} {:0>2} {}'.format(
                num2words(int(obj.biko_amount_untaxed), lang='uk'),
                self.biko_currency_name,
                round(100 * (obj.biko_amount_untaxed - int(obj.biko_amount_untaxed))),
                self.biko_currency_cent_name,
            ).capitalize() 
            
    def _compute_biko_taxed_ukr_text(self):
        for obj in self:
            obj.biko_taxed_ukr_text = '{} {} {:0>2} {}'.format(
                num2words(int(obj.biko_amount_tax), lang='uk'),
                self.biko_currency_name,
                round(100 * (obj.biko_amount_tax - int(obj.biko_amount_tax))),
                self.biko_currency_cent_name,
            ).capitalize()                       
            
    def _compute_biko_currency_name(self):
        for obj in self:
            if obj.company_currency.currency_unit_label == 'Euros':
                self.biko_currency_name = 'EUR'
                self.biko_currency_cent_name = 'cent'
            elif obj.company_currency.currency_unit_label == 'Dollars':
                self.biko_currency_name = 'USD'
                self.biko_currency_cent_name = 'cent'
            elif obj.company_currency.currency_unit_label == 'Hryvnia':
                self.biko_currency_name = 'грн.'
                self.biko_currency_cent_name = 'коп.'
            else:
                self.biko_currency_name = obj.company_currency.currency_unit_label
                self.biko_currency_cent_name = \
                    obj.company_currency.currency_subunit_label            