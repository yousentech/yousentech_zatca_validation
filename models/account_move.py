# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime

class xx_account_move(models.Model):
    _inherit = 'account.move'
    
    zatca_production_flag = fields.Boolean(compute="_get_zatca_production_value")
    
    def _get_zatca_production_value(self):
        for rec in self:
            zatca_config = self.env['res.config.settings'].search([])
            # print("zatca_config",zatca_config.l10n_sa_api_mode)
            if zatca_config.l10n_sa_api_mode:
               rec.zatca_production_flag = True
            else:
                rec.zatca_production_flag = False
    
    def button_draft(self):
        for rec in self:
            if not self.user_has_groups("yousentech_zatca_validation.group_exceed_zatca_validation"):

                if rec.move_type in ('out_invoice','out_refund'):
                    if rec.edi_state in (False, None, ''):
                        continue
                    else:

                        if rec.edi_state in ('sent'):
                            raise ValidationError(
                                "تنبيه : تم الارسال للهيئة لا يمكن اعادة التعيين كمسودة")
            
        return super(xx_account_move,self).button_draft()
    
    def action_reverse(self):
        for rec in self:
            if not self.user_has_groups("yousentech_zatca_validation.group_exceed_zatca_validation"):
                if rec.move_type in ('out_refund'):
                    if rec.edi_state in (False, None, ''):
                        continue
                    else:
                        if rec.edi_state in ('sent') :
                            raise ValidationError( "تنبيه : تم الارسال للهيئة لا يمكن انشاء مرتجع من فاتورة مرتجعة")

        return super(xx_account_move,self).action_reverse()
   
    def action_post(self):
        for rec in self:
            if not self.user_has_groups("yousentech_zatca_validation.group_exceed_zatca_validation"):
                if rec.move_type in ('out_invoice','out_refund'):
                    for line in rec.invoice_line_ids:
                        if not line.product_id and not line.display_type:
                            raise ValidationError(
                                "تنبيه : لا يمكن ترحيل بسبب عدم اسم للمنتجات")

        return super(xx_account_move,self).action_post()
  
    def button_cancel(self):
        for rec in self:
            if not self.user_has_groups("yousentech_zatca_validation.group_allow_cancel_entry"):
                if rec.move_type in ('out_invoice','out_refund'):
                    
                            raise ValidationError(
                                   "تنبيه : لا يمكن الغاء الفاتورة ")

        return super(xx_account_move,self).button_cancel()
        
    def unlink(self):
        for rec in self:
            if not self.user_has_groups("yousentech_zatca_validation.group_allow_delete_entry"):
                if rec.move_type in ('out_invoice','out_refund'):
                     
                            raise ValidationError(
                                   "تنبيه : لا يمكن حذف الفاتورة ")

        return super(xx_account_move,self).unlink()