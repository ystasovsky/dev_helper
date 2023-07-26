# -*- coding: utf-8 -*-
{
    'name': "dev_helper",

    'author': "Y.Stasovsky",
    'website': "http://qarea.com",
    'summary': """Reveal some useful fields in views for ir.model, ir.model.fields, etc, for helping developers in theirs problem solving processes""",

    'category': 'Developer',
    'version': '15.08',

    'depends': ['base', 'group_menu_no_access', 'hr_holidays'],
    # 'depends': ['base', 'group_menu_no_access'],

    'data': [
        'views/base-view_model_form.xml',
        'views/base-view_model_fields_tree.xml',
        'views/base-view_model_tree.xml',
        'views/res_users_view_inh.xml',
        'views/res_groups_tree.xml',
        'views/base-ir-ui-menu.xml',
        'views/base-view_view_tree.xml',
        'views/base-view_view_form.xml',
        'views/base-module_form_inh.xml',
        'views/base-module_tree_inh.xml',
             ],
}