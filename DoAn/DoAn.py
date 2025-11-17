from math import e
import tkinter as tk
from tkinter import Menu, ttk, messagebox
from tkcalendar import DateEntry
import pyodbc
import subprocess
import sys
from openpyxl import Workbook
from tkinter import filedialog
# ====== Kết nối cơ sở dữ liệu ======
conn = pyodbc.connect(
            'DRIVER={SQL Server};'
            'SERVER=ADMIN-PC\\SQLEXPRESS;'
            'DATABASE=QLGV;'
            'Trusted_Connection=yes;'
        )

cur = conn.cursor()


# ====== Hàm canh giữa cửa sổ ====== 
def center_window(win, w=700, h=600):
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    x = (ws // 2) - (w // 2)
    y = (hs // 2) - (h // 2)
    win.geometry(f'{w}x{h}+{x}+{y}')
# ====== Cửa sổ chính ======
root = tk.Tk()
root.title("Quản lý giáo viên")
center_window(root, 700, 600)
root.resizable(False, False)



# ================================= MENU ===================================

def mo_form_dangnhap():
     root.withdraw()
     try:
         subprocess.Popen([sys.executable, r"E:\DoAn_QLGV\QLGV\Login.py"])
         root.destroy()  # đóng form hiện tại hoàn toàn
     except Exception as e:
         messagebox.showerror("Lỗi", f"Không thể mở form đăng nhập:\n{e}")
menubar = tk.Menu(root)

# ----- Menu Quản lý -----
menu_quanly = tk.Menu(menubar, tearoff=0)
menu_quanly.add_command(label="Quản lý giáo viên",font=("Times New Roman", 11), 
                        command=lambda: messagebox.showinfo("Thông báo", "Bạn đang ở trang Quản lý giáo viên"))
menu_quanly.add_command(label="Đăng xuất",font=("Times New Roman", 11), command=lambda: mo_form_dangnhap())
menubar.add_cascade(label="Menu",font=("Times New Roman", 11),menu=menu_quanly)

root.config(menu=menubar)


# ========================================== TIÊU ĐỀ ==================================================
lbl_tieu_de = tk.Label(root, text="QUẢN LÝ GIÁO VIÊN THPT", font=("Times New Roman", 18, "bold")  )
lbl_tieu_de.pack(pady=10)
# ====== Frame nhập thông tin ====== 
frame_tt = tk.Frame(root) 
frame_tt.pack(pady=5, padx=10, fill="x")

tk.Label(frame_tt, text="Mã GV", font=("Times New Roman", 13),bg="#F5F5F5").grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_maso = tk.Entry(frame_tt, width=20)
entry_maso.grid(row=0, column=1, padx=5, pady=5, sticky="w")

# Đặt khoảng cách lớn giữa entry_maso và label "Lớp"
frame_tt.grid_columnconfigure(2, minsize=100)

tk.Label(frame_tt, text="Họ tên", font=("Times New Roman", 13),bg="#F5F5F5").grid(row=1,	column=0, padx=5, pady=5, sticky="w")
entry_hoten = tk.Entry(frame_tt, width=35) 
entry_hoten.grid(row=1, column=1, padx=5, pady=5, sticky="w")

# ====== Ô nhập SĐT ======
tk.Label(frame_tt, text="SĐT", font=("Times New Roman", 13), bg="#F5F5F5").grid(row=3, column=0, padx=5, pady=5, sticky="w")
entry_sdt = tk.Entry(frame_tt, width=20)
entry_sdt.grid(row=3, column=1, padx=5, pady=5, sticky="w")



tk.Label(frame_tt, text="Chức Vụ", font=("Times New Roman", 13),bg="#F5F5F5").grid(row=0, column=3, padx=5, pady=5, sticky="w")
cbb_cv = ttk.Combobox(frame_tt, values=["Giáo viên chủ nhiệm", "Giáo viên bộ môn"], width=15)
cbb_cv.grid(row=0, column=4, padx=5, pady=5, sticky="w")



tk.Label(frame_tt, text="Giới tính", font=("Times New Roman", 13),bg="#F5F5F5").grid(row=2, column=0, padx=5, pady=5, sticky="w") 
gender_var = tk.StringVar(value="Nam")
tk.Radiobutton(frame_tt,	text="Nam",font=("Times New Roman", 13),bg="#F5F5F5",
               variable=gender_var, value="Nam").grid(row=2, column=1, padx=5, sticky="w")
tk.Radiobutton(frame_tt, text="Nữ",font=("Times New Roman", 13),bg="#F5F5F5",
               variable=gender_var, value="Nữ").grid(row=2, column=1, padx=70, sticky="w")

tk.Label(frame_tt, text="Mã CV", font=("Times New Roman", 13),bg="#F5F5F5").grid(row=1, column=3, padx=5, pady=5, sticky="w")
entry_macv = tk.Entry(frame_tt, width=18)
entry_macv.grid(row=1, column=4, padx=5, pady=5, sticky="w")


tk.Label(frame_tt, text="Ngày sinh", font=("Times New Roman", 13),bg="#F5F5F5").grid(row=2, column=3, padx=5, pady=5, sticky="w")
date_entry = DateEntry(frame_tt, width=13, background="darkblue", 
                       foreground="white", date_pattern="yyyy-mm-dd", font=("Times New Roman", 11))
date_entry.grid(row=2, column=4, padx=5, pady=5, sticky="w")

#========================================= CÁC HÀM CHỨC NĂNG ================================================
cv_duoc_chon = ""


cv_to_macv = {
    "Giáo viên bộ môn": "CV02",
    "Giáo viên chủ nhiệm": "CV01"
}

# Tạo bản đồ ngược lại (Mã cv → cv)
macv_to_cv = {v: k for k, v in cv_to_macv.items()}

# Khi chọn cv, tự điền mã cv 
def capnhat_macv(event=None):
    ma_cv= entry_macv.get().strip().upper()
    cv = macv_to_cv.get(ma_cv, "")
    if cv:
        cbb_cv.set(cv)
        global cv_duoc_chon
        cv_duoc_chon = cv
        load_du_lieu()  # Tự động lọc khi nhập mã cv

def on_cv_duoc_chon(event=None):
    global cv_duoc_chon
    cv_duoc_chon = cbb_cv.get()
    # Cập nhật mã cv
    ma_cv = cv_to_macv.get(cv_duoc_chon, "")
    entry_macv.delete(0, tk.END)
    entry_macv.insert(0, ma_cv)
    load_du_lieu()  # Load danh sách theo cv
    capnhat_so_luong()

cbb_cv.bind("<<ComboboxSelected>>", on_cv_duoc_chon)


def capnhat_so_luong():
    """Cập nhật số lượng giáo viên đang hiển thị"""
    if cv_duoc_chon:
        # Đếm số gv theo cv
        cur.execute("SELECT COUNT(*) FROM GIAOVIEN WHERE MaGV = ?", (cv_to_macv[cv_duoc_chon],))
        so_luong = cur.fetchone()[0]
        #label_Soluong.config(text=f"Số lượng giáo viên  {cv_duoc_chon}: {so_luong}")
    else:
        # Đếm tổng số gv (khi chưa chọn cv)
        cur.execute("SELECT COUNT(*) FROM GIAOVIEN")
        so_luong = cur.fetchone()[0]
        label_Soluong.config(text=f"Tổng số giáo viên: {so_luong}")

def load_du_lieu():
    for i in tree.get_children():
        tree.delete(i)

    if cv_duoc_chon:
        cur.execute("SELECT MaGV, TenGV, SDT, NgaySinh, GioiTinh, MaCV FROM GIAOVIEN WHERE MaCV=?", (cv_to_macv[cv_duoc_chon],))
    else:
        cur.execute("SELECT MaGV, TenGV, SDT, NgaySinh, GioiTinh, MaCV FROM GIAOVIEN")

    rows = cur.fetchall()
    for row in rows:

        
        #đảm bảo đủ 6 cột: Mã GV, Họ tên, SDT, Ngày Sinh, Giới tính, Mã CV
        capnhat_so_luong()
        tree.insert("", tk.END, values=(row[0], row[1], row[2], row[3], row[4], row[5]))

   



def Huy_tt():
    entry_maso.delete(0, tk.END)
    entry_hoten.delete(0, tk.END)
    entry_macv.delete(0, tk.END)
    gender_var.set("Nam")
    date_entry.set_date("2000-01-01")
    cbb_cv.set("")


def them_gv():
    maso = entry_maso.get().strip()
    hoten = entry_hoten.get().strip()
    sdt = entry_sdt.get().strip()
    ngaysinh = date_entry.get_date()
    phai = gender_var.get()
    macv = entry_macv.get().strip()

    if not maso or not hoten or not macv:
        messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ thông tin.")
        return

    try:
        # Kiểm tra mã gv đã tồn tại chưa
        cur.execute("SELECT COUNT(*) FROM GIAOVIEN WHERE MaGV = ?", (maso,))
        count_magv = cur.fetchone()[0]

        if count_magv > 0:
            messagebox.showerror("Lỗi", "Mã giáo viên đã tồn tại. Vui lòng nhập mã khác.")
            return

        # Kiểm tra cv đã tồn tại chưa
        cur.execute("SELECT COUNT(*) FROM CHUCVU WHERE MaCV = ?", (macv,))
        count_cv = cur.fetchone()[0]

        # Nếu chưa có cv thì thêm vào bảng cv
        if count_cv == 0:
            # Ở đây bạn có thể yêu cầu người dùng nhập thêm TenCV (nếu có Textbox riêng)
            # hoặc tạm thời dùng MaCV làm CV
            cur.execute("INSERT INTO CV (MaGV, MaCV) VALUES (?, ?)", (magv, macv))
            conn.commit()

        # Thêm gv vào bảng gv
        cur.execute("""
            INSERT INTO GIAOVIEN (MaGV, TenGV, SDT, NgaySinh, GioiTinh, MaCV)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (maso, hoten,sdt, ngaysinh.strftime("%Y-%m-%d"), phai, macv))
        conn.commit()

        messagebox.showinfo("Thành công", "Thêm giáo viên thành công.")
        load_du_lieu()
        capnhat_so_luong()
        Huy_tt()

    except Exception as e:
        messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {str(e)}")

def xoa_gv():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn giáo viên để xóa.")
        return
    hoi = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa giáo viên này không?")
    if hoi:
        maso = tree.item(selected[0])['values'][0]
        cur.execute("DELETE FROM GIAOVIEN WHERE MaGV=?", (maso,))
        cur.execute("DELETE FROM GIAOVIEN WHERE MaGV = ?", (maso,))
    
        conn.commit()
        messagebox.showinfo("Thành công","Xóa giáo viên thành công.")
        load_du_lieu()
        Huy_tt()
    else:
        return

# global selected_maso dùng chung
selected_maso = None

def sua_gv():
    global selected_maso
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn giáo viên để sửa.")
        return

    selected_maso = tree.item(selected[0])["values"][0]
    values = tree.item(selected[0])["values"]

    entry_maso.delete(0, tk.END)
    entry_maso.insert(0, values[0])

    entry_hoten.delete(0, tk.END)
    entry_hoten.insert(0, values[1])

    entry_sdt.delete(0, tk.END)
    entry_sdt.insert(0, values[2])  # SĐT

    try:
        date_entry.set_date(values[3])  # Ngày sinh (chỉ số 3)
    except Exception:
        pass

    gender_var.set(values[4])
    cbb_cv.set(values[5])
    entry_macv.delete(0, tk.END)
    entry_macv.insert(0, values[5])





def luu_sua():
    global selected_maso
    maso_moi = entry_maso.get().strip()
    hoten = entry_hoten.get().strip()
    sdt = entry_sdt.get().strip()
    ngaysinh = date_entry.get_date()
    phai = gender_var.get()
    macv = entry_macv.get().strip()

    if not maso_moi or not hoten or not macv:
        messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ thông tin.")
        return

    if not selected_maso:
        messagebox.showwarning("Cảnh báo", "Không xác định giáo viên đang sửa.")
        return

    hoi = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn lưu thay đổi không?")
    if not hoi:
        return

    try:
        # ========= KIỂM TRA TRÙNG MÃ GV TRỪ CHÍNH NÓ =========
        cur.execute("""
            SELECT COUNT(*) 
            FROM GIAOVIEN 
            WHERE MaGV = ? AND MaGV <> ?
        """, (maso_moi, selected_maso))

        if cur.fetchone()[0] > 0:
            messagebox.showerror("Lỗi", "Mã giáo viên mới đã tồn tại. Vui lòng nhập mã khác.")
            return

        # ========= CẬP NHẬT =========
        cur.execute("""
            UPDATE GIAOVIEN
            SET MaGV=?, TenGV=?, SDT=?, NgaySinh=?, GioiTinh=?, MaCV=?
            WHERE MaGV=?
        """, (maso_moi, hoten, sdt, ngaysinh.strftime("%Y-%m-%d"), phai, macv, selected_maso))

        conn.commit()
        messagebox.showinfo("Thành công", "Cập nhật giáo viên thành công.")

        # Load lại danh sách
        load_du_lieu()

        # Chọn lại row mới sửa trong tree
        try:
            for iid in tree.get_children():
                vals = tree.item(iid, "values")
                if vals and vals[0] == maso_moi:
                    tree.selection_set(iid)
                    tree.focus(iid)
                    break
        except:
            pass

        Huy_tt()
        selected_maso = None

    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể cập nhật giáo viên:\n{e}")


def Huy_gv():
    hoi = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn hủy thao tác không?")
    if not hoi:
        return
    Huy_tt()
    messagebox.showinfo("Hủy", "Hủy thao tác thành công.")
    load_du_lieu()

def Thoat():
    if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn thoát không?"):
        try:
            conn.close()
        except:
            pass
        root.destroy()

def xuat_excel():
    if not cv_duoc_chon:
        messagebox.showwarning("Thông báo", "Vui lòng chọn lớp để xuất danh sách giáo viên!")
        return
    hoi = messagebox.askyesno("Xác nhận", f"Bạn có chắc chắn muốn xuất danh sách giáo viên {cv_duoc_chon} ra file Excel không?")
    if not hoi:
        return
    # Lấy dữ liệu hiện tại từ Treeview
    rows = [tree.item(item, "values") for item in tree.get_children()]
    if not rows:
        messagebox.showinfo("Thông báo", "Không có dữ liệu để xuất.")
        return


    # Chọn nơi lưu file
    file_path = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Excel files", "*.xlsx")],
        title="Lưu danh sách giáo viên",
        initialfile=f"DanhSachGV_{cv_duoc_chon}.xlsx"
    )
    if not file_path:
        return

    try:
        wb = Workbook()
        ws = wb.active
        ws.title = f"CV {cv_duoc_chon}"

        # Ghi tiêu đề theo Treeview
        headers = ["Mã GV", "Họ tên","SDT", "Ngày sinh", "Giới tính", "Mã CV"]
        ws.append(headers)

        # Ghi dữ liệu
        for row in rows:
            ws.append(row)

        # Căn chỉnh độ rộng cột tự động
        for col in ws.columns:
            max_length = max(len(str(cell.value)) if cell.value else 0 for cell in col)
            ws.column_dimensions[col[0].column_letter].width = max_length + 3

        wb.save(file_path)
        messagebox.showinfo("Thành công", f"Đã xuất danh sách giáo viên{cv_duoc_chon} ra file Excel thành công!")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể xuất file Excel:\n{e}")




# ==================================================== NÚT BẤM =================================================
frame_nut = tk.Frame(root) 
frame_nut.pack(pady=10, anchor="w", padx=10) 
 
btn_them = tk.Button(
    frame_nut, text="Thêm",
    font=("Times New Roman", 11),
    width=11,
    relief="ridge",
    cursor="hand2",
    command= them_gv
    )
btn_them.grid(row=0, column=0, padx=5) 

btn_xoa = tk.Button(
    frame_nut,  text="Xóa", 
    font=("Times New Roman", 11), 
    width=11, 
    relief="ridge",
    cursor="hand2",
    command= xoa_gv
    )
btn_xoa.grid(row=0, column=1, padx=5)


btn_sua = tk.Button(
    frame_nut, 
    text="Sửa", 
    font=("Times New Roman", 11), 
    width=11, 
    relief="ridge",
    cursor="hand2",
    command= sua_gv
    )
btn_sua.grid(row=0, column=2, padx=5)


btn_luu = tk.Button(
    frame_nut, 
    text="Lưu", 
    font=("Times New Roman", 11),
    relief="ridge",
    cursor="hand2",
    width=11, 
    command= luu_sua
    )
btn_luu.grid(row=0, column=3, padx=5)


btn_huy = tk.Button(
    frame_nut, text="Hủy", 
    font=("Times New Roman", 11), 
    width=11, 
    relief="ridge",
    cursor="hand2",
    command= Huy_gv
    )
btn_huy.grid(row=0, column=4, padx=5)


btn_thoat = tk.Button(
    frame_nut, 
    text="Thoát",
    font=("Times New Roman", 11), 
    width=11, 
    relief="ridge",
    cursor="hand2",
    command= Thoat
    )
btn_thoat.grid(row=0, column=5, padx=5)

btn_in_excel = tk.Button(
    frame_nut,
    text="In Danh Sách",
    font=("Times New Roman", 12),
    relief="ridge",
    cursor="hand2",
    command=xuat_excel
)
btn_in_excel.grid(row=1, column=5, padx=5, pady=5)

label_Soluong = tk.Label(
    frame_nut,
    text="(Số lượng học sinh)",
    font=("Times New Roman", 11, "bold"),
    bg="#F5F5F5"
)
label_Soluong.grid(row=1, column=0, columnspan=4, sticky="w", padx=5, pady=5)

#================================= FRAME TREEVIEW ==================================
lbl_ds = tk.Label(root, text="Danh sách giáo viên", font=("Times New Roman", 13, "bold"))
lbl_ds.pack(pady=5, anchor="w", padx=10)
#====== Treeview hiển thị danh sách học sinh ======


# ====== Frame chứa Treeview và thanh cuộn ======
frame_tree = tk.Frame(root)
frame_tree.pack(padx=10, pady=5, fill="both", expand=True)

# Thanh cuộn
thanhcuon_doc = tk.Scrollbar(frame_tree, orient="vertical")
thanhcuon_doc.pack(side="right", fill="y")

# Cấu hình Treeview
columns = ("Mã GV", "Họ tên", "SDT", "Ngày Sinh", "Giới tính","Mã Chức Vụ" )
tree = ttk.Treeview(frame_tree, columns=columns, show="headings", height=10, yscrollcommand=thanhcuon_doc.set)
thanhcuon_doc.config(command=tree.yview)

# Đặt tiêu đề cột 
for col in columns:
    tree.heading(col, text=col)

# Đặt kích thước cột 
tree.column("Mã GV", width=80, anchor="center")
tree.column("Họ tên", width=150)
tree.column("SDT", width=120, anchor="center")
tree.column("Ngày Sinh", width=80, anchor="center")
tree.column("Giới tính", width=100, anchor="center")
tree.column("Mã Chức Vụ", width=100, anchor="center")


tree.pack(fill="both", expand=True)
style = ttk.Style()
style.configure("Treeview",
                font=("Times New Roman", 11),
                rowheight=25)
style.configure("Treeview.Heading",
               font=("Times New Roman", 12, "bold"))



#=========================================== MÀU NỀN ========================================
# Màu nền form - Xám kem tinh tế
root.configure(bg="#F5F5F5")
frame_tt.configure(bg="#F5F5F5")
frame_nut.configure(bg="#F5F5F5")

# Màu tiêu đề - Slate đậm
lbl_tieu_de.configure(bg="#F5F5F5", fg="#0000FF")
lbl_ds.configure(bg="#F5F5F5",fg="#0000FF")

style = ttk.Style()
style.configure("Treeview",
                font=("Times New Roman", 11),
                rowheight=25,
                background="#FFFFFF",
                fieldbackground="#FFFFFF",
                foreground="#1E293B")

style.configure("Treeview.Heading",
               font=("Times New Roman", 12, "bold"),
               background="#64748B")

style.map("Treeview", background=[("selected", "#003366")])


# ====== Tải dữ liệu ban đầu ======
load_du_lieu()
root.mainloop()


