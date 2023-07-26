# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ir_module_module(models.Model):
    _inherit = 'ir.module.module'
    _rec_name = 'name'

    dependent_ids = fields.Many2many(comodel_name='ir.module.module', compute='_get_dependent_ids')

    # @api.multi
    def _get_dependent_ids(self):
        mod_env = self.env['ir.module.module']
        for inst in self:
            # sql = "select immd.name,imm.name   from ir_module_module_dependency immd join ir_module_module imm on immd.module_id=imm.id where immd.name='hr_one2many_field_action'"
            sql = "select imm.id   from ir_module_module_dependency immd join ir_module_module imm on immd.module_id=imm.id where immd.name='{}'".format(inst.name)
            inst.env.cr.execute(sql)
            dependent_module_ids = [row[0] for row in inst.env.cr.fetchall()]
            modules = mod_env.browse(dependent_module_ids)
            inst.dependent_ids = modules

