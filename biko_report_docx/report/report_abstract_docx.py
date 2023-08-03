# Copyright 2015 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from io import BytesIO
import os
from odoo import models, api
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm

class ReportDocxAbstract(models.AbstractModel):
    _name = "report.report_docx.abstract"
    _description = "Abstract DOCX Report"

    def _get_objs_for_report(self, docids, data):
        """
        Returns objects for xlx report.  From WebUI these
        are either as docids taken from context.active_ids or
        in the case of wizard are in data.  Manual calls may rely
        on regular context, setting docids, or setting data.

        :param docids: list of integers, typically provided by
            qwebactionmanager for regular Models.
        :param data: dictionary of data, if present typically provided
            by qwebactionmanager for TransientModels.
        :param ids: list of integers, provided by overrides.
        :return: recordset of active model for ids.
        """
        if docids:
            ids = docids
        elif data and "context" in data:
            ids = data["context"].get("active_ids", [])
        else:
            ids = self.env.context.get("active_ids", [])
        return self.env[self.env.context.get("active_model")].browse(ids)

    @api.model
    def create_docx_report(self, docids, data):
        objs = self._get_objs_for_report(docids, data)
        context_leads = self.generate_docx_report(data, objs)
        context_leads['object']=objs
        template_path = context_leads["path"]
        
        doc = DocxTemplate(template_path)  
        # if 'stamp' in context_leads:      
        #     context_leads['stamp_img'] = InlineImage(doc, context_leads['stamp'], height=Mm(50))
                   
        doc.render(context_leads)
        
        # Удаление временных файлов
        if context_leads['is_template']:            
            os.remove(template_path)
  
        doc_buffer = BytesIO()
        doc.save(doc_buffer)
        doc_buffer.seek(0)

        # return doc_bytes
        return doc_buffer.read(), "docx"

    def generate_docx_report(self, workbook, data, objs):
        raise NotImplementedError()
