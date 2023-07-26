# -*- coding: utf-8 -*-
from openerp import models, fields, api, SUPERUSER_ID

class resUsers(models.Model):
    _inherit = 'res.users'

    # _rec_name = "login"


    groups_id_normal = fields.Many2many('res.groups', 'res_groups_users_rel', 'uid', 'gid', 'Groups')

class cset(object):
    """ A cset (constrained set) is a set of elements that may be constrained to
        be a subset of other csets.  Elements added to a cset are automatically
        added to its supersets.  Cycles in the subset constraints are supported.
    """
    def __init__(self, xs):
        self.supersets = set()
        self.elements = set(xs)
    def subsetof(self, other):
        if other is not self:
            self.supersets.add(other)
            other.update(self.elements)
    def update(self, xs):
        xs = set(xs) - self.elements
        if xs:      # xs will eventually be empty in case of a cycle
            self.elements.update(xs)
            for s in self.supersets:
                s.update(xs)
    def __iter__(self):
        return iter(self.elements)

class resGroups(models.Model):
    _inherit = 'res.groups'
    _rec_name = 'external_id_name'

    @api.multi
    def _get_external_id_name(self):
        for inst in self:
            ir_model_data_env = inst.env['ir.model.data']
            res_id = inst.id
            eid = ir_model_data_env.sudo().search([('model', '=', 'res.groups'), ('res_id', '=', res_id)])
            inst.external_id_name = eid.module + '.' + eid.name if eid.module else eid.name


    external_id_name = fields.Char(string='External ID', compute='_get_external_id_name')
    parent_groups = fields.Many2many('res.groups', 'res_groups_implied_rel', 'hid', 'gid', string='Direct parent groups')

    @api.multi
    def _get_parent_implied(self):
    # def _get_trans_implied(self, cr, uid, ids, field, arg, context=None):
        "computes the transitive closure of relation implied_ids"
        memo = {}           # use a memo for performance and cycle avoidance
        def computed_set(g):
            if g not in memo:
                # memo[g] = cset(g.implied_ids)
                memo[g] = cset(g.parent_groups)
                # for h in g.implied_ids:
                for h in g.parent_groups:
                    computed_set(h).subsetof(memo[g])
            res =  memo[g]
            return res

        # res = {}
        for g in self:
            # res[g.id] = map(int, computed_set(g))
            res = []
            memores = computed_set(g)
            for el in memores.elements:
                res.append(el.id)
            g.trans_parent_groups = [(6,0, res)]


    trans_parent_groups = fields.Many2many(comodel_name='res.groups', compute='_get_parent_implied')
