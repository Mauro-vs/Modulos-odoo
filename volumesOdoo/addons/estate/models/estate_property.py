# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError

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

    best_offer = fields.Float(string="Mejor Oferta",compute="_compute_best_offer",readonly=True)
    total_area = fields.Integer(string="Área Total", compute="_compute_total_area", readonly=True)


     # RELACIONES
    tag_ids = fields.Many2many(
        "estate.property.tag",
        string="Etiquetas",
    )
    property_type_id = fields.Many2one(
        "estate.property.type",
        string="Tipo de propiedad",
    )
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
    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_id",
        string="Ofertas",
    )

    # FUNCIONES
    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        for prop in self:
            if prop.offer_ids:
                prop.best_offer = max(prop.offer_ids.mapped('price'))
            else:
                prop.best_offer = 0.0

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for prop in self:
            prop.total_area = prop.living_area + (prop.garden_area or 0)
    
    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'N'
        else:
            self.garden_area = 0
            self.garden_orientation = None

    def button_sold(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError("No se puede vender una propiedad cancelada.")
            record.state = 'sold'
        return True
    
    def button_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("No se puede cancelar una propiedad vendida.")
            record.state = 'canceled'
        return True
            
    #RESTRICCIONES
    _sql_constraints = [
        ('expected_price_positive', 'CHECK(expected_price > 0)', 'El precio esperado debe ser mayor que cero.'),
        ('selling_price_positive', 'CHECK(selling_price >= 0)', 'El precio de venta no puede ser negativo.'),
    ]