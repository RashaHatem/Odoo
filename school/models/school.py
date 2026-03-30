from odoo import fields, models
from odoo import api
from lxml import etree


class SchollProfile(models.Model):
    _name = "school.profile"
    _description = "school profile"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char(string = "Name", tracking=True)
    email = fields.Char(string = "Email", tracking=True)
    phone = fields.Char("Phone")
    is_virtual_class = fields.Boolean(string = "select")
    currency_id = fields.Many2one ("res.currency", string = "currency")
    fees = fields.Monetary(string='Fees')
    active = fields.Boolean(string='Active', 
    default=True
    )
    new_field = fields.Char(
        string='field_name',
    )
    attachment_ids = fields.Many2many(
        'ir.attachment', 
        string='Attachments'
    )
    school_type = fields.Selection(
        string='School Type',
        selection=[('public', 'Public School'), ('private', 'Private School')]
    ) 
    message = fields.Html(
        string='Message',
        sanitize=True,              
        strip_style=False,          
        translate=True,             
        sanitize_attributes=False,
        
        default="<p>يرجى كتابة رسالة هنا...</p>"
        
    )
    date = fields.Date(
        string='Date',
        default=fields.Date.context_today,
    )
    partner_id = fields.Many2one('res.partner', string="Related Partner")
    related_count = fields.Integer(compute='_compute_related_count')
    
    def _compute_related_count(self):
        for record in self:
            record.related_count = self.env['school.profile'].search_count([])
    
    def print_word(self):
        print("Done.................")
        
   
    def action_toggle_active(self):
        for record in self:
            record.active = not record.active
            
    # @api.model
    # def _name_search(self, name, args=None, operator='ilike', limit=100):
       
    #     args = args or []
    #     name_domain = []
    #     if name:
    #         name_domain = ['|', '|', ('name', operator, name), ('email', operator, name), ('phone', operator, name)]
            
    #     records = self._search(name_domain + args, limit=limit)
    #     return [(record.id,record.display_name) for record in records] 
    
    
    
    
        
    def action_view_related_records(self):
        
        return {
            'name': 'Related Records',
            'type': 'ir.actions.act_window',
            'res_model': 'school.student',
            'view_mode': 'list,form',    
            'domain': [('school_id','=',self.id),('state_','ilike','accepted')], 
            'context': {
            'default_school_id': self.id, 
        },
            'target': 'new',
        }
        
    
    
    def action_done(self):
   
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'نجاح',
                'message': 'تم تحديث البيانات بنجاح',
                'sticky': False, 
                'type': 'success', 
            }
    }
    
   
    @api.depends('name', 'school_type')
    def _compute_display_name(self):
        for record in self:
            name = record.name or ''
            if record.school_type:
                record.display_name = f"{name} ({record.school_type})"
            else:
                record.display_name = name
   
    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=None):
        
        args = args or []
        domain =[]
        if name:
            domain = ['|','|','|', ('name', operator, name), ('phone', operator, name),('email', operator, name), ('school_type', operator, name) ] + args
        
        records = self.search(domain, limit=limit)
        print('wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww',records)
        return [(record.id,record.display_name) for record in records]
    
    # @api.model
    # def _name_search(self, name, domain=None, operator='ilike', limit=None, order=None):

    #     domain = domain or []
    #     if name:
    #         domain = ['|', ('name', operator, name), ('phone', operator, name)] + domain
        
    #     return self._search(domain, limit=limit, order=order)
    
    
    
    # # @api.model
    # # def name_search(self, name, args=None, operator='ilike', limit=100):
    # #     args = args or []
    # #     domain = []
    # #     if name:
    # #         domain = [
    # #            '|', '|', ('name', '=ilike', name), ('email', operator, name) , ('phone', operator, name)
    # #         ]
            
    # #     records = self.search(domain + args, limit=limit)
    # #     return records._compute_display_name()
    
    
    
   
    
    