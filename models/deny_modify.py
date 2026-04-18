# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError



class period_closed(models.Model):
    _name = 'zatca.deny.modify'

    _rec_name = 'id' 

    closed_date_to = fields.Date(required=True,string="ايقاف التعديل الى تاريخ")
 

class zatca_operation_closed(models.Model):
    _inherit = 'account.move'

    def button_draft(self):
        for rec in self:
            if rec.move_type in ('out_invoice','out_refund'):
                if not self.user_has_groups('yousentech_zatca_validation.group_allow_modify_inv_before_zatca'):
                    rec.check_invoice_date2()
            
        return super(zatca_operation_closed,self).button_draft()
   
   
    def action_reverse(self):
        for rec in self:
            if rec.move_type in ('out_invoice','out_refund'):
                if not self.user_has_groups('yousentech_zatca_validation.group_allow_modify_inv_before_zatca'):
                    rec.check_invoice_date2()
            
        return super(zatca_operation_closed,self).action_reverse()

        
    def button_cancel(self):
        for rec in self:
            if rec.move_type in ('out_invoice','out_refund'):
                if not self.user_has_groups('yousentech_zatca_validation.group_allow_modify_inv_before_zatca'):
                    rec.check_invoice_date2()
            
        return super(zatca_operation_closed,self).button_cancel()
  
    def action_post(self):
        for rec in self:
            if rec.move_type in ('out_invoice','out_refund'):
                if not self.user_has_groups('yousentech_zatca_validation.group_allow_modify_inv_before_zatca'):
                    rec.check_invoice_date2()
            
        return super(zatca_operation_closed,self).action_post()

    @api.constrains('invoice_date', 'date','l10n_sa_confirmation_datetime','l10n_sa_qr_code_str')
    def check_invoice_date(self):
        for rec in self:
            if rec.move_type in ('out_invoice','out_refund'):

                sql_query = ""
            
                allow_operation_flag = self.user_has_groups('yousentech_zatca_validation.group_allow_modify_inv_before_zatca')

            
          
                if rec.invoice_date:
                    sql_query = """  select count(*) as exist_res from  zatca_deny_modify
                                        where '{}' <=  closed_date_to
                                        """.format(rec.invoice_date)
                if rec.date:
                
                    sql_query = """   select count(*) as exist_res from  zatca_deny_modify
                                        where '{}' <=  closed_date_to
                                        """.format(rec.date)
                
                if sql_query:
                    self.env.cr.execute(sql_query)
                    seq = self.env.cr.fetchone()
                    x = seq[0]
                    if x:
                        if not allow_operation_flag:
                            raise ValidationError(  "تنبيه .. لا يمكن تعديل الفواتير قبل مرحلة الربط مع الهيئة (%s)" % rec.name)
 
 
    def check_invoice_date2(self):
        for rec in self:
            if rec.move_type in ('out_invoice','out_refund'):
                sql_query = ""
                allow_operation_flag = self.user_has_groups('yousentech_zatca_validation.group_allow_modify_inv_before_zatca')
                if rec.invoice_date:
                    sql_query = """  select count(*) as exist_res from  zatca_deny_modify
                                        where '{}' <=  closed_date_to
                                        """.format(rec.invoice_date)
                if rec.date:
                
                    sql_query = """   select count(*) as exist_res from  zatca_deny_modify
                                        where '{}' <=  closed_date_to
                                        """.format(rec.date)
            
                if sql_query:
                    self.env.cr.execute(sql_query)
                    seq = self.env.cr.fetchone()
                    x = seq[0]
                    if x:
                        if not allow_operation_flag:
                            raise ValidationError(  "تنبيه .. لا يمكن تعديل الفواتير قبل مرحلة الربط مع الهيئة (%s)" % rec.name)

    def write(self, vals):
        for rec in self:
            if rec.move_type in ('out_invoice','out_refund'):
                if not self.user_has_groups('yousentech_zatca_validation.group_allow_modify_inv_before_zatca'):
                    if vals.get('l10n_sa_confirmation_datetime') or vals.get('l10n_sa_qr_code_str'):
                        self.check_invoice_date2()
        res = super(zatca_operation_closed, self).write(vals)
        return res
 