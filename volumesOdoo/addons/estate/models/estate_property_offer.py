# -*- coding: utf-8 -*-

from datetime import date

from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Oferta de propiedad"

    # Campos
    price = fields.Float(string="Precio", required=True)
    status = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        string="Estado",
        copy=False,
    )

    validity = fields.Integer(string='Validity (days)', default=7)
    date_deadline = fields.Date(string='Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline')

    # FUNCIONES
    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for offer in self:
            date_initial = offer.create_date.date() if offer.create_date else date.today()
            offer.date_deadline = fields.Date.add(date_initial, days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            if offer.date_deadline:
                date_initial = offer.create_date.date() if offer.create_date else date.today()
                offer.validity = (offer.date_deadline - date_initial).days
            else:
                offer.validity = 0

    # RELACIONES
    partner_id = fields.Many2one(
        "res.partner",
        string="Partner",
    )
    property_id = fields.Many2one(
        "estate.property",
        string="Propiedad",
        required=True,
    )
    