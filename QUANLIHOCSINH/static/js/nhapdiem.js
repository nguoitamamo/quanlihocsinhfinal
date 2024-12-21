const errorContainer = document.querySelector('.alert-danger');
const errorText = document.getElementById('error');


function Column15phut(state) {


    fetch(`${state}`, {
        method: 'put',
        headers: {
            'Content-Type': 'application/json',
        }
    }).then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.reload();
            } else {
                errorText.innerText = data.error; // Hiển thị nội dung lỗi
                errorContainer.style.display = "block";
            }
        })


}


function Column1tiet(state) {


    fetch(`/user/nhapdiem/column1tiet/${state}`, {
        method: 'put',
        headers: {
            'Content-Type': 'application/json',
        }
    }).then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.reload();
            } else {
                errorText.innerText = data.error; // Hiển thị nội dung lỗi
                errorContainer.style.display = "block";
            }
        })

}


function GetDataTable() {


    const socot15phut = parseInt(document.getElementById("socot15phut").textContent.trim());
    const socot1tiet = parseInt(document.getElementById("socot1tiet").textContent.trim());


    diemhocsinh = []

    $('#scoreTable tr').each(function () {

        var maHocSinh = ''

        maHocSinh = $(this).attr("id");

        var hoten = $(this).find("td").eq(1).text();

        if (maHocSinh === "") {
            return; // Skip this row if maHocSinh is empty
        }

        console.log(hoten)
        var diem15phut = [];
        for (var i = 2; i < 2 + socot15phut; i++) {
            var diem = $(this).find("td").eq(i).find("input").val();
            if (diem && diem.trim() !== "") {
                diem15phut.push(diem.trim());
            } else {
                diem15phut.push('');
            }
        }


        var diem1tiet = [];
        for (var i = 2 + socot15phut; i < 2 + socot15phut + socot1tiet; i++) {
            var diem = $(this).find("td").eq(i).find("input").val();
            if (diem && diem.trim() !== "") {
                diem1tiet.push(diem.trim());
            } else {
                diem1tiet.push('');
            }
        }

        var diemthi = $(this).find("td").last().find("input").val();
        if (!diemthi) {
            diemthi = "";
        }

        if (maHocSinh && maHocSinh.trim() !== "" && (diem15phut.length > 0 || diem1tiet.length > 0 || diemthi !== "")) {
            diemhocsinh.push({
                maHocSinh: maHocSinh,
                hoten: hoten,
                diem15phut: diem15phut,
                diem1tiet: diem1tiet,
                diemthi: diemthi
            });
        }


    });
    return diemhocsinh
}


// function Suggestion(keyword, searchInput, suggestionsList, field) {
//
//     let malop = 'lop'
//
//     if (field === 'monhoc') {
//         const lop = document.getElementById('dslop');
//         malop = lop.value;
//
//         console.log("Monhoc" + malop);
//     }
//
//     fetch(`/user/nhapdiem/lop/search/${keyword}/${field}/${malop}`)
//         .then(response => response.json())
//         .then(data => {
//
//             suggestionsList.innerHTML = '';
//
//             data.forEach(suggestionEdOfKeyword => {
//                 suggestionEdOfKeyword.forEach(item => {
//
//                     const li = document.createElement('li');
//                     li.textContent = item;
//
//                     li.addEventListener('click', () => {
//                         searchInput.value = item;
//                         suggestionsList.innerHTML = '';
//
//
//                         for (let i = 0; i < lop.options.length; i++) {
//                             if (lop.options[i].text === searchInputLop.value) {
//                                 lop.selectedIndex = i;
//
//                                 break;
//                             }
//                         }
//                         LoadMonOfLop();
//
//                     });
//
//                     suggestionsList.appendChild(li);
//                 });
//             });
//         })
// }


function updateMonHocOfLop(obj) {


    const malop = obj.options[obj.selectedIndex].value;

    LoadMonOfLop(malop);


}


