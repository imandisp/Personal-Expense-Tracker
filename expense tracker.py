import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json

root=tk.Tk()
root.geometry("900x700")
root.title("Personal Expense Tracker")

Categories={
    "Food":0,
    "Transport":0,
    "Clothes":0,
    "Entertainment":0,
    "Utilities":0,
    "Other":0
}

Total=tk.IntVar(value=0)


def update_summary():
    for row_id in table2.get_children():
        table2.delete(row_id)
    for key,value in Categories.items():
        table2.insert("",index="end",values=(key,value))


def save_to_file():
    entries = []

    # Collect all entries from table1
    for row_id in table1.get_children():
        date_val, category_val, desc_val, amount_val = table1.item(row_id)["values"]
        entries.append({
            "date": date_val,
            "category": category_val,
            "description": desc_val,
            "amount": amount_val
        })

    # Combine everything into one data dictionary
    data = {
        "categories": Categories,
        "total": Total.get(),
        "entries": entries
    }

    # Save to a single JSON file
    with open("expense_data.json", "w") as file:
        json.dump(data, file, indent=4)


def save():

    dt=date_entry.get()
    ctgy=category_entry.get()
    dscrptn=description_entry.get()
    amt_str=amount_entry.get()

    if not(dt and ctgy and dscrptn and amt_str):
        messagebox.showinfo("Error","Please enter all fields")
        return

    try:
        amt=float(amt_str)
    except ValueError:
        messagebox.showerror("Error","Amount cannot be a string")
        return

    global Total

    table1.insert("",index="end",values=(date_entry.get(),category_entry.get(),description_entry.get(),amount_entry.get()))
    
    type=category_entry.get()
    match type:
        case "Food":
            Categories["Food"]+=amt
        case "Transport":
            Categories["Transport"]+=amt
        case "Clothes":
            Categories["Clothes"]+=amt
        case "Entertainment":
            Categories["Entertainment"]+=amt
        case "Utilities":
            Categories["Utilities"]+=amt
        case _:
            Categories["Other"]+=amt
    
    update_summary()

    Total.set(Total.get()+amt)
    Total_label.configure(text=f"Total = {Total.get()}")
    
    date_entry.delete(0, tk.END)
    category_entry.set("")
    description_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)

    save_to_file()

def open_file():
    try:
        with open("expense_data.json", "r") as file:
            data = json.load(file)

            # Load Categories
            for key in Categories:
                Categories[key] = data.get("categories", {}).get(key, 0)

            # Load Total
            Total.set(data.get("total", 0))
            Total_label.configure(text=f"Total = {Total.get()}")

            # Load entries into table1
            for entry in data.get("entries", []):
                table1.insert("", "end", values=(
                    entry["date"],
                    entry["category"],
                    entry["description"],
                    entry["amount"]
                ))

            # Load summary into table2
            for key, value in Categories.items():
                table2.insert("", "end", values=(key, value))

    except FileNotFoundError:
        pass


entry_frame=ttk.Frame(root)
entry_frame.pack(pady=20)

date_entry=ttk.Entry(entry_frame,width=18)
date_entry.grid(column=0,row=0,padx=5)
date_label=ttk.Label(entry_frame,text="Date")
date_label.grid(column=0,row=1,padx=5)

category_entry=ttk.Combobox(entry_frame,values=[key for key in Categories])
category_entry.grid(column=1,row=0,padx=5)
category_label=ttk.Label(entry_frame,text="Category")
category_label.grid(column=1,row=1,padx=5)

description_entry=ttk.Entry(entry_frame,width=30)
description_entry.grid(column=2,row=0,padx=5)
description_label=ttk.Label(entry_frame,text="Description")
description_label.grid(column=2,row=1,padx=5)

amount_entry=ttk.Entry(entry_frame)
amount_entry.grid(column=3,row=0,padx=5)
amount_label=ttk.Label(entry_frame,text="Amount")
amount_label.grid(column=3,row=1,padx=5)

btn=ttk.Button(entry_frame,text="Save",command=save)
btn.grid(column=3,row=2,padx=20,pady=30)

table_frame=ttk.Frame(root)
table_frame.pack(pady=10)

table1=ttk.Treeview(table_frame,columns=("Date","Category","Description","Amount"),show="headings")
for col in ("Date","Category","Description","Amount"):
    table1.heading(col,text=col)
table1.pack()

table2=ttk.Treeview(table_frame,columns=("Category","Total"),show="headings")
table2.heading("Category",text="Category")
table2.heading("Total",text="Total")
table2.pack(pady=10)

Total_label=ttk.Label(root,text="Total = 0")
Total_label.pack()

open_file()

root.mainloop()