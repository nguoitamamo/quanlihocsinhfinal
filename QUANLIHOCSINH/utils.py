from itertools import islice

from QUANLIHOCSINH import app, db
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import pandas as pd
from math import ceil
from dao import  LoadLop

dataframe1 = pd.read_excel(os.getcwd() + '\\templates\\layout\\infor.xlsx', dtype={"Số điện thoại": str})


def rand_Pass_Confirm_Email():
    return str(random.randint(10000, 99999))


def checklistdiem(listdiem):
    for diem in listdiem:
        try:
            if float(diem) > 10.0 or float(diem) < 0.0:
                return False
        except ValueError:
            if diem == '':
                return True
            return False
    return True


def check_diem(diem15phut, diem1tiet, diemthi):
    if not checklistdiem(diem15phut):
        return False
    if not checklistdiem(diem1tiet):
        return False

    try:
        if float(diemthi) > 10.0:
            return False
    except ValueError:
        if diemthi == '':
            return True
        return False

    return True


info = {
    "diem15phut": ["9.0", "9.0", "11"],
    "diem1tiet": ["", "", ""],
    "diemthi": "10.0"
}


def Send_Email(subject, content, email_rec):
    email = "2251052130truong@ou.edu.vn"
    passw = "18072004@Hnt"
    email_send = email_rec
    mail_content = content

    smtp_session = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_session.starttls()
    smtp_session.login(email, passw)  #

    message = MIMEMultipart()
    message['From'] = email
    message['To'] = email_send
    message['Subject'] = subject
    message.attach(MIMEText(mail_content, 'plain'))

    smtp_session.sendmail(email, email_send, message.as_string())

    smtp_session.quit()
    print("Email đã được gửi thành công!")


def LoadFile(file):
    df = pd.read_excel(file, dtype={"Số điện thoại": str})

    dic = []

    for i, row in df.iterrows():
        dic.append({
            "STT": row["STT"],
            "Họ": row["Họ"],
            "Tên": row["Tên"],
            "Điểm": row["Điểm"],
            "Ngày sinh": row["Ngày sinh"],
            "Giới tính": row["Giới tính"],
            "Địa chỉ": row["Địa chỉ"],
            "Email": row["Email"],
            "Số điện thoại": row["Số điện thoại"]
        })

    return dic


def Pagination_Data(data, page, total_record=10):
    total_page = ceil(len(data) / total_record)

    start = (page - 1) * total_record
    end = start + total_record

    df_page = list(islice(data, start, end))

    return {
        "dic_page": df_page,
        "total_page": total_page
    }


def SaveIntoSession(dshocsinh):
    dic = []

    for hs in dshocsinh:
        for info in hs:
            dic.append({
                "UserID": info.UserID,
                "Họ": info.Ho,
                "Tên": info.Ten,
                "Điểm": info.DiemTbDauVao,
                "Ngày sinh": info.NgaySinh,
                "Giới tính": info.GioiTinh,
                "Địa chỉ": info.DiaChi
            })

    return dic




def GetDsHocSinh( listmalop , listmahocsinh, mamonhoc, namhoc):

    dshocsinhnew = []
    listmahocsinhnew = []

    for k in range(len(listmalop)):

        if len(listmahocsinh) != 0:
            listmahocsinhnew=listmahocsinh[listmalop[k]]


        diemhk1 = LoadLop(malop = listmalop[k] , listmahocsinh=listmahocsinhnew, key="diem", mamonhoc=mamonhoc, mahocki='1_' + namhoc)
        diemhk2 = LoadLop(malop = listmalop[k] , listmahocsinh=listmahocsinhnew, key="diem", mamonhoc=mamonhoc, mahocki='2_' + namhoc)

        max_15phut_hocki1 = diemhk1['max15phut']  if diemhk1['max15phut'] > 1 else 1
        max_1tiet_hocki1 = diemhk1['max1tiet'] if diemhk1['max1tiet'] > 1 else 1
        max_15phut_hocki2 = diemhk2['max15phut'] if diemhk2['max15phut'] > 1 else 1
        max_1tiet_hocki2 = diemhk2['max1tiet']  if diemhk2['max1tiet'] > 1 else 1


        for i in range(len(diemhk1['diemdshocsinh'])):

            dshocsinhnew.append(DiemHocSinh(mahocsinh=diemhk1['diemdshocsinh'][i]['MaHocSinh'],
                                               hoten=diemhk1['diemdshocsinh'][i]['HoTen'],
                                               listdiem15phuthk1=diemhk1['diemdshocsinh'][i]['15phut'],
                                               listdiem1tiethk1=diemhk1['diemdshocsinh'][i]['1tiet'],
                                               listdiem15phuthk2=diemhk2['diemdshocsinh'][i]['15phut'],
                                               listdiem1tiethk2=diemhk2['diemdshocsinh'][i]['1tiet'],
                                               listdiemcuoikihk1=diemhk1['diemdshocsinh'][i]['diemthi'],
                                               listdiemcuoikihk2=diemhk2['diemdshocsinh'][i]['diemthi'],
                                               max_15phut_hocki1=max_15phut_hocki1,
                                               max_1tiet_hocki1=max_1tiet_hocki1,
                                               max_15phut_hocki2=max_15phut_hocki2,
                                               max_1tiet_hocki2=max_1tiet_hocki2,
                                               malop = listmalop[k]
                                               ))

    return dshocsinhnew

def DiemHocSinh(mahocsinh, hoten, listdiem15phuthk1, listdiem1tiethk1, listdiemcuoikihk1,
                listdiem15phuthk2, listdiem1tiethk2, listdiemcuoikihk2,
                max_15phut_hocki1, max_1tiet_hocki1,
                max_15phut_hocki2, max_1tiet_hocki2,
                malop):
    return {
        "MaHocSinh": mahocsinh,
        "HoTen": hoten,
        "TBHK1": CalTinhDiemTb(listdiem15phuthk1,
                               listdiem1tiethk1,
                               listdiemcuoikihk1,
                               max15phut=max_15phut_hocki1,
                               max1tiet=max_1tiet_hocki1),

        "TBHK2": CalTinhDiemTb(listdiem15phuthk2,
                               listdiem1tiethk2,
                               listdiemcuoikihk2,
                               max15phut=max_15phut_hocki2,
                               max1tiet=max_1tiet_hocki2),
        "MaLop": malop
    }


def CalTinhDiemTb(listdiem15phut, listdiem1tiet, listcuoiki, max15phut, max1tiet):
    tb15phut = 0
    tb1tiet = 0
    cuoiki = 0

    if len(listdiem15phut) > 0:
        tb15phut = sum(listdiem15phut) / max15phut
    if len(listdiem1tiet):
        tb1tiet = sum(listdiem1tiet) / max1tiet
    if len(listcuoiki) > 0:
        cuoiki = listcuoiki[0]

    return round(tb15phut * app.config["15PHUT"] + tb1tiet * app.config["1TIET"] + cuoiki * app.config["CUOIKY"], 1)



def CheckHsExitsInSession(session, mahocsinh):
    return [hs for hs in session if hs["MaHocSinh"] == mahocsinh]



if __name__ == '__main__':
    with app.app_context():
        flag = check_diem(info["diem15phut"], info["diem1tiet"], info["diemthi"])
        print(f"Điểm hợp lệ: {flag}")

