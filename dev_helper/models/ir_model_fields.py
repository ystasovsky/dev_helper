# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ir_model_fields(models.Model):
    _inherit = 'ir.model.fields'

    @api.multi
    def _get_external_id_name(self):
        for inst in self:
            ir_model_data_env = inst.env['ir.model.data']
            res_id = inst.id
            eids = ir_model_data_env.sudo().search([('model','=','ir.model.fields'),('res_id','=', res_id)])

            inst.external_id_name = str([eid.module+'.'+eid.name if eid.module else eid.name for eid in eids])


    external_id_name = fields.Char(string='External ID', compute='_get_external_id_name')
