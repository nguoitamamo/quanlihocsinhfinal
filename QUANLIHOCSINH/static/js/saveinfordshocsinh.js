const errorContainer = document.querySelector('.alert-danger');
const errorText = document.getElementById('error');


function UpdateSdt(stt, obj) {


    fetch('/user/uploaddanhsachhocsinh/updatesdt', {
        method: 'put',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            STT: stt,
            sdt: obj.value
        })
    })


}


function RemoveHocSinh(stt) {

    fetch(`/user/uploaddanhsachhocsinh/removehocsinh/${stt}`, {
        method: 'delete',
        headers: {
            'Content-Type': 'application/json',
        },
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const row = document.getElementById(`hs${stt}`);
                if (row) {
                    row.remove();
                }
            } else {
                errorText.innerText = "Xóa thất bại. Vui lòng thử lại!";
                errorContainer.style.display = "block";
            }
        })

}


function SaveInforDshocsinh() {


    fetch('/user/uploaddanhsachhocsinh/savedshocsinh', {
        method: 'post',
        headers: {
            'Content-Type': 'application/json',
        }
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


function RemoveHS(MaHocSinh, malop) {

    const dskhoi = document.getElementById('dskhoi');

    const makhoi = dskhoi.options[dskhoi.selectedIndex].value;

    fetch(`/user/dieuchinhdanhsachlop/removehocsinh/${malop}/${MaHocSinh}/${makhoi}`, {
        method: 'post',
        headers: {
            'Content-Type': 'application/json',
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const row = document.getElementById(`${MaHocSinh}`);
                if (row) {
                    row.remove();
                }
                window.location.reload();
            } else {
                errorText.innerText = "Xóa thất bại. Vui lòng thử lại!";
                errorContainer.style.display = "block";
            }
        })
}

function CheckAddHocSinh(hocsinhid, obj) {

    if (obj.checked) {
        console.log(hocsinhid);
        fetch(`/user/dieuchinhdanhsachlop/addhocsinh/${hocsinhid}`, {
            method: 'post',
            headers: {
                'Content-Type': 'application/json',
            }
        })
    } else {
        fetch(`/user/dieuchinhdanhsachlop/removehocsinh/${hocsinhid}`, {
            method: 'post',
            headers: {
                'Content-Type': 'application/json',
            }
        })
    }


}


function AddHocSinhToLop(malop) {

    const dskhoi = document.getElementById('dskhoi');
    const makhoi = dskhoi.options[dskhoi.selectedIndex].value;

    fetch(`/user/dieuchinhdanhsachlop/addhocsinh/ds/${malop}/${makhoi}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }

    }).then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.reload();
            } else {

                const errorContainer = document.querySelector('.alert-danger');
                const errorText = document.getElementById('error');
                errorText.innerText = data.error;
                errorContainer.style.display = "block";
            }
        })

}

window.onload = function () {
    const checkboxes = document.querySelectorAll('.form-check-input');
    checkboxes.forEach(checkbox => {
        checkbox.checked = false;
    });
}


function SelectKhoi(obj) {


    alert(obj.value);

    fetch(`/user/dieuchinhdanhsachlop/khoi/${obj.value}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }

    }).then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.reload();
            }
        })

}


function DevisionClassBegin0() {

    fetch('/user/dieuchinhdanhsachlop/sapxeptudau', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    }).then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.reload();
            }
        })

}


// function CheckAddAllHocSinh(obj) {
//
//     // if( obj.checked) {
//         const dschecbox = document.querySelectorAll('.form-check-input-creatlop');
//
//         dschecbox.forEach(checkbox => {
//             checkbox.checked = obj.checked;
//
//             const checkboxId = checkbox.getAttribute('id')
//
//             if (checkboxId) {
//                 CheckAddHocSinh(checkboxId, checkbox)
//             }
//         });
//     // }
//
//
// }


function CreateLopWithDsHocSinh() {

    const tenlop = document.getElementById('tenlop').value.trim();
    fetch(`/user/dieuchinhdanhsachlop/taolop/ds/${tenlop}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },

    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.reload();
            }
        })

}


function FindOfCondition() {
    const selectcondition = document.getElementById('selectcondition').value;
    const textcondition = document.getElementById('textcondition').value.trim();


    const value = parseFloat(textcondition);


    const rows = document.querySelectorAll('.createlop tbody tr');

    rows.forEach(row => {
        const diemCell = row.querySelector('.diem');
        if (!diemCell) return;

        const diem = parseFloat(diemCell.textContent);

        let match = false;
        switch (selectcondition) {
            case '1':
                match = diem > value;
                break;
            case '2':
                match = diem < value;
                break;
            case '3':
                match = diem >= value;
                break;
            case '4':
                match = diem <= value;
                break;
        }

        if (match) {
            row.classList.add('highlight-row');
        } else {
            row.classList.remove('highlight-row');
        }
    });
}





