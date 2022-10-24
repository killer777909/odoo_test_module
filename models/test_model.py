from odoo import api, fields, models


class TestModel(models.Model):
    _name = 'test.model'
    _description = 'My test model'

    name = fields.Char()
    description = fields.Text()
    count = fields.Integer()
    float = fields.Float()
    currency_id = fields.Many2one('res.currency')  # for Monetary field
    money = fields.Monetary()
    html = fields.Html()
    date = fields.Date()
    time = fields.Datetime()
    checkbox = fields.Boolean()
    selection = fields.Selection(selection=[])
    priority = fields.Selection(
        selection=[('0', 'Normal'), ('1', 'Low'), ('2', 'High'), ('3', 'Very High')])
    file = fields.Binary()
    image = fields.Binary()
    sign = fields.Binary()

    doc_creator_id = fields.Many2one('res.users', default=lambda self: self.env.user, string='Создатель документа', required=True)
    manager_id = fields.Many2one('res.partner', string='Ответственный')
    customer_ids = fields.One2many('test.model.lines', 'test_model_id', string='Клиенты')

    boolean_1 = fields.Boolean(string='1')
    boolean_2 = fields.Boolean(string='2')
    boolean_all = fields.Boolean(string='all')

    @api.onchange('boolean_1', 'boolean_2')
    def _onchange_boolean_1_2(self):
        """Sets boolean_all to True when boolean_1 and boolean_2 are set to True"""
        if self.boolean_1 and self.boolean_2:
            self.boolean_all = True
        else:
            self.boolean_all = False

    @api.onchange('boolean_all')
    def _onchange_boolean_all(self):
        """Sets boolean_1 and boolean_2 to the correct states when boolean_all changes"""
        if self.boolean_all:
            self.boolean_1 = True
            self.boolean_2 = True
        elif self.boolean_all and not self.boolean_1:
            self.boolean_2 = True
        elif self.boolean_all and not self.boolean_2:
            self.boolean_1 = True
        if not self.boolean_all and (self.boolean_1 and self.boolean_2):
            self.boolean_1 = False
            self.boolean_2 = False


class TestModelLines(models.Model):
    _name = 'test.model.lines'
    _description = 'Model for One2Many field'

    test_model_id = fields.Many2one('test.model', ondelete='cascade')
    res_partner_id = fields.Many2one('res.partner', ondelete='cascade')
    email = fields.Char(related='res_partner_id.email')
    