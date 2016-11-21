from django.core.mail import EmailMultiAlternatives
import re


class CompanyEmail:

    from_email = 'kwasi.innovate@gmail.com'
    to_email = 'kwasi.adu@gmail.com'
    subject = 'Hi'
    html_content = ""

    def remove_html_tags(self, content):
        """Remove html tags from a string"""
        reg_expr = re.compile('<.*?>')
        return re.sub(reg_expr, '', content)

    def __init__(self, from_email=from_email,
                 to_email=to_email, subject=subject, html_content=html_content):

        self.from_email = from_email
        self.to_email = to_email
        self.subject = subject
        self.html_content = html_content
        self.text_content = self.remove_html_tags(html_content)

    def send(self):

        msg = EmailMultiAlternatives(self.subject, self.text_content, self.from_email,
                                     [self.to_email])
        msg.attach_alternative(self.html_content, "text/html")
        msg.send()


class NewTalentEmail(CompanyEmail):

    def __init__(self):

        self.subject = 'Welcome'
        self.html_content = """
    <p>Thanks for signing up with us</p>
    """
        self.text_content = self.remove_html_tags(self.html_content)


class NewContactNotification(CompanyEmail):

    def __init__(self, contact):

        self.contact = contact
        self.subject = "New Innovate Contact"
        self.to_email = "kwasi.adu@gmail.com"
        self.html_content = """
    <p style='color:red'>A new company request has been entered</p><ul>
    """

        for k, v in self.contact.iteritems():
            html_line = "<li style='display: block'>" + "<strong>" + k + ":</strong> " \
                        + v + "</li>"
            self.html_content += html_line

        self.html_content += "</ul>"
        self.text_content = self.remove_html_tags(self.html_content)


class NewContactEmail(CompanyEmail):

    def __init__(self, contact):
        contact_name = contact['name']
        self.subject = "Welcome"
        self.to_email = contact['email']
        self.html_content = """
            <p>Hi %(contact_name)s,</p>
            <p> Thank you for choosing us. We shall get back to you within 24
            hrs
            </p>

            """ % locals()

        self.text_content = self.remove_html_tags(self.html_content)