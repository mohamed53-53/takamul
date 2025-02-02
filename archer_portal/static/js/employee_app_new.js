const cssAnimationList = {
    cssSlideH: {
        prefixCss: 'animate__animated animate__faster',
        fwdShowCss: 'animate__slideInLeft',
        fwdHideCss: 'animate__slideOutRight',
        bckShowCss: 'animate__slideInRight',
        bckHideCss: 'animate__slideOutLeft',
    }, cssSlideV: {
        prefixCss: 'animate__animated animate__faster',
        fwdShowCss: 'animate__slideInDown',
        fwdHideCss: 'animate__slideOutDown',
        bckShowCss: 'animate__slideInUp',
        bckHideCss: 'animate__slideOutUp',
    }, cssFade: {
        prefixCss: 'animate__animated animate__faster',
        fwdShowCss: 'animate__fadeIn',
        fwdHideCss: 'animate__fadeOut',
        bckShowCss: 'animate__fadeIn',
        bckHideCss: 'animate__fadeOut',
    }, cssFadeSlideH: {
        prefixCss: 'animate__animated animate__faster',
        fwdShowCss: 'animate__fadeInLeft',
        fwdHideCss: 'animate__fadeOutRight',
        bckShowCss: 'animate__fadeInRight',
        bckHideCss: 'animate__fadeOutLeft',
    }, cssFadeSlideV: {
        prefixCss: 'animate__animated animate__faster',
        fwdShowCss: 'animate__fadeInDown',
        fwdHideCss: 'animate__fadeOutDown',
        bckShowCss: 'animate__fadeInUp',
        bckHideCss: 'animate__fadeOutUp',
    }, cssFadeSlideCorner1: {
        prefixCss: 'animate__animated animate__faster',
        fwdShowCss: 'animate__fadeInTopLeft',
        fwdHideCss: 'animate__fadeOutBottomRight',
        bckShowCss: 'animate__fadeInBottomRight',
        bckHideCss: 'animate__fadeOutTopLeft',
    }, cssFadeSlideCorner2: {
        prefixCss: 'animate__animated animate__faster',
        fwdShowCss: 'animate__fadeInBottomLeft',
        fwdHideCss: 'animate__fadeOutTopRight',
        bckShowCss: 'animate__fadeInTopRight',
        bckHideCss: 'animate__fadeOutBottomLeft',
    }, cssBounce: {
        prefixCss: 'animate__animated animate__faster',
        fwdShowCss: 'animate__bounceIn',
        fwdHideCss: 'animate__bounceOut',
        bckShowCss: 'animate__bounceIn',
        bckHideCss: 'animate__bounceOut',
    }, cssBounceSlideH: {
        prefixCss: 'animate__animated animate__faster',
        fwdShowCss: 'animate__bounceInLeft',
        fwdHideCss: 'animate__bounceOutRight',
        bckShowCss: 'animate__bounceInRight',
        bckHideCss: 'animate__bounceOutLeft',
    }, cssBounceSlideV: {
        prefixCss: 'animate__animated animate__faster',
        fwdShowCss: 'animate__bounceInDown',
        fwdHideCss: 'animate__bounceOutDown',
        bckShowCss: 'animate__bounceInUp',
        bckHideCss: 'animate__bounceOutUp',
    }, cssBackSlideH: {
        prefixCss: 'animate__animated animate__faster',
        fwdShowCss: 'animate__backInLeft',
        fwdHideCss: 'animate__backOutRight',
        bckShowCss: 'animate__backInRight',
        bckHideCss: 'animate__backOutLeft',
    }, cssBackSlideV: {
        prefixCss: 'animate__animated animate__faster',
        fwdShowCss: 'animate__backInDown',
        fwdHideCss: 'animate__backOutDown',
        bckShowCss: 'animate__backInUp',
        bckHideCss: 'animate__backOutUp',
    }, cssFlipH: {
        prefixCss: 'animate__animated animate__faster',
        fwdShowCss: 'animate__flipInY',
        fwdHideCss: 'animate__flipOutY',
        bckShowCss: 'animate__flipInY',
        bckHideCss: 'animate__flipOutY',
    }, cssFlipV: {
        prefixCss: 'animate__animated animate__faster',
        fwdShowCss: 'animate__flipInX',
        fwdHideCss: 'animate__flipOutX',
        bckShowCss: 'animate__flipInX',
        bckHideCss: 'animate__flipOutX',
    }, cssLightspeed: {
        prefixCss: 'animate__animated animate__faster',
        fwdShowCss: 'animate__lightSpeedInLeft',
        fwdHideCss: 'animate__lightSpeedOutRight',
        bckShowCss: 'animate__lightSpeedInRight',
        bckHideCss: 'animate__lightSpeedOutLeft',
    }, cssRotate: {
        prefixCss: 'animate__animated animate__faster',
        fwdShowCss: 'animate__rotateIn',
        fwdHideCss: 'animate__rotateOut',
        bckShowCss: 'animate__rotateIn',
        bckHideCss: 'animate__rotateOut',
    }, cssRotateClock: {
        prefixCss: 'animate__animated animate__faster',
        fwdShowCss: 'animate__rotateInDownLeft',
        fwdHideCss: 'animate__rotateOutDownLeft',
        bckShowCss: 'animate__rotateInUpLeft',
        bckHideCss: 'animate__rotateOutUpLeft',
    }, cssRotateAntiClock: {
        prefixCss: 'animate__animated animate__faster',
        fwdShowCss: 'animate__rotateInDownRight',
        fwdHideCss: 'animate__rotateOutDownRight',
        bckShowCss: 'animate__rotateInUpRight',
        bckHideCss: 'animate__rotateOutUpRight',
    }, cssZoom: {
        prefixCss: 'animate__animated animate__faster',
        fwdShowCss: 'animate__zoomIn',
        fwdHideCss: 'animate__zoomOut',
        bckShowCss: 'animate__zoomIn',
        bckHideCss: 'animate__zoomOut',
    }
}

const cssColors = ["--sw-border-color", "--sw-toolbar-btn-color", "--sw-toolbar-btn-background-color", "--sw-anchor-default-primary-color", "--sw-anchor-default-secondary-color", "--sw-anchor-active-primary-color", "--sw-anchor-active-secondary-color", "--sw-anchor-done-primary-color", "--sw-anchor-done-secondary-color", "--sw-anchor-disabled-primary-color", "--sw-anchor-disabled-secondary-color", "--sw-anchor-anchor-error-primary-color", "--sw-anchor-anchor-error-secondary-color", "--sw-anchor-anchor-warning-primary-color", "--sw-anchor-anchor-warning-secondary-color", "--sw-progress-color", "--sw-progress-background-color", "--sw-loader-color", "--sw-loader-background-color", "--sw-loader-background-wrapper-color"];

const presetColors = {
    "Blue (Default)": {
        "--sw-toolbar-btn-background-color": "#009EF7",
        "--sw-anchor-default-primary-color": "#f8f9fa",
        "--sw-anchor-default-secondary-color": "#b0b0b1",
        "--sw-anchor-active-primary-color": "#009EF7",
        "--sw-anchor-active-secondary-color": "#ffffff",
        "--sw-anchor-done-primary-color": "#90d4fa",
        "--sw-anchor-done-secondary-color": "#fefefe",
        "--sw-progress-color": "#009EF7",
        "--sw-loader-color": "#009EF7",
    }, "Green": {
        "--sw-border-color": "#eeeeee",
        "--sw-toolbar-btn-color": "#ffffff",
        "--sw-toolbar-btn-background-color": "#008931",
        "--sw-anchor-default-primary-color": "#f8f9fa",
        "--sw-anchor-default-secondary-color": "#b0b0b1",
        "--sw-anchor-active-primary-color": "#78c043",
        "--sw-anchor-active-secondary-color": "#ffffff",
        "--sw-anchor-done-primary-color": "#588835",
        "--sw-anchor-done-secondary-color": "#c2c2c2",
        "--sw-anchor-disabled-primary-color": "#f8f9fa",
        "--sw-anchor-disabled-secondary-color": "#dbe0e5",
        "--sw-anchor-error-primary-color": "#dc3545",
        "--sw-anchor-error-secondary-color": "#ffffff",
        "--sw-anchor-warning-primary-color": "#ffc107",
        "--sw-anchor-warning-secondary-color": "#ffffff",
        "--sw-progress-color": "#78c043",
        "--sw-progress-background-color": "#f8f9fa",
        "--sw-loader-color": "#78c043",
        "--sw-loader-background-color": "#f8f9fa",
        "--sw-loader-background-wrapper-color": "rgba(255, 255, 255, 0.7)",
    }, "Yellow": {
        "--sw-border-color": "#eeeeee",
        "--sw-toolbar-btn-color": "#ffffff",
        "--sw-toolbar-btn-background-color": "#e4a707",
        "--sw-anchor-default-primary-color": "#f8f9fa",
        "--sw-anchor-default-secondary-color": "#b0b0b1",
        "--sw-anchor-active-primary-color": "#fbbd19",
        "--sw-anchor-active-secondary-color": "#ffffff",
        "--sw-anchor-done-primary-color": "#e4a707",
        "--sw-anchor-done-secondary-color": "#dbe0e5",
        "--sw-anchor-disabled-primary-color": "#f8f9fa",
        "--sw-anchor-disabled-secondary-color": "#dbe0e5",
        "--sw-anchor-error-primary-color": "#dc3545",
        "--sw-anchor-error-secondary-color": "#ffffff",
        "--sw-anchor-warning-primary-color": "#ffc107",
        "--sw-anchor-warning-secondary-color": "#ffffff",
        "--sw-progress-color": "#fbbd19",
        "--sw-progress-background-color": "#f8f9fa",
        "--sw-loader-color": "#fbbd19",
        "--sw-loader-background-color": "#f8f9fa",
        "--sw-loader-background-wrapper-color": "rgba(255, 255, 255, 0.7)",
    }, "Red": {
        "--sw-border-color": "#eeeeee",
        "--sw-toolbar-btn-color": "#ffffff",
        "--sw-toolbar-btn-background-color": "#f44336",
        "--sw-anchor-default-primary-color": "#f8f9fa",
        "--sw-anchor-default-secondary-color": "#b0b0b1",
        "--sw-anchor-active-primary-color": "#f44336",
        "--sw-anchor-active-secondary-color": "#ffffff",
        "--sw-anchor-done-primary-color": "#f8877f",
        "--sw-anchor-done-secondary-color": "#fefefe",
        "--sw-anchor-disabled-primary-color": "#f8f9fa",
        "--sw-anchor-disabled-secondary-color": "#dbe0e5",
        "--sw-anchor-error-primary-color": "#dc3545",
        "--sw-anchor-error-secondary-color": "#ffffff",
        "--sw-anchor-warning-primary-color": "#ffc107",
        "--sw-anchor-warning-secondary-color": "#ffffff",
        "--sw-progress-color": "#f44336",
        "--sw-progress-background-color": "#f8f9fa",
        "--sw-loader-color": "#f44336",
        "--sw-loader-background-color": "#f8f9fa",
        "--sw-loader-background-wrapper-color": "rgba(255, 255, 255, 0.7)",
    }, "Lite Blue": {
        "--sw-border-color": "#eeeeee",
        "--sw-toolbar-btn-color": "#ffffff",
        "--sw-toolbar-btn-background-color": "#0cb6d8",
        "--sw-anchor-default-primary-color": "#f8f9fa",
        "--sw-anchor-default-secondary-color": "#b0b0b1",
        "--sw-anchor-active-primary-color": "#00d5ff",
        "--sw-anchor-active-secondary-color": "#ffffff",
        "--sw-anchor-done-primary-color": "#0cb6d8",
        "--sw-anchor-done-secondary-color": "#dbe0e5",
        "--sw-anchor-disabled-primary-color": "#f8f9fa",
        "--sw-anchor-disabled-secondary-color": "#dbe0e5",
        "--sw-anchor-error-primary-color": "#dc3545",
        "--sw-anchor-error-secondary-color": "#ffffff",
        "--sw-anchor-warning-primary-color": "#ffc107",
        "--sw-anchor-warning-secondary-color": "#ffffff",
        "--sw-progress-color": "#0dcaf0",
        "--sw-progress-background-color": "#f8f9fa",
        "--sw-loader-color": "#0dcaf0",
        "--sw-loader-background-color": "#f8f9fa",
        "--sw-loader-background-wrapper-color": "rgba(255, 255, 255, 0.7)",
    }, "Dark": {
        "--sw-border-color": "#eeeeee",
        "--sw-toolbar-btn-color": "#ffffff",
        "--sw-toolbar-btn-background-color": "#0a2730",
        "--sw-anchor-default-primary-color": "#757575",
        "--sw-anchor-default-secondary-color": "#b0b0b1",
        "--sw-anchor-active-primary-color": "#000000",
        "--sw-anchor-active-secondary-color": "#ffffff",
        "--sw-anchor-done-primary-color": "#333333",
        "--sw-anchor-done-secondary-color": "#aaaaaa",
        "--sw-anchor-disabled-primary-color": "#f8f9fa",
        "--sw-anchor-disabled-secondary-color": "#dbe0e5",
        "--sw-anchor-error-primary-color": "#dc3545",
        "--sw-anchor-error-secondary-color": "#ffffff",
        "--sw-anchor-warning-primary-color": "#ffc107",
        "--sw-anchor-warning-secondary-color": "#ffffff",
        "--sw-progress-color": "#0a2730",
        "--sw-progress-background-color": "#f8f9fa",
        "--sw-loader-color": "#0a2730",
        "--sw-loader-background-color": "#f8f9fa",
        "--sw-loader-background-wrapper-color": "rgba(255, 255, 255, 0.7)",
    }
}

