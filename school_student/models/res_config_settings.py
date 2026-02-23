from odoo import api, models,fields


class ResConfigSettings(models.TransientModel):
    
    _inherit = 'res.config.settings'
     
    max_absence_days = fields.Integer(
        string='max_absence_dayes',
        config_parameter= 'school_student.max_absence_days'
    )
   
       
    
    
    

    
