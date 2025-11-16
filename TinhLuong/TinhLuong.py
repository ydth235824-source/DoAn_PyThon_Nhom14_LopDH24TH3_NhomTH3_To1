import tkinter as tk
from tkinter import messagebox
import pyodbc

# ====== Kết nối cơ sở dữ liệu ======
conn = pyodbc.connect(
    'DRIVER={SQL Server};'
    'SERVER=ADMIN-PC\\SQLEXPRESS;'
    'DATABASE=QLGV;'
    'Trusted_Connection=yes;'
)
cur = conn.cursor()

# ====== Hàm tự động hiện tên GV ======
def hien_ten(event=None):
    ma_gv = entry_magv.get().strip()
    entry_ten.config(state='normal')
    entry_ten.delete(0, tk.END)
    if not ma_gv:
        entry_ten.insert(0, "")
    else:
        try:
            cur.execute("SELECT TenGV FROM GIAOVIEN WHERE MaGV=?", (ma_gv,))
            row = cur.fetchone()
            if row:
                entry_ten.insert(0, row[0])
            else:
                entry_ten.insert(0, "GV mới")  # Nếu chưa có trong DB
        except Exception as e:
            entry_ten.insert(0, f"Lỗi: {e}")
    entry_ten.config(state='readonly')


# ====== Hàm tính lương ======
def tim_va_tinh_luong():
    ma_gv = entry_magv.get().strip()
    if not ma_gv:
        messagebox.showwarning("Cảnh báo", "Vui lòng nhập Mã GV!")
        return

    try:
        # Lấy mã lương của giáo viên
        cur.execute("SELECT MaLuong FROM GIAOVIEN WHERE MaGV=?", (ma_gv,))
        row = cur.fetchone()

        if not row:
            messagebox.showerror("Lỗi", f"Không tìm thấy GV có Mã: {ma_gv}")
            return

        ma_luong = row[0]

        # Nếu giáo viên chưa có mã lương → lương mặc định
        if not ma_luong:
            he_so = 1.0
            luong_cb = 5000000
            phu_cap = 0

        else:
            # Lấy thông tin từ bảng LUONG
            cur.execute("""
                SELECT HeSoLuong, LuongCoBan, PhuCap
                FROM LUONG
                WHERE MaLuong = ?
            """, (ma_luong,))
            luong_data = cur.fetchone()

            if luong_data:
                he_so = float(str(luong_data[0]).replace(",", "."))
                luong_cb = luong_data[1]
                phu_cap = luong_data[2]
            else:
                # Nếu mã lương không tồn tại trong bảng LUONG
                he_so = 1.0
                luong_cb = 5000000
                phu_cap = 0

        # Tính tổng lương
        tong = he_so * luong_cb + phu_cap

        # Đổ dữ liệu lên giao diện
        entry_heso.config(state="normal")
        entry_heso.delete(0, tk.END)
        entry_heso.insert(0, he_so)
        entry_heso.config(state="readonly")

        entry_luongcb.config(state="normal")
        entry_luongcb.delete(0, tk.END)
        entry_luongcb.insert(0, luong_cb)
        entry_luongcb.config(state="readonly")

        entry_phucap.config(state="normal")
        entry_phucap.delete(0, tk.END)
        entry_phucap.insert(0, phu_cap)
        entry_phucap.config(state="readonly")

        entry_tong.config(state="normal")
        entry_tong.delete(0, tk.END)
        entry_tong.insert(0, int(tong))
        entry_tong.config(state="readonly")

    except Exception as e:
        messagebox.showerror("Lỗi", str(e))

# ====== Giao diện ======
root = tk.Tk()
root.title("Tính Lương GV theo Mã GV")
root.geometry("400x350")
root.resizable(False, False)

tk.Label(root, text="TÍNH LƯƠNG GIÁO VIÊN", font=("Times New Roman", 16, "bold")).pack(pady=10)

frame_input = tk.Frame(root)
frame_input.pack(padx=10, pady=10, fill='x')

# Mã GV
tk.Label(frame_input, text="Mã GV:", font=("Times New Roman", 12)).grid(row=0, column=0, sticky='w', pady=5)
entry_magv = tk.Entry(frame_input, width=25)
entry_magv.grid(row=0, column=1, pady=5)
entry_magv.bind("<FocusOut>", hien_ten)  # Khi rời khỏi ô nhập, hiển thị tên GV

# Tên GV (tự động hiện)
tk.Label(frame_input, text="Họ tên:", font=("Times New Roman", 12)).grid(row=1, column=0, sticky='w', pady=5)
entry_ten = tk.Entry(frame_input, width=25, state='readonly')
entry_ten.grid(row=1, column=1, pady=5)

# Hệ số lương
tk.Label(frame_input, text="Hệ số lương:", font=("Times New Roman", 12)).grid(row=2, column=0, sticky='w', pady=5)
entry_heso = tk.Entry(frame_input, width=25, state='readonly')
entry_heso.grid(row=2, column=1, pady=5)

# Lương cơ bản
tk.Label(frame_input, text="Lương cơ bản:", font=("Times New Roman", 12)).grid(row=3, column=0, sticky='w', pady=5)
entry_luongcb = tk.Entry(frame_input, width=25, state='readonly')
entry_luongcb.grid(row=3, column=1, pady=5)

# Phụ cấp
tk.Label(frame_input, text="Phụ cấp:", font=("Times New Roman", 12)).grid(row=4, column=0, sticky='w', pady=5)
entry_phucap = tk.Entry(frame_input, width=25, state='readonly')
entry_phucap.grid(row=4, column=1, pady=5)

# Tổng lương
tk.Label(frame_input, text="Tổng lương:", font=("Times New Roman", 12)).grid(row=5, column=0, sticky='w', pady=5)
entry_tong = tk.Entry(frame_input, width=25, state='readonly')
entry_tong.grid(row=5, column=1, pady=5)

# Nút bấm
frame_btn = tk.Frame(root)
frame_btn.pack(pady=10)

btn_tinh = tk.Button(frame_btn, text="Tính lương", font=("Times New Roman", 12), width=12, command=tim_va_tinh_luong)
btn_tinh.grid(row=0, column=0, padx=5)

btn_thoat = tk.Button(frame_btn, text="Thoát", font=("Times New Roman", 12), width=12, command=root.destroy)
btn_thoat.grid(row=0, column=1, padx=5)

root.mainloop()