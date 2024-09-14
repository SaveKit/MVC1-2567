import tkinter as tk
from tkinter import messagebox


class CowView:
    def __init__(self, root, controller):
        self.controller = controller
        self.root = root
        self.root.title("Cow Milk Production System")
        self.root.geometry("600x400")  # กำหนดขนาดหน้าจอ GUI

        self.label = tk.Label(root, text="Enter Cow ID (8 digits):")
        self.label.pack(pady=20)

        self.entry = tk.Entry(root)
        self.entry.pack(pady=10)

        self.button = tk.Button(root, text="Find Cow", command=self.find_cow)
        self.button.pack(pady=10)

        self.result_label = tk.Label(root, text="", font=("Arial", 14))
        self.result_label.pack(pady=20)

        self.milk_button = tk.Button(
            root, text="Milk Cow", command=self.milk_cow, state=tk.DISABLED
        )
        self.milk_button.pack(pady=10)

        self.lemon_button = tk.Button(
            root,
            text="Milk with Lemon",
            command=self.milk_cow_with_lemon,
            state=tk.DISABLED,
        )
        self.lemon_button.pack(pady=10)

        self.report_button = tk.Button(
            root, text="Show Report", command=self.show_report
        )
        self.report_button.pack(pady=10)

        self.reset_all_button = tk.Button(
            root, text="Reset All BSOD", command=self.reset_all_bsod
        )
        self.reset_all_button.pack(pady=10)

    # ค้นหาข้อมูลวัวจากรหัสวัวที่ป้อน
    def find_cow(self):
        cow_id = self.entry.get()

        # ตรวจสอบความถูกต้องของรหัสวัว
        if not cow_id.isdigit():  # ตรวจสอบว่าเป็นตัวเลขหรือไม่
            messagebox.showerror("Error", "Cow ID must be a number.")
            return
        if len(cow_id) != 8:  # ตรวจสอบว่ามี 8 หลักหรือไม่
            messagebox.showerror("Error", "Cow ID must be 8 digits.")
            return
        if cow_id.startswith("0"):  # ตรวจสอบว่าไม่ขึ้นต้นด้วย 0
            messagebox.showerror("Error", "Cow ID must not start with 0.")
            return

        # ตรวจสอบข้อมูลวัวในฐานข้อมูล
        cow = self.controller.find_cow(cow_id)
        if cow:
            self.result_label.config(
                text=f"Cow {cow_id}: {cow['color'].capitalize()}, Age: {cow['age_years']} years, {cow['age_months']} months"
            )
            self.milk_button.config(state=tk.NORMAL)
            self.lemon_button.config(
                state=tk.NORMAL if cow["color"] == "white" else tk.DISABLED
            )
        else:
            messagebox.showerror("Error", "Cow not found.")
            self.result_label.config(text="")

    # รีดนมวัวที่ไม่กินมะนาว
    def milk_cow(self):
        cow_id = self.entry.get()
        cow = self.controller.milk_cow(cow_id)
        if cow:
            if cow["bsod"]:
                messagebox.showerror("BSOD", f"Cow {cow_id} has BSOD. Please reset.")
            else:
                messagebox.showinfo("Success", f"Cow {cow_id} produced milk.")
            self.update_result(cow)
        self.show_report()

    # รีดนมวัวที่กินมะนาว
    def milk_cow_with_lemon(self):
        cow_id = self.entry.get()
        cow = self.controller.milk_cow_with_lemon(cow_id)
        # แสดงข้อความแจ้งเตือนว่าวัวที่กินมะนาวจะไม่เกิด BSOD
        messagebox.showinfo("Report", "Cows that eat lemon do not experience BSOD.")
        if cow:
            if cow["bsod"]:
                messagebox.showerror("BSOD", f"Cow {cow_id} has BSOD. Please reset.")
            else:
                messagebox.showinfo("Success", f"Cow {cow_id} produced sour milk.")
            self.update_result(cow)
        self.show_report()

    # แสดงข้อมูลสถานะวัวที่รีดนมล่าสุดที่ดูข้อมูล
    def update_result(self, cow):
        self.result_label.config(
            text=f"Cow {cow['id']}: {cow['color'].capitalize()}, Age: {cow['age_years']} years, Milk: {cow['milk_produced']} bottles"
        )

    # สรุปข้อมูลการผลิตนมของวัวทั้งหมด
    def show_report(self):
        total_milk = 0
        total_plain = 0
        total_sour = 0
        total_choco = 0
        bsod_count = 0
        for cow in self.controller.model.cows.values():
            total_milk += cow["milk_produced"]
            total_plain += cow["milk_plain"]
            total_sour += cow["milk_sour"]
            total_choco += cow["milk_choco"]
            if cow["bsod"]:
                bsod_count += 1

        report = (
            f"Total Milk Produced: {total_milk} bottles\n"
            f"Plain Milk: {total_plain} bottles\n"
            f"Sour Milk: {total_sour} bottles\n"
            f"Chocolate Milk: {total_choco} bottles\n"
            f"Cows with BSOD: {bsod_count}"
        )
        messagebox.showinfo("Report", report)

    # รีเซ็ตวัวที่เกิด BSOD ทั้งหมด
    def reset_all_bsod(self):
        for cow_id, cow in self.controller.model.cows.items():
            if cow["bsod"]:
                self.controller.reset_cow(cow_id)
        messagebox.showinfo("Reset", "All BSOD cows have been reset.")
