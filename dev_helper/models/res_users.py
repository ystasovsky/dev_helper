# -*- coding: utf-8 -*-
from odoo import models, fields, api

class resUsers(models.Model):
    _inherit = 'res.users'

    _rec_name = "login"


    groups_id_normal = fields.Many2many('res.groups', 'res_groups_users_rel', 'uid', 'gid', 'Groups')

class resGroups(models.Model):
    _inherit = 'res.groups'

    # @api.multi
    def _get_external_id_name(self):
        for inst in self:
            ir_model_data_env = inst.env['ir.model.data']
            res_id = inst.id
            eid = ir_model_data_env.sudo().search([('model', '=', 'res.groups'), ('res_id', '=', res_id)])
            inst.external_id_name = eid.module + '.' + eid.name if eid.module else eid.name

    external_id_name = fields.Char(string='External ID', compute='_get_external_id_name')