function displayColors() {
    let html = '';
    const cmpStyle = window.getComputedStyle(document.documentElement);

    cssColors.forEach(col => {
        let color = cmpStyle.getPropertyValue(col).trim();
        html += `<div class="col-sm-2 mt-2">
                <input type="color" class="form-control form-control-color color-picker" id="${col}" value="${color}" title="${col}">
              </div>`;

    })

    $('#color-list').html(html);
}

function loadColorList() {
    $.each(presetColors, function (key, objColors) {
        $('#theme_colors').append($('<option/>', {
            value: key, text: key, 'data-colors': window.btoa(JSON.stringify(objColors))
        }));
    });
}

function applyColors(colorObj) {
    colorObj = JSON.parse(window.atob(colorObj));
    $.each(colorObj, function (key, val) {
        document.documentElement.style.setProperty(key, val);
    });

    displayColors();
}


function onCancel() {
    // Reset wizard
    $('#employee_wizard').smartWizard("reset");
}

function onConfirm() {
    const urlParams = new URLSearchParams(window.location.search);
    const pageSize = urlParams.get('app');
    db.transaction('r', db.tables, () => {
        return Promise.all(db.tables.map(table => table.toArray()
            .then(rows => ({table: table.name, rows: rows}))));
    }).then(function (jsondb) {
        $.ajax({
            url: '/job/app/submit',
            type: 'post',
            dataType: 'json',
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify({
                'application_token': pageSize, 'csrfmiddlewaretoken': '{{ csrf_token }}', 'db': JSON.stringify(jsondb)
            }),
            success: function (ress) {
                $('#btnFinish').hide();
                $('#btnFinish').hide();
                $('.sw-btn-prev').hide(); // show the button extra only in the last page

                document.getElementById('last_step_row').innerText = ''
                document.getElementById('last_step_row').innerHTML = '<div class="col-3">\n' + '                                                                    <img src="https://img.icons8.com/color/96/000000/ok--v2.png"\n' + '                                                                         class="fit-image"/>\n' + '                                                                </div>'
            }
        })
    });

}

function showConfirm() {
    const name = $('#first-name').val() + ' ' + $('#last-name').val();
    const products = $('#sel-products').val();
    const shipping = $('#address').val() + ' ' + $('#state').val() + ' ' + $('#zip').val();
    let html = `<h4 class="mb-3-">Customer Details</h4>
                  <hr class="my-2">
                  <div class="row g-3 align-items-center">
                    <div class="col-auto">
                      <label class="col-form-label">Name</label>
                    </div>
                    <div class="col-auto">
                      <span class="form-text-">${name}</span>
                    </div>
                  </div>
        
                  <h4 class="mt-3">Products</h4>
                  <hr class="my-2">
                  <div class="row g-3 align-items-center">
                    <div class="col-auto">
                      <span class="form-text-">${products}</span>
                    </div>
                  </div>

                  <h4 class="mt-3">Shipping</h4>
                  <hr class="my-2">
                  <div class="row g-3 align-items-center">
                    <div class="col-auto">
                      <span class="form-text-">${shipping}</span>
                    </div>
                  </div>`;
    $("#order-details").html(html);
}

function addExperienceNewRow() {
    var table = document.getElementById("experience_table");
    var rowCount = table.rows.length;
    var cellCount = table.rows[0].cells.length;
    var row = table.insertRow(rowCount);
    for (var i = 0; i < cellCount; i++) {
        var cell = row.insertCell(i);
        cell.classList.add('pt-1');
        cell.classList.add('p-0');
        if (i < cellCount - 1) {
            if (i == 0) {
                cell.innerHTML = '<div class="col-12 m-0 p-1">\n' +
                    '                                                                                <input type="text" class="form-control"\n' +
                    '                                                                                       id="job_name"\n' +
                    '                                                                                       name="job_name" placeholder="Job Name"/>\n' +
                    '                                                                                <div class="valid-feedback">\n' +
                    '                                                                                    Looks good!\n' +
                    '                                                                                </div>\n' +
                    '                                                                                <div class="invalid-feedback">\n' +
                    '                                                                                    Please provide Job Name.\n' +
                    '                                                                                </div>\n' +
                    '                                                                            </div>'
            }
            if (i == 1) {
                cell.innerHTML = '<div class="col-12 m-0 p-1">\n' +
                    '                                                                                <input type="text" class="form-control tk_input"\n' +
                    '                                                                                       id="employer_name" name="employer_name"\n' +
                    '                                                                                       placeholder="Employer Name"/>\n' +
                    '                                                                                <div class="valid-feedback">\n' +
                    '                                                                                    Looks good!\n' +
                    '                                                                                </div>\n' +
                    '                                                                                <div class="invalid-feedback">\n' +
                    '                                                                                    Please provide Employer Name.\n' +
                    '                                                                                </div>\n' +
                    '                                                                            </div>'
            }
            if (i == 2) {
                cell.innerHTML = '<div class="col-12 m-0 p-1">\n' +
                    '                                                                                <div class="input-group date add-on">\n' +
                    '                                                                                    <input type="text" class="form-control date"\n' +
                    '                                                                                           id="date_from" name="date_from"\n' +
                    '                                                                                           placeholder="Date From"/>\n' +
                    '                                                                                    <div class="input-group-btn dup">\n' +
                    '                                                                                        <i class="fa fa-calendar"></i>\n' +
                    '                                                                                    </div>\n' +
                    '                                                                                </div>\n' +
                    '                                                                                <div class="valid-feedback">\n' +
                    '                                                                                    Looks good!\n' +
                    '                                                                                </div>\n' +
                    '                                                                                <div class="invalid-feedback">\n' +
                    '                                                                                    Please provide Date From.\n' +
                    '                                                                                </div>\n' +
                    '                                                                            </div>'
            }
            if (i == 3) {
                cell.innerHTML = '<div class="col-12 m-0 p-1">\n' +
                    '                                                                                <div class="input-group date add-on">\n' +
                    '                                                                                    <input type="text" class="form-control date"\n' +
                    '                                                                                           id="date_to" name="date_to"\n' +
                    '                                                                                           placeholder="Date To"/>\n' +
                    '                                                                                    <div class="input-group-btn dup">\n' +
                    '                                                                                        <i class="fa fa-calendar"></i>\n' +
                    '                                                                                    </div>\n' +
                    '                                                                                </div>\n' +
                    '                                                                                <div class="valid-feedback">\n' +
                    '                                                                                    Looks good!\n' +
                    '                                                                                </div>\n' +
                    '                                                                                <div class="invalid-feedback">\n' +
                    '                                                                                    Please provide Date To.\n' +
                    '                                                                                </div>\n' +
                    '                                                                            </div>'
            }
            if (i == 4) {
                cell.innerHTML = '<div class="col-12 m-0 p-1 include-doc">\n' +
                    '                                                                                <input type="file" name="service_certificate"\n' +
                    '                                                                                       placeholder="Service Certificate"\n' +
                    '                                                                                       accept=".doc,.docx,.xml,application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document"/>\n' +
                    '                                                                                <div class="valid-feedback">\n' +
                    '                                                                                    Looks good!\n' +
                    '                                                                                </div>\n' +
                    '                                                                                <div class="invalid-feedback">\n' +
                    '                                                                                    Please provide Attach.\n' +
                    '                                                                                </div>\n' +
                    '                                                                            </div>'
            }


        } else {
            cell.innerHTML = '<a type="button"\n' +
                '                                                                               class="btn btn-danger rounded experience_delete_btn mt-1 "\n' +
                '                                                                            >\n' +
                '                                                                                <i class="fa fa-trash text-white"></i>\n' +
                '                                                                            </a>';
        }
        $('.date_from').datepicker({
            format: "yyyy-mm-dd", endDate: '-3d', autoclose: true
        });
        $('.date_to').datepicker({
            format: "yyyy-mm-dd", endDate: '-3d', autoclose: true
        });

    }

    function deleteExperienceRow(ele) {
        var table = document.getElementById('experience_table');
        var rowCount = table.rows.length;

        if (ele) {
            //delete specific row

            ele.parentNode.parentNode.remove();
            // document.getElementById('experience_delete').value += ele.getAttribute('data') + ','

        } else {
            //delete last row
            table.deleteRow(rowCount - 1);
        }
    }

    $('.experience_delete_btn').click(function (eb) {
        deleteExperienceRow(this)
    })
    $(":file").filestyle({
        badge: true,
        btnClass: 'btn-primary',
        htmlIcon: '<i class="fa fa-cloud-upload"></i> ',
        placeholder: 'Select File',
        classList: 'col-6'
    });
    $('#date_from').datepicker({
        format: "yyyy-mm-dd", endDate: '-3d', autoclose: true
    });// Leave step event is used for validating the forms
    $('#date_to').datepicker({
        format: "yyyy-mm-dd", endDate: '-3d', autoclose: true
    });// Leave step event is used for validating the forms

}

