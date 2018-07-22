import settings
from django.template import loader
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives


def email_send(
    request,
    template_path,
    to_address,
    from_address=settings.DEFAULT_FROM_EMAIL,
    context={},
    use_https=False,
):
    try:
        current_origin = get_current_site(request)
        domain = current_origin.domain
    except AttributeError:
        domain = "sandwhichi.com"
        use_https = True

    # Set Context
    default_context = {
        'domain': domain,
        'protocol': 'https' if use_https else 'http',
    }
    new_context = default_context.copy()
    new_context.update(context)
    context = new_context

    # Render Email Template
    subject_template_path = template_path + '_subject.txt'
    text_template_path = template_path + '.txt'
    html_template_path = template_path + '.html'

    subject_template = loader.render_to_string(subject_template_path, context)
    text_template = loader.render_to_string(text_template_path, context)
    html_template = loader.render_to_string(html_template_path, context)

    email_subject = ''.join(subject_template.splitlines()) # Email subject *must not* contain newlines

    email = EmailMultiAlternatives(email_subject, text_template, from_address, [to_address])
    email.attach_alternative(html_template, 'text/html')

    try:
        return email.send(fail_silently=True)
    except IndexError:
        return 0
