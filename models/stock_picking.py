from odoo import models, fields, api
from odoo.exceptions import UserError

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def open_stock_quant_wizard(self):

        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Stock Quant Wizard',
            'res_model': 'wizard.stock.quant',
            'view_mode': 'form',
            'view_id': False,  # Can be set to a specific view ID if needed
            'target': 'new',  # Opens in a popup window
            'context': {
                'default_move_raw_ids': self.move_ids_without_package.ids,  # Passing only the ids of move_raw_ids
                'default_location_src_id':self.location_id.id,
            },
        }
