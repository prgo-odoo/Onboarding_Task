{
    'name': 'Product Extension',
    'version': '1.0',
    'description': "Product Extension",
    'depends': [
        'sale', 'stock'
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/product_status_views.xml',
        'views/product_template_views.xml',
        'views/product_packaging_extension_view.xml',
        'views/product_pallet_spec_views.xml',
        'views/product_category_views.xml',
        # 'data/product_status_data.xml'
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3'
}
