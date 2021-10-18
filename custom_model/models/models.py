# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class CustomModel(models.Model):
    _name = 'custom_model.custom_model'
    _rec_name = 'description'

    name = fields.Char()
    value = fields.Integer()
    value2 = fields.Float(compute="_value_pc", store=True)
    description = fields.Text()

    @api.depends('value')
    def _value_pc(self):
        self.value2 = float(self.value) / 100

class CrmLead(models.Model):
    _inherit = 'crm.lead'
    _rec_name = 'new_display_name'

    new_display_name = fields.Text(compute="_compute_new_disp_name")
    custom_field = fields.Many2one('custom_model.custom_model')

    @api.depends('custom_field')
    def _compute_new_disp_name(self):
        for rec in self:
            if rec.custom_field:
                rec.new_display_name = f"New display_name is: {rec.custom_field.description}"
            else:
                rec.new_display_name = "No new display name"


class ResPartner(models.Model):
    _inherit = 'res.partner'
    _rec_name = 'new_display_name'

    new_display_name = fields.Text(compute="_compute_partner_new_disp_name")
    custom_field = fields.Many2one('custom_model.custom_model')

    @api.multi
    def name_get(self):
        result = []
        name = self._rec_name
        if name in self._fields:
            convert = self._fields[name].convert_to_display_name
            for record in self:
                result.append((record.id, convert(record[name], record)))
        else:
            for record in self:
                result.append((record.id, "%s,%s" % (record._name, record.id)))

        return result

    @api.model
    def name_create(self, name):
        if self._rec_name:
            record = self.create({self._rec_name: name})
            return record.name_get()[0]
        else:
            _logger.warning("Cannot execute name_create, no _rec_name defined on %s", self._name)
            return False

    @api.depends('custom_field')
    def _compute_partner_new_disp_name(self):
        for rec in self:
            if rec.custom_field:
                rec.new_display_name = f"New display_name is: {rec.custom_field.description}"
            else:
                rec.new_display_name = "No new display name"