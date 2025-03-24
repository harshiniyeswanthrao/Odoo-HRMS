
{
    'name': 'Odoo 18 HR Payroll',
    'version': '18.0.1.0.0',
    'category': 'Human Resources',
    'summary': """Odoo 18 HR Payroll, Odoo18 Payroll, Payroll, Odoo Payroll, Payroll V18, Odoo18, Payroll Management, Odoo18 Payslip""",
    'description': """The system automates payroll management by streamlining
     key processes such as calculating employee salaries, deductions, and 
     benefits based on predefined rules and regulations. It also facilitates
     the automatic generation of detailed payslips, ensuring accuracy in 
     payment breakdowns for each employee. This reduces manual effort, 
     minimizes errors, and ensures compliance with tax and labor laws, while
     providing employees with timely and accurate payment information""",
    'author': ' MY HRMS DASHBOARD',
    'company': 'SAKSHATH TECHNOLOGIES',
    'maintainer': 'HARSHINI G Y ',
    'depends': ['hr_contract', 'hr_holidays'],
    'data': [
        'security/hr_payroll_community_security.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'data/hr_payroll_community_data.xml',
        'wizard/hr_payslips_employees_views.xml',
        'wizard/payslip_lines_contribution_register_views.xml',
        'report/hr_payroll_report.xml',
        'report/report_contribution_register_templates.xml',
        'report/report_payslip_templates.xml',
        'report/report_payslip_details_templates.xml',
        'views/hr_leave_type_views.xml',
        'views/hr_contract_views.xml',
        'views/hr_salary_rule_views.xml',
        'views/hr_salary_rule_category_views.xml',
        'views/hr_contribution_register_views.xml',
        'views/hr_payroll_structure_views.xml',
        'views/hr_payslip_views.xml',
        'views/hr_payslip_line_views.xml',
        'views/hr_employee_views.xml',
        'views/hr_payslip_run_views.xml',
        'views/res_config_settings_views.xml',
    ],
    'demo': ['data/hr_payroll_community_demo.xml'],
    'images': ['static/description/banner.png'],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
}
