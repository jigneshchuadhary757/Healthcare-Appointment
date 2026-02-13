# Copyright (c) 2026, jignesh chaudhary and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime, timedelta, time
from frappe.utils import getdate, get_time, nowdate
from frappe import _
class PatientAppointment(Document):
     
	def validate(self):
		self.set_total_amount()
		self.validate_appointment_time_overlap()
		self.validate_working_hours()

	def on_update(self):
		if self.has_value_changed("status") and self.status == "Completed":
			frappe.logger().info(
				f"Appointment {self.name} marked as Completed."
			)

	def after_insert(self):
		self.create_paid_invoice_from_web()

	

	def set_total_amount(self):
		if not self.service:
			return
		
		service_price = get_service_price(self.service)

		if not service_price:
			frappe.throw(_("Price is not set as service is not set there in the appointment."))

		self.total_amount = service_price





	def validate_appointment_time_overlap(self):
		if not self.appointment_time or not self.estimated_end_time:
			return

		existing_appointments = frappe.get_all(
			"Patient Appointment",
			filters={
				"patient_contact": self.patient_contact,
				"appointment_date": self.appointment_date,
				"status": "Scheduled",
				"name": ["!=", self.name]
			},
			fields=["appointment_time", "estimated_end_time"]
		)

		new_start = get_time(self.appointment_time)
		new_end = get_time(self.estimated_end_time)

		for appt in existing_appointments:
			existing_start = get_time(appt.appointment_time)
			existing_end = get_time(appt.estimated_end_time)

			if new_start < existing_end and new_end > existing_start:
				frappe.throw(
					_("This appointment overlaps with an existing Scheduled appointment for Patient Contact No {0} on {1}. Please select a different time.")
					.format(self.patient_contact, self.appointment_date),
					frappe.ValidationError
				)



	def validate_working_hours(self):

		if not self.appointment_time:
			return

		appointment_time = datetime.strptime(
			str(self.appointment_time),
			"%H:%M:%S"
		).time()

		clinic_start = time(9, 0, 0)   
		clinic_end = time(17, 0, 0)    

		if not (clinic_start <= appointment_time <= clinic_end):
			frappe.throw(
					_("Appointment time must be within clinic working hours (09:00 AM to 05:00 PM)."),
					frappe.ValidationError
				)
			




	def create_paid_invoice_from_web(self):

		companies = frappe.get_all("Company", pluck="name")
		if not companies:
			frappe.throw("No Company Found.")
		
		company = companies[0]
		company_currency = frappe.get_cached_value("Company", company, "default_currency")

		service_price = frappe.db.get_value(
			"Healthcare Service",
			self.service,
			"price"
		)

		invoice = frappe.get_doc({
			"doctype": "Sales Invoice",
			"company": company,
			"customer": "Walk-in Customer",
			"currency": company_currency,
			"conversion_rate": 1,
			"selling_price_list": "Standard Selling",
			"price_list_currency": company_currency,
			"plc_conversion_rate": 1,
			"posting_date": nowdate(),
			"set_posting_time": 1,
			"items": [
				{
					"item_code": "Healthcare Service",
					"qty": 1,
					"rate": service_price
				}
			]
		})

		invoice.insert()
		invoice.submit()
		cash_account = frappe.get_value(
			"Account",
			{
				"account_type": "Cash",
				"company": company,
				"is_group": 0
			},
			"name"
		)

		account_currency = frappe.get_value("Account", cash_account, "account_currency")

		payment = frappe.get_doc({
			"doctype": "Payment Entry",
			"payment_type": "Receive",
			"company": company,
			"party_type": "Customer",
			"party": "Walk-in Customer",
			"posting_date": nowdate(),
			"mode_of_payment": "Cash",
			"paid_amount": invoice.grand_total,
			"received_amount": invoice.grand_total,
			"source_exchange_rate": 1,
			"target_exchange_rate": 1,
			"paid_to": cash_account,
    		"paid_to_account_currency": account_currency,
			"references": [
				{
					"reference_doctype": "Sales Invoice",
					"reference_name": invoice.name,
					"allocated_amount": invoice.grand_total
				}
			]
		})

		payment.insert()
		payment.submit()

		self.sales_invoice = invoice.name
		self.total_amount = invoice.grand_total
		self.status = "Scheduled"

		self.db_update()








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

