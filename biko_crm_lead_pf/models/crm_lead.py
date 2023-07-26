from odoo import api, fields, models
from datetime import date
import os
import tempfile
from io import BytesIO
import base64

class CrmLead(models.Model):
    _inherit = 'crm.lead'
    
    def _get_report_pf_filename(self):
        if len(self) > 1:
            return f'"'
        else:
            doc_num = self.name.split('/')[-1]
            doc_date = self.date_open.strftime("%d.%m.%Y")
            return f' {doc_num} от {doc_date}'
        
    def _get_report_data(self, report_name, with_stamp):
        # 
        for lead in self:            
            path = os.path.dirname(__file__).split("/")[0:-1]
            path = "/".join(path)    
                              
            dic = {}  
            
            dic['report_name'] = report_name
            report = self.env['biko.pf.template'].search([('report_name', '=', report_name)]) 
            if with_stamp:
                file_name = 'datas_stamp'
                name_file = 'fname_stamp'
            else:
                file_name = 'datas'
                name_file = 'fname'
            # if report.datas:                
            if report[file_name]:   
                template_path = os.path.join(tempfile.gettempdir(), report_name + '.docx') 
                # template_path = f"{path}/static/template/co_geodesy_copy.docx"
                fdata = decoded_data = base64.b64decode(report[file_name]) 
                with open(template_path, 'wb') as f:
                    f.write((fdata))
                    f.close()
                dic['path'] = template_path
                dic['is_template'] = True

            else:
                dic['path'] = f"{path}/static/template/{report[name_file]}"
                dic['is_template'] = False
                
               
            # dic['current_date'] = date.today()
            dic['current_date'] = fields.Date.context_today(lead)
            dic['code'] = lead.code
            dic['partner_id_name'] = f'{lead.partner_id.name}'
            dic['function'] = lead.function
            dic['contact_name'] = lead.contact_name
            
            
            dic['biko_amount_untaxed'] = lead.biko_amount_untaxed
            dic['biko_amount_tax'] = lead.biko_amount_tax
            dic['biko_amount_total'] = lead.biko_amount_total
            dic['avans70'] = lead.biko_amount_total * 0.7 
            
            
            # А может аванс% брать из поля x_advance? или попросту x_advance_pay
            dic['remainder'] = 100 - lead.x_advance
            dic['biko_amount_ukr_text'] = lead.biko_amount_ukr_text
            dic['biko_amount_untaxed_ukr_text'] = lead.biko_amount_untaxed_ukr_text
            dic['biko_taxed_ukr_text'] = lead.biko_taxed_ukr_text
            
            dic['x_field_stage'] = lead.x_field_stage
            dic['x_conditions'] = lead.x_conditions
            dic['x_object_address'] = lead.x_object_address
            dic['x_term'] = lead.x_term
            dic['x_advance'] = lead.x_advance
            dic['x_date_act'] = lead.x_date_act
            dic['x_contract_number'] = lead.x_contract_number
            dic['x_date_contract'] = lead.x_date_contract
            dic['x_advance_pay'] = lead.x_advance_pay
            dic['over'] = lead.biko_amount_total - lead.x_advance_pay
            
            
            nom = 0
            products = []
            for str in lead.lead_product_ids:
                nom += 1
                products.append({
                    'nom': nom,
                    'product_id': str.product_id.with_context(lang='uk_UA').name,
                    'qty': str.qty,
                    'product_uom': str.product_uom.with_context(lang='uk_UA').name,
                    'price_unit': str.price_unit,
                    'biko_price_subtotal': str.biko_price_total,
                })

            dic['products'] = products                   
                        
            return  dic           