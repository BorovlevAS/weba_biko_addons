from odoo import models


class LeadDocxCOGeodesy(models.AbstractModel):
    _name = 'report.co_geodesy'            
    _inherit = "report.report_docx.abstract"
    
    def generate_docx_report(self, data, leads):        
        return leads._get_report_data("co_geodesy", False)
    
class LeadDocxCOGeodesyStamp(models.AbstractModel):
    _name = 'report.co_geodesy_with_stamp'            
    _inherit = "report.report_docx.abstract"
    
    def generate_docx_report(self, data, leads):        
        return leads._get_report_data("co_geodesy", True)

class LeadDocxCOLaser(models.AbstractModel):
    _name = 'report.co_laser'            
    _inherit = "report.report_docx.abstract"
    
    def generate_docx_report(self, data, leads):        
        return leads._get_report_data("co_laser", False)
    
class LeadDocxCOLaserStamp(models.AbstractModel):
    _name = 'report.co_laser_with_stamp'            
    _inherit = "report.report_docx.abstract"
    
    def generate_docx_report(self, data, leads):        
        return leads._get_report_data("co_laser", True)
    
class LeadDocxInvoiceVAT(models.AbstractModel):
    _name = 'report.invoice_vat'            
    _inherit = "report.report_docx.abstract"
    
    def generate_docx_report(self, data, leads):        
        return leads._get_report_data("invoice_vat", False)
    
class LeadDocxInvoiceVATStamp(models.AbstractModel):
    _name = 'report.invoice_vat_with_stamp'            
    _inherit = "report.report_docx.abstract"
    
    def generate_docx_report(self, data, leads):        
        return leads._get_report_data("invoice_vat", True)    
    
class LeadDocxInvoiceWithoutVAT(models.AbstractModel):
    _name = 'report.invoice_without_vat'            
    _inherit = "report.report_docx.abstract"
    
    def generate_docx_report(self, data, leads):        
        return leads._get_report_data("invoice_without_vat", False)    
    
class LeadDocxInvoiceWithoutVATStamp(models.AbstractModel):
    _name = 'report.invoice_without_vat_with_stamp'            
    _inherit = "report.report_docx.abstract"
    
    def generate_docx_report(self, data, leads):        
        return leads._get_report_data("invoice_without_vat", True)          
    
class LeadDocxActVAT(models.AbstractModel):
    _name = 'report.act_vat'            
    _inherit = "report.report_docx.abstract"
    
    def generate_docx_report(self, data, leads):        
        return leads._get_report_data("act_vat", False)
    
class LeadDocxActVATStamp(models.AbstractModel):
    _name = 'report.act_vat_with_stamp'            
    _inherit = "report.report_docx.abstract"
    
    def generate_docx_report(self, data, leads):        
        return leads._get_report_data("act_vat", True) 
        
class LeadDocxActWithoutVAT(models.AbstractModel):
    _name = 'report.act_without_vat'            
    _inherit = "report.report_docx.abstract"
    
    def generate_docx_report(self, data, leads):        
        return leads._get_report_data("act_without_vat", False)    
    
class LeadDocxActWithoutVATStamp(models.AbstractModel):
    _name = 'report.act_without_vat_with_stamp'            
    _inherit = "report.report_docx.abstract"
    
    def generate_docx_report(self, data, leads):        
        return leads._get_report_data("act_without_vat", True)     
    
class LeadDocxContractVAT(models.AbstractModel):
    _name = 'report.contract_vat'            
    _inherit = "report.report_docx.abstract"
    
    def generate_docx_report(self, data, leads):        
        return leads._get_report_data("contract_vat", False)
    
class LeadDocxContractVATStamp(models.AbstractModel):
    _name = 'report.contract_vat_with_stamp'            
    _inherit = "report.report_docx.abstract"
    
    def generate_docx_report(self, data, leads):        
        return leads._get_report_data("contract_vat", True) 
        
class LeadDocxContractWithoutVAT(models.AbstractModel):
    _name = 'report.contract_without_vat'            
    _inherit = "report.report_docx.abstract"
    
    def generate_docx_report(self, data, leads):        
        return leads._get_report_data("contract_without_vat", False)    
    
class LeadDocxContractWithoutVATStamp(models.AbstractModel):
    _name = 'report.contract_without_vat_with_stamp'            
    _inherit = "report.report_docx.abstract"
    
    def generate_docx_report(self, data, leads):        
        return leads._get_report_data("contract_without_vat", True)         