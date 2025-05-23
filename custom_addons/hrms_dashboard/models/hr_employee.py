
import pandas as pd
from collections import defaultdict
from datetime import timedelta, datetime, date
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, _
from odoo.http import request
from odoo.tools import float_utils
from odoo.tools import format_duration
from pytz import utc

ROUNDING_FACTOR = 16


class HrEmployee(models.Model):
    """ Inherit hr_employee to add birthday field and custom methods. """
    _inherit = 'hr.employee'

    birthday = fields.Date(string='Date of Birth', groups="base.group_user",
                           help="Birthday of employee")

    def attendance_manual(self):
        """Create and update an attendance for the user employee"""
        employee = request.env['hr.employee'].sudo().browse(
            self.env.user.employee_id.id)
        employee.sudo()._attendance_action_change({
            'city': request.geoip.city.name or _('Unknown'),
            'country_name': request.geoip.country.name or
                            request.geoip.continent.name or _('Unknown'),
            'latitude': request.geoip.location.latitude or False,
            'longitude': request.geoip.location.longitude or False,
            'ip_address': request.geoip.ip,
            'browser': request.httprequest.user_agent.browser,
            'mode': 'kiosk'
        })
        return employee

    @api.model
    def check_user_group(self):
        """To check the user is a hr manager or not"""
        uid = request.session.uid
        user = self.env['res.users'].sudo().search([('id', '=', uid)], limit=1)
        if user.has_group('hr.group_hr_manager'):
            return True
        else:
            return False

    @api.model
    def get_user_employee_details(self):
        """To fetch the details of employee"""
        uid = request.session.uid
        employee = self.env['hr.employee'].sudo().search_read(
            [('user_id', '=', uid)], limit=1)
        attendance = self.env['hr.attendance'].sudo().search_read(
            [('employee_id', '=', employee[0]['id'])],
            fields=['id', 'check_in', 'check_out', 'worked_hours'])
        attendance_line = []
        for line in attendance:
            if line['check_in'] and line['check_out']:
                val = {
                    'id':line['id'],
                    'date': line['check_in'].date(),
                    'sign_in': line['check_in'].time().strftime('%H:%M'),
                    'sign_out': line['check_out'].time().strftime('%H:%M'),
                    'worked_hours': format_duration(line['worked_hours'])
                }
                attendance_line.append(val)
        leaves = self.env['hr.leave'].sudo().search_read(
            [('employee_id', '=', employee[0]['id'])],
            fields=['request_date_from', 'request_date_to', 'state',
                    'holiday_status_id'])
        for line in leaves:
            line['type'] = line.pop('holiday_status_id')[1]
            if line['state'] == 'confirm':
                line['state'] = 'To Approve'
                line['color'] = 'orange'
            elif line['state'] == 'validate1':
                line['state'] = 'Second Approval'
                line['color'] = '#7CFC00'
            elif line['state'] == 'validate':
                line['state'] = 'Approved'
                line['color'] = 'green'
            elif line['state'] == 'cancel':
                line['state'] = 'Cancelled'
                line['color'] = 'red'
            else:
                line['state'] = 'Refused'
                line['color'] = 'red'
        expense = self.env['hr.expense'].sudo().search_read(
            [('employee_id', '=', employee[0]['id'])],
            fields=['name', 'date', 'state', 'total_amount'])
        for line in expense:
            if line['state'] == 'draft':
                line['state'] = 'To Report'
                line['color'] = '#17A2B8'
            elif line['state'] == 'reported':
                line['state'] = 'To Submit'
                line['color'] = '#17A2B8'
            elif line['state'] == 'submitted':
                line['state'] = 'Submitted'
                line['color'] = '#FFAC00'
            elif line['state'] == 'approved':
                line['state'] = 'Approved'
                line['color'] = '#28A745'
            elif line['state'] == 'done':
                line['state'] = 'Done'
                line['color'] = '#28A745'
            else:
                line['state'] = 'Refused'
                line['color'] = 'red'
        leaves_to_approve = self.env['hr.leave'].sudo().search_count(
            [('state', 'in', ['confirm', 'validate1'])])
        today = datetime.strftime(datetime.today(), '%Y-%m-%d')
        query = """
        select count(id)
        from hr_leave
        WHERE (hr_leave.date_from::DATE,hr_leave.date_to::DATE) 
        OVERLAPS ('%s', '%s') and
        state='validate'""" % (today, today)
        cr = self._cr
        cr.execute(query)
        leaves_today = cr.fetchall()
        first_day = date.today().replace(day=1)
        last_day = (date.today() + relativedelta(months=1, day=1)) - timedelta(
            1)
        query = """
                select count(id)
                from hr_leave
                WHERE (hr_leave.date_from::DATE,hr_leave.date_to::DATE) 
                OVERLAPS ('%s', '%s')
                and  state='validate'""" % (first_day, last_day)
        cr = self._cr
        cr.execute(query)
        leaves_this_month = cr.fetchall()
        leaves_alloc_req = self.env['hr.leave.allocation'].sudo().search_count(
            [('state', 'in', ['confirm', 'validate1'])])
        timesheet_count = self.env['account.analytic.line'].sudo().search_count(
            [('project_id', '!=', False), ('user_id', '=', uid)])
        timesheet_view_id = self.env.ref(
            'hr_timesheet.hr_timesheet_line_search')
        job_applications = self.env['hr.applicant'].sudo().search_count([])
        if employee:
            sql = """select broad_factor from hr_employee_broad_factor 
            where id =%s"""
            self.env.cr.execute(sql, (employee[0]['id'],))
            result = self.env.cr.dictfetchall()
            broad_factor = result[0]['broad_factor'] if result[0][
                'broad_factor'] else False
            if employee[0]['birthday']:
                diff = relativedelta(datetime.today(), employee[0]['birthday'])
                age = diff.years
            else:
                age = False
            if employee[0]['joining_date']:
                diff = relativedelta(datetime.today(),
                                     employee[0]['joining_date'])
                years = diff.years
                months = diff.months
                days = diff.days
                experience = '{} years {} months {} days'.format(years, months,
                                                                 days)
            else:
                experience = False
            if employee:
                data = {
                    'broad_factor': broad_factor if broad_factor else 0,
                    'leaves_to_approve': leaves_to_approve,
                    'leaves_today': leaves_today,
                    'leaves_this_month': leaves_this_month,
                    'leaves_alloc_req': leaves_alloc_req,
                    'emp_timesheets': timesheet_count,
                    'job_applications': job_applications,
                    'timesheet_view_id': timesheet_view_id,
                    'experience': experience,
                    'age': age,
                    'attendance_lines': attendance_line,
                    'leave_lines': leaves,
                    'expense_lines': expense
                }
                employee[0].update(data)
            return employee
        else:
            return False


    @api.model
    def get_upcoming(self):
        """It returns upcoming events, announcements, birthdays, and work anniversaries"""
        cr = self._cr
        uid = request.session.uid
        employee = self.env['hr.employee'].search([('user_id', '=', uid)], limit=1)
        today = fields.Date.today()

        # Fetch employees with birthdays
        birthday_employees = self.env['hr.employee'].search_read(
            [('birthday', '!=', False)],  # Ensure birthday is not null
            fields=['id', 'name', 'birthday']
        )

        upcoming_birthdays = []  # Initialize list to store processed data

        # Process each employee's birthday
        for emp in birthday_employees:
            birthday = emp['birthday']  # Employee's birthday

            # Convert the birthday to this year's date
            emp_birthday_this_year = birthday.replace(year=today.year)

            # If the birthday has already passed this year, move it to next year
            if emp_birthday_this_year < today:
                emp_birthday_this_year = emp_birthday_this_year.replace(year=today.year + 1)

            # Calculate the days left for the birthday
            days_left = (emp_birthday_this_year - today).days

            # Add only employees whose birthdays are within the next 5 days
            if 0 <= days_left <= 5:
                emp['is_birthday'] = (days_left == 0)  # Mark if today is their birthday
                emp['days'] = days_left
                emp['next_birthday'] = emp_birthday_this_year
                upcoming_birthdays.append(emp)

        # Sort the employees by the next birthday (if not already sorted)
        birthday_employees.sort(key=lambda emp: (emp['birthday'].month, emp['birthday'].day))


        # Limit to 5 results
        upcoming_birthdays = upcoming_birthdays[:5]



        # Fetch work anniversaries
        work_anniversaries = []
        employees = self.env['hr.employee'].search(
            [('joining_date', '!=', False)],
            order='joining_date ASC'
        )

        for emp in employees:
            joining_date = fields.Date.from_string(emp.joining_date)
            next_anniversary = joining_date.replace(year=today.year)

            # If the anniversary date has already passed this year, update it to the next year
            if next_anniversary < today:
                next_anniversary = next_anniversary.replace(year=today.year + 1)

            days_until_anniversary = (next_anniversary - today).days

            # Include anniversaries only within the next 5 days
            if 0 < days_until_anniversary <= 5:
                work_anniversaries.append({
                    'id': emp.id,
                    'name': emp.name,
                    'anniversary_date': str(next_anniversary),
                    'is_anniversary': days_until_anniversary == 0,
                    'days': days_until_anniversary,
                })

                # Sort the work anniversaries list by the anniversary date (ascending order)
                work_anniversaries = sorted(work_anniversaries, key=lambda x: x['anniversary_date'])

                # Optional: Limit the results to the top 5 upcoming anniversaries
                work_anniversaries = work_anniversaries[:7]

        # Fetch announcements
        announcements = self.env['hr.announcement'].search_read(
            [('state', '=', 'approved'),
             ('date_start', '<=', fields.Date.today()),
             '|', ('is_announcement', '=', True),
             '|', '|',
             ('employee_ids', 'in', employee.id),
             ('department_ids', 'in', employee.department_id.id),
             ('position_ids', 'in', employee.job_id.id),
             ], fields=['announcement_reason', 'date_start', 'date_end'])

        # Fetch upcoming events
        lang = self.env.context.get('lang', 'en_US')
        cr.execute(f"""
                     SELECT e.id,
                     COALESCE(e.name ->> '{lang}', e.name ->> 'en_US', e.name::text) as name,
                     e.date_begin,
                     e.date_end,
                     rp.name as location
                     FROM event_event e
                     INNER JOIN res_partner rp
                     ON e.address_id = rp.id
                     WHERE e.date_begin >= NOW()
                     ORDER BY e.date_begin
                """)
        events = cr.fetchall()


        return {
            'birthday': birthday_employees,
            'event': events,
            'announcement': announcements,
            'employee_work_anniversary': work_anniversaries,
        }


    @api.model
    def get_dept_employee(self):
        """Retrieve the details of employees in each department."""
        cr = self._cr
        cr.execute("""select department_id, hr_department.name,count(*)
        from hr_employee join hr_department on 
        hr_department.id=hr_employee.department_id
        group by hr_employee.department_id,hr_department.name""")
        dat = cr.fetchall()
        data = []
        for i in range(0, len(dat)):
            data.append(
                {'label': list(dat[i][1].values())[0], 'value': dat[i][2]})
        return data

    @api.model
    def get_department_leave(self):
        """Returns the department monthly wise leave information"""
        month_list = []
        graph_result = []
        for i in range(5, -1, -1):
            last_month = datetime.now() - relativedelta(months=i)
            text = format(last_month, '%B %Y')
            month_list.append(text)
        self.env.cr.execute(
            """select id, name from hr_department where active=True """)
        departments = self.env.cr.dictfetchall()
        department_list = [list(x['name'].values())[0] for x in departments]
        for month in month_list:
            leave = {}
            for dept in departments:
                leave[list(dept['name'].values())[0]] = 0
            vals = {
                'l_month': month,
                'leave': leave
            }
            graph_result.append(vals)
        sql = """
        SELECT h.id, h.employee_id,h.department_id
             , extract('month' FROM y)::int AS leave_month
             , to_char(y, 'Month YYYY') as month_year
             , GREATEST(y                    , h.date_from) AS date_from
             , LEAST   (y + interval '1 month', h.date_to)   AS date_to
        FROM  (select * from hr_leave where state = 'validate') h
             , generate_series(date_trunc('month', date_from::timestamp)
                             , date_trunc('month', date_to::timestamp)
                             , interval '1 month') y
        where date_trunc('month', GREATEST(y , h.date_from)) >= 
        date_trunc('month', now()) - interval '6 month' and
        date_trunc('month', GREATEST(y , h.date_from)) <= 
        date_trunc('month', now())
        and h.department_id is not null
        """
        self.env.cr.execute(sql)
        results = self.env.cr.dictfetchall()
        leave_lines = []
        for line in results:
            employee = self.browse(line['employee_id'])
            from_dt = fields.Datetime.from_string(line['date_from'])
            to_dt = fields.Datetime.from_string(line['date_to'])
            days = employee.get_work_days_dashboard(from_dt, to_dt)
            line['days'] = days
            vals = {
                'department': line['department_id'],
                'l_month': line['month_year'],
                'days': days
            }
            leave_lines.append(vals)
        if leave_lines:
            df = pd.DataFrame(leave_lines)
            rf = df.groupby(['l_month', 'department']).sum()
            result_lines = rf.to_dict('index')
            for month in month_list:
                for line in result_lines:
                    if month.replace(' ', '') == line[0].replace(' ', ''):
                        match = list(filter(lambda d: d['l_month'] in [month],
                                            graph_result))[0]['leave']
                        dept_name = self.env['hr.department'].browse(
                            line[1]).name
                        if match:
                            match[dept_name] = result_lines[line]['days']
        for result in graph_result:
            result['l_month'] = result['l_month'].split(' ')[:1][0].strip()[
                                :3] + " " + \
                                result['l_month'].split(' ')[1:2][0]

        return graph_result, department_list

    def get_work_days_dashboard(self, from_datetime, to_datetime,
                                compute_leaves=False, calendar=None,
                                domain=None):
        """Calculate employee worked hours/day details"""
        resource = self.resource_id
        calendar = calendar or self.resource_calendar_id
        if not from_datetime.tzinfo:
            from_datetime = from_datetime.replace(tzinfo=utc)
        if not to_datetime.tzinfo:
            to_datetime = to_datetime.replace(tzinfo=utc)
        from_full = from_datetime - timedelta(days=1)
        to_full = to_datetime + timedelta(days=1)
        intervals = calendar._attendance_intervals_batch(from_full, to_full,
                                                         resource)
        day_total = defaultdict(float)
        for start, stop, meta in intervals[resource.id]:
            day_total[start.date()] += (stop - start).total_seconds() / 3600
        if compute_leaves:
            intervals = calendar._work_intervals_batch(from_datetime,
                                                       to_datetime, resource,
                                                       domain)
        else:
            intervals = calendar._attendance_intervals_batch(from_datetime,
                                                             to_datetime,
                                                             resource)
        day_hours = defaultdict(float)
        for start, stop, meta in intervals[resource.id]:
            day_hours[start.date()] += (stop - start).total_seconds() / 3600
        days = sum(
            float_utils.round(ROUNDING_FACTOR * day_hours[day] / day_total[
                day]) / ROUNDING_FACTOR
            for day in day_hours
        )
        return days

    @api.model
    def employee_leave_trend(self):
        """Logged employee monthly wise leave information"""
        leave_lines = []
        month_list = []
        graph_result = []
        for i in range(5, -1, -1):
            last_month = datetime.now() - relativedelta(months=i)
            text = format(last_month, '%B %Y')
            month_list.append(text)
        uid = request.session.uid
        employee = self.env['hr.employee'].sudo().search_read(
            [('user_id', '=', uid)], limit=1)
        for month in month_list:
            vals = {
                'l_month': month,
                'leave': 0
            }
            graph_result.append(vals)
        sql = """
                SELECT h.id, h.employee_id
                     , extract('month' FROM y)::int AS leave_month
                     , to_char(y, 'Month YYYY') as month_year
                     , GREATEST(y                    , h.date_from) AS date_from
                     , LEAST   (y + interval '1 month', h.date_to)   AS date_to
                FROM  (select * from hr_leave where state = 'validate') h
                     , generate_series(date_trunc('month', date_from::timestamp)
                                     , date_trunc('month', date_to::timestamp)
                                     , interval '1 month') y
                where date_trunc('month', GREATEST(y , h.date_from)) >= 
                date_trunc('month', now()) - interval '6 month' and
                date_trunc('month', GREATEST(y , h.date_from)) <= 
                date_trunc('month', now()) and h.employee_id = %s """
        self.env.cr.execute(sql, (employee[0]['id'],))
        results = self.env.cr.dictfetchall()
        for line in results:
            employee = self.browse(line['employee_id'])
            from_dt = fields.Datetime.from_string(line['date_from'])
            to_dt = fields.Datetime.from_string(line['date_to'])
            days = employee.get_work_days_dashboard(from_dt, to_dt)
            line['days'] = days
            vals = {
                'l_month': line['month_year'],
                'days': days
            }
            leave_lines.append(vals)
        if leave_lines:
            df = pd.DataFrame(leave_lines)
            rf = df.groupby(['l_month']).sum()
            result_lines = rf.to_dict('index')
            for line in result_lines:
                match = list(filter(
                    lambda d: d['l_month'].replace(' ', '') == line.replace(' ',
                                                                            ''),
                    graph_result))
                if match:
                    match[0]['leave'] = result_lines[line]['days']
        for result in graph_result:
            result['l_month'] = result['l_month'].split(' ')[:1][0].strip()[
                                :3] + " " + \
                                result['l_month'].split(' ')[1:2][0]
        return graph_result

    @api.model
    def join_resign_trends(self):
        """Returns join/resign details of departments"""
        cr = self._cr
        month_list = []
        join_trend = []
        resign_trend = []
        for i in range(11, -1, -1):
            last_month = datetime.now() - relativedelta(months=i)
            text = format(last_month, '%B %Y')
            month_list.append(text)
        for month in month_list:
            vals = {
                'l_month': month,
                'count': 0
            }
            join_trend.append(vals)
        for month in month_list:
            vals = {
                'l_month': month,
                'count': 0
            }
            resign_trend.append(vals)
        cr.execute('''select to_char(joining_date, 'Month YYYY') as l_month,
         count(id) from hr_employee
        WHERE joining_date BETWEEN CURRENT_DATE - INTERVAL '12 months'
        AND CURRENT_DATE + interval '1 month - 1 day'
        group by l_month''')
        join_data = cr.fetchall()
        cr.execute('''select to_char(resign_date, 'Month YYYY') as l_month,
         count(id) from hr_employee
        WHERE resign_date BETWEEN CURRENT_DATE - INTERVAL '12 months'
        AND CURRENT_DATE + interval '1 month - 1 day'
        group by l_month;''')
        resign_data = cr.fetchall()

        for line in join_data:
            match = list(filter(
                lambda d: d['l_month'].replace(' ', '') == line[0].replace(' ',
                                                                           ''),
                join_trend))
            if match:
                match[0]['count'] = line[1]
        for line in resign_data:
            match = list(filter(
                lambda d: d['l_month'].replace(' ', '') == line[0].replace(' ',
                                                                           ''),
                resign_trend))
            if match:
                match[0]['count'] = line[1]
        for join in join_trend:
            join['l_month'] = join['l_month'].split(' ')[:1][0].strip()[:3]
        for resign in resign_trend:
            resign['l_month'] = resign['l_month'].split(' ')[:1][0].strip()[:3]
        graph_result = [{
            'name': 'Join',
            'values': join_trend
        }, {
            'name': 'Resign',
            'values': resign_trend
        }]
        return graph_result


    @api.model
    def get_employee_skill(self):
        """ Retrieve employee skills and its progress"""
        employee = self.env['hr.employee'].sudo().search(
            [('user_id', '=', request.session.uid)], limit=1)
        skills = self.env['hr.employee.skill'].sudo().search_read(
            [('employee_id', '=', employee.id)])
        dataset = []
        for rec in skills:
            vals = {
                'skills': rec['skill_type_id'][1] + '-' + rec['skill_id'][1],
                'progress': rec['level_progress']
            }
            dataset.append(vals)
        return dataset