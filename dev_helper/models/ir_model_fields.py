# -*- coding: utf-8 -*-
from openerp import models, fields, api

class ir_model_fields(models.Model):
    _inherit = 'ir.model.fields'

    @api.multi
    def _get_external_id_name(self):
        for inst in self:
            ir_model_data_env = inst.env['ir.model.data']
            res_id = inst.id
            eid = ir_model_data_env.sudo().search([('model','=','ir.model.fields'),('res_id','=', res_id)])
            inst.external_id_name = eid.module+'.'+eid.name if eid.module else eid.name

    @api.multi
    def _get_views_list(self):
        for inst in self:
            ir_ui_view_env = inst.env['ir.ui.view']
            field_in_these_views = ir_ui_view_env.search([('arch', 'ilike', inst.name), ('model', '=', inst.model_id.model), ('active', '=', True)])
            inst.view_list_ids = field_in_these_views
            res = ''
            for view in field_in_these_views:
                res += "[* {} | {} | {} *]\n".format(str(view.name), str(view.type), str(view.mode))
                # inst.view_list_ids += view
            inst.views_list_txt = res

    external_id_name = fields.Char(string='External ID', compute='_get_external_id_name')
    views_list_txt = fields.Text(string='Used in Views', compute='_get_views_list')
    view_list_ids = fields.Many2many(string='Used in Views', comodel_name='ir.ui.view', compute='_get_views_list')
