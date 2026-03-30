# -*- coding: utf-8 -*-
{
    'name': "school_student",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,
    'license': 'LGPL-3',
    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mail','school'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/hobbies.csv',
        'wizard/update_fees_wizard.xml',
        'views/views.xml',
        'views/templates.xml',
        'data/delete.xml',
                
    ],
    'assets': {
    'web._assets_primary_variables': [
    
        ('prepend','school_student/static/src/scss/style.scss')
    ],
    'web.assets_backend': [
        'school_student/static/src/css/style.css',
    ],
},
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

