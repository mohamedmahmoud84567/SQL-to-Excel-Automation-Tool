import tkinter as tk
from tkinter import messagebox, filedialog
import os
# استدعاء الدالة الاحترافية التي قمنا ببنائها وتجربتها في الملف السابق
from exporter import export_sql_table_to_excel, BASE_DIR

def run_automation():
    db_path = entry_db.get()
    table_name = entry_table.get()
    
    if not db_path or not table_name:
        messagebox.showwarning("تحذير / Warning", "برجاء ملء جميع الحقول المطلوبة أولاً!")
        return
        
    if not os.path.exists(db_path):
        messagebox.showerror("خطأ / Error", "ملف قاعدة البيانات المحددة غير موجود!")
        return
        
    # تشغيل الأتمتة وتصدير الملف إلى المجلد الرئيسي للمشروع
    export_sql_table_to_excel(db_path=db_path, table_name=table_name, output_folder=BASE_DIR)
    messagebox.showinfo("نجاح / Success", f"تم سحب البيانات بنجاح وتصدير جدول '{table_name}' إلى ملف Excel!")

def browse_file():
    filename = filedialog.askopenfilename(title="اختر قاعدة البيانات", filetypes=[("Database Files", "*.db *.sqlite")])
    if filename:
        entry_db.delete(0, tk.END)
        entry_db.insert(0, filename)

# --- إعداد واجهة البرنامج باستخدام Tkinter ---
root = tk.Tk()
root.title("SQL to Excel Automation Tool 🚀")
root.geometry("550x250")
root.resizable(False, False)

# حقل اختيار قاعدة البيانات
tk.Label(root, text="SQL Database Path:", font=("Arial", 10, "bold")).pack(pady=5)
frame_db = tk.Frame(root)
frame_db.pack()
entry_db = tk.Entry(frame_db, width=50)
entry_db.pack(side=tk.LEFT, padx=5)
# وضع مسار قاعدة البيانات الوهمية تلقائياً للتسهيل أثناء التجربة
default_db = os.path.join(BASE_DIR, "Database", "mock_company.db")
entry_db.insert(0, default_db)
tk.Button(frame_db, text="Browse", command=browse_file).pack(side=tk.LEFT)

# حقل كتابة اسم الجدول
tk.Label(root, text="Target Table Name:", font=("Arial", 10, "bold")).pack(pady=10)
entry_table = tk.Entry(root, width=30)
entry_table.pack()
entry_table.insert(0, "employees") # وضع اسم الجدول الافتراضي للتجربة

# زر بدء الأتمتة والتحويل
tk.Button(root, text="⚡ Convert SQL Table to Excel ⚡", font=("Arial", 11, "bold"), bg="#4CAF50", fg="white", command=run_automation, pady=8).pack(pady=25)

root.mainloop()