function addFamilyRelationNewRow() {
    var table = document.getElementById("child_info_table");
    var rowCount = table.rows.length;
    var cellCount = table.rows[0].cells.length;
    var row = table.insertRow(rowCount);
    for (var i = 0; i < cellCount; i++) {
        var cell = row.insertCell(i);
        cell.classList.add('pt-1')
        cell.classList.add('p-0')
        if (i < cellCount - 1) {
            if (i == 0) {
                cell.innerHTML = '<div class="col-12 m-0 p-1">\n' +
                    '                                                                                <input type="text" class="form-control" id="child_name" placeholder="Name"/>\n' +
                    '                                                                                <div class="valid-feedback">\n' +
                    '                                                                                    Looks good!\n' +
                    '                                                                                </div>\n' +
                    '                                                                                <div class="invalid-feedback">\n' +
                    '                                                                                    Please provide Child Name.\n' +
                    '                                                                                </div>\n' +
                    '                                                                            </div>'
            }
            if (i == 1) {
                cell.innerHTML = '<div class="col-12 m-0 p-1">\n' +
                    '                                                                                <input type="text" class="form-control" id="child_id_number"\n' +
                    '                                                                                        placeholder="ID Number"\n' +
                    '                                                                                       oninput="this.value = this.value.replace(/[^0-9.]/g, \'\').replace(/(\\..*)\\./g, \'$1\');"/>\n' +
                    '                                                                                <div class="valid-feedback">\n' +
                    '                                                                                    Looks good!\n' +
                    '                                                                                </div>\n' +
                    '                                                                                <div class="invalid-feedback">\n' +
                    '                                                                                    Please provide Child ID Number.\n' +
                    '                                                                                </div>\n' +
                    '                                                                            </div>'
            }
            if (i == 2) {
                cell.innerHTML = '<div class="col-12 m-0 p-1">\n' +
                    '                                                                                <select class="form-control gender" id="child_gender"\n' +
                    '                                                                                        name="child_gender">\n' +
                    '                                                                                    <option value="male">Male</option>\n' +
                    '                                                                                    <option value="female">Female</option>\n' +
                    '                                                                                </select>\n' +
                    '                                                                                <div class="valid-feedback">\n' +
                    '                                                                                    Looks good!\n' +
                    '                                                                                </div>\n' +
                    '                                                                                <div class="invalid-feedback">\n' +
                    '                                                                                    Please provide Child Gender.\n' +
                    '                                                                                </div>\n' +
                    '                                                                            </div>'
            }
            if (i == 3) {
                cell.innerHTML = '<div class="col-12 m-0 p-1 input-group add-on">\n' +
                    '                                                                                <input type="text" class="form-control" id="child_birthdate"\n' +
                    '                                                                                        placeholder="Date"/>\n' +
                    '                                                                                <div class="input-group-btn dup">\n' +
                    '                                                                                    <i class="fa fa-calendar"></i>\n' +
                    '                                                                                </div>\n' +
                    '                                                                                <div class="valid-feedback">\n' +
                    '                                                                                    Looks good!\n' +
                    '                                                                                </div>\n' +
                    '                                                                                <div class="invalid-feedback">\n' +
                    '                                                                                    Please provide Child Date od Birth.\n' +
                    '                                                                                </div>\n' +
                    '                                                                            </div>'
            }
            if (i == 4) {
                cell.innerHTML = '<div class="col-12 m-0 p-1">\n' +
                    '                                                                                <input type="text" class="form-control" id="child_phone"\n' +
                    '                                                                                       placeholder="Phone"\n' +
                    '                                                                                       oninput="this.value = this.value.replace(/[^0-9.]/g, \'\').replace(/(\\..*)\\./g, \'$1\');"/>\n' +
                    '                                                                                <div class="valid-feedback">\n' +
                    '                                                                                    Looks good!\n' +
                    '                                                                                </div>\n' +
                    '                                                                                <div class="invalid-feedback">\n' +
                    '                                                                                    Please provide Child Phone.\n' +
                    '                                                                                </div>\n' +
                    '                                                                            </div>'
            }
            if (i == 5) {
                cell.innerHTML = '<div class="col-12 m-0 p-1 include-doc">\n' +
                    '                                                                                <input type="file" class="form-control" id="child_attach"\n' +
                    '                                                                                       placeholder="Select File"\n' +
                    '                                                                                       accept=".doc,.docx,.xml,application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document"/>\n' +
                    '                                                                                <div class="valid-feedback">\n' +
                    '                                                                                    Looks good!\n' +
                    '                                                                                </div>\n' +
                    '                                                                                <div class="invalid-feedback">\n' +
                    '                                                                                    Please provide Child Birth Attach.\n' +
                    '                                                                                </div>\n' +
                    '                                                                            </div>'
            }
        } else {
            cell.innerHTML = '<a type="button"\n' +
                '                                                                               class="btn btn-danger rounded family_delete_btn mt-1 "\n' +
                '                                                                            >\n' +
                '                                                                                <i class="fa fa-trash text-white"></i>\n' +
                '                                                                            </a>';
            cell.classList.add('spouse-del-btn');
        }
        $('.birthdate').datepicker({
            format: "yyyy-mm-dd", endDate: '-3d', autoclose: true
        });
        $('.child_birthdate').datepicker({
            format: "yyyy-mm-dd", endDate: '-3d', autoclose: true
        });
    }

    /* This method will delete a row */
    function deleteFamilyRelationRow(ele) {
        var table = document.getElementById('child_info_table');
        var rowCount = table.rows.length;

        if (ele) {
            //delete specific row
            ele.parentNode.parentNode.remove();
            // document.getElementById('family_delete').value += ele.getAttribute('data') + ','
        } else {
            //delete last row
            table.deleteRow(rowCount - 1);
        }
    }

    $('.family_delete_btn').click(function (eb) {
        deleteFamilyRelationRow(this)
    })
    $(":file").filestyle({
        badge: true,
        btnClass: 'btn-primary',
        htmlIcon: '<i class="fa fa-cloud-upload"></i> ',
        placeholder: 'Select File',
        classList: 'col-6'
    });
    $('#child_birthdate').datepicker({
        format: "yyyy-mm-dd", endDate: '-3d', autoclose: true
    });// Leave step event is used for validating the forms

}

const convertFileToBase64 = (file) => {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => resolve(reader.result);
        reader.onerror = (error) => reject(error);
    });
};

function limit(element) {
    if (document.getElementById("international_bank").checked) {

        var max_chars = 34;
    }
    if (!document.getElementById("international_bank").checked) {

        var max_chars = 24;
    }
    if (sessionStorage.getItem('country_code') === 'SA') {
        var max_chars = 24;

    }
    if (element.value.length > max_chars) {
        element.value = element.value.substr(0, max_chars);
    }
}

function internationalBankClick() {
    // Get the checkbox
    var checkBox = document.getElementById("international_bank");
    if (checkBox.checked == true) {
        document.getElementById("international_bank_div").classList.remove('d-none');
        document.getElementById("local_bank_div").classList.add('d-none');
        document.getElementById('iban_val_cond').innerText = ' IBAN length must be 34 characters'
        document.getElementById("bank_name").setAttribute('required', '""');
        document.getElementById("branch_name_code").setAttribute('required', '""');

    }
    if (checkBox.checked == false) {

        document.getElementById("international_bank_div").classList.add('d-none');
        document.getElementById("local_bank_div").classList.remove('d-none');
        document.getElementById('iban_val_cond').innerText = ' IBAN must start with SA \n IBAN length must be 24 characters'
        document.getElementById("bank_name").required = false;
        document.getElementById("branch_name_code").required = false;


    }
}

function NotHaveGosiClick() {
    // Get the checkbox
    var checkBox = document.getElementById("not_have_gosi");
    if (checkBox.checked == true) {
        document.getElementById("gosi_div").classList.add('d-none');
        document.getElementById("gosi_number").required = false;
        document.getElementById("gosi_start_date").required = false;
        sessionStorage.setItem('gosi', false)
        localStorage.removeItem('gosi_number');
        localStorage.removeItem('gosi_start_date');
    }
    if (checkBox.checked == false) {
        document.getElementById("gosi_div").classList.remove('d-none');
        document.getElementById("gosi_number").setAttribute('required', '""');
        document.getElementById("gosi_start_date").setAttribute('required', '""');

    }
}

$(function () {

    loadColorList();

    displayColors();

    // External Button Events
    $("#reset-btn").on("click", function () {
        // Reset wizard
        $('#employee_wizard').smartWizard("reset");
        return true;
    });

    $("#prev-btn").on("click", function () {
        // Navigate previous
        $('#employee_wizard').smartWizard("prev");
        return true;
    });

    $("#next-btn").on("click", function () {
        // Navigate next
        $('#employee_wizard').smartWizard("next");
        return true;
    });

    // Demo Button Events
    $("#btn-go-to").on("click", function () {
        // Go to step
        var step_index = $("#got_to_step").val() - 1;
        $('#employee_wizard').smartWizard("goToStep", step_index, false);
        return true;
    });

    $("#btn-go-to-forced").on("click", function () {
        // Go to step forced
        var step_index = $("#got_to_step").val() - 1;
        $('#employee_wizard').smartWizard("goToStep", step_index, true);
        return true;
    });

    $(".option-setting-checkbox").on("click", function () {
        // Change options
        let val = $(this).prop("checked");
        let options = {};
        switch ($(this).prop("id")) {
            case 'back_button_support':
                options = {
                    backButtonSupport: val
                }
                break;
            case 'key_navigation':
                options = {
                    keyboard: {
                        keyNavigation: val
                    }
                }
                break;
            case 'is_justified':
                options = {
                    justified: val
                }
                break;
            case 'anchor_navigation':
                options = {
                    anchor: {
                        enableNavigation: val
                    }
                }
                break;
            case 'enableNavigationAlways':
                options = {
                    anchor: {
                        enableNavigationAlways: val
                    }
                }
                break;
            case 'enableDoneState':
                options = {
                    anchor: {
                        enableDoneState: val
                    }
                }
                break;
            case 'markPreviousStepsAsDone':
                options = {
                    anchor: {
                        markPreviousStepsAsDone: val
                    }
                }
                break;
            case 'unDoneOnBackNavigation':
                options = {
                    anchor: {
                        unDoneOnBackNavigation: val
                    }
                }
                break;
            case 'enableDoneStateNavigation':
                options = {
                    anchor: {
                        enableDoneStateNavigation: val
                    }
                }
                break;
            case 'toolbar-showNextButton':
                options = {
                    toolbar: {
                        showNextButton: val
                    }
                }
                break;
            case 'toolbar-showPreviousButton':
                options = {
                    toolbar: {
                        showPreviousButton: val
                    }
                }
                break;
        }


        $('#employee_wizard').smartWizard("setOptions", options);
        return true;
    });

    $('input[type=radio][name=toolbar-position]').on('change', function () {
        let options = {
            toolbar: {
                position: $(this).val()
            }
        }
        $('#employee_wizard').smartWizard("setOptions", options);
    });

    $("#animation").on("change", function () {
        const anim = $(this).val();
        const cssAnim = cssAnimationList[anim];
        var options = {};

        if (cssAnim != undefined) {
            options = {
                transition: {
                    animation: 'css', ...cssAnim
                },
            };
        } else {
            options = {
                transition: {
                    animation: anim
                },
            };
        }

        $('#employee_wizard').smartWizard("setOptions", options);
        return true;
    });

    $("#theme_selector").on("change", function () {
        // Change theme
        var options = {
            theme: $(this).val()
        };
        $('#employee_wizard').smartWizard("setOptions", options);
        return true;
    });

    $(".color-picker").on("change", function () {
        // Set color
        document.documentElement.style.setProperty($(this).prop('id'), $(this).val());
        return true;
    });

    $("#btn-state-set").on("click", function () {
        // Set state
        let step_index = $("#state_step_selection").val() - 1;
        let state_name = $("#state_selection").val();
        $('#employee_wizard').smartWizard("setState", [step_index], state_name);
        return true;
    });

    $("#btn-state-unset").on("click", function () {
        // Unset state
        let step_index = $("#state_step_selection").val() - 1;
        let state_name = $("#state_selection").val();
        $('#employee_wizard').smartWizard("unsetState", [step_index], state_name);
        return true;
    });

    $("#theme_colors").on("change", function () {
        applyColors($('#theme_colors option:selected').data('colors'));
        return true;
    });
});

