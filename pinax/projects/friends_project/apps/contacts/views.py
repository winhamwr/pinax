from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from django.contrib.auth.decorators import login_required

from contacts_import.models import TransientContact
from emailconfirmation.models import EmailAddress

from contacts.models import Contact


@login_required
def contacts(request, template_name="contacts/contacts.html"):
    
    contacts = request.user.contacts.all()
    
    ctx = {
        "contacts": contacts,
    }
    
    return render_to_response(template_name, RequestContext(request, ctx))


def import_callback(request, selected):
    """
    This function is called by django-contacts-import (configured via
    CONTACTS_IMPORT_CALLBACK) once an import is done and the user has selected
    contacts they want to use.
    """
    
    imported_contacts = TransientContact.objects.filter(pk__in=selected)
    
    # look for on site users of the selected contacts
    on_site_users = {}
    email_addresses = EmailAddress.objects.filter(
        email__in = [c.email for c in imported_contacts],
        verified = True
    ).select_related("user").values("email", "user")
    for email_address in email_addresses:
        on_site_users[email_address["email"]] = email_address["user"]
    
    for imported_contact in imported_contacts:
        contact = Contact(
            owner = request.user,
            name = imported_contact.name,
            email = imported_contact.email,
        )
        contact.user_id = on_site_users.get(imported_contact.email)
        contact.save()
    
    return HttpResponseRedirect(reverse("contacts"))