{
    'name': 'MRP Product Location',
    'version': '1.0',
    'author':'ANFEPI: Roberto Requejo Fernández',
    'depends': ['mrp'],
    'description': """
    """,
    'data': [
        'views/mrp_production_views.xml',
        'views/wizard_stock_quant_view.xml',
        'security/ir.model.access.csv',
        'report/stock_quant_report.xml',
        'views/view_stock_picking.xml'
    ],
    'images': ['static/description/icon.png'],
    'installable': True,
    'auto_install': False,
    "license": "AGPL-3",
}