# -*- coding: utf-8 -*-
from odoo import models, fields

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    
    name = fields.Char(string="Nombre Propiedad", required=True)
    cp = fields.Char(string="Código Postal")
    date_availability = fields.Date(string="Fecha de Disponibilidad", default=fields.Date.today)
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