from odoo import models, fields, api
from email.message import EmailMessage
import smtplib
import os
from datetime import datetime, timedelta
from datetime import date
from pytz import timezone
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from io import BytesIO
import base64
import random



class HREmployee(models.Model):
    _inherit = 'hr.employee'

    user_id = fields.Many2one('res.users', string="Related User", required=True)


class VisitorRecord(models.Model):
    _name = 'visitor.record'
    _description = 'Visitor Record'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'host'

    name = fields.Char(string="Visitor Name", required=True)
    email = fields.Char(string="Email", required=True)
    phone = fields.Char(string="Phone")
    station_id = fields.Many2one('visitor.station', string="Station", required=True)
    visit_date = fields.Datetime(string="Visit Date", default=fields.Datetime.now)
    purpose = fields.Char(string="Purpose")
    host = fields.Many2one('hr.employee', string="To Meet", required=True)
    aadhar_id = fields.Char(string="Aadhar ID")
    place = fields.Char(string="Place")

    # security_name = fields.Many2one('hr.employee',string="Security Guard",
    #                                 related='station_id.security_name')

    security_name = fields.Many2one('hr.employee', string="Security Guard", related='station_id.security_name',
                                    )

    state = fields.Selection([
        ('draft', 'Draft'),
        ('notified', 'Notified'),
        ('approved', 'Approved'),
        ('refused', 'Refused'),
        ('checked_in', 'Checked In'),
        ('checked_out', 'Checked Out')
    ], string="Status", default='draft', tracking=True)

    check_in_time = fields.Datetime(string="Check-In Time", readonly=True)
    check_out_time = fields.Datetime(string="Check-Out Time", readonly=True)

    @api.model
    def get_todays_visitors(self):
        """Return visitor records for today's date, handling timezones correctly."""
        # User's timezone (default to UTC if not set)
        user_tz = self.env.user.tz or 'UTC'
        local_tz = timezone(user_tz)

        # Get the current date in the user's timezone
        local_now = datetime.now(local_tz)
        start_of_day = datetime.combine(local_now.date(), datetime.min.time())
        end_of_day = datetime.combine(local_now.date(), datetime.max.time())

        # Convert the local start and end of the day to UTC for database filtering
        start_of_day_utc = local_tz.localize(start_of_day).astimezone(UTC)
        end_of_day_utc = local_tz.localize(end_of_day).astimezone(UTC)

        # ORM search using UTC timestamps
        visitors = self.search([
            ('visit_date', '>=', start_of_day_utc),
            ('visit_date', '<=', end_of_day_utc)
        ])

        # Return the visitors found
        return visitors

    # def action_approve(self):
    #     """Approve the visitor record."""
    #     for record in self:
    #         if record.state == 'notified':
    #             record.state = 'approved'

    # def action_generate_visitor_badge(self):
    #     """Generate and download a visitor badge."""
    #     for record in self:
    #         # Create a PDF in memory
    #         buffer = BytesIO()
    #         c = canvas.Canvas(buffer, pagesize=letter)
    #         c.drawString(100, 750, f"Visitor Badge")
    #         c.drawString(100, 730, f"Name: {record.name}")
    #         c.drawString(100, 710, f"Date: {record.visit_date.strftime('%Y-%m-%d')}")
    #         c.drawString(100, 690, f"Host: {record.host.name}")
    #         c.drawString(100, 670, f"Station: {record.station_id.name}")
    #         c.save()
    #
    #         # Encode the PDF for download
    #         buffer.seek(0)
    #         pdf_data = buffer.read()
    #         buffer.close()
    #
    #         # Create an attachment
    #         attachment = self.env['ir.attachment'].create({
    #             'name': f'Visitor_Badge_{record.name}.pdf',
    #             'type': 'binary',
    #             'datas': base64.b64encode(pdf_data),
    #             'res_model': self._name,
    #             'res_id': record.id,
    #             'mimetype': 'application/pdf',
    #         })
    #
    #         # Trigger a download for the badge
    #         return {
    #             'type': 'ir.actions.act_url',
    #             'url': f'/web/content/{attachment.id}?download=true',
    #             'target': 'new',
    #         }

    # def action_generate_visitor_badge(self):
    #     """Generate and download a visitor badge with ID card size."""
    #     for record in self:
    #         # Define ID card size in points (3.5 x 2 inches)
    #         width = 252
    #         height = 144
    #
    #         # Create a PDF in memory with ID card size
    #         buffer = BytesIO()
    #         c = canvas.Canvas(buffer, pagesize=(width, height))
    #
    #         # Add Border
    #         c.setStrokeColor(colors.black)
    #         c.setLineWidth(2)
    #         c.rect(5, 5, width - 10, height - 10)  # x, y, width, height with margin
    #
    #         # Title with bold text
    #         c.setFont("Helvetica-Bold", 14)
    #         c.drawString(90, 120, "Visitor Badge")
    #
    #         # Add Visitor Details with Bold Text for Labels
    #         c.setFont("Helvetica-Bold", 10)
    #         c.drawString(10, 100, "Name: ")
    #         c.setFont("Helvetica", 10)
    #         c.drawString(60, 100, f"{record.name}")
    #
    #         c.setFont("Helvetica-Bold", 10)
    #         c.drawString(10, 85, "Date: ")
    #         c.setFont("Helvetica", 10)
    #         c.drawString(60, 85, f"{record.visit_date.strftime('%Y-%m-%d')}")
    #
    #         c.setFont("Helvetica-Bold", 10)
    #         c.drawString(10, 70, "Host: ")
    #         c.setFont("Helvetica", 10)
    #         c.drawString(60, 70, f"{record.host.name}")
    #
    #         c.setFont("Helvetica-Bold", 10)
    #         c.drawString(10, 55, "Station: ")
    #         c.setFont("Helvetica", 10)
    #         c.drawString(60, 55, f"{record.station_id.name}")
    #
    #         # Draw a simple "icon" (circle)
    #         c.setFillColor(colors.blue)
    #         c.circle(230, 120, 6, fill=1)  # Circle with center at (230, 120) and radius 6
    #
    #         # Draw a random "barcode" (random vertical lines) at the bottom
    #         c.setStrokeColor(colors.black)
    #         barcode_y = 10
    #         for _ in range(20):
    #             barcode_x = random.randint(10, 240)
    #             c.setLineWidth(random.randint(1, 3))
    #             c.line(barcode_x, barcode_y, barcode_x, barcode_y + 20)
    #
    #         c.save()
    #
    #         # Encode the PDF for download
    #         buffer.seek(0)
    #         pdf_data = buffer.read()
    #         buffer.close()
    #
    #         # Create an attachment
    #         attachment = self.env['ir.attachment'].create({
    #             'name': f'Visitor_Badge_{record.name}.pdf',
    #             'type': 'binary',
    #             'datas': base64.b64encode(pdf_data),
    #             'res_model': self._name,
    #             'res_id': record.id,
    #             'mimetype': 'application/pdf',
    #         })
    #
    #         # Trigger a download for the badge
    #         return {
    #             'type': 'ir.actions.act_url',
    #             'url': f'/web/content/{attachment.id}?download=true',
    #             'target': 'new',
    #         }

    def action_approve(self):
        """Approve the visitor record and notify the security guard."""
        for record in self:
            if record.state == 'notified':
                # Update visitor state to 'approved'
                record.state = 'approved'

                # Send a notification to the security guard using activity_schedule
                if record.security_name:
                    record.activity_schedule(
                        activity_type_id=self.env.ref('mail.mail_activity_data_todo').id,  # To-Do activity
                        summary="Visitor Approved",
                        note=f"Visitor '{record.name}' has been approved and is scheduled to meet {record.host.name}.",
                        user_id=record.security_name.user_id.id,  # Security guard's user_id
                        date_deadline=fields.Date.today() + timedelta(days=3)  # Set a 3-day deadline for action
                    )

                    subject = f"Notification: Visitor Approved"
                    body = f"""
                                <p>Dear {record.security_name.name}</p>
                               
                                <p> <h1>Visitor :{record.name} </h1> has been approved to by the host {record.host.name}</p>
                                <p>Kindly Admit the visitor</p>
                                <p>Thank you for your attention to this matter.</p>
                                <p>Best regards,<br>
                                                                    


                                                                """

                    # Create and send the email
                    mail = self.env['mail.mail'].create({
                        'subject': subject,
                        'body_html': body,
                        'email_to': record.security_name.email,
                    })
                    mail.send()




    # def action_refuse(self):
    #     """Refuse the visitor record."""
    #     for record in self:
    #         if record.state == 'notified':
    #             record.state = 'refused'

    def action_refuse(self):
        """Refuse the visitor record and notify the security guard."""
        for record in self:
            if record.state == 'notified':
                # Update visitor state to 'refused'
                record.state = 'refused'

                # Send a notification to the security guard using activity_schedule
                if record.security_name:
                    record.activity_schedule(
                        activity_type_id=self.env.ref('mail.mail_activity_data_todo').id,  # To-Do activity
                        summary="Visitor Refused",
                        note=f"Visitor '{record.name}' has been refused entry by the host {record.host.name}. Please take further action.",
                        user_id=record.security_name.user_id.id,  # Security guard's user_id
                        date_deadline=fields.Date.today() + timedelta(days=3)  # Set a 3-day deadline for action
                    )

                    subject = f"Notification: Visitor Refused"
                    body = f"""
                                               <p>Dear {record.security_name.name}</p>
                                               <p><h1>Visitor :{record.name} </h1> has been refused by the host {record.host.name}</p>
                                              
                                               <p>Thank you for your attention to this matter.</p>
                                               <p>Best regards,<br>



                                                                               """

                    # Create and send the email
                    mail = self.env['mail.mail'].create({
                        'subject': subject,
                        'body_html': body,
                        'email_to': record.security_name.email,
                    })
                    mail.send()

    def action_check_in(self):
        """Set Check-In Time and notify host."""
        for record in self:
            if record.state == 'approved' and not record.check_in_time:
                record.check_in_time = datetime.now()
                record.state = 'checked_in'

    def action_check_out(self):
        """Set Check-Out Time."""
        for record in self:
            if record.state == 'checked_in' and not record.check_out_time:
                record.check_out_time = datetime.now()
                record.state = 'checked_out'


    def action_notify_host(self):
        """Notify the host when the visitor is confirmed."""
        for record in self:
            # Confirm the visitor record by changing the state
            record.state = 'notified'  # or whatever state you need

            # Send a notification to the host using activity_schedule
            if record.host:
                record.activity_schedule(
                    activity_type_id=self.env.ref('mail.mail_activity_data_todo').id,  # To-Do activity
                    summary="Visitor Confirmed",
                    note=f"Visitor '{record.name}' is confirmed and scheduled to meet you.",
                    user_id=record.host.user_id.id,  # Assuming `host` is related to `hr.employee` which has `user_id`
                    date_deadline=fields.Date.today() + timedelta(days=3)  # Set a 3-day deadline for action
                )

    def send_visitor_notification(self):
        """Send an email and notify the host when the visitor is approved or checked in."""
        for record in self:
            subject = f"Notification: Visitor Arrived"
            body = f"""
                                    <p>Dear {record.host.name}</p>
                                    <p>We would like to inform you that <strong>{record.name}</strong> has arrived at the company and is awaiting your approval to proceed with the meeting.</p>

                                    <p>Kindly review the visitor's details and approve or decline the meeting request as appropriate.</p>
                                    
                                    
                                    <p>Thank you for your attention to this matter.</p>
                                    
                                    <p>Best regards,<br>
                                    
                                   
                                """

            # Create and send the email
            mail = self.env['mail.mail'].create({
                'subject': subject,
                'body_html': body,
                'email_to': record.host.email,
            })
            mail.send()
            record.state = 'notified'

            # Schedule an activity for the host
            if record.host and record.host.user_id:
                try:
                    record.activity_schedule(
                        activity_type_id=self.env.ref('mail.mail_activity_data_todo').id,  # To-Do activity
                        summary="Visitor Confirmed",
                        note=f"Visitor '{record.name}' is confirmed and scheduled to meet you.",
                        user_id=record.host.user_id.id,
                        # Assuming `host` is related to `hr.employee` which has `user_id`
                        date_deadline=fields.Date.today() + timedelta(days=3)  # Set a 3-day deadline for action
                    )
                except Exception as e:
                    # Log failure to schedule activity
                    log_message = f"{datetime.now()} - ERROR: Failed to schedule activity for host '{record.host.work_email}' for visitor '{record.name}'. Error: {str(e)}\n"
                    log_file.write(log_message)
            pass

    # def send_visitor_notification(self):
    #     """Send an email and notify the host when the visitor is approved or checked in."""
    #     for record in self:
    #         # Log file path for notifications
    #         log_file_path = '/home/user/odoo18/visitor_notifications.log'
    #
    #         # Ensure the log directory exists
    #         log_directory = os.path.dirname(log_file_path)
    #         if not os.path.exists(log_directory):
    #             os.makedirs(log_directory)
    #
    #         # Open log file in append mode
    #         with open(log_file_path, 'a') as log_file:
    #             # Check if host has an email address
    #             if record.host and record.host.work_email:
    #                 # Ensure 'purpose' is a string
    #                 if not isinstance(record.purpose, str):
    #                     record.purpose = str(record.purpose) if record.purpose else "(No purpose provided)"
    #
    #                 # Compose email content
    #                 email_content = f"Visitor Details:\n"
    #                 email_content += f"Name: {record.name}\n"
    #                 email_content += f"Phone: {record.phone}\n"
    #                 email_content += f"Purpose: {record.purpose}\n"
    #                 email_content += f"Visit Date: {record.visit_date}\n"
    #                 email_content += f"Visitor's Email: {record.email}\n"
    #                 email_content += f"Host's Email: {record.host.work_email}\n"
    #
    #                 # Compose the email
    #                 email = EmailMessage()
    #                 email['From'] = 'admin@company.com'  # Replace with an actual sender email address
    #                 email['To'] = record.host.work_email  # Host's email
    #                 email['Subject'] = f"Visitor Notification: {record.name} visiting at {record.visit_date}"
    #                 email.set_content(email_content)
    #
    #                 try:
    #                     # Simulate sending the email (using local SMTP for testing)
    #                     smtp_host = 'localhost'  # Local SMTP server address
    #                     smtp_port = 1025  # Local SMTP server port (adjust for your server)
    #
    #                     with smtplib.SMTP(smtp_host, smtp_port) as server:
    #                         server.send_message(email)
    #
    #                     # Log success
    #                     log_message = f"{datetime.now()} - SUCCESS: Email sent to {record.host.work_email} for visitor '{record.name}'\n"
    #                     log_file.write(log_message)
    #
    #                 except Exception as e:
    #                     # Log failure
    #                     log_message = f"{datetime.now()} - ERROR: Failed to send email to {record.host.work_email} for visitor '{record.name}'. Error: {str(e)}\n"
    #                     log_file.write(log_message)
    #
    #             # Schedule an activity for the host
    #             if record.host and record.host.user_id:
    #                 try:
    #                     record.activity_schedule(
    #                         activity_type_id=self.env.ref('mail.mail_activity_data_todo').id,  # To-Do activity
    #                         summary="Visitor Confirmed",
    #                         note=f"Visitor '{record.name}' is confirmed and scheduled to meet you.",
    #                         user_id=record.host.user_id.id,
    #                         # Assuming `host` is related to `hr.employee` which has `user_id`
    #                         date_deadline=fields.Date.today() + timedelta(days=3)  # Set a 3-day deadline for action
    #                     )
    #                 except Exception as e:
    #                     # Log failure to schedule activity
    #                     log_message = f"{datetime.now()} - ERROR: Failed to schedule activity for host '{record.host.work_email}' for visitor '{record.name}'. Error: {str(e)}\n"
    #                     log_file.write(log_message)
    #
    #             # Update state to 'notified' after sending the email and scheduling the activity
    #             record.state = 'notified'
