from odoo import models, fields, api
from odoo.exceptions import UserError
class WizardStockQuant(models.TransientModel):
    _name = 'wizard.stock.quant'
    _description = 'Stock Quant Wizard'

    stock_quant_ids = fields.One2many('wizard.stock.quant.line', 'wizard_id', string='Stock Quants')

    @api.model
    def default_get(self, fields):
        res = super(WizardStockQuant, self).default_get(fields)
        
        # Check if default_move_raw_ids exists in context, and build the lines accordingly
        if self.env.context.get('default_move_raw_ids'):
            move_raw_ids = self.env.context['default_move_raw_ids']
            location = self.env.context['default_location_src_id']

            location_id = self.env['stock.location'].search([('id','=',location)])

            # Iterate over the move_raw_ids and create stock quant lines for each one
            quant_lines = []
            for move_raw_id in self.env['stock.move'].browse(move_raw_ids):
                quants = self.env['stock.quant'].search([
                    # ('product_id', '=', move_raw_id.product_id.id),
                    ('location_id', '=', location_id.id)  # Apply the location filter
                ])

                for quant in quants:
                    quant_lines.append((0, 0, {
                        'location_id': quant.location_id.id,
                        'quantity': quant.quantity,
                        'reserved_quantity': quant.reserved_quantity,
                        'product_name': quant.product_id.display_name,  # Get the product name
                        'serial_number': quant.lot_id.name,  # Get the serial number if available
                    }))
            res['stock_quant_ids'] = quant_lines
        
        return res
    
    def print_report(self):
        data = {
            'stock_quants': [
                {
                    'product_name': line.product_name,
                    'location_name': line.location_id.display_name,
                    'quantity': line.quantity,
                    'reserved_quantity': line.reserved_quantity,
                    'serial_number': line.serial_number
                } for line in self.stock_quant_ids
            ]
        }
        print("\n\n\n")
        print(data)
        return self.env.ref('mrp_product_location.action_stock_quant_report').report_action([], data=data)


class WizardStockQuantLine(models.TransientModel):
    _name = 'wizard.stock.quant.line'
    _description = 'Stock Quant Line'

    wizard_id = fields.Many2one('wizard.stock.quant', string='Wizard')
    location_id = fields.Many2one('stock.location', string='Location')
    quantity = fields.Float(string='Quantity', readonly=True)
    reserved_quantity = fields.Float(string='Reserved Quantity', readonly=True)
    product_name = fields.Char(string='Product Name', readonly=True)
    serial_number = fields.Char(string='Serial Number', readonly=True)
