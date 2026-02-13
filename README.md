# Healthcare-Appointment

This is a custom Frappe application developed as part of a technical assignment.

The system allows public users to book a Patient Appointment via a Web Form.  
Upon successful booking:

- Appointment is validated (working hours & overlap check)
- Sales Invoice is automatically created
- Payment Entry is automatically created
- Appointment is marked as Confirmed

The system ensures that appointments created via the Web Form are treated as paid bookings.

---

#  Implemented Features

##  Public Appointment Booking
- Public Web Form for booking Patient Appointments
- Validation for:
  - Clinic Working Hours (09:00 AM – 05:00 PM)
  - Appointment Time Overlap Prevention
- Automatic calculation of total consultation amount
- Automatic creation of:
  - Sales Invoice (Submitted)
  - Payment Entry (Submitted)
- Appointment automatically marked as Confirmed after payment
- Client Script enhancements
- Fixtures included for Web Form and Client Script
##  Fixtures Included
The following are exported as fixtures:

- Client Script (Patient Appointment)
- Web Form (Patient Appointment)

These are automatically installed when the app is installed.

---

#  Setup Instructions

## Step 1: Install Frappe Bench (If Not Installed)

Follow official documentation:

https://frappeframework.com/docs

Or:

```bash
pip install frappe-bench
bench init frappe-bench --frappe-branch version-15
cd frappe-bench

# Required System Configuration
1. Company
Must have default currency set
2. Item (Healthcare Service)
Create Item:
Item Code: HEALTHCARE-SERVICE
Item Group: Services
Is Stock Item: No
Include in Sales: Yes
Standard Selling Price: Set consultation price
3. Customer
Create: Walk-in Customer
4. Mode of Payment
Create: Cash
