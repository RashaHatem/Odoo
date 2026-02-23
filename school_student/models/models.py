from odoo import fields, models
from odoo import api
from odoo.exceptions import ValidationError, UserError
# from lxml import etree
class SchoolStudent(models.Model):
    _name = "school.student"
    
    name =  fields.Char(string='Student Name')
    school_id = fields.Many2one('school.profile', string= 'School Name')
    
    hobby_list = fields.Many2many(
        string='Hobby',
        comodel_name='hobbies',
        relation='school_hobby_rel',
        column1='student_id',
        column2='hobby_id',
    )
    absence_count = fields.Integer("عدد أيام الغياب")
    state = fields.Selection([
        ('active', 'مستمر'),
        ('suspended', 'موقوف')
    ], string="الحالة", compute="check_absence_limit", store=True, readonly=True)
    
    priority = fields.Selection([
    ('0', 'Low'),
    ('1', 'Normal'),
    ('2', 'High')
], string="Priority", default='1')
    state_ = fields.Selection([
        ('draft', 'مسودة'),
        ('submitted', 'تم التقديم'),
        ('accepted', 'مقبول'),
        ('rejected', 'مرفوض'),
    ], string="الحالة", default='draft', tracking=True)

    @api.onchange('absence_count')
    def _onchange_absence_count(self):
        if self.absence_count<3:
            return{
                'warning':{
                    'title':'Wait',
                    'message':'You can not edit it',
                    'type':'notification'
                }
            }
    @api.constrains('absence_count')
    def _check_day(self):
        for rec in self:
            if rec.absence_count>3:
                raise UserError ('You cant enter grater than 3')
            
    def action_done(self):
   
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'نجاح',
                'message': 'تم تحديث البيانات بنجاح',
                'sticky': False, 
                'type': 'success',
                'next':{
                    'type':'ir.actions.client',
                    'tag':'soft_reload'
                } 
            }
    }

    def reload_page(self):
        return {
            'type':'ir.actions.client',
            'tag':'reload'
        }
   
    def action_submit(self):
        for rec in self:
            rec.state_ = 'submitted'

    
    def action_accept(self):
        for rec in self:
            rec.state_ = 'accepted'

    
    def action_reject(self):
        for rec in self:
            rec.state_ = 'rejected'
            
   
    def action_draft(self):
        for rec in self:
            rec.state_ = 'draft'
    def unlink(self):
        return super().unlink()
    
    @api.depends('absence_count')
    def check_absence_limit(self):
        
        param_obj = self.env['ir.config_parameter'].sudo()
        max_days_raw = param_obj.get_param('school_student.max_absence_days')
        max_days = int(max_days_raw) if max_days_raw else 0

        for record in self:
            
            if record.absence_count > max_days:
                record.state = 'suspended'
                
            else:
                record.state = 'active'
    
    
    @api.model
    def create(self,val):
        rtn= super(SchoolStudent,self).create(val)
        return rtn
    def costom_method(self):
        self.ensure_one()
        print(self.name)
        
    def print_word(self):
        print('print_word......................')
            
    
        
        
                
                
                
class SchoolProfile(models.Model):
    
    _inherit ="school.profile"
    
    school_list = fields.One2many('school.student', 'school_id', string='schools')
    student_count_ = fields.Integer(compute = '_compute_student_count_')
    
    @api.depends('school_list')
    def _compute_student_count_(self):
        for rec in self:
            
            accepted_std = rec.school_list.filtered(lambda lm : lm.state_ == 'accepted')
            print('--------------------------------------------------------------',accepted_std)
            rec.student_count_ = len(accepted_std)
            
    def print_school_name(self):
       std_list = [std.name for std in self.school_list if std.name]
       std_join= ", ".join(std_list)
       return{
            'type':'ir.actions.client',
            'tag':'display_notification',
            'params':{
                'type':'info',
                'message':f'{std_join} in {self.name}'
            }
            
        }   
   
    # @api.model
    # def get_view(self, view_id=None, view_type='form', **options):
    #     res = super(SchoolProfile,self).get_view(view_id=view_id, view_type=view_type, **options)

    #     field = etree.Element('field', {'name':'school_list'})
    
    #     if view_type == 'form' and 'arch' in res:
    #         doc = etree.fromstring(res['arch'])
    #         position = doc.xpath("//field[@name = 'phone']")
    #         if position:
    #              tree = etree.SubElement(field, 'list')
    #              etree.SubElement(tree, 'field', {'name': 'name'})
    #              
    #         res['arch'] = etree.tostring(doc, encoding = 'unicode')
    #     return res
   
    
class Hobby (models.Model):
    _name ="hobbies"
    
    name = fields.Char("Hobby")
