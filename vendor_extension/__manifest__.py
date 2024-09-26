{
    'name': 'Vendor Extension',
    'version': '1.0',
    'description': "Vendor Extension",
    'depends': [
        'purchase', 'product_extension'
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/vendor_status_data.xml',
        'views/vendor_status_views.xml',
        'views/res_partner_views.xml',
        'views/gfsi_scheme_views.xml',
        'views/gfsi_grade_views.xml',
        'views/other_certification_views.xml',
        'views/vendor_pricelist_views.xml',
    ],
    'demo': [
        'demo/gfsi_scheme_demo_data.xml',
        'demo/gfsi_grade_demo_data.xml',
        'demo/other_certification_demo_data.xml'
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3'
}