$(function () {
    $(":file").filestyle({
        badge: true,
        btnClass: 'btn-primary',
        htmlIcon: '<i class="fa fa-cloud-upload"></i> ',
        placeholder: 'Select File',
        classList: 'col-6',
    });
    $('#birthday').datepicker({
        format: "yyyy-mm-dd", endDate: '-6575d', autoclose: true
    });
//    $("#birthday-btn").onclick = function (ev) {
//        ev.preventDefault();
//        alert("hiii");
//        $('#birthday').datepicker();
//    };
//     $("#birthday-btn").on("click", function (ev) {
//        ev.preventDefault();
//        alert("hiii");
//        $('#birthday').datepicker();
//    });
    $('#gosi_start_date').datepicker({
        format: "yyyy-mm-dd", endDate: '-1d', autoclose: true
    });
    $('#graduate_date').datepicker({
        format: "yyyy-mm-dd", endDate: '-3d', autoclose: true
    });
    $('#expiration_date').datepicker({
        format: "yyyy-mm-dd", autoclose: true
    });
    $('#arrival_date').datepicker({
        format: "yyyy-mm-dd", endDate: '-3d', autoclose: true
    });
    $('#resid_issuance_date').datepicker({
        format: "yyyy-mm-dd", endDate: '-3d', autoclose: true
    });
    $('#father_birthdate').datepicker({
        format: "yyyy-mm-dd", endDate: '-6575d', autoclose: true
    });
    $('#mother_birthdate').datepicker({
        format: "yyyy-mm-dd", endDate: '-6575d', autoclose: true
    });
    $('#spouse_birthdate').datepicker({
        format: "yyyy-mm-dd", endDate: '-6575d', autoclose: true
    });
    $('#child_gender').datepicker({
        format: "yyyy-mm-dd", endDate: '-3d', autoclose: true
    });
    $('#child_birthdate').datepicker({
        format: "yyyy-mm-dd", endDate: '-3d', autoclose: true
    });
    $('#date_from').datepicker({
        format: "yyyy-mm-dd", endDate: '-3d', autoclose: true
    });
    $('#date_to').datepicker({
        format: "yyyy-mm-dd", endDate: '-3d', autoclose: true
    });

    $('#expiration_date').on('change', function (ev) {

        hijri_date = new Date(this.value).toLocaleDateString(
            'en-GB-u-ca-islamic-umalqura',
            {year: 'numeric', month: '2-digit', day: '2-digit'}
        );
        $('#expiration_date_in_hijri').val(hijri_date)
        localStorage.setItem('expiration_date_in_hijri', hijri_date);

    })

    function deleteFamilyRelationRow(ele) {
        var table = document.getElementById('child_info_table');
        var rowCount = table.rows.length;

        if (ele) {
            //delete specific row
            ele.parentNode.parentNode.remove();
            // document.getElementById('family_delete').value += ele.getAttribute('data') + ','
        } else {
            //delete last row
            table.deleteRow(rowCount - 1);
        }
    }

    $('.family_delete_btn').click(function (eb) {
        deleteFamilyRelationRow(this)
    })

    function onCancel() {
        // Reset wizard
        $('#employee_wizard').smartWizard("reset");

        // Reset form
        document.getElementById("form-1").reset();
        document.getElementById("form-2").reset();
        document.getElementById("form-3").reset();
        document.getElementById("form-4").reset();
    }


    $(function () {
        personal_form = document.forms["form-1"];
        education_form = document.forms["form-2"];
        gosi_form = document.forms["form-3"];
        sponsor_form = document.forms["form-4"];
        bank_form = document.forms["form-5"];
        family_form = document.forms["form-6"];
        child_table = $('#child_info_table')
        experience_table = $('#experience_table')

        personal_form['partner_name'].value = localStorage.getItem('name_en') ? localStorage.getItem('name_en') : personal_form['partner_name'].value;
        personal_form['name_ar'].value = localStorage.getItem('name_ar') ? localStorage.getItem('name_ar') : personal_form['name_ar'].value;
        personal_form['birthday'].value = localStorage.getItem('birthday') ? localStorage.getItem('birthday') : personal_form['birthday'].value;
        personal_form['country_id'].value = localStorage.getItem('country_id') ? localStorage.getItem('country_id') : personal_form['country_id'].value;
        personal_form['civil_id'].value = localStorage.getItem('civil_id') ? localStorage.getItem('civil_id') : personal_form['civil_id'].value;
        personal_form['passport_id'].value = localStorage.getItem('passport') ? localStorage.getItem('passport') : personal_form['passport_id'].value;
        personal_form['marital'].value = localStorage.getItem('marital') ? localStorage.getItem('marital') : personal_form['marital'].value;
        personal_form['gender'].value = localStorage.getItem('gender') ? localStorage.getItem('gender') : personal_form['gender'].value;
        // personal_form['national_address_attach'] = localStorage.getItem(national_address_attach);
        personal_form['partner_mobile'].value = localStorage.getItem('partner_mobile') ? localStorage.getItem('partner_mobile') : personal_form['partner_mobile'].value;
        personal_form['country_of_birth'].value = localStorage.getItem('country_of_birth') ? localStorage.getItem('country_of_birth') : personal_form['country_of_birth'].value;
        personal_form['place_of_birth'].value = localStorage.getItem('place_of_birth') ? localStorage.getItem('place_of_birth') : personal_form['place_of_birth'].value;
        personal_form['religion'].value = localStorage.getItem('religion') ? localStorage.getItem('religion') : personal_form['religion'].value;
        personal_form['email_from'].value = localStorage.getItem('email_from') ? localStorage.getItem('email_from') : personal_form['email_from'].value;

        education_form['graduate_date'].value = localStorage.getItem('graduate_date') ? localStorage.getItem('graduate_date') : education_form['graduate_date'].value;
        education_form['certificate'].value = localStorage.getItem('certificate') ? localStorage.getItem('certificate') : education_form['certificate'].value;
        education_form['study_field'].value = localStorage.getItem('study_field') ? localStorage.getItem('study_field') : education_form['study_field'].value;
        education_form['study_school'].value = localStorage.getItem('study_school') ? localStorage.getItem('study_school') : education_form['study_school'].value;

        gosi_form['not_have_gosi'].checked = localStorage.getItem('not_have_gosi') == 'true' ? true : false ? localStorage.getItem('not_have_gosi') : gosi_form['not_have_gosi'] == 'true' ? true : false;
        gosi_form['gosi_number'].value = localStorage.getItem('gosi_number') ? localStorage.getItem('gosi_number') : gosi_form['gosi_number'].value;
        gosi_form['gosi_start_date'].value = localStorage.getItem('gosi_start_date') ? localStorage.getItem('gosi_start_date') : gosi_form['gosi_start_date'].value;


        var checkBox_gosi = document.getElementById("not_have_gosi");
        if (checkBox_gosi.checked == true) {
            document.getElementById("gosi_div").classList.add('d-none');
            document.getElementById("gosi_number").required = false;
            document.getElementById("gosi_start_date").required = false;
            sessionStorage.setItem('gosi', false)
        }
        if (checkBox_gosi.checked == false) {
            document.getElementById("gosi_div").classList.remove('d-none');
            document.getElementById("gosi_number").setAttribute('required', '""');
            document.getElementById("gosi_start_date").setAttribute('required', '""');

        }


        sponsor_form['sponsor_name'].value = localStorage.getItem('sponsor_name') ? localStorage.getItem('sponsor_name') : sponsor_form['sponsor_name'].value;
        sponsor_form['sponsor_phone'].value = localStorage.getItem('sponsor_phone') ? localStorage.getItem('sponsor_phone') : sponsor_form['sponsor_phone'].value;
        sponsor_form['sponsor_address'].value = localStorage.getItem('sponsor_address') ? localStorage.getItem('sponsor_address') : sponsor_form['sponsor_address'].value;
        sponsor_form['residency_number'].value = localStorage.getItem('residency_number') ? localStorage.getItem('residency_number') : sponsor_form['residency_number'].value;
        sponsor_form['serial_number'].value = localStorage.getItem('serial_number') ? localStorage.getItem('serial_number') : sponsor_form['serial_number'].value;
        sponsor_form['resid_job_title'].value = localStorage.getItem('resid_job_title') ? localStorage.getItem('resid_job_title') : sponsor_form['resid_job_title'].value;
        sponsor_form['place_of_issuance'].value = localStorage.getItem('place_of_issuance') ? localStorage.getItem('place_of_issuance') : sponsor_form['place_of_issuance'].value;
        sponsor_form['expiration_date'].value = localStorage.getItem('expiration_date') ? localStorage.getItem('expiration_date') : sponsor_form['expiration_date'].value;
        hijri_date = new Date(sponsor_form['expiration_date'].value).toLocaleDateString(
            'en-GB-u-ca-islamic-umalqura',
            {year: 'numeric', month: '2-digit', day: '2-digit'}
        );
        $('#expiration_date_in_hijri').val(hijri_date)
        sponsor_form['arrival_date'].value = localStorage.getItem('arrival_date') ? localStorage.getItem('arrival_date') : sponsor_form['arrival_date'].value;
        sponsor_form['resid_issuance_date'].value = localStorage.getItem('resid_issuance_date') ? localStorage.getItem('resid_issuance_date') : sponsor_form['resid_issuance_date'].value;

        // bank_form['international_bank'].checked = localStorage.getItem('international_bank') === 'true' ? true : false;

        bank_form['bank_id'].value = localStorage.getItem('bank_id') ? localStorage.getItem('bank_id') : bank_form['bank_id'].value
        bank_form['bank_country_id'].value = localStorage.getItem('bank_country_id') ? localStorage.getItem('bank_country_id') : bank_form ['bank_country_id'].value
        bank_form['bank_name'].value = localStorage.getItem('bank_name') ? localStorage.getItem('bank_name') : bank_form['bank_name'].value
        bank_form['branch_name_code'].value = localStorage.getItem('branch_name_code') ? localStorage.getItem('branch_name_code') : bank_form ['branch_name_code'].value
        bank_form['iban_no'].value = localStorage.getItem('iban_no') ? localStorage.getItem('iban_no') : bank_form['iban_no'].value

        if (sessionStorage.getItem('marital') === 'single') {
            document.getElementById("spouse_name").required = false;
            document.getElementById("spouse_id_number").required = false;
            document.getElementById("spouse_birthdate").required = false;
            document.getElementById("spouse_phone").required = false;
            document.getElementById("spouse_family_attach").required = false;

            if (sessionStorage.getItem('country_code') !== 'SA') {
                $('#employee_wizard').smartWizard("setState", [5], "disable");
                $('#employee_wizard').smartWizard("setState", [5], "hide");
                document.getElementById("father_name").required = false;
                document.getElementById("father_id_number").required = false;
                document.getElementById("father_birthdate").required = false;
                document.getElementById("father_phone").required = false;
                document.getElementById("father_family_attach").required = false;

                document.getElementById("mother_name").required = false;
                document.getElementById("mother_id_number").required = false;
                document.getElementById("mother_birthdate").required = false;
                document.getElementById("mother_phone").required = false;
                document.getElementById("mother_family_attach").required = false;

                document.getElementById("spouse_name").required = false;
                document.getElementById("spouse_id_number").required = false;
                document.getElementById("spouse_birthdate").required = false;
                document.getElementById("spouse_phone").required = false;
                document.getElementById("spouse_family_attach").required = false;

                document.getElementById("child_name").required = false;
                document.getElementById("child_id_number").required = false;
                document.getElementById("child_birthdate").required = false;
                document.getElementById("child_phone").required = false;
                document.getElementById("child_attach").required = false;

                // return $('#employee_wizard').smartWizard("_showStep", 6);


            }
            if (sessionStorage.getItem('country_code') === 'SA') {
                $('#employee_wizard').smartWizard("setState", [5], "enable");
                $('#employee_wizard').smartWizard("setState", [5], "show");
                document.getElementById("father_row").classList.remove('d-none');
                document.getElementById("mother_row").classList.remove('d-none');

            }

        } else {
            $('#employee_wizard').smartWizard("setState", [5], "enable");
            $('#employee_wizard').smartWizard("unsetState", [5], "disable");
            $('#employee_wizard').smartWizard("setState", [5], "show");
            $('#employee_wizard').smartWizard("unsetState", [5], "hide");
            if (sessionStorage.getItem('country_code') !== 'SA') {
                document.getElementById("spouse_row").classList.remove('d-none');
                document.getElementById("children_row").classList.remove('d-none');
                // father fields
                document.getElementById("father_name").required = false;
                document.getElementById("father_id_number").required = false;
                document.getElementById("father_birthdate").required = false;
                document.getElementById("father_phone").required = false;
                document.getElementById("father_family_attach").required = false;

                document.getElementById("mother_name").required = false;
                document.getElementById("mother_id_number").required = false;
                document.getElementById("mother_birthdate").required = false;
                document.getElementById("mother_phone").required = false;
                document.getElementById("mother_family_attach").required = false;


            }
            if (sessionStorage.getItem('country_code') === 'SA') {
                document.getElementById("father_row").classList.remove('d-none');
                document.getElementById("mother_row").classList.remove('d-none');
                document.getElementById("spouse_row").classList.remove('d-none');
                document.getElementById("children_row").classList.remove('d-none');
            }

        }


        family_form['father_name'].value = localStorage.getItem('father_name') ? localStorage.getItem('father_name') : family_form['father_name'].value
        family_form['father_id_number'].value = localStorage.getItem('father_id_number') ? localStorage.getItem('father_id_number') : family_form['father_id_number'].value
        family_form['father_birthdate'].value = localStorage.getItem('father_birthdate') ? localStorage.getItem('father_birthdate') : family_form['father_birthdate'].value
        family_form['father_phone'].value = localStorage.getItem('father_phone') ? localStorage.getItem('father_phone') : family_form['father_phone'].value
        // bank_form['father_family_attach'].value = localStorage.getItem('iban_no') ? localStorage.getItem('iban_no') : bank_form['iban_no'].value

        family_form['mother_name'].value = localStorage.getItem('mother_name') ? localStorage.getItem('mother_name') : family_form['mother_name'].value
        family_form['mother_id_number'].value = localStorage.getItem('mother_id_number') ? localStorage.getItem('mother_id_number') : family_form['mother_id_number'].value
        family_form['mother_birthdate'].value = localStorage.getItem('mother_birthdate') ? localStorage.getItem('mother_birthdate') : family_form['mother_birthdate'].value
        family_form['mother_phone'].value = localStorage.getItem('mother_phone') ? localStorage.getItem('mother_phone') : family_form['mother_phone'].value
        // bank_form['father_family_attach'].value = localStorage.getItem('iban_no') ? localStorage.getItem('iban_no') : bank_form['iban_no'].value

        family_form['spouse_name'].value = localStorage.getItem('spouse_name') ? localStorage.getItem('spouse_name') : family_form['spouse_name'].value
        family_form['spouse_id_number'].value = localStorage.getItem('spouse_id_number') ? localStorage.getItem('spouse_id_number') : family_form['spouse_id_number'].value
        family_form['spouse_birthdate'].value = localStorage.getItem('spouse_birthdate') ? localStorage.getItem('spouse_birthdate') : family_form['spouse_birthdate'].value
        family_form['spouse_phone'].value = localStorage.getItem('spouse_phone') ? localStorage.getItem('spouse_phone') : family_form['spouse_phone'].value
        // bank_form['father_family_attach'].value = localStorage.getItem('iban_no') ? localStorage.getItem('iban_no') : bank_form['iban_no'].value
        if (JSON.parse(localStorage.getItem('child_list'))) {
            for (const item of JSON.parse(localStorage.getItem('child_list'))) {
                child_table.find('tbody').append('<tr>' +
                    '                                                                        <td class="pt-1 p-0">' +
                    '                                                                            <div class="col-12 m-0 p-1">' +
                    '                                                                                <input type="text" class="form-control" id="child_name" value="' + item['child_name'] + '"/>' +
                    '                                                                                <div class="valid-feedback">' +
                    '                                                                                    Looks good!' +
                    '                                                                                </div>' +
                    '                                                                                <div class="invalid-feedback">' +
                    '                                                                                    Please provide Child Name.' +
                    '                                                                                </div>' +
                    '                                                                            </div>' +
                    '                                                                        </td>' +
                    '                                                                        <td class="pt-1 p-0">' +
                    '                                                                            <div class="col-12 m-0 p-1">' +
                    '                                                                                <input type="text" class="form-control" id="child_id_number"' +
                    '                                                                                        value="' + item['child_id_number'] + '" oninput="this.value = this.value.replace(/[^0-9.]/g, \'\').replace(/(\\..*)\\./g, \'$1\');"/>' +
                    '                                                                                <div class="valid-feedback">' +
                    '                                                                                    Looks good!' +
                    '                                                                                </div>' +
                    '                                                                                <div class="invalid-feedback">' +
                    '                                                                                    Please provide Child ID Number.' +
                    '                                                                                </div>' +
                    '                                                                            </div>' +
                    '                                                                        </td>' +
                    '                                                                        <td class="pt-1 p-0">' +
                    '                                                                            <div class="col-12 m-0 p-1">' +
                    '                                                                                <select class="form-control gender" id="child_gender"' +
                    '                                                                                        name="child_gender">' +
                    '                                                                                    <option ' + (item["child_gender"] === "male" ? "selected=\"\"" : "") + 'value="male">Male</option>' +
                    '                                                                                    <option ' + (item["child_gender"] === "female" ? "selected=\"\"" : "") + 'value="female">Female</option>' +
                    '                                                                                </select>' +
                    '                                                                                <div class="valid-feedback">' +
                    '                                                                                    Looks good!' +
                    '                                                                                </div>' +
                    '                                                                                <div class="invalid-feedback">' +
                    '                                                                                    Please provide Child Gender.' +
                    '                                                                                </div>' +
                    '                                                                            </div>' +
                    '                                                                        </td>' +
                    '                                                                        <td class="pt-1 p-0">' +
                    '                                                                            <div class="col-12 m-0 p-1">' +
                    '                                                                                <input type="text" class="form-control " value="' + item["child_birthdate"] + '" id="child_birthdate"/>' +
                    '                                                                                <div class="valid-feedback">' +
                    '                                                                                    Looks good!' +
                    '                                                                                </div>' +
                    '                                                                                <div class="invalid-feedback">' +
                    '                                                                                    Please provide Child Date od Birth.' +
                    '                                                                                </div>' +
                    '                                                                            </div>' +
                    '                                                                        </td>' +
                    '                                                                        <td class="pt-1 p-0">' +
                    '                                                                            <div class="col-12 m-0 p-1">' +
                    '                                                                                <input type="text" class="form-control "  value="' + item["child_phone"] + '"  id="child_phone"' +
                    '                                                                                       oninput="this.value = this.value.replace(/[^0-9.]/g, \'\').replace(/(\\..*)\\./g, \'$1\');"/>' +
                    '                                                                                <div class="valid-feedback">' +
                    '                                                                                    Looks good!' +
                    '                                                                                </div>' +
                    '                                                                                <div class="invalid-feedback">' +
                    '                                                                                    Please provide Child Phone.' +
                    '                                                                                </div>' +
                    '                                                                            </div>' +
                    '                                                                        </td>' +
                    '                                                                        <td class="pt-1 p-0">' +
                    '                                                                            <div class="col-12 m-0 p-1 include-doc">' +
                    '                                                                                <input type="file" class="form-control"  id="child_attach" accept=".doc,.docx,.xml,application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document"//>' +
                    '                                                                                <div class="valid-feedback">' +
                    '                                                                                    Looks good!' +
                    '                                                                                </div>' +
                    '                                                                                <div class="invalid-feedback">' +
                    '                                                                                    Please provide Child Birth Attach.' +
                    '                                                                                </div>' +
                    '                                                                            </div>' +
                    '                                                                        </td>' +
                    '                                                                        <td class="pt-1 p-0">' +
                    '                                                                            <a type="button"' +
                    '                                                                               class="btn btn-danger rounded family_delete_btn mt-1 "' +
                    '                                                                            >' +
                    '                                                                                <i class="fa fa-trash text-white"></i>' +
                    '                                                                            </a>' +
                    '                                                                        </td>' +
                    '                                                                    </tr>');

            }

        }

        function deleteFamilyRelationRow(ele) {
            var table = document.getElementById('child_info_table');
            var rowCount = table.rows.length;

            if (ele) {
                //delete specific row
                ele.parentNode.parentNode.remove();
                // document.getElementById('family_delete').value += ele.getAttribute('data') + ','
            } else {
                //delete last row
                table.deleteRow(rowCount - 1);
            }
        }

        $('.family_delete_btn').click(function (eb) {
            deleteFamilyRelationRow(this)
        })
        if (JSON.parse(localStorage.getItem('jobs_list'))) {
            for (const item of JSON.parse(localStorage.getItem('jobs_list'))) {
                experience_table.find('tbody').append(
                    '<tr>' +
                    '                                                                        <td class="pt-1 p-0">' +
                    '                                                                            <div class="col-12  m-0 p-1">' +
                    '                                                                                <input type="text" class="form-control tk_input"' +
                    '                                                                                       value="' + item['job_name'] + '" id="job_name"' +
                    '                                                                                       name="job_name" placeholder="Job Name"/>' +
                    '                                                                                <div class="valid-feedback">' +
                    '                                                                                    Looks good!' +
                    '                                                                                </div>' +
                    '                                                                                <div class="invalid-feedback">' +
                    '                                                                                    Please provide Job Name.' +
                    '                                                                                </div>' +
                    '                                                                            </div>' +
                    '                                                                        </td>' +
                    '                                                                        <td class="pt-1 p-0">' +
                    '                                                                            <div class="col-12 m-0 p-1">' +
                    '                                                                                <input type="text" class="form-control tk_input"' +
                    '                                                                                       value="' + item['employer_name'] + '" id="employer_name" name="employer_name"' +
                    '                                                                                       placeholder="Employer Name"/>' +
                    '                                                                                <div class="valid-feedback">' +
                    '                                                                                    Looks good!' +
                    '                                                                                </div>' +
                    '                                                                                <div class="invalid-feedback">' +
                    '                                                                                    Please provide Employer Name.' +
                    '                                                                                </div>' +
                    '                                                                            </div>' +
                    '                                                                        </td>' +
                    '                                                                        <td class="pt-1 p-0">' +
                    '                                                                            <div class="col-12 m-0 p-1">' +
                    '                                                                                <div class="input-group date">' +
                    '                                                                                    <input type="text" class="form-control date tk_input"' +
                    '                                                                                           value="' + item['date_from'] + '" id="date_from" name="date_from"' +
                    '                                                                                           placeholder="Date From"/>' +
                    '                                                                                    <div class="input-group-addon">' +
                    '                                                                                        <span class="glyphicon glyphicon-th"/>' +
                    '                                                                                    </div>' +
                    '                                                                                </div>' +
                    '                                                                                <div class="valid-feedback">' +
                    '                                                                                    Looks good!' +
                    '                                                                                </div>' +
                    '                                                                                <div class="invalid-feedback">' +
                    '                                                                                    Please provide Date From.' +
                    '                                                                                </div>' +
                    '                                                                            </div>' +
                    '                                                                        </td>\n' +
                    '                                                                        <td class="pt-1 p-0">' +
                    '                                                                            <div class="col-12 m-0 p-1">' +
                    '                                                                                <div class="input-group date">' +
                    '                                                                                    <input type="text" class="form-control date tk_input"' +
                    '                                                                                           value="' + item['date_to'] + '" id="date_to" name="date_to"' +
                    '                                                                                           placeholder="Date To"/>' +
                    '                                                                                    <div class="input-group-addon">' +
                    '                                                                                        <span class="glyphicon glyphicon-th"/>' +
                    '                                                                                    </div>' +
                    '                                                                                </div>' +
                    '                                                                                <div class="valid-feedback">' +
                    '                                                                                    Looks good!' +
                    '                                                                                </div>' +
                    '                                                                                <div class="invalid-feedback">' +
                    '                                                                                    Please provide Date To.' +
                    '                                                                                </div>' +
                    '                                                                            </div>' +
                    '                                                                        </td>' +
                    '                                                                        <td class="pt-1 p-0">' +
                    '                                                                            <div class="col-12 m-0 p-1">' +
                    '                                                                                <input type="file" name="service_certificate" class="tk_input"' +
                    '                                                                                       placeholder="Service Certificate"/>' +
                    '                                                                                <div class="valid-feedback">' +
                    '                                                                                    Looks good!' +
                    '                                                                                </div>' +
                    '                                                                                <div class="invalid-feedback">' +
                    '                                                                                    Please provide Attach.' +
                    '                                                                                </div>' +
                    '                                                                            </div>' + '                                                                        </td>' +
                    '                                                                        <td class="pt-1 p-0">' +
                    '                                                                            <a type="button"' +
                    '                                                                               class="btn btn-danger rounded experience_delete_btn mt-1 "' +
                    '                                                                            >' +
                    '                                                                                <i class="fa fa-trash text-white"></i>' +
                    '                                                                            </a>' +
                    '                                                                        </td>' +
                    '                                                                    </tr>'
                );

            }

            function deleteExperienceRow(ele) {
                var table = document.getElementById('experience_table');
                var rowCount = table.rows.length;

                if (ele) {
                    //delete specific row

                    ele.parentNode.parentNode.remove();
                    // document.getElementById('experience_delete').value += ele.getAttribute('data') + ','

                } else {
                    //delete last row
                    table.deleteRow(rowCount - 1);
                }
            }

            $('.experience_delete_btn').click(function (eb) {
                deleteExperienceRow(this)
            })
            $(":file").filestyle({
                badge: true, btnClass: 'btn-primary', htmlIcon: '<span class="oi oi-folder"></span> '
            });
            $('#date_from').datepicker({
                format: "yyyy-mm-dd", endDate: '-3d', autoclose: true
            });// Leave step event is used for validating the forms
            $('#date_to').datepicker({
                format: "yyyy-mm-dd", endDate: '-3d', autoclose: true
            });// Leave step event is used for validating the forms

        }



        // Leave step event is used for validating the forms
        $("#employee_wizard").on("leaveStep", function (e, anchorObject, currentStepIdx, nextStepIdx, stepDirection) {
            // Validate only on forward movement
            if (stepDirection == 'forward') {
                let form = document.getElementById('form-' + (currentStepIdx + 1));
                if (form) {
                    if (!form.checkValidity()) {
                        form.classList.add('was-validated');
                        $('#employee_wizard').smartWizard("setState", [currentStepIdx], 'error');
                        $("#employee_wizard").smartWizard('fixHeight');
                        return false;
                    }
                    $('#employee_wizard').smartWizard("unsetState", [currentStepIdx], 'error');

                    if (form.id === 'form-5') {
                        if (form['iban_no'].value.trim() !== form['reconfirm_iban_no'].value.trim()) {
                            form.classList.add('was-validated');
                            $('#employee_wizard').smartWizard("setState", [currentStepIdx], 'error');
                            document.getElementById('iban_note').innerText = 'IBAN Confirm and IBAN not matched'
                            return false;
                        }
                        if (sessionStorage.getItem('country_code') === 'SA') {
                            if (form['iban_no'].value.trim().slice(0, 2) !== 'SA') {
                                $('#employee_wizard').smartWizard("setState", [currentStepIdx], 'error');
                                document.getElementById('iban_note').innerText = ' IBAN must start with SA \n IBAN length must be 24 characters'
                                return false;
                            } else if (form['iban_no'].value.trim().length !== 24 || form['reconfirm_iban_no'].value.trim().length != 24) {
                                $('#employee_wizard').smartWizard("setState", [currentStepIdx], 'error');
                                document.getElementById('iban_note').innerText = ' IBAN must start with SA \n IBAN length must be 24 characters'
                                return false;
                            }
                        }
                        if (!document.getElementById("international_bank").checked) {
                            if (form['iban_no'].value.trim().length !== 24 || form['reconfirm_iban_no'].value.trim().length !== 24) {
                                $('#employee_wizard').smartWizard("setState", [currentStepIdx], 'error');
                                document.getElementById('iban_note').innerText = ' IBAN must start with SA \n IBAN length must be 24 characters'
                                return false;
                            }
                        }
                        if (document.getElementById("international_bank").checked) {
                            if (form['iban_no'].value.trim().length !== 34 || form['reconfirm_iban_no'].value.trim().length !== 34) {
                                $('#employee_wizard').smartWizard("setState", [currentStepIdx], 'error');
                                return false;
                            }
                        }
                    }

                }


            }

        });

        // Step show event
        $("#employee_wizard").on("showStep", async function (e, anchorObject, stepIndex, stepDirection, stepPosition) {
            // Get step info from Smart Wizard
            if (sessionStorage.getItem('country_code') === 'SA') {
                $('#employee_wizard').smartWizard("setState", [3], "disable");
                $('#employee_wizard').smartWizard("setState", [3], "hide");
                $('#international_bank_row').addClass('d-none')
                $('#international_check_div').addClass('d-none')
                document.getElementById("bank_name").required = false;
                document.getElementById("branch_name_code").required = false;
                document.getElementById('iban_val_cond').innerText = 'IBAN must start with SA \nIBAN length must be 24 characters'
            }
            if (sessionStorage.getItem('country_code') !== 'SA') {
                $('#employee_wizard').smartWizard("setState", [3], "enable");
                $('#employee_wizard').smartWizard("setState", [3], "show");
            }
            if (!document.getElementById('international_bank').checked) {
                document.getElementById("bank_name").required = false;
                document.getElementById("branch_name_code").required = false;
                document.getElementById('iban_val_cond').innerText = 'IBAN must start with SA \nIBAN length must be 24 characters'

            }
            if (document.getElementById('international_bank').checked) {
                document.getElementById('iban_val_cond').innerText = 'IBAN length must be 34 characters'

            }
            let stepInfo = $('#employee_wizard').smartWizard("getStepInfo");
            $("#sw-current-step").text(stepInfo.currentStep + 1);
            $("#sw-total-step").text(stepInfo.totalSteps);

            // Focus first name
            if (stepPosition === 'last') {
                $('#btnFinish').show(); // show the button extra only in the last page
                $('.sw-btn-next').hide(); // show the button extra only in the last page
                $("#btnFinish").removeClass('disabled').prop('disabled', false)
                $("#btnFinish").removeClass('disabled').prop('disabled', false)
            } else {
                $('#btnFinish').hide();
                $('.sw-btn-next').show();
            }
            if (stepPosition !== 'first') {
                $('.sw-btn-prev').show(); // show the button extra only in the last page
            } else {
                $('.sw-btn-prev').hide();
            }
            if (stepInfo['currentStep'] === 0) {
                sessionStorage.setItem('birthday', personal_form['birthday'].value.trim())
                sessionStorage.setItem('country_code', personal_form['country_id'].options[personal_form['country_id'].selectedIndex].getAttribute('code'))
                sessionStorage.setItem('marital', personal_form['marital'].value)
                sessionStorage.setItem('gender', personal_form.elements['gender'].value)
                db.personal.clear()
                if (sessionStorage.getItem('marital') === 'single') {
                    document.getElementById("spouse_name").required = false;
                    document.getElementById("spouse_id_number").required = false;
                    document.getElementById("spouse_birthdate").required = false;
                    document.getElementById("spouse_phone").required = false;
                    document.getElementById("spouse_family_attach").required = false;

                    if (sessionStorage.getItem('country_code') !== 'SA') {
                        $('#employee_wizard').smartWizard("setState", [5], "disable");
                        $('#employee_wizard').smartWizard("setState", [5], "hide");
                        document.getElementById("father_name").required = false;
                        document.getElementById("father_id_number").required = false;
                        document.getElementById("father_birthdate").required = false;
                        document.getElementById("father_phone").required = false;
                        document.getElementById("father_family_attach").required = false;

                        document.getElementById("mother_name").required = false;
                        document.getElementById("mother_id_number").required = false;
                        document.getElementById("mother_birthdate").required = false;
                        document.getElementById("mother_phone").required = false;
                        document.getElementById("mother_family_attach").required = false;

                        document.getElementById("spouse_name").required = false;
                        document.getElementById("spouse_id_number").required = false;
                        document.getElementById("spouse_birthdate").required = false;
                        document.getElementById("spouse_phone").required = false;
                        document.getElementById("spouse_family_attach").required = false;

                        // return $('#employee_wizard').smartWizard("_showStep", 6);


                    }
                    if (sessionStorage.getItem('country_code') === 'SA') {
                        $('#employee_wizard').smartWizard("setState", [5], "enable");
                        $('#employee_wizard').smartWizard("setState", [5], "show");
                        document.getElementById("father_row").classList.remove('d-none');
                        document.getElementById("mother_row").classList.remove('d-none');

                    }

                } else {
                    $('#employee_wizard').smartWizard("setState", [5], "enable");
                    $('#employee_wizard').smartWizard("unsetState", [5], "disable");
                    $('#employee_wizard').smartWizard("setState", [5], "show");
                    $('#employee_wizard').smartWizard("unsetState", [5], "hide");
                    if (sessionStorage.getItem('country_code') !== 'SA') {
                        document.getElementById("spouse_row").classList.remove('d-none');
                        document.getElementById("children_row").classList.remove('d-none');
                        // father fields
                        document.getElementById("father_name").required = false;
                        document.getElementById("father_id_number").required = false;
                        document.getElementById("father_birthdate").required = false;
                        document.getElementById("father_phone").required = false;
                        document.getElementById("father_family_attach").required = false;

                        document.getElementById("mother_name").required = false;
                        document.getElementById("mother_id_number").required = false;
                        document.getElementById("mother_birthdate").required = false;
                        document.getElementById("mother_phone").required = false;
                        document.getElementById("mother_family_attach").required = false;


                    }
                    if (sessionStorage.getItem('country_code') === 'SA') {
                        document.getElementById("father_row").classList.remove('d-none');
                        document.getElementById("mother_row").classList.remove('d-none');
                        document.getElementById("spouse_row").classList.remove('d-none');
                        document.getElementById("children_row").classList.remove('d-none');
                    }

                }

                localStorage.setItem('name_en', personal_form['partner_name'].value.trim(),);
                localStorage.setItem('name_ar', personal_form['name_ar'].value.trim(),);
                localStorage.setItem('birthday', personal_form['birthday'].value.trim(),);
                localStorage.setItem('country_id', personal_form['country_id'].options[personal_form['country_id'].selectedIndex].value,);
                localStorage.setItem('civil_id', (personal_form['civil_id'].value) ? personal_form['civil_id'].value.trim() : false,);
                localStorage.setItem('passport', (personal_form['passport_id'].value) ? personal_form['passport_id'].value.trim() : false,);
                localStorage.setItem('marital', personal_form['marital'].options[personal_form['marital'].selectedIndex].value,);
                localStorage.setItem('gender', personal_form.elements['gender'].value,);
                localStorage.setItem('national_address', (personal_form.elements['national_address_attach']) ? await convertFileToBase64(new File(["file"], personal_form.elements['national_address_attach'])) : false,);
                localStorage.setItem('partner_mobile', personal_form['partner_mobile'].value.trim(),);
                localStorage.setItem('country_of_birth', personal_form['country_of_birth'].options[personal_form['country_of_birth'].selectedIndex].value,);
                localStorage.setItem('place_of_birth', personal_form['place_of_birth'].value.trim(),);
                localStorage.setItem('religion', personal_form.elements['religion'].value,);
                localStorage.setItem('email_from', personal_form['email_from'].value.trim(),);

                return db.personal.put({
                    name_en: personal_form['partner_name'].value.trim(),
                    name_ar: personal_form['name_ar'].value.trim(),
                    birthday: personal_form['birthday'].value.trim(),
                    country_id: personal_form['country_id'].options[personal_form['country_id'].selectedIndex].value,
                    civil_id: (personal_form['civil_id'].value) ? personal_form['civil_id'].value.trim() : false,
                    passport: (personal_form['passport_id'].value) ? personal_form['passport_id'].value.trim() : false,
                    marital: personal_form['marital'].options[personal_form['marital'].selectedIndex].value,
                    gender: personal_form.elements['gender'].value,
                    national_address: (personal_form.elements['national_address_attach']) ? await convertFileToBase64(new File(["file"], personal_form.elements['national_address_attach'])) : false,
                    partner_mobile: personal_form['partner_mobile'].value.trim(),
                    country_of_birth: personal_form['country_of_birth'].options[personal_form['country_of_birth'].selectedIndex].value,
                    place_of_birth: personal_form['place_of_birth'].value.trim(),
                    religion: personal_form.elements['religion'].value,
                    email_from: personal_form['email_from'].value.trim(),
                });
            }
            if (stepInfo['currentStep'] === 1) {
                localStorage.setItem('graduate_date', education_form['graduate_date'].value.trim());
                localStorage.setItem('certificate', education_form['certificate'].options[education_form['certificate'].selectedIndex].value);
                localStorage.setItem('study_field', education_form['study_field'].value.trim());
                localStorage.setItem('study_school', education_form['study_school'].value.trim());

                db.personal.where("id").aboveOrEqual(0).modify({
                    graduate_date: education_form['graduate_date'].value.trim(),
                    certificate: education_form['certificate'].options[education_form['certificate'].selectedIndex].value,
                    study_field: education_form['study_field'].value.trim(),
                    study_school: education_form['study_school'].value.trim(),
                });
            }
            if (stepInfo['currentStep'] === 2) {
                localStorage.setItem('not_have_gosi', gosi_form['not_have_gosi'].checked);
                localStorage.setItem('gosi_number', gosi_form['gosi_number'].value.trim());
                localStorage.setItem('gosi_start_date', gosi_form['gosi_start_date'].value.trim());

                db.personal.where("id").aboveOrEqual(0).modify({
                    gosi_number: (gosi_form['gosi_number'].value) ? gosi_form['gosi_number'].value.trim() : false,
                    gosi_start_date: (gosi_form['gosi_start_date'].value) ? gosi_form['gosi_start_date'].value.trim() : false,
                });
            }
            if (stepInfo['currentStep'] === 3) {

                localStorage.setItem('sponsor_name', sponsor_form['sponsor_name'].value.trim());
                localStorage.setItem('sponsor_phone', sponsor_form['sponsor_phone'].value.trim());
                localStorage.setItem('sponsor_address', sponsor_form['sponsor_address'].value.trim());
                localStorage.setItem('residency_number', sponsor_form['residency_number'].value.trim());
                localStorage.setItem('serial_number', sponsor_form['serial_number'].value.trim());
                localStorage.setItem('resid_job_title', sponsor_form['resid_job_title'].value.trim());
                localStorage.setItem('place_of_issuance', sponsor_form['place_of_issuance'].value.trim());
                localStorage.setItem('expiration_date', sponsor_form['expiration_date'].value.trim());
                localStorage.setItem('arrival_date', sponsor_form['arrival_date'].value.trim());
                localStorage.setItem('resid_issuance_date', sponsor_form['resid_issuance_date'].value.trim());

                db.personal.where("id").aboveOrEqual(0).modify({
                    sponsor_name: sponsor_form['sponsor_name'].value.trim(),
                    sponsor_phone: sponsor_form['sponsor_phone'].value.trim(),
                    sponsor_address: sponsor_form['sponsor_address'].value.trim(),
                    residency_number: sponsor_form['residency_number'].value.trim(),
                    serial_number: sponsor_form['serial_number'].value.trim(),
                    resid_job_title: sponsor_form['resid_job_title'].value.trim(),
                    place_of_issuance: sponsor_form['place_of_issuance'].value.trim(),
                    expiration_date: sponsor_form['expiration_date'].value.trim(),
                    expiration_date_in_hijri: sponsor_form['expiration_date_in_hijri'].value.trim(),
                    arrival_date: sponsor_form['arrival_date'].value.trim(),
                    resid_issuance_date: sponsor_form['resid_issuance_date'].value.trim(),
                });

            }
            if (stepInfo['currentStep'] === 4) {

                var checkBox = document.getElementById("international_bank");
                if (checkBox.checked == true) {
                    document.getElementById("international_bank_div").classList.remove('d-none');
                    document.getElementById("local_bank_div").classList.add('d-none');
                    document.getElementById('iban_val_cond').innerText = 'IBAN length must be 34 characters'
                    document.getElementById("bank_name").setAttribute('required', '""');
                    document.getElementById("branch_name_code").setAttribute('required', '""');
                    document.getElementById('iban_val_cond').innerText = 'IBAN length must be 34 characters'


                }
                if (checkBox.checked == false) {

                    document.getElementById("international_bank_div").classList.add('d-none');
                    document.getElementById("local_bank_div").classList.remove('d-none');
                    document.getElementById('iban_val_cond').innerText = 'IBAN must start with SA \n- IBAN length must be 24 characters'
                    document.getElementById("bank_name").required = false;
                    document.getElementById("branch_name_code").required = false;


                }
                if (sessionStorage.getItem('marital') === 'single') {
                    document.getElementById("spouse_name").required = false;
                    document.getElementById("spouse_id_number").required = false;
                    document.getElementById("spouse_birthdate").required = false;
                    document.getElementById("spouse_phone").required = false;
                    document.getElementById("spouse_family_attach").required = false;

                    if (sessionStorage.getItem('country_code') !== 'SA') {
                        $('#employee_wizard').smartWizard("setState", [5], "disable");
                        $('#employee_wizard').smartWizard("setState", [5], "hide");
                        document.getElementById("father_name").required = false;
                        document.getElementById("father_id_number").required = false;
                        document.getElementById("father_birthdate").required = false;
                        document.getElementById("father_phone").required = false;
                        document.getElementById("father_family_attach").required = false;

                        document.getElementById("mother_name").required = false;
                        document.getElementById("mother_id_number").required = false;
                        document.getElementById("mother_birthdate").required = false;
                        document.getElementById("mother_phone").required = false;
                        document.getElementById("mother_family_attach").required = false;

                        document.getElementById("spouse_name").required = false;
                        document.getElementById("spouse_id_number").required = false;
                        document.getElementById("spouse_birthdate").required = false;
                        document.getElementById("spouse_phone").required = false;
                        document.getElementById("spouse_family_attach").required = false;

                        document.getElementById("child_name").required = false;
                        document.getElementById("child_id_number").required = false;
                        document.getElementById("child_birthdate").required = false;
                        document.getElementById("child_phone").required = false;
                        document.getElementById("child_attach").required = false;

                        // return $('#employee_wizard').smartWizard("_showStep", 6);


                    }
                    if (sessionStorage.getItem('country_code') === 'SA') {
                        $('#employee_wizard').smartWizard("setState", [5], "enable");
                        $('#employee_wizard').smartWizard("setState", [5], "show");
                        document.getElementById("father_row").classList.remove('d-none');
                        document.getElementById("mother_row").classList.remove('d-none');

                    }

                } else {
                    $('#employee_wizard').smartWizard("setState", [5], "enable");
                    $('#employee_wizard').smartWizard("unsetState", [5], "disable");
                    $('#employee_wizard').smartWizard("setState", [5], "show");
                    $('#employee_wizard').smartWizard("unsetState", [5], "hide");
                    if (sessionStorage.getItem('country_code') !== 'SA') {
                        document.getElementById("spouse_row").classList.remove('d-none');
                        document.getElementById("children_row").classList.remove('d-none');
                        // father fields
                        document.getElementById("father_name").required = false;
                        document.getElementById("father_id_number").required = false;
                        document.getElementById("father_birthdate").required = false;
                        document.getElementById("father_phone").required = false
                        document.getElementById("father_family_attach").required = false;

                        document.getElementById("mother_name").required = false;
                        document.getElementById("mother_id_number").required = false;
                        document.getElementById("mother_birthdate").required = false;
                        document.getElementById("mother_phone").required = false;
                        document.getElementById("mother_family_attach").required = false;


                    }
                    if (sessionStorage.getItem('country_code') === 'SA') {
                        document.getElementById("father_row").classList.remove('d-none');
                        document.getElementById("mother_row").classList.remove('d-none');
                        document.getElementById("spouse_row").classList.remove('d-none');
                        document.getElementById("children_row").classList.remove('d-none');
                    }

                }

                localStorage.setItem('international_bank', bank_form['international_bank'].checked);
                localStorage.setItem('bank_id', bank_form['bank_id'].value.trim());
                localStorage.setItem('bank_country_id', bank_form['bank_country_id'].value.trim());
                localStorage.setItem('bank_name', bank_form['bank_name'].value.trim());
                localStorage.setItem('branch_name_code', bank_form['branch_name_code'].value.trim());
                localStorage.setItem('iban_no', bank_form['iban_no'].value.trim());

                if (!bank_form['international_bank'].checked) {
                    db.personal.where("id").aboveOrEqual(0).modify({
                        international_bank: false,
                        bank_id: bank_form['bank_id'].options[bank_form['bank_id'].selectedIndex].value,
                        bank_country_id: false,
                        bank_name: false,
                        branch_name_code: false,
                        iban_no: bank_form['iban_no'].value.trim(),

                    });
                }
                if (bank_form['international_bank'].checked) {
                    db.personal.where("id").aboveOrEqual(0).modify({
                        international_bank: true,
                        bank_id: false,
                        bank_country_id: bank_form['bank_country_id'].options[bank_form['bank_country_id'].selectedIndex].value,
                        bank_name: bank_form['bank_name'].value.trim(),
                        branch_name_code: bank_form['branch_name_code'].value.trim(),
                        iban_no: bank_form['iban_no'].value.trim(),


                    });
                }
            }
            if (stepInfo['currentStep'] === 5) {
                if (family_form['father_name'].value.trim() !== '' || family_form['father_id_number'].value.trim() !== '' || family_form['father_birthdate'].value.trim() !== '' || family_form['father_family_attach'].value.trim() !== '') {
                    db.father.clear()
                    localStorage.setItem('father_name', sponsor_form['father_name'].value.trim());
                    localStorage.setItem('father_id_number', sponsor_form['father_id_number'].value.trim());
                    localStorage.setItem('father_birthdate', sponsor_form['father_birthdate'].value.trim());
                    localStorage.setItem('father_phone', sponsor_form['father_phone'].value.trim());
                    localStorage.setItem('father_family_attach', (family_form.elements['father_family_attach']) ? await convertFileToBase64(new File(["file"], family_form.elements['father_family_attach'])) : false,);

                    db.father.put({
                        father_name: family_form['father_name'].value.trim() !== '' ? family_form['father_name'].value.trim() : false,
                        father_id_number: family_form['father_id_number'].value.trim() !== '' ? family_form['father_id_number'].value.trim() : false,
                        father_birthdate: family_form['father_birthdate'].value.trim() !== '' ? family_form['father_birthdate'].value.trim() : false,
                        father_phone: family_form['father_phone'].value.trim() !== '' ? family_form['father_phone'].value.trim() : false,
                        father_family_attach: (family_form['father_family_attach'].value) ? await convertFileToBase64(family_form['father_family_attach'].files[0]) : false
                    })
                }
                if (family_form['mother_name'].value.trim() !== '' || family_form['mother_id_number'].value.trim() !== '' || family_form['mother_birthdate'].value.trim() !== '' || family_form['mother_family_attach'].value.trim() !== '') {
                    db.mother.clear()
                    localStorage.setItem('mother_name', family_form['father_name'].value.trim());
                    localStorage.setItem('mother_id_number', family_form['father_id_number'].value.trim());
                    localStorage.setItem('mother_birthdate', family_form['father_birthdate'].value.trim());
                    localStorage.setItem('mother_phone', family_form['father_phone'].value.trim());
                    localStorage.setItem('mother_family_attach', (family_form.elements['mother_family_attach']) ? await convertFileToBase64(new File(["file"], family_form.elements['mother_family_attach'])) : false,);

                    db.mother.put({
                        mother_name: family_form['mother_name'].value.trim() !== '' ? family_form['mother_name'].value.trim() : false,
                        mother_id_number: family_form['mother_id_number'].value.trim() !== '' ? family_form['mother_id_number'].value.trim() : false,
                        mother_birthdate: family_form['mother_birthdate'].value.trim() !== '' ? family_form['mother_birthdate'].value.trim() : false,
                        mother_phone: family_form['mother_phone'].value.trim() !== '' ? family_form['mother_phone'].value.trim() : false,
                        mother_family_attach: (family_form['mother_family_attach'].value) ? await convertFileToBase64(family_form['mother_family_attach'].files[0]) : false
                    })
                }
                if (family_form['spouse_name'].value.trim() !== '' || family_form['spouse_id_number'].value.trim() !== '' || family_form['spouse_birthdate'].value.trim() !== '' || family_form['spouse_family_attach'].value.trim() !== '') {
                    db.spouse.clear()
                    localStorage.setItem('spouse_name', family_form['spouse_name'].value.trim());
                    localStorage.setItem('spouse_id_number', family_form['spouse_id_number'].value.trim());
                    localStorage.setItem('spouse_birthdate', family_form['spouse_birthdate'].value.trim());
                    localStorage.setItem('spouse_phone', family_form['spouse_phone'].value.trim());
                    localStorage.setItem('spouse_family_attach', (family_form.elements['spouse_family_attach']) ? await convertFileToBase64(new File(["file"], family_form.elements['spouse_family_attach'])) : false,);

                    db.spouse.put({
                        spouse_name: family_form['spouse_name'].value.trim() !== '' ? family_form['spouse_name'].value.trim() : false,
                        spouse_id_number: family_form['spouse_id_number'].value.trim() !== '' ? family_form['spouse_id_number'].value.trim() : false,
                        spouse_birthdate: family_form['spouse_birthdate'].value.trim() !== '' ? family_form['spouse_birthdate'].value.trim() : false,
                        spouse_phone: family_form['spouse_phone'].value.trim() !== '' ? family_form['spouse_phone'].value.trim() : false,
                        spouse_family_attach: (family_form['spouse_family_attach'].value) ? await convertFileToBase64(family_form['spouse_family_attach'].files[0]) : false
                    })
                }
                let result = [];
                $("#child_info_table tbody tr").each(function (ind) {
                    var allValues = {};
                    $(this).find("input").each(function (index) {
                        console.log($(this).attr("id"))
                        if (($(this).attr("id") == 'child_name' && $(this).val() !== '')) {
                            const fieldName = $(this).attr("id");
                            allValues[fieldName] = $(this).val();

                        } else {
                            return false;
                        }

                    });

                    if (result) {
                        $(this).find("select").each(function (index) {
                            if(($(this).attr("id") == 'child_gender' && $(this).val() !== '')) {
                                const fieldName = $(this).attr("name");
                                allValues[fieldName] = $(this).val();
                            }else {
                                return false;
                            }
                        });

                    }
                    result.push(allValues);
                })
                db.children.clear()

                if (result) {

                    storage_child_list = []
                    for (const item of result) {
                        if (item['child_name']) {
                            storage_child_list.push({
                                'child_name': item['child_name'],
                                'child_id_number': item['child_id_number'],
                                'child_birthdate': item['child_birthdate'],
                                'child_gender': item['child_gender'],
                                'child_phone': item['child_phone'],
                                'child_family_attach': item['child_family_attach'].value ? await convertFileToBase64(new File(["file"], item['child_family_attach'].files[0])) : false
                            })
                        }
                    }
                    localStorage.setItem('child_list', JSON.stringify(storage_child_list));

                    for (const item of result) {
                        db.children.add({
                            child_name: item['child_name'],
                            child_id_number: item['child_id_number'],
                            child_birthdate: item['child_birthdate'],
                            child_gender: item['child_gender'],
                            child_phone: item['child_phone'],
                            child_family_attach: (item['child_family_attach']) ? await convertFileToBase64(new File(["file"], item['child_family_attach'])) : false
                        })
                    }
                }
            }
            if (stepInfo['currentStep'] === 6) {
                let result = [];
                $("#experience_table tbody tr").each(function () {

                    var allValues = {};
                    $(this).find("input").each(function (index) {
                        if (($(this).attr("id") == 'job_name' && $(this).val() !== '') || $(this).val() !== '' || $(this).val() !== 'false') {
                            const fieldName = $(this).attr("name");
                            allValues[fieldName] = $(this).val();
                        }
                    });
                    result.push(allValues);

                })
                if (result) {
                    db.experience.clear()
                    storage_job_list = []
                    for (const item of result) {
                        if (item['job_name'] && item['employer_name']) {
                            storage_job_list.push({
                                job_name: item['job_name'],
                                employer_name: item['employer_name'],
                                date_from: item['date_from'],
                                date_to: item['date_to'],
                                service_certificate: (item['service_certificate']) ? await convertFileToBase64(new File(["file"], item['service_certificate'])) : false
                            })
                        }
                    }
                    localStorage.setItem('jobs_list', JSON.stringify(storage_job_list));

                    for (const item of result) {
                        const index = result.indexOf(item);
                        db.experience.add({
                            job_name: item['job_name'],
                            employer_name: item['employer_name'],
                            date_from: item['date_from'],
                            date_to: item['date_to'],
                            service_certificate: (item['service_certificate']) ? await convertFileToBase64(new File(["file"], item['service_certificate'])) : false
                        })
                    }
                }

            }
            if (stepInfo['currentStep'] === 7) {
                attach_form = document.forms["form-8"];
                db.attaches.clear()
                attach_form.querySelectorAll(`[name^="attach_"]`).forEach(async (ele) => {
                    if (ele.value) {
                        db.attaches.add({
                            dbid: ele.getAttribute('atcid'),
                            name: ele.name,
                            attach: (ele.value) ? await convertFileToBase64(ele.files[0]) : false
                        })
                    }
                })

            }
        });

        // Smart Wizard
        $('#employee_wizard').smartWizard({
            selected: 0, justified: true, autoAdjustHeight: false, enableAllSteps: false, theme: 'dots', // basic, arrows, square, round, dots
            transition: {
                animation: 'none'
            }, toolbar: {
                showNextButton: true, // show/hide a Next button
                showPreviousButton: true, // show/hide a Previous button
                position: 'bottom', // none/ top/ both bottom
                extraHtml: `<button class="btn btn-success" id="btnFinish" disabled onclick="onConfirm()">Submit</button>`
            }, anchor: {
                enableNavigation: false, // Enable/Disable anchor navigation
                enableNavigationAlways: false, // Activates all anchors clickable always
                enableDoneState: true, // Add done state on visited steps
                markPreviousStepsAsDone: true, // When a step selected by url hash, all previous steps are marked done
                unDoneOnBackNavigation: true, // While navigate back, done state will be cleared
                enableDoneStateNavigation: true // Enable/Disable the done state navigation
            },
        });

        $("#state_selector").on("change", function () {
            $('#employee_wizard').smartWizard("setState", [$('#step_to_style').val()], $(this).val(), !$('#is_reset').prop("checked"));
            return true;
        });

        $("#style_selector").on("change", function () {
            $('#employee_wizard').smartWizard("setStyle", [$('#step_to_style').val()], $(this).val(), !$('#is_reset').prop("checked"));
            return true;
        });

    });


});

$(function () {
    var canvas = document.getElementById('signature-pad');

});