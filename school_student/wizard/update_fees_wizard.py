from odoo import models, fields, api

class StudentFeesUpdateWizard(models.TransientModel):
    _name = "student.fees.update.wizard"
    _description = "StudentFeesUpdateWizard"
    
    name = fields.Char(
    string='Student Name',
    readonly=True
    )
    total_fees = fields.Float(
    string='Student Fees',
    required=True
    )
    
    def action_update_fees(self):
        active_ids = self._context.get('active_ids', [])
        
        if active_ids:
            students = self.env['school.student'].browse(active_ids)
        else:
            students = self.env['school.student'].search([])
        
        if students:
            students.write({
                'total_fees': self.total_fees
            })
            
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,      
            'view_mode': 'form',          
            'res_id': self.id,           
            'target': 'new',              
            'context': self._context,     
        }
        
    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        active_ids = self._context.get('active_ids',[])
        
        if active_ids:
            students = self.env['school.student'].browse(active_ids)
            
            if students.exists():                
                res['name'] = ", ".join(students.mapped('name'))
                # res['total_fees'] = float(", ".join(students.mapped(lambda lm: str(lm.total_fees))))
               
                if len(students) == 1:
                    res['total_fees'] = students.total_fees
                else:
                    res['total_fees'] = 0
                    
        else:
            res['name'] = "No student selected , the change for all"
                    
        return res
            
        