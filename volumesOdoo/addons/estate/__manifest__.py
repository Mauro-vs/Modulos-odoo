{
    'name': 'Real_Estate',
    'version': '1.0',
    'summary': 'Módulo de gestión inmobiliaria',
    'description': 'Este módulo permite gestionar propiedades inmobiliarias, clientes y agentes.',
    'author': 'Mauro',
    'category': 'Real Estate',
    'application': True,
    'depends': ['base'],
    'data': [
        'data/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_view.xml',
        'views/estate_property_tags_view.xml',
        'views/estate_property_offer_view.xml',
        'views/estate_menus.xml',
    ],
}