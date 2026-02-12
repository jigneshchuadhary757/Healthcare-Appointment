# Copyright (c) 2026, jignesh chaudhary and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime, timedelta
from frappe.utils import getdate, get_time

class PatientAppointment(Document):
	pass


@frappe.whitelist()
def calculate_end_time(service, appointment_time):
    if not service or not appointment_time:
        return None

    service_doc = frappe.get_doc("Healthcare Service", service)

    duration = service_doc.duration_minutes
    start_time = datetime.strptime(appointment_time, "%H:%M:%S")

    end_time = start_time + timedelta(minutes=duration)

    return end_time.time().strftime("%H:%M:%S")

@frappe.whitelist()
def get_service_price(service):
    if not service:
        return 0

    service_doc = frappe.get_doc("Healthcare Service", service)
    return service_doc.price

