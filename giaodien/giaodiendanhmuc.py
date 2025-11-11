# ================== GIAO DIỆN TKINTER ==================
from zoneinfo._common import load_data

from common.delete_danhmuc import delete_danhmuc
from common.insertdanhmuc import insert_danhmuc
from common.update_danhmuc import update_danhmuc
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error

from ketnoidb.ketnoi_mysql import connect_mysql

def insert_danhmuc():
    tendm = entry_ten.get()
    mota = entry_mota.get()
    if tendm == "":
        messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập tên danh mục!")
        return
    try:
        conn = connect_mysql()
        if conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO danhmuc (tendm, mota) VALUES (%s, %s)", (tendm, mota))
            conn.commit()
            messagebox.showinfo("Thành công", "Đã thêm danh mục mới!")
            load_danhmuc()
            entry_ten.delete(0, tk.END)
            entry_mota.delete(0, tk.END)
    except Error as e:
        messagebox.showerror("Lỗi", f"Lỗi khi thêm danh mục: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def update_danhmuc():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Chưa chọn", "Vui lòng chọn danh mục cần sửa!")
        return
    madm = tree.item(selected[0], "values")[0]
    tendm = entry_ten.get()
    mota = entry_mota.get()
    if tendm == "":
        messagebox.showwarning("Thiếu dữ liệu", "Tên danh mục không được để trống!")
        return
    try:
        conn = connect_mysql()
        if conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE danhmuc SET tendm=%s, mota=%s WHERE madm=%s", (tendm, mota, madm))
            conn.commit()
            messagebox.showinfo("Thành công", "Đã cập nhật danh mục!")
            load_danhmuc()
    except Error as e:
        messagebox.showerror("Lỗi", f"Lỗi khi cập nhật: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def delete_danhmuc():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Chưa chọn", "Vui lòng chọn danh mục cần xóa!")
        return
    madm = tree.item(selected[0], "values")[0]
    if messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa danh mục ID {madm}?"):
        try:
            conn = connect_mysql()
            if conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM danhmuc WHERE madm=%s", (madm,))
                conn.commit()
                messagebox.showinfo("Thành công", "Đã xóa danh mục!")
                load_danhmuc()
        except Error as e:
            messagebox.showerror("Lỗi", f"Lỗi khi xóa: {e}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
def on_select(event):
    selected = tree.selection()
    if selected:
        values = tree.item(selected[0], "values")
        entry_ten.delete(0, tk.END)
        entry_ten.insert(0, values[1])
        entry_mota.delete(0, tk.END)
        entry_mota.insert(0, values[2])
# ================== HÀM XỬ LÝ MYSQL ==================
def load_danhmuc():
    for row in tree.get_children():
        tree.delete(row)
    try:
        conn = connect_mysql()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM danhmuc")
            for madm, tendm, mota in cursor.fetchall():
                tree.insert("", "end", values=(madm, tendm, mota))
    except Error as e:
        messagebox.showerror("Lỗi", f"Lỗi khi tải dữ liệu: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

root = tk.Tk()
root.title("Quản lý Danh mục Sản phẩm")
root.geometry("700x400")
root.resizable(False, False)

# ========== Frame nhập dữ liệu ==========
frame_input = tk.LabelFrame(root, text="Thông tin danh mục", padx=10, pady=10)
frame_input.pack(fill="x", padx=10, pady=10)

tk.Label(frame_input, text="Tên danh mục:").grid(row=0, column=0, padx=5, pady=5)
entry_ten = tk.Entry(frame_input, width=40)
entry_ten.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Mô tả:").grid(row=1, column=0, padx=5, pady=5)
entry_mota = tk.Entry(frame_input, width=40)
entry_mota.grid(row=1, column=1, padx=5, pady=5)

# ========== Nút chức năng ==========
frame_btn = tk.Frame(root)
frame_btn.pack(fill="x", pady=10)

btn_them = tk.Button(frame_btn, text="➕ Thêm", width=12,command=insert_danhmuc )
btn_them.pack(side="left", padx=5)
btn_sua = tk.Button(frame_btn, text="📝 Sửa", width=12,command=update_danhmuc )
btn_sua.pack(side="left", padx=5)
btn_xoa = tk.Button(frame_btn, text="❌ Xóa", width=12,command=delete_danhmuc )
btn_xoa.pack(side="left", padx=5)
btn_hienthi = tk.Button(frame_btn, text="🔄 Làm mới", width=12,command=load_danhmuc )
btn_hienthi.pack(side="left", padx=5)

# ========== Bảng hiển thị ==========
frame_table = tk.LabelFrame(root, text="Danh sách danh mục", padx=5, pady=5)
frame_table.pack(fill="both", expand=True, padx=10, pady=5)

columns = ("madm", "tendm", "mota")
tree = ttk.Treeview(frame_table, columns=columns, show="headings", height=10)
tree.heading("madm", text="Mã danh mục")
tree.heading("tendm", text="Tên danh mục")
tree.heading("mota", text="Mô tả")
tree.column("madm", width=100)
tree.column("tendm", width=200)
tree.column("mota", width=300)
tree.pack(fill="both", expand=True)
tree.bind("<<TreeviewSelect>>", on_select)

# ========== Load dữ liệu khi mở ==========
load_danhmuc()
root.mainloop()