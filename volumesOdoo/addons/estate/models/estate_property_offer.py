# -*- coding: utf-8 -*-

from odoo import models, fields


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
    partner_id = fields.Many2one(
        "res.partner",
        string="Partner",
    )
    property_id = fields.Many2one(
        "estate.property",
        string="Propiedad",
        required=True,
    )
    