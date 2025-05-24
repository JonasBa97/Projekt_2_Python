# ----------------------------------------------------------------
# Import von Bibliotheken
# ----------------------------------------------------------------
import csv
import os
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog
import matplotlib.pyplot as plt # type: ignore
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg # type: ignore
import pandas as pd # type: ignore
from datetime import datetime
from tkcalendar import DateEntry # type: ignore
from fpdf import FPDF # type: ignore

# ----------------------------------------------------------------
# Grundattribute setzen
# ----------------------------------------------------------------
# Datei, in der die Finanzdaten gespeichert werden
csv_file = 'finanzdaten.csv'
# Kategorien für Ausgaben
categories = ['Gehalt', 'Bareinzahlung', 'Miete', 'Versicherungen', 'Altersvorsorge', 'Verpflegung', 'Spassgeld']
# Sparziele
targets = {'Notfallfonds': 0, 'Urlaub': 0}

# ----------------------------------------------------------------
# Aufruf von Funktionen und Inhalten der App
# ----------------------------------------------------------------
class PersonalFinanceDashboard:
    # Daten laden
    @staticmethod
    def load_data():
        if not os.path.exists(csv_file):
            return [], []
        revenues = []
        expenditures = []
        with open(csv_file, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['Typ'] == 'Einnahme':
                    revenues.append(row)
                elif row['Typ'] == 'Ausgabe':
                    expenditures.append(row)
                elif row['Typ'] in targets:
                    targets[row['Typ']] = float(row['Betrag'])
        return revenues, expenditures
    
    # Daten speichern
    @staticmethod
    def save_data(revenues, expenditures):
        with open(csv_file, mode='w', newline='') as file:
            fieldnames = ['Datum', 'Typ', 'Betrag', 'Kategorie']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for revenue in revenues:
                writer.writerow(revenue)
            for expenditure in expenditures:
                writer.writerow(expenditure)
            for target, amount in targets.items():
                writer.writerow({'Datum': '', 'Typ': target, 'Betrag': amount, 'Kategorie': ''})
    
    # Einnahmen hinzufügen
    @staticmethod
    def add_revenue(revenues, date, amount, category):
        revenues.append({'Datum': date, 'Typ': 'Einnahme', 'Betrag': amount, 'Kategorie': category})
    
    # Ausgaben hinzufügen
    @staticmethod
    def add_expenditure(expenditures, date, amount, category):
        expenditures.append({'Datum': date, 'Typ': 'Ausgabe', 'Betrag': amount, 'Kategorie': category})
    
    # Ziele setzen
    @staticmethod
    def set_target(target, amount):
        targets[target] = amount
    
    # Fortschritt anzeigen
    @staticmethod
    def show_progress(revenues, expenditures):
        total_revenues = sum(float(e['Betrag']) for e in revenues)
        total_expenditures = sum(float(a['Betrag']) for a in expenditures)
        remaining_budget = total_revenues - total_expenditures
        progress_data = []
        for target, targetamount in targets.items():
            paid_in = sum(float(e['Betrag']) for e in expenditures if e['Kategorie'] == f'Sparen: {target}')
            progress = (paid_in / targetamount) * 100 if targetamount > 0 else 0
            progress_data.append((target, progress, paid_in, targetamount))
        return remaining_budget, progress_data
    
    # Betrag aus verbleibendem Budget einem Sparziel zuweisen
    @staticmethod
    def allocate_to_target(revenues, expenditures, target, amount):
        remaining_budget, _ = PersonalFinanceDashboard.show_progress(revenues, expenditures)
        if amount <= remaining_budget:
            expenditures.append({'Datum': datetime.today().strftime('%Y-%m-%d'), 'Typ': 'Ausgabe', 'Betrag': amount, 'Kategorie': f'Sparen: {target}'})
            return True
        return False
    
    # Daten exportieren
    @staticmethod
    def export_data(revenues, expenditures, file_path):
        if file_path.endswith('.pdf'):
            PersonalFinanceDashboard.export_data_to_pdf(revenues, expenditures, targets, file_path)
        else:
            data = revenues + expenditures
            for target, amount in targets.items():
                data.append({'Datum': '', 'Typ': target, 'Betrag': amount, 'Kategorie': ''})
            df = pd.DataFrame(data)
            if file_path.endswith('.csv'):
                df.to_csv(file_path, index=False)
            elif file_path.endswith('.xlsx'):
                df.to_excel(file_path, index=False, engine='openpyxl')
    
    # Export in PDF -> Kontoauszug
    @staticmethod
    def export_data_to_pdf(revenues, expenditures, targets, file_path):
        pdf = PDF()
        pdf.add_page()
        
        # Verfügbares Budget
        total_revenues = sum(float(r['Betrag']) for r in revenues)
        total_expenditures = sum(float(e['Betrag']) for e in expenditures)
        remaining_budget = total_revenues - total_expenditures
        pdf.set_font('Arial', 'B', 11)
        pdf.cell(0, 10, f'Verfügbares Budget: {remaining_budget:.2f} EUR', ln=True)
        pdf.ln(5)

        # Einnahmen
        pdf.chapter_title('Einnahmen')
        revenue_data = [(r['Datum'], r['Kategorie'], r['Betrag']) for r in revenues]
        pdf.add_table(['Datum', 'Kategorie', 'Betrag'], revenue_data)

        # Ausgaben
        pdf.chapter_title('Ausgaben')
        expenditure_data = [(e['Datum'], e['Kategorie'], e['Betrag']) for e in expenditures]
        pdf.add_table(['Datum', 'Kategorie', 'Betrag'], expenditure_data)

        # Sparziele
        pdf.chapter_title('Sparziele')
        progress_data = []
        for target, target_amount in targets.items():
            paid_in = sum(float(e['Betrag']) for e in expenditures if e['Kategorie'] == f'Sparen: {target}')
            progress = (paid_in / target_amount) * 100 if target_amount > 0 else 0
            progress_data.append((target, f"{paid_in:.2f}", f"{target_amount:.2f}", f"{progress:.2f}%"))
        pdf.add_table(['Ziel', 'Eingezahlt', 'Zielbetrag', 'Fortschritt'], progress_data)
        pdf.output(file_path)

# ----------------------------------------------------------------
# Graphical-User-Interface
# ----------------------------------------------------------------
class PFD_GUI:
    def __init__(self, master):
        self.master = master
        master.title("Personal Finance Dashboard")
        master.columnconfigure(0, weight=1)
        master.columnconfigure(1, weight=2)
        self.revenues, self.expenditures = PersonalFinanceDashboard.load_data()
        
        # Einnahmen hinzufügen
        self.revenue_frame = ttk.LabelFrame(master, text="Einnahme hinzufügen")
        self.revenue_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.revenue_date_label = ttk.Label(self.revenue_frame, text="Datum (YYYY-MM-DD):")
        self.revenue_date_label.grid(row=0, column=0, padx=5, pady=5)
        self.revenue_date_entry = DateEntry(self.revenue_frame, date_pattern='yyyy-mm-dd')
        self.revenue_date_entry.grid(row=0, column=1, padx=5, pady=5)
        self.revenue_amount_label = ttk.Label(self.revenue_frame, text="Betrag:")
        self.revenue_amount_label.grid(row=1, column=0, padx=5, pady=5)
        self.revenue_amount_entry = ttk.Entry(self.revenue_frame)
        self.revenue_amount_entry.grid(row=1, column=1, padx=5, pady=5)
        self.revenue_category_label = ttk.Label(self.revenue_frame, text="Kategorie:")
        self.revenue_category_label.grid(row=2, column=0, padx=5, pady=5)
        self.revenue_category_combobox = ttk.Combobox(self.revenue_frame, values=categories)
        self.revenue_category_combobox.grid(row=2, column=1, padx=5, pady=5)
        self.add_revenue_button = ttk.Button(self.revenue_frame, text="Hinzufügen", command=self.add_revenue)
        self.add_revenue_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        # Ausgaben hinzufügen
        self.expenditure_frame = ttk.LabelFrame(master, text="Ausgabe hinzufügen")
        self.expenditure_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        self.expenditure_date_label = ttk.Label(self.expenditure_frame, text="Datum (YYYY-MM-DD):")
        self.expenditure_date_label.grid(row=0, column=0, padx=5, pady=5)
        self.expenditure_date_entry = DateEntry(self.expenditure_frame, date_pattern='yyyy-mm-dd')
        self.expenditure_date_entry.grid(row=0, column=1, padx=5, pady=5)
        self.expenditure_amount_label = ttk.Label(self.expenditure_frame, text="Betrag:")
        self.expenditure_amount_label.grid(row=1, column=0, padx=5, pady=5)
        self.expenditure_amount_entry = ttk.Entry(self.expenditure_frame)
        self.expenditure_amount_entry.grid(row=1, column=1, padx=5, pady=5)
        self.expenditure_category_label = ttk.Label(self.expenditure_frame, text="Kategorie:")
        self.expenditure_category_label.grid(row=2, column=0, padx=5, pady=5)
        self.expenditure_category_combobox = ttk.Combobox(self.expenditure_frame, values=categories)
        self.expenditure_category_combobox.grid(row=2, column=1, padx=5, pady=5)
        self.add_expenditure_button = ttk.Button(self.expenditure_frame, text="Hinzufügen", command=self.add_expenditure)
        self.add_expenditure_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        # Ziel setzen
        self.target_frame = ttk.LabelFrame(master, text="Ziel setzen")
        self.target_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        self.target_label = ttk.Label(self.target_frame, text="Ziel:")
        self.target_label.grid(row=0, column=0, padx=5, pady=5)
        self.target_combobox = ttk.Combobox(self.target_frame, values=list(targets.keys()))
        self.target_combobox.grid(row=0, column=1, padx=5, pady=5)
        self.target_amount_label = ttk.Label(self.target_frame, text="Zielbetrag:")
        self.target_amount_label.grid(row=1, column=0, padx=5, pady=5)
        self.target_amount_entry = ttk.Entry(self.target_frame)
        self.target_amount_entry.grid(row=1, column=1, padx=5, pady=5)
        self.set_target_button = ttk.Button(self.target_frame, text="Setzen", command=self.set_target)
        self.set_target_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        # Zielen ein Budget zuweisen
        self.allocate_frame = ttk.LabelFrame(master, text="Budget einem Ziel zuweisen")
        self.allocate_frame.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
        self.allocate_target_label = ttk.Label(self.allocate_frame, text="Ziel:")
        self.allocate_target_label.grid(row=0, column=0, padx=5, pady=5)
        self.allocate_target_combobox = ttk.Combobox(self.allocate_frame, values=list(targets.keys()))
        self.allocate_target_combobox.grid(row=0, column=1, padx=5, pady=5)
        self.allocate_target_entry = ttk.Label(self.allocate_frame, text="Betrag:")
        self.allocate_target_entry.grid(row=1, column=0, padx=5, pady=5)
        self.allocate_amount_entry = ttk.Entry(self.allocate_frame)
        self.allocate_amount_entry.grid(row=1, column=1, padx=5, pady=5)
        self.allocate_button = ttk.Button(self.allocate_frame, text="Zuweisen", command=self.allocate_to_target)
        self.allocate_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        # Fortschritt anzeigen
        self.progress_frame = ttk.LabelFrame(master, text="Fortschritt anzeigen")
        self.progress_frame.grid(row=0, column=1, rowspan=6, padx=10, pady=10, sticky="nsew")
        self.progress_button = ttk.Button(self.progress_frame, text="Aktualisieren", command=self.show_progress)
        self.progress_button.grid(row=0, column=0, padx=5, pady=5)
        self.figure, self.ax = plt.subplots(figsize=(5, 4))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.progress_frame)
        self.canvas.get_tk_widget().grid(row=1, column=0, padx=5, pady=5)

        # Daten exportieren
        self.export_frame = ttk.LabelFrame(master, text="Daten exportieren")
        self.export_frame.grid(row=4, column=0, padx=10, pady=10, sticky="ew")
        self.export_button = ttk.Button(self.export_frame, text="Exportieren", command=self.export_data)
        self.export_button.grid(row=0, column=0, padx=5, pady=5)
        
        # Daten speichern
        self.save_button = ttk.Button(master, text="Speichern", command=self.save_data)
        self.save_button.grid(row=5, column=0, padx=10, pady=10, sticky="ew")

        # Anwendung beenden
        self.quit_button = ttk.Button(master, text="Beenden", command=master.quit)
        self.quit_button.grid(row=6, column=0, padx=10, pady=10, sticky="ew")

    # Einnahmen hinzufügen
    def add_revenue(self):
        date = self.revenue_date_entry.get()
        amount = self.revenue_amount_entry.get()
        category = self.revenue_category_combobox.get()
        if date and amount and category:
            try:
                amount = float(amount)
                PersonalFinanceDashboard.add_revenue(self.revenues, date, amount, category)
                messagebox.showinfo("Erfolg", "Einnahme hinzugefügt!")
                self.revenue_date_entry.delete(0, tk.END)
                self.revenue_date_entry.insert(0, datetime.today().strftime('%Y-%m-%d'))
                self.revenue_amount_entry.delete(0, tk.END)
                self.revenue_category_combobox.set('')
            except ValueError:
                messagebox.showerror("Fehler", "Ungültiger Betrag!")
        else:
            messagebox.showerror("Fehler", "Bitte alle Felder ausfüllen!")

    # Ausgaben hinzufügen
    def add_expenditure(self):
        date = self.expenditure_date_entry.get()
        amount = self.expenditure_amount_entry.get()
        category = self.expenditure_category_combobox.get()
        if date and amount and category:
            try:
                amount = float(amount)
                PersonalFinanceDashboard.add_expenditure(self.expenditures, date, amount, category)
                messagebox.showinfo("Erfolg", "Ausgabe hinzugefügt!")
                self.expenditure_date_entry.delete(0, tk.END)
                self.expenditure_date_entry.insert(0, datetime.today().strftime('%Y-%m-%d'))
                self.expenditure_amount_entry.delete(0, tk.END)
                self.expenditure_category_combobox.set('')
            except ValueError:
                messagebox.showerror("Fehler", "Ungültiger Betrag!")
        else:
            messagebox.showerror("Fehler", "Bitte alle Felder ausfüllen!")

    # Sparziel setzen
    def set_target(self):
        target = self.target_combobox.get()
        amount = self.target_amount_entry.get()
        if target and amount:
            try:
                amount = float(amount)
                PersonalFinanceDashboard.set_target(target, amount)
                messagebox.showinfo("Erfolg", "Ziel gesetzt!")
                self.target_combobox.set('')
                self.target_amount_entry.delete(0, tk.END)
            except ValueError:
                messagebox.showerror("Fehler", "Ungültiger Betrag!")
        else:
            messagebox.showerror("Fehler", "Bitte alle Felder ausfüllen!")

    # Betrag einem Sparziel zuweisen
    def allocate_to_target(self):
        target = self.allocate_target_combobox.get()
        amount = self.allocate_amount_entry.get()
        if target and amount:
            try:
                amount = float(amount)
                success = PersonalFinanceDashboard.allocate_to_target(self.revenues, self.expenditures, target, amount)
                if success:
                    messagebox.showinfo("Erfolg", "Betrag zugewiesen!")
                    self.allocate_target_combobox.set('')
                    self.allocate_amount_entry.delete(0, tk.END)
                else:
                    messagebox.showerror("Fehler", "Nicht genügend Budget verfügbar!")
            except ValueError:
                messagebox.showerror("Fehler", "Ungültiger Betrag!")
        else:
            messagebox.showerror("Fehler", "Bitte alle Felder ausfüllen!")

    # Fortschritt anzeigen
    def show_progress(self):
        remaining_budget, progress_data = PersonalFinanceDashboard.show_progress(self.revenues, self.expenditures)
        self.ax.clear()
        targets, progress, paid_in, targetamount = zip(*progress_data)
        if progress_data:
            targets, progress, paid_in, targetamount = zip(*progress_data)
            # Balkenfarbe abhängig von Fortschritt
            colors = []
            for p in progress:
                if p < 40:
                    colors.append('red')
                elif p < 60:
                    colors.append('orange')
                elif p < 80:
                    colors.append('yellow')
                else:
                    colors.append('green')
            # Fortschritt mit Zahlenwerten anzeigen
            bars = self.ax.bar(targets, progress, color=colors)
            for bar, paid, goal in zip(bars, paid_in, targetamount):
                label = f"{paid:.0f}€ / {goal:.0f}€"
                height = bar.get_height()
                self.ax.text(bar.get_x() + bar.get_width() / 2, height + 2, label, ha='center', fontsize=8)
            self.ax.set_ylim(0, 100)
            self.ax.set_ylabel('Fortschritt (%)')
            self.ax.set_title(f'Verbleibendes Budget: {remaining_budget:.2f} EUR')
        else:
            self.ax.text(0.5, 0.5, 'Keine Ziele gesetzt', ha='center')
        self.ax.set_ylim(0, 100)
        self.ax.set_ylabel('Fortschritt (%)')
        self.ax.set_title(f'Verbleibendes Budget: {remaining_budget:.2f} EUR')
        self.canvas.draw()

    # Daten exportieren
    def export_data(self):
        timestamp = datetime.now().strftime("%Y_%m%d_%H%M")
        default_filename = f"finanzdaten_{timestamp}.pdf"
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", initialfile=default_filename, filetypes=[("PDF-Datei", "*.pdf"), ("CSV-Datei", "*.csv"), ("Excel-Datei", "*.xlsx")])
        if file_path:
            PersonalFinanceDashboard.export_data(self.revenues, self.expenditures, file_path)
            messagebox.showinfo("Erfolg", f"Daten exportiert nach {file_path}")

    # Daten speichern
    def save_data(self):
        PersonalFinanceDashboard.save_data(self.revenues, self.expenditures)
        messagebox.showinfo("Erfolg", "Daten gespeichert!")

# ----------------------------------------------------------------
# Hilfsklasse für PDF-Export
# ----------------------------------------------------------------
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Finanzdaten Export', 0, 1, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(5)

    def add_table(self, header, data):
        self.set_font('Arial', 'B', 10)
        for col in header:
            self.cell(48, 8, col, 1)
        self.ln()
        self.set_font('Arial', '', 9)
        for row in data:
            for item in row:
                self.cell(48, 8, str(item), 1)
            self.ln()

# ----------------------------------------------------------------
# Aufruf der Main-Funktion
# ----------------------------------------------------------------
def main():
    root = tk.Tk()
    app = PFD_GUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()