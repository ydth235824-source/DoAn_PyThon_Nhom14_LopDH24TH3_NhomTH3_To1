CREATE DATABASE QLGV
ON(
    NAME = QLGV_mdf,
    FILENAME = 'D:\Python\QLGV.mdf',
    SIZE = 15MB,
    MAXSIZE = 50MB,
    FILEGROWTH = 5MB
)
LOG ON(
    NAME = QLGV_log,
    FILENAME = 'D:\Python\QLGV.ldf',
    SIZE = 15MB,
    MAXSIZE = 50MB,
    FILEGROWTH = 5MB
);
GO
USE QLGV;
GO

-- Bảng Chức vụ
CREATE TABLE CHUCVU(
    MaCV NVARCHAR(50) PRIMARY KEY,
    TenCV NVARCHAR(50)
);

-- Bảng Lương
CREATE TABLE LUONG(
    MaLuong CHAR(5) PRIMARY KEY,
    HeSoLuong DECIMAL(10,2),
    LuongCoBan FLOAT,
    PhuCap FLOAT
);

-- Bảng Giáo viên
CREATE TABLE GIAOVIEN (
    MaGV CHAR(10) PRIMARY KEY,
    TenGV NVARCHAR(100) NOT NULL,
    SDT VARCHAR(15) UNIQUE,
    NgaySinh DATE,
    GioiTinh NVARCHAR(5),
    MaLuong CHAR(5),
    MaCV NVARCHAR(50),
    FOREIGN KEY (MaCV) REFERENCES CHUCVU(MaCV),
    FOREIGN KEY (MaLuong) REFERENCES LUONG(MaLuong)
);

-- Bảng Môn học
CREATE TABLE MONHOC (
    MaMH CHAR(10) PRIMARY KEY,
    TenMH NVARCHAR(50) NOT NULL,
    SoTiet INT NOT NULL
);

-- Bảng Lớp
CREATE TABLE LOP (
    MaLop CHAR(10) PRIMARY KEY,
    TenLop NVARCHAR(50) NOT NULL,
    NamHoc CHAR(9) NOT NULL,
    Khoi TINYINT NOT NULL,
    MaGV CHAR(10),
    FOREIGN KEY (MaGV) REFERENCES GIAOVIEN(MaGV)
);

-- Giáo viên dạy môn học
CREATE TABLE GV_MH(
    MaGV CHAR(10) ,
    MaMH CHAR(10)  ,
    PRIMARY KEY (MaGV,MaMH),
    FOREIGN KEY (MaGV) REFERENCES GIAOVIEN(MaGV),
    FOREIGN KEY (MaMH) REFERENCES MONHOC(MaMH)
);

-- Giáo viên dạy lớp
CREATE TABLE GV_LOP(
    MaGV CHAR(10),
    MaLop CHAR(10),
    PRIMARY KEY(MaGV, MaLop),
    FOREIGN KEY (MaGV) REFERENCES GIAOVIEN(MaGV),
    FOREIGN KEY (MaLop) REFERENCES LOP(MaLop)
);
Select * From CHUCVU;
Select * From LUONG;
Select * From MONHOC;
Select * From GIAOVIEN;
Select * From LOP;
Select * From GV_MH;
Select * From GV_LOP;



