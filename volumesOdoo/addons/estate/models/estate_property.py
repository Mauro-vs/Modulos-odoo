# -*- coding: utf-8 -*-
from odoo import models, fields

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    
    name = fields.Char(string="Titulo", required=True)
    cp = fields.Char(string="Código Postal")
    date_availability = fields.Date(string="Fecha de Disponibilidad", default=lambda self: fields.Date.add(fields.Date.today(), months=3))
    description = fields.Text(string="Descripción")
    expected_price = fields.Float(string="Precio Esperado", required=True)
    selling_price = fields.Float(string="Precio de Venta", readonly=True)
    bedrooms = fields.Integer(string="Número de Dormitorios", default=2)
    living_area = fields.Integer(string="Área Habitable")
    facades = fields.Integer(string="Número de Fachadas")
    garage = fields.Boolean(string="Garaje")
    garden = fields.Boolean(string="Jardín")
    garden_area = fields.Integer(string="Área de Jardín")
    garden_orientation = fields.Selection([
        ('N', 'Norte'),
        ('S', 'Sur'),
        ('E', 'Este'),
        ('W', 'Oeste')
    ], string="Orientación")

    # Etiquetas (tags)
    tag_ids = fields.Many2many(
        "estate.property.tag",
        string="Etiquetas",
    )

    # Relación con el tipo de propiedad
    property_type_id = fields.Many2one(
        "estate.property.type",
        string="Tipo de propiedad",
    )

    # Relaciones con comprador y comercial
    buyer_id = fields.Many2one(
        "res.partner",
        string="Comprador",
        copy=False,
    )
    salesman_id = fields.Many2one(
        "res.users",
        string="Comercial",
        default=lambda self: self.env.user,
    )

    # Ofertas relacionadas
    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_id",
        string="Ofertas",
    )

    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ("new", "Nueva Propiedad"),
            ("offer_received", "Recibida"),
            ("offer_accepted", "Aceptada"),
            ("sold", "Vendido"),
            ("canceled", "Cancelado"),
        ],
        string="Estado",
        required=True,
        copy=False,
        default="new",
    )

    _sql_constraints = [
        (
            "check_expected_price",
            "CHECK(expected_price > 0)",
            "Se espera que el precio sea mayor que 0.",
        ),
    ]