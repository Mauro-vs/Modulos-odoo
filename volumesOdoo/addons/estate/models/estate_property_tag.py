# -*- coding: utf-8 -*-

from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Etiqueta de propiedad"

    # Campos
    name = fields.Char(string="Nombre", required=True)
    color = fields.Integer(string="Color")
    property_ids = fields.Many2many(
        "estate.property",
        string="Propiedades",
    )