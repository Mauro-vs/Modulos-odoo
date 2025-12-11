# -*- coding: utf-8 -*-

from odoo import models, fields

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Tipo de propiedad"

    # Campos
    name = fields.Char(string="Nombre", required=True)
    sequence = fields.Integer(string="Secuencia", default=10)
    property_ids = fields.One2many(
        "estate.property",
        "property_type_id",
        string="Propiedades",
    )
    offer_count = fields.Integer(string="Número de ofertas")
    active = fields.Boolean(string="Activo", default=True)