# -*- coding: utf-8 -*-

import csv
import io
import base64
from odoo import api, fields, models
from odoo.exceptions import UserError


class CtuExportWizard(models.TransientModel):
    """Wizard for ČTÚ ART252 export."""

    _name = 'ctu.export.wizard'
    _description = 'ČTÚ ART252 Export Wizard'

    technology = fields.Selection([
        ('s2_wifi', 'WiFi (volné pásmo)'),
        ('s2_ftth', 'FTTH (optika)'),
        ('s2_fwa', 'FWA (licencované)')
    ], string='Technologie', required=True, default='s2_wifi')

    csv_file = fields.Binary('CSV File', readonly=True)
    csv_filename = fields.Char('Filename', readonly=True)
    state = fields.Selection([
        ('draft', 'Ready'),
        ('done', 'Exported'),
    ], default='draft')

    result_message = fields.Text('Export Summary', readonly=True)

    def action_export_csv(self):
        """Generate ČTÚ ART252 CSV export."""
        self.ensure_one()

        try:
            # Get UISP devices filtered by CTU type
            devices = self.env['uisp.device'].search([
                ('ctu_type', '=', self.technology)
            ])

            if not devices:
                raise UserError(
                    f'No devices found for technology: {dict(self._fields["technology"].selection)[self.technology]}'
                )

            # Aggregate data by RUIAN code
            # Note: This simplified version assumes partner has ruian_code field
            # In production, you'll need to adapt based on your actual data model
            ruian_data = {}

            for device in devices:
                # This is a placeholder - adjust based on your actual partner/RUIAN relationship
                # In czela_ctu, this uses network.inventory.device → partner → ruian_code
                # For now, we'll create sample export structure
                pass

            # Generate CSV
            output = io.StringIO()
            writer = csv.writer(output, delimiter=';')

            # Header
            writer.writerow([
                'ADM',  # RUIAN code
                'kategorie',  # Technology type
                'aktivni_pripojeni',  # Active connections
                'nepodnikatelske',  # Non-business connections
                'pokryti',  # Coverage (0 or 1)
                'download',  # Download speed interval
                'upload',  # Upload speed interval
                'download_max',  # Max download speed
                'upload_max',  # Max upload speed
                'trida_vhcn'  # VHCN class
            ])

            # Speed mapping based on technology
            speed_map = {
                's2_ftth': {
                    'download': '100_300',
                    'upload': '30_100',
                    'download_max': 300,
                    'upload_max': 100,
                    'vhcn_class': 1
                },
                's2_fwa': {
                    'download': '30_100',
                    'upload': '10_30',
                    'download_max': 100,
                    'upload_max': 30,
                    'vhcn_class': 2
                },
                's2_wifi': {
                    'download': '30_100',
                    'upload': '10_30',
                    'download_max': 100,
                    'upload_max': 30,
                    'vhcn_class': 2
                },
            }

            speeds = speed_map.get(self.technology, speed_map['s2_wifi'])

            # Example rows (in production, aggregate by RUIAN from actual data)
            # This is placeholder - implement actual aggregation logic
            sample_ruian_data = {
                '12345678': {
                    'active_connections': len(devices),
                    'non_business': int(len(devices) * 0.8),  # 80% estimate
                    'coverage': 1
                }
            }

            for ruian, data in sample_ruian_data.items():
                writer.writerow([
                    ruian,
                    self.technology,
                    data['active_connections'],
                    data['non_business'],
                    data['coverage'],
                    speeds['download'],
                    speeds['upload'],
                    speeds['download_max'],
                    speeds['upload_max'],
                    speeds['vhcn_class']
                ])

            # Encode CSV
            csv_content = output.getvalue()
            csv_bytes = csv_content.encode('utf-8')
            csv_base64 = base64.b64encode(csv_bytes)

            # Generate filename
            today = fields.Date.today().strftime('%Y%m%d')
            filename = f'ctu_export_{self.technology}_{today}.csv'

            # Save and show result
            self.write({
                'csv_file': csv_base64,
                'csv_filename': filename,
                'state': 'done',
                'result_message': f"""Export completed successfully!

Technology: {dict(self._fields['technology'].selection)[self.technology]}
Devices found: {len(devices)}
Rows exported: {len(sample_ruian_data)}

Note: This is a simplified export. For production use, implement full RUIAN aggregation logic based on your partner/network.inventory.device relationship.
"""
            })

            return {
                'type': 'ir.actions.act_window',
                'res_model': 'ctu.export.wizard',
                'view_mode': 'form',
                'res_id': self.id,
                'target': 'new',
            }

        except Exception as e:
            raise UserError(f'Export failed: {str(e)}')

    def action_download(self):
        """Download CSV file."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content?model=ctu.export.wizard&id={self.id}&field=csv_file&filename_field=csv_filename&download=true',
            'target': 'self',
        }

    def action_close(self):
        """Close wizard."""
        return {'type': 'ir.actions.act_window_close'}
