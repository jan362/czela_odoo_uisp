# -*- coding: utf-8 -*-

from odoo import api, fields, models


class UispSite(models.Model):
    """UISP Site - network location."""

    _name = 'uisp.site'
    _description = 'UISP Site'
    _parent_name = 'parent_id'
    _parent_store = True
    _order = 'name'

    uisp_id = fields.Char('UISP ID', required=True, index=True)
    name = fields.Char('Site Name', required=True)
    parent_id = fields.Many2one('uisp.site', 'Parent Site', index=True, ondelete='cascade')
    parent_path = fields.Char(index=True)

    # Location
    latitude = fields.Float('Latitude', digits=(10, 7))
    longitude = fields.Float('Longitude', digits=(10, 7))

    # Relations
    device_ids = fields.One2many('uisp.device', 'site_id', 'Devices')
    device_count = fields.Integer('Device Count', compute='_compute_device_count', store=True)

    # Metadata
    sync_date = fields.Datetime('Last Synced', default=lambda self: fields.Datetime.now())

    @api.depends('device_ids')
    def _compute_device_count(self):
        for site in self:
            site.device_count = len(site.device_ids)
