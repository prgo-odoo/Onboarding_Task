{
    'name': 'Product Extension',
    'version': '1.0',
    'description': "Product Extension",
    'depends': ['stock', 'sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_status_views.xml',
        'views/product_template_views.xml',
        'views/product_packaging_extension_view.xml',
        'views/product_pallet_spec_views.xml',
        'views/product_category_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3'
}
