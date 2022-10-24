from odoo import fields, models
from odoo.exceptions import ValidationError


class CreateCustomerWizard(models.TransientModel):
    _name = 'test.model.create.customer'
    _description = 'Create customer wizard model'

    name = fields.Char(string='Имя', required=True)
    res_partner_id = fields.Many2one('res.partner')
    test_model_id = fields.Many2one('test.model')

    def action_create_and_add_customer(self):
        self.check_unique_customer_name()
        self.res_partner_id.create({'name': self.name})
        res_partner_name_id = self.env['res.partner'].search([('name', '=', self.name)]).id
        self.test_model_id.write({'customer_ids': [[0, 0, {'res_partner_id': res_partner_name_id}]]})

    def action_create_and_edit_customer(self):
        self.action_create_and_add_customer()
        res_partner_name_id = self.env['res.partner'].search([('name', '=', self.name)]).id
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'res.partner',
            'view_id': self.env.ref('base.view_partner_form').id,
            'res_id': res_partner_name_id
        }
    
    def check_unique_customer_name(self):
        if self.env['res.partner'].search([('name', '=', self.name)]):
            raise ValidationError('Имя клиента должно быть уникальным')
