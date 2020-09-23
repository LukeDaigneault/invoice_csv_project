import csv
import sqlite3
import calendar

header = ["Client Name",	"Invoice #",	"Date",	"Item Name",	"Item Description",	"Unit amount excluding taxes",
          "Quantity",	"Amount excluding taxes",	"Tax percent",	"Tax amount",	"Amount including taxes",	"Currency"]


client = "Danone"
tax_rate = .2
item_prefix = "Line "
item_description_prefix = "Services for "
currency = "EUR"

print("Dougs CSV Invoice Tool")
print("----------------------")

invoice_number = int(input("Enter invoice number: "))
invoice_date = input("Enter invoice date (format dd/MM/yyyy): ")
file_name = "Invoice Details ENINTSOL " + \
    calendar.month_name[int(invoice_date.split(
        "/")[1])] + " " + invoice_date.split("/")[-1] + ".csv"

with open(file_name, "w") as file:
    writer = csv.writer(file)
    writer.writerow(header)
    with sqlite3.connect("db.sqlite3") as connection:
        command = "select * FROM Employees"
        cursor = connection.execute(command)

        employees = cursor.fetchall()
        for employee in employees:
            invoice_line_number = str(
                invoice_number + 1) if employee[2] == "BT" else str(invoice_number)
            days_worked = float(
                input("Enter days worked for " + employee[0] + ": "))
            writer.writerow([client,
                             invoice_date.split(
                                 "/")[-1] + "-" + invoice_line_number,
                             invoice_date,
                             item_prefix + str(employee[1]),
                             item_description_prefix + employee[0],
                             employee[3],
                             f'{days_worked:.2f}',
                             f'{days_worked * employee[3]:.2f}',
                             f'{tax_rate * 100:.2f}',
                             f'{(days_worked * employee[3]) * tax_rate:.2f}',
                             f'{days_worked * employee[3] * (1 + tax_rate):.2f}',
                             currency
                             ])