function saveTableData(state) {

    errorContainer.style.display = "none";

    diemhocsinh = GetDataTable()

    console.log(diemhocsinh)

    const dslop = document.getElementById('dslop');
    const dsmonhoc = document.getElementById('dsmonhoc');
    const hocki = document.getElementById('hocki');

    const malop = dslop.options[dslop.selectedIndex].value;
    const mamonhoc = dsmonhoc.options[dsmonhoc.selectedIndex].value;
    const mahocki = hocki.options[hocki.selectedIndex].value;


    fetch(`/user/nhapdiem/diemdshocsinh/${malop}/${mamonhoc}/${mahocki}/${state}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            diemdshocsinh: diemhocsinh
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {

                errorText.innerText = data.state;


            } else {
                errorText.innerText = data.state;

            }
            errorContainer.style.display = "block";
        })


}

function LoadALlLopEdHocInHocKiEd(obj, feild) {

    const value = obj.options[obj.selectedIndex].value;

    fetch(`/user/nhapdiem/loadalllopedinhockied/${value}/${feild}`, {
        method: 'post',
        headers: {
            'Content-Type': 'application/json',
        }
    }).then(response => response.json())
        .then(data => {
            if (data.success) {
                const lophocinhockis = data.lophocinhockis;
                const dskhoi = data.dskhoi;

                const khois = document.getElementById('dskhoi');
                khois.innerHTML = '';

                dskhoi.forEach(khoi => {

                    const option = document.createElement("option");
                    option.text = `${khoi['TenKhoi']}`;
                    option.value = `${khoi['MaKhoi']}`;
                    khois.add(option);
                });

                AddLopEdInHocKi(lophocinhockis);

                // MonOfLop(allmon);


            } else {
                alert(data.error);
            }
        })


}

function AddLopEdInHocKi(lophocinhockis) {

    const LopSelect = document.querySelector("select[name='dslop']");

    LopSelect.innerHTML = '';

    lophocinhockis.forEach(malop => {

        const option = document.createElement("option");
        option.text = `${malop.slice(1).split('_')[0]}`;
        option.value = `${malop}`;
        LopSelect.add(option);
    });

}

function LoadAlLLopOfKhoi(obj) {

    const hocki = document.getElementById('hocki');
    var mahocki = '0'
    if ( hocki !== undefined) {
        mahocki = hocki.options[hocki.selectedIndex].value;
    }


    const tenkhoi = obj.options[obj.selectedIndex].textContent;

    fetch(`/user/nhapdiem/loadalllopofkhoi/${mahocki}/${tenkhoi}`, {
        method: 'post',
        headers: {
            'Content-Type': 'application/json',
        }
    }).then(response => response.json())
        .then(data => {
            if (data.success) {
                const lophocinhockis = data.lophocinhockis;

                AddLopEdInHocKi(lophocinhockis);


            } else {
                alert(data.error);
            }
        })

}


function LoadMonOfLop(malop) {


    fetch(`/user/nhapdiem/loadmon/${malop}`, {
        method: 'post',
        headers: {
            'Content-Type': 'application/json',
        }
    }).then(response => response.json())
        .then(data => {
            if (data.success) {
                const monhocs = data.dsmonhoc;

                MonOfLop(monhocs);

            } else {
                alert(data.error);
            }
        })

}


function MonOfLop(monhocs) {
    const monHocSelect = document.querySelector("select[name='dsmonhoc']");

    monHocSelect.innerHTML = '';

    monhocs.forEach(mon => {

        const option = document.createElement("option");
        option.text = `${mon.TenMonHoc}`;
        option.value = `${mon.MaMonHoc}`
        monHocSelect.add(option);
    });
}

function CancelluuAndLuuTam() {
    const input = document.getElementById('searchhocsinh').value;
    if (input !== "") {
        document.getElementById('btnLuuTam').disabled = true;
        document.getElementById('btnLuu').disabled = true;
    } else {
        document.getElementById('btnLuuTam').disabled = false;
        document.getElementById('btnLuu').disabled = false;
    }
}


// // Hàm kích hoạt lại các nút sau khi dừng nhập liệu
// function RestoreButtons() {
//     // Cho phép các nút hoạt động trở lại nếu input không còn trống
//     const inputValue = document.getElementById('searchhocsinh').value.trim();
//     if (inputValue !== '') {
//         document.getElementById('btnLuuTam').disabled = false;
//         document.getElementById('btnLuu').disabled = false;
//     }
// }