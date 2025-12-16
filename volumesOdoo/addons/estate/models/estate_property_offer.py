# -*- coding: utf-8 -*-

from datetime import date

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


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

    @api.model_create_multi
    def create(self, vals_list):
        """Crea registros de ofertas y actualiza el estado de la propiedad"""
        records = super().create(vals_list)
        for record in records:
            if record.property_id.state == 'new':
                record.property_id.state = 'offer_received'
        return records
    
    def action_accept(self):
        """Acepta la oferta y actualiza el estado de la propiedad"""
        for offer in self:
            if offer.property_id.offer_ids.filtered(lambda o: o.status == 'accepted' and o.id != offer.id):
                raise UserError("Ya hay una oferta aceptada para esta propiedad.")
            offer.status = 'accepted'
            offer.property_id.state = 'offer_accepted'
            offer.property_id.selling_price = offer.price
            offer.property_id.buyer_id = offer.partner_id
        return True

    def action_refuse(self):
        """Rechaza la oferta"""
        for offer in self:
            acepted_offers = offer.status == 'accepted'
            offer.status = 'refused'
            if acepted_offers:
                offer.property_id.state = 'offer_received'
                offer.property_id.buyer_id = False
                offer.property_id.selling_price = 0
        return True

    def reset_to_new(self):
        """Restablece el estado de la oferta a nuevo"""
        for offer in self:
            pid = offer.property_id
            if pid:
                pid.state = 'new'
                pid.buyer_id = False
                pid.selling_price = 0
        return super(EstatePropertyOffer, self).reset_to_new()
    
    @api.constrains('price')
    def _check_expected_price(self):
        for record in self:
            best_offer = record.property_id.expected_price
            if best_offer and record.price < 0.9 * best_offer:
                raise ValidationError(f"La oferta debe ser al menos el 90% de la mejor oferta.")

    # RESTRICCIONES
    _sql_constraints = [
        ('price_positive', 'CHECK(price > 0)', 'El precio debe ser mayor que cero.')
    ]

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
    