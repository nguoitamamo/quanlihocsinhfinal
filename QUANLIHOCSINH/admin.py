from operator import or_
from pstats import Stats
import re
from QUANLIHOCSINH import app, db
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
import models
from flask import redirect, request
import dao
from flask_login import current_user, logout_user
from flask import url_for

admin = Admin(app=app, name="E-commerce Administration", template_mode='bootstrap4')


class AdminView(ModelView):
    column_display_pk = True
    can_export = True

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role.__eq__(models.Role.Admin)


class ThongbaoView(AdminView):
    column_list = ['PermissionID', 'UserID']

    column_searchable_list = ['PermissionID', 'UserID']

    column_labels = {
        'PermissionID': 'Mã quyền',
        'UserID': 'Mã người dùng'
    }
    list_template = 'admin/thongbao.html'


from wtforms_sqlalchemy.fields import QuerySelectField


class ViewGiangVien(AdminView):
    column_list = ['MaGiangVien', 'MaMonHoc', 'Hocs']

    column_labels = {
        'MaGiangVien': 'Mã giảng viên',
        'MaMonHoc': 'Mã môn học',
        'Hocs': 'Danh sách lớp dạy'
    }
    form_columns = ['MaGiangVien', 'Hocs']


class ViewMonHocKhoi(AdminView):
    column_list = ['MaMonHoc', 'MaKhoi', 'MonHocs', 'Khois']

    # Các nhãn cho cột
    column_labels = {
        'MaMonHoc': 'Mã môn học',
        'MaKhoi': 'Mã khối'
    }

    form_columns = ['MaMonHoc', 'MaKhoi']
    list_template = 'admin/monhocandkhoi.html'


class ViewAccout(AdminView):
    column_searchable_list = ['TenDangNhap', 'id', 'NgayTao']

    column_labels = {
        'id': 'Mã người dùng',
        'TenDangNhap': 'Tên đăng nhập',
        'NgayTao': 'Ngày tạo',
        'Active': 'Trạng thái'

    }


class ThongTinUser(AdminView):
    column_list = ['Ho', 'Ten', 'NgaySinh', 'GioiTinh', 'DiaChi', 'Email']

    column_searchable_list = ['Ho', 'Ten', 'NgaySinh', 'GioiTinh', 'DiaChi', 'Email']

    column_labels = {
        'UserID': 'Mã người dùng',
        'Ho': 'Họ',
        'Ten': 'Tên',
        'NgaySinh': 'Ngày sinh',
        'GioiTinh': 'Giới tính',
        'DiaChi': 'Địa chỉ',
        'Email': 'Email'
    }


class ViewLop(AdminView):
    column_searchable_list = ['MaLop', 'TenLop']
    column_labels = {
        'MaLop': 'Mã lớp',
        'TenLop': 'Tên lớp',
        'SiSo': 'Sĩ số'
    }


class ViewLopHocSinh(AdminView):
    can_export = True
    column_list = ['MaLop', 'MaHocSinh', 'NamTaoLop']

    column_searchable_list = ['id', 'MaLop', 'MaHocSinh', 'NamTaoLop']

    column_labels = {
        'MaLop': 'Mã lớp',
        'MaHocSinh': 'Mã học sinh',
        'NamTaoLop': 'Ngày tạo'
    }


class ViewPerMission(AdminView):
    can_export = True

    column_searchable_list = ['Value']

    column_labels = {
        'PermissionID': 'Mã quyền',
        'Value': 'Quyền'
    }


class AuthenticatedView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role.__eq__(models.Role.Admin)


class LogoutView(AuthenticatedView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')


class ThongKeView(AuthenticatedView):
    @expose('/')
    def index(self):
        danh_sach_mon_hoc = dao.Load_MonHoc()
        danh_sach_hoc_ki = dao.load_hoc_ki()

        return self.render('admin/baocaothongke.html', danh_sach_mon_hoc=danh_sach_mon_hoc,
                           danh_sach_hoc_ki=danh_sach_hoc_ki)

    @expose('/submit', methods=["POST"])
    def submit(self):
        danh_sach_mon_hoc = dao.Load_MonHoc()
        danh_sach_hoc_ki = dao.load_hoc_ki()

        MonHoc = request.form.get('MonHoc')
        HocKi = request.form.get('HocKi')

        danh_sach_lop_hoc = dao.LoadLopHoc(MonHoc, HocKi)
        TenMonHoc = ""
        TenHocKi = ""
        TenNamHoc = ""
        ds_lop = []

        for MH in danh_sach_mon_hoc:
            if MonHoc == MH.MaMonHoc:
                TenMonHoc = MH.TenMonHoc
        for Hk in danh_sach_hoc_ki:
            if HocKi == Hk.MaHocKi:
                TenHocKi = Hk.TenHocKi
                TenNamHoc = Hk.NamHoc

        stt = 0
        for lop in danh_sach_lop_hoc:
            stt += 1
            soluongdat = dao.tinh_so_luong_dat_cua_lop(lop.MaLop, MonHoc, HocKi)
            tile = round((soluongdat / lop.SiSo) * 100, 2) if lop.SiSo != 0 else 0
            ds_lop.append([stt, lop.TenLop, lop.SiSo, soluongdat, tile])

        return self.render('admin/baocaothongke.html',
                           danh_sach_mon_hoc=danh_sach_mon_hoc,
                           danh_sach_hoc_ki=danh_sach_hoc_ki,
                           TenMonHoc=TenMonHoc,
                           TenHocKi=TenHocKi,
                           TenNamHoc=TenNamHoc,
                           Lop=ds_lop)




class MonHocKhoiView(AuthenticatedView):
    @expose('/')
    def index(self):
        monhoc_full = models.MonHoc.query.all()
        monhoc_khoi_data = (
            db.session.query(models.MonHoc_Khoi.Id, models.MonHoc_Khoi.MaKhoi, models.MonHoc_Khoi.MaMonHoc,
                             models.MonHoc.MaMonHoc, models.MonHoc.TenMonHoc, models.Khoi.MaKhoi, models.Khoi.TenKhoi)
            .join(models.Khoi, models.Khoi.MaKhoi == models.MonHoc_Khoi.MaKhoi)
            .join(models.MonHoc, models.MonHoc.MaMonHoc == models.MonHoc_Khoi.MaMonHoc).all())
        dskhoi = models.Khoi.query.all()

        return self.render('admin/monhoc_khoi.html',
                           monhoc_full=monhoc_full,
                           monhoc_khoi_data=monhoc_khoi_data,
                           dskhoi=dskhoi)

    @expose('/create_monhoc', methods=['POST'])
    def create_monhoc(self):
        ma_monhoc = request.form.get('MaMonHoc')
        ten_monhoc = request.form.get('TenMonHoc')
        monhoc = models.MonHoc(MaMonHoc=ma_monhoc, TenMonHoc=ten_monhoc)
        db.session.add(monhoc)
        db.session.commit()
        return redirect(url_for('.index'))

    @expose('/edit/monhoc/<ma_monhoc>', methods=['POST'])
    def edit_monhoc(self, ma_monhoc):

        ma_monhoc_new = request.form.get('MaMonHoc')
        ten_monhoc_new = request.form.get('TenMonHoc')

        if ma_monhoc_new and ten_monhoc_new:

            monhoc = models.MonHoc.query.filter_by(MaMonHoc=ma_monhoc).first()

            if monhoc:
                monhoc.MaMonHoc = ma_monhoc_new
                monhoc.TenMonHoc = ten_monhoc_new

                db.session.commit()

        return redirect(url_for('.index'))

    @expose('/timkiem_monhoc', methods=['POST'])
    def timkiem_monhoc(self):

        inputsearch = request.form.get('inputsearch')


        monhoc_khoi_data = (
            db.session.query(
                models.MonHoc_Khoi.Id,
                models.MonHoc_Khoi.MaKhoi,
                models.MonHoc_Khoi.MaMonHoc,
                models.MonHoc.MaMonHoc,
                models.MonHoc.TenMonHoc,
                models.Khoi.MaKhoi,
                models.Khoi.TenKhoi
            )
            .join(models.Khoi, models.Khoi.MaKhoi == models.MonHoc_Khoi.MaKhoi)
            .join(models.MonHoc, models.MonHoc.MaMonHoc == models.MonHoc_Khoi.MaMonHoc)
            .filter(
                or_(
                    models.MonHoc_Khoi.MaMonHoc.ilike(f"%{inputsearch}%"),
                    models.MonHoc_Khoi.MaKhoi.ilike(f"%{inputsearch}%"),

                ))
            .all())

        monhoc_full = models.MonHoc.query.all()

        return self.render('admin/monhoc_khoi.html',
                           monhoc_full=monhoc_full,
                           monhoc_khoi_data=monhoc_khoi_data, inputsearch=inputsearch,
                           dskhoi=models.Khoi.query.all()
                           )

    @expose('/create', methods=['POST'])
    def create_monhoc_khoi(self):
        ma_monhoc = request.form.get('MaMonHoc')
        ma_khoi = request.form.get('MaKhoi')

        new_monhoc_khoi = models.MonHoc_Khoi(MaMonHoc=ma_monhoc, MaKhoi=ma_khoi)
        db.session.add(new_monhoc_khoi)
        db.session.commit()

        return redirect(url_for('.index'))

    @expose('/delete/<int:id>', methods=['POST'])
    def delete_monhoc_khoi(self, id):

        record = models.MonHoc_Khoi.query.get(id)
        if record:
            db.session.delete(record)
            db.session.commit()
        return redirect(url_for('.index'))

    @expose('/edit/monhoc_khoi/<ma_monhoc>/<ma_khoi>', methods=['POST'])
    def edit_monhoc_khoi(self, ma_monhoc, ma_khoi):

        ma_monhoc_new = request.form.getlist('MaMonHoc')
        print(ma_monhoc_new)
        makhoi_new = request.form.getlist('MaKhoi')
        print(makhoi_new)
        if ma_monhoc_new and makhoi_new:

            monhoc = models.MonHoc_Khoi.query.filter_by(MaMonHoc=ma_monhoc_new, MaKhoi=makhoi_new).first()

            if monhoc:
                monhoc_full = models.MonHoc.query.all()
                monhoc_khoi_data = models.MonHoc_Khoi.query.all()
                dskhoi = models.Khoi.query.all()

                return self.render('admin/monhoc_khoi.html',
                                   monhoc_full=monhoc_full,
                                   monhoc_khoi_data=monhoc_khoi_data,
                                   dskhoi=dskhoi, error="Mã khối và mã môn học này đã tồn tại!"
                                   )
            else:
                monhoc = models.MonHoc_Khoi.query.filter_by(MaMonHoc=ma_monhoc, MaKhoi=ma_khoi).first()
                monhoc.MaMonHoc = ma_monhoc_new
                monhoc.MaKhoi = makhoi_new

                db.session.commit()

        return redirect(url_for('.index'))


class ViewQuanLiLop_MonHoc(AuthenticatedView):
    @expose('/')
    def index(self):

        dsgiangvien = models.GiangVien.query.all()
        return self.render('admin/quanlilophoc_mon.html', dskhoi=dao.LoadKhoi(),
                           danh_sach_hoc_ki=dao.load_hoc_ki(),  monhoc_full=models.MonHoc.query.all(), giangvien= dsgiangvien
                           )

    @expose('/load_info_lop', methods=['POST'])
    def load_info_lop(self , malop = None, makhoi = None, mahocki = None, error = None):

        if not (malop and makhoi and mahocki):
            data = request.form
            malop = data.get('dslop', '')
            makhoi = data.get('dskhoi', '')
            mahocki = data.get('hocki', '')
            error = None

        infolop = (db.session.query(models.Hoc.MaMonHoc , models.Hoc.MaLop, models.Hoc.MaGiangVien, models.MonHoc.TenMonHoc)
                   .join(models.MonHoc, models.MonHoc.MaMonHoc == models.Hoc.MaMonHoc)
                   .filter(models.Hoc.MaLop == malop, models.Hoc.MaHocKi == mahocki).all())


        dsgiangvien = models.GiangVien.query.all()
        return self.render('admin/quanlilophoc_mon.html', dskhoi=dao.LoadKhoi(),
                           infolop = infolop, malop = malop,
                           danh_sach_hoc_ki=dao.load_hoc_ki(),mahocki = mahocki,
                           monhoc_full=models.MonHoc.query.all(),
                           giangvien=dsgiangvien,
                           error=error
                           )

    @expose('/addmonhoctolop', methods=['POST'])
    def addmonhoctolop(self):
        data = request.form
        malop = data.get('malop', '')
        mahocki = data.get('mahocki', '')
        mamonhoc = data.get('MaMonHoc', '')
        magiangvien = data.get('giangvien', '')

        match = re.search(r'L(\d+)', malop)
        tenkhoi = match.group(1) if match else None

        makhoi = models.Khoi.query.filter(models.Khoi.TenKhoi == tenkhoi).first().MaKhoi

        contidion = models.MonHoc_Khoi.query.filter( models.MonHoc_Khoi.MaMonHoc == mamonhoc, models.MonHoc_Khoi.MaKhoi == makhoi ).first()

        if contidion:

            hocEd = models.Hoc.query.filter( models.Hoc.MaLop == malop, models.Hoc.MaMonHoc == mamonhoc,
                                             models.Hoc.MaGiangVien == magiangvien, models.Hoc.MaHocKi == mahocki ).all()
            if hocEd:
                return self.load_info_lop(malop=malop, makhoi=makhoi, mahocki=mahocki,
                                          error="Lớp đã học môn này!!")
            else:
                hoc = models.Hoc( MaLop = malop, MaMonHoc = mamonhoc, MaGiangVien = magiangvien,MaHocKi = mahocki)

                db.session.add(hoc)
                db.session.commit()
                return self.load_info_lop(malop=malop, makhoi=makhoi, mahocki=mahocki,
                                          error = None)

        else:
            return self.load_info_lop(malop=malop, makhoi=makhoi, mahocki=mahocki, error = "Khối " + tenkhoi + " không được phép học môn này")




class ViewThayDoiQuyDinh(AuthenticatedView):

    @expose('/')
    def index(self):
        return self.render('admin/thaydoiquydinh.html',
                           max_ss_lop=app.config["MAX_SS_LOP"],
                           si_so_min=app.config["SI_SO_MIN"],
                           si_so_max=app.config["SI_SO_MAX"])


    @expose('/change_max_ss_lop', methods=['POST'])
    def change_max_ss_lop(self):
        if request.method == 'POST':
            max_ss_lop = int(request.form['max_ss_lop'])
            app.config["MAX_SS_LOP"] = max_ss_lop
            return redirect(url_for('.index'))



    @expose('/change_age_range', methods=['POST'])
    def change_age_range(self):
        if request.method == 'POST':
            si_so_min = int(request.form['si_so_min'])
            si_so_max = int(request.form['si_so_max'])
            app.config["SI_SO_MIN"] = si_so_min
            app.config["SI_SO_MAX"] = si_so_max
            return redirect(url_for('.index'))



class ViewMonHoc(AdminView):
    column_list = ['MaMonHoc', 'TenMonHoc']

    column_labels = {
        'MaMonHoc': 'Mã môn học',
        'TenMonHoc': 'Tên môn học',
    }

    form_columns = ['MaMonHoc', 'TenMonHoc']


admin.add_view(ViewAccout(models.Account, db.session, name="Tài khoản"))
admin.add_view(ThongTinUser(models.UserInfor, db.session, name="Thông tin tài khoản"))
admin.add_view(ViewGiangVien(models.GiangVien, db.session, name="Giảng viên"))
admin.add_view(ViewLop(models.Lop, db.session, name="Lớp"))
admin.add_view(ViewLopHocSinh(models.LopHocSinh, db.session, name="Lớp-Học sinh"))
admin.add_view(ViewPerMission(models.Permission, db.session, name="Quyền"))

admin.add_view(ThongbaoView(models.PermissionUser, db.session, name="Thông báo "))

admin.add_view(ThongKeView(name='Thống kê'))
admin.add_view(LogoutView(name='Đăng xuất'))

admin.add_view(ViewMonHoc(models.MonHoc, db.session, name="Môn học"))
admin.add_view(MonHocKhoiView(name='Quản lí môn học của khối'))
admin.add_view(ViewQuanLiLop_MonHoc(name='Quản lí môn học của lớp'))
admin.add_view(ViewThayDoiQuyDinh(name='Thay đổi quy định') )

