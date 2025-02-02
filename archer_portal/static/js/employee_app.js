function addExperienceNewRow() {
    var table = document.getElementById("experience_table");
    var rowCount = table.rows.length;
    var cellCount = table.rows[0].cells.length;
    var row = table.insertRow(rowCount);
    for (var i = 0; i < cellCount; i++) {
        var cell = row.insertCell(i);
        if (i < cellCount - 1) {
            if (i == 0) {
                cell.innerHTML = '<div class="input-control">\n' +
                    '                                                                                <input type="text" class="form-control" id="job_name" name="job_name" placeholder="Job Name"/>\n' +
                    '                                                                                    <div class="error"/>\n' +
                    '                                                                                </div>'
            }
            if (i == 1) {
                cell.innerHTML = '<div class="input-control">\n' +
                    '                                                                                <input type="text" class="form-control" placeholder="Employer Name"\n' +
                    '                                                                                       id="employer_name"  name="employer_name"/>\n' +
                    '                                                                                <div class="error"/>\n' +
                    '                                                                                </div>'
            }
            if (i == 2) {
                cell.innerHTML = '<div class="input-control">\n' +
                    '                                                                                    <div class="input-group date" >\n' +
                    '                                                                                        <input type="text" class="form-control date_from" id="date_from" name="date_from"  placeholder="Date From"/>\n' +
                    '                                                                                        <div class="input-group-addon">\n' +
                    '                                                                                            <span class="glyphicon glyphicon-th"></span>\n' +
                    '                                                                                        </div>\n' +
                    '                                                                                    </div>\n' +
                    '                                                                                    <div class="error"/>\n' +
                    '                                                                                </div>'
            }
            if (i == 3) {
                cell.innerHTML = '<div class="input-control">\n' +
                    '                                                                                    <div class="input-group date">\n' +
                    '                                                                                        <input type="text" class="form-control date_to"  id="date_to" name="date_to" placeholder="Date To"/>\n' +
                    '                                                                                        <div class="input-group-addon">\n' +
                    '                                                                                            <span class="glyphicon glyphicon-th"></span>\n' +
                    '                                                                                        </div>\n' +
                    '                                                                                    </div>\n' +
                    '                                                                                    <div class="error"/>\n' +
                    '                                                                                </div>'
            }
            if (i == 4) {
                cell.innerHTML = '<div class="input-control">\n' +
                    '                                                                                    <input type="file" name="service_certificate"\n' +
                    '                                                                                           placeholder="Service Certificate"/>\n' +
                    '                                                                                <div class="error"/>\n' +
                    '                                                                                </div>'
            }


        } else {
            cell.innerHTML = '<a type="button" class="btn btn-danger experience_delete_btn">delete</a>';
        }
        $('.date_from').datepicker({
            format: "dd-mm-yyyy",
            endDate: '-3d',
            autoclose: true
        });
        $('.date_to').datepicker({
            format: "dd-mm-yyyy",
            endDate: '-3d',
            autoclose: true
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

}

function addFamilyRelationNewRow() {
    var table = document.getElementById("family_info_table");
    var rowCount = table.rows.length;
    var cellCount = table.rows[0].cells.length;
    var row = table.insertRow(rowCount);
    for (var i = 0; i < cellCount; i++) {
        var cell = row.insertCell(i);
        if (i < cellCount - 1) {
            if (i == 0) {
                cell.innerHTML = '<div class="input-control">\n' +
                    '                                                                                    <input type="text" class="form-control" id="name"\n' +
                    '                                                                                           name="name"/>\n' +
                    '                                                                                    <div class="error"/>\n' +
                    '                                                                                </div>'
            }
            if (i == 1) {
                cell.innerHTML = '<div class="input-control">\n' +
                    '                                                                                    <input type="text" class="form-control"\n' +
                    '                                                                                           oninput="this.value = this.value.replace(/[^0-9.]/g, \'\').replace(/(\\..*)\\./g, \'$1\');"\n' +
                    '                                                                                           id="id_number" name="id_number"/>\n' +
                    '                                                                                    <div class="error"/>\n' +
                    '                                                                                </div>'
            }
            if (i == 2) {
                cell.innerHTML = '<div class="input-control">\n' +
                    '                                                                                    <select class="form-control gender" id="gender"\n' +
                    '                                                                                            name="gender">\n' +
                    '                                                                                        <option value="male">Male</option>\n' +
                    '                                                                                        <option value="female">Female\n' +
                    '                                                                                        </option>\n' +
                    '                                                                                    </select>\n' +
                    '                                                                                    <div class="error"/>\n' +
                    '                                                                                </div>'
            }
            if (i == 3) {
                cell.innerHTML = '<div class="input-control">\n' +
                    '                                                                                    <div class="input-group date">\n' +
                    '                                                                                        <input type="text" class="form-control birthdate"\n' +
                    '                                                                                               id="birthdate" name="birthdate"/>\n' +
                    '                                                                                        <div class="input-group-addon">\n' +
                    '                                                                                            <span class="glyphicon glyphicon-th"></span>\n' +
                    '                                                                                        </div>\n' +
                    '                                                                                    </div>\n' +
                    '                                                                                    <div class="error"/>\n' +
                    '                                                                                </div>'
            }
            if (i == 4) {
                cell.innerHTML = '<div class="input-control">\n' +
                    '                                                                                    <input type="text" class="form-control" id="phone"\n' +
                    '                                                                                           name="phone"\n' +
                    '                                                                                           oninput="this.value = this.value.replace(/[^0-9.]/g, \'\').replace(/(\\..*)\\./g, \'$1\');"/>\n' +
                    '                                                                                    <div class="error"/>\n' +
                    '                                                                                </div>'
            }
            if (i == 5) {
                cell.innerHTML = '<div class="input-control">\n' +
                    '                                                                                    <div class="input-control">\n' +
                    '                                                                                        <input type="file"\n' +
                    '                                                                                               name="family_attach"\n' +
                    '                                                                                               placeholder="Birth Certificate"/>\n' +
                    '                                                                                        <div class="error"/>\n' +
                    '                                                                                    </div>\n' +
                    '                                                                                </div>'
            }
        } else {
            cell.innerHTML = '<a type="button" class="btn btn-danger family_delete_btn">delete</a>';
        }
        $('.birthdate').datepicker({
            format: "dd-mm-yyyy",
            endDate: '-3d',
            autoclose: true
        });
    }

    /* This method will delete a row */
    function deleteFamilyRelationRow(ele) {
        var table = document.getElementById('family_info_table');
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

}


function internationalBankClick() {
    // Get the checkbox
    var checkBox = document.getElementById("international_bank");
    if (checkBox.checked == true) {
        document.getElementById("international_bank_div").style.display = "block";
        document.getElementById("local_bank_div").style.display = "none";
    }
    if (checkBox.checked == false) {

        document.getElementById("international_bank_div").style.display = "none";
        document.getElementById("local_bank_div").style.display = "block";

    }
}

const setError = (element, message) => {
    const inputControl = element.parentElement;
    const errorDisplay = inputControl.querySelector('.error');
    debugger
    element.children[0].classList.add('alert-danger')
    element.children[0].classList.add('border-danger')

    errorDisplay.innerText = message;
    inputControl.classList.add('error');
    // inputControl.classList.remove('success')
}
const isValidEmail = email => {
    const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(email).toLowerCase());
}

if (sessionStorage.getItem('marital') == 'single') {
    document.getElementById('spouse_div').hidden = true
    document.getElementById('children_div').hidden = true

}
if (sessionStorage.getItem('country_id') != 'SA') {
    document.getElementById('parents_div').hidden = true

}
$(document).ready(function () {
    ff = $('input[type=file]')
    console.log(ff)

    var checkBox = document.getElementById("international_bank");
    if (checkBox.checked == true) {
        document.getElementById("international_bank_div").style.display = "block";
        document.getElementById("local_bank_div").style.display = "none";
    }
    if (checkBox.checked == false) {

        document.getElementById("international_bank_div").style.display = "none";
        document.getElementById("local_bank_div").style.display = "block";

    }
    var experience_table = document.getElementById("experience_table");

    $('#date_from').datepicker({
        format: "dd-mm-yyyy",
        endDate: '-3d',
        autoclose: true
    });
    $('#date_to').datepicker({
        format: "dd-mm-yyyy",
        endDate: '-3d',
        autoclose: true
    });


    var current_fs, next_fs, previous_fs; //fieldsets
    var opacity;

    function go_next(current_id, next_id) {
        current_fs = $(document.getElementById(current_id));
        next_fs = $(document.getElementById(next_id));
        //Add Class Active
        $("#progressbar li").eq($("fieldset").index(next_fs)).addClass("active");

        //show the next fieldset
        next_fs.show();
        //hide the current fieldset with style
        current_fs.animate({opacity: 0}, {
            step: function (now) {
                // for making fielset appear animation
                opacity = 1 - now;

                current_fs.css({
                    'display': 'none',
                    'position': 'relative'
                });
                next_fs.css({'opacity': opacity});
            },
            duration: 600
        });
    };


    $(".previous").click(function () {

        current_fs = $(this).parent();
        previous_fs = $(this).parent().prev();
        //Remove class active
        $("#progressbar li").eq($("fieldset").index(current_fs)).removeClass("active");

        //show the previous fieldset
        if (current_fs[0].id == 'bank_fieldset' && sessionStorage.getItem('country_id') === 'SA') {
            previous_fs = $(document.getElementById('gosi_fieldset'))
        }
        previous_fs.show();

        //hide the current fieldset with style
        current_fs.animate({opacity: 0}, {
            step: function (now) {
                // for making fielset appear animation
                opacity = 1 - now;

                current_fs.css({
                    'display': 'none',
                    'position': 'relative'
                });
                previous_fs.css({'opacity': opacity});
            },
            duration: 600
        });
    });

    $('.radio-group .radio').click(function () {
        $(this).parent().find('.radio').removeClass('selected');
        $(this).addClass('selected');
    });

    $(".submit").click(function () {
        return false;
    })

    function internationalBankClick() {
        // Get the checkbox
        var checkBox = document.getElementById("international_bank");
        if (checkBox.checked == true) {
            document.getElementById("international_bank_div").style.display = "block";
            document.getElementById("local_bank_div").style.display = "none";
        }
        if (checkBox.checked == false) {

            document.getElementById("international_bank_div").style.display = "none";
            document.getElementById("local_bank_div").style.display = "block";

        }
    }

    function deleteFamilyRelationRow(ele) {
        var table = document.getElementById('family_info_table');
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

    // personal fieldset
    const partner_name = document.getElementById('partner_name');
    const name_ar = document.getElementById('name_ar');
    const birthday = document.getElementById('birthday');
    const birth_attach = document.getElementById('birth_attach');
    const country_id = document.getElementById('country_id');
    const identification_id = document.getElementById('identification_id');
    const passport_id = document.getElementById('passport_id');
    const marital = document.getElementById('marital');
    const gender = document.getElementById('gender');
    const passport_attach = document.getElementById('passport_attach');
    const civil_id_attach = document.getElementById('civil_id_attach');

    // personal2 fieldset2
    const national_address = document.getElementById('national_address');
    const national_address_attach = document.getElementById('national_address_attach');
    const email_from = document.getElementById('email_from');
    const phone = document.getElementById('phone');
    const partner_mobile = document.getElementById('partner_mobile');
    const country_of_birth = document.getElementById('country_of_birth');
    const place_of_birth = document.getElementById('place_of_birth');
    const religion = document.getElementById('religion');

    // education fieldset
    const graduate_date = document.getElementById('graduate_date');
    const certificate = document.getElementById('certificate');
    const study_field = document.getElementById('study_field');
    const study_school = document.getElementById('study_school');
    const certificate_attach = document.getElementById('certificate_attach');

    // gosi fieldset
    const gosi_number = document.getElementById('gosi_number');
    const gosi_start_date = document.getElementById('gosi_start_date');
    const gosi_attach = document.getElementById('gosi_attach');

    // sponsor fieldset
    const sponsor_name = document.getElementById('sponsor_name');
    const sponsor_phone = document.getElementById('sponsor_phone');
    const sponsor_address = document.getElementById('sponsor_address');

    // residency fieldset
    const residency_number = document.getElementById('residency_number');
    const serial_number = document.getElementById('serial_number');
    const resid_job_title = document.getElementById('resid_job_title');
    const place_of_issuance = document.getElementById('place_of_issuance');
    const expiration_date = document.getElementById('expiration_date');
    const expiration_date_in_hijri = document.getElementById('expiration_date_in_hijri');
    const arrival_date = document.getElementById('arrival_date');
    const resid_issuance_date = document.getElementById('resid_issuance_date');
    const residency_attach = document.getElementById('residency_attach');


    // bank fieldset
    const international_bank = document.getElementById('international_bank');
    const bank_id = document.getElementById('bank_id');
    const bank_country_id = document.getElementById('bank_country_id');
    const bank_name = document.getElementById('bank_name');
    const branch_name_code = document.getElementById('branch_name_code');
    const iban_no = document.getElementById('iban_no');
    const reconfirm_iban_no = document.getElementById('reconfirm_iban_no');

    // father fieldset
    const father_name = document.getElementById('father_name');
    const father_id_number = document.getElementById('father_id_number');
    const father_birthdate = document.getElementById('father_birthdate');
    const father_phone = document.getElementById('father_phone');
    const father_family_attach = document.getElementById('father_family_attach');


    // mother fieldset
    const mother_name = document.getElementById('mother_name');
    const mother_id_number = document.getElementById('mother_id_number');
    const mother_birthdate = document.getElementById('mother_birthdate');
    const mother_phone = document.getElementById('mother_phone');
    const mother_family_attach = document.getElementById('mother_family_attach');


    // spouse fieldset
    const spouse_name = document.getElementById('spouse_name');
    const spouse_id_number = document.getElementById('spouse_id_number');
    const spouse_birthdate = document.getElementById('spouse_birthdate');
    const spouse_phone = document.getElementById('spouse_phone');
    const spouse_family_attach = document.getElementById('spouse_family_attach');


    // children fieldset
    const name = document.getElementById('name');
    const id_number = document.getElementById('id_number');
    const family_gender = document.getElementById('gender');
    const family_phone = document.getElementById('phone');
    const birthdate = document.getElementById('birthdate');
    const family_attach = document.getElementById('family_attach');

    // experience fieldset
    const job_name = document.getElementById('job_name');
    const employer_name = document.getElementById('employer_name');
    const date_from = document.getElementById('date_from');
    const date_to = document.getElementById('date_to');
    const service_certificate = document.getElementById('service_certificate');


    $('#personal_next_btn').click(function () {
        if (partner_name.value.trim() === '') {
            setError(partner_name, 'Required');
        } else if (name_ar.value.trim() === '') {
            setError(name_ar, 'Required');
        } else if (birthday.value.trim() === '') {
            setError(birthday, 'Required');
        } else if (birth_attach.value.trim() === '') {
            setError(birth_attach, 'Required');
        } else if (country_id.options[country_id.selectedIndex].getAttribute('code') !== 'SA' && passport_id.value.trim() === '') {
            setError(passport_id, 'Required');
        } else if (country_id.options[country_id.selectedIndex].getAttribute('code') !== 'SA' && passport_attach.value.trim() === '') {
            setError(passport_attach, 'Required');
        } else if (identification_id.value.trim() === '') {
            setError(identification_id, 'Required');
        } else {

            sessionStorage.setItem('birthday', birthday.value.trim())
            sessionStorage.setItem('country_id', country_id.options[country_id.selectedIndex].getAttribute('code'))
            sessionStorage.setItem('marital', marital.options[marital.selectedIndex].value)
            sessionStorage.setItem('gender', gender.options[gender.selectedIndex].value)
            db.open().then(async function () {
                db.personal.clear()
                return db.personal.put({
                    name_en: partner_name.value.trim(),
                    name_ar: name_ar.value.trim(),
                    birthday: birthday.value.trim(),
                    birthday_attach: await convertFileToBase64(birth_attach.files[0]),
                    country_id: country_id.options[country_id.selectedIndex].value,
                    civil_id: (identification_id.value) ? identification_id.value.trim() : false,
                    passport: (passport_id.value) ? passport_id.value.trim() : false,
                    marital: marital.options[marital.selectedIndex].value,
                    gender: gender.options[gender.selectedIndex].value,
                    civil_id_attach: (civil_id_attach.value) ? await convertFileToBase64(civil_id_attach.files[0]) : false,
                    passport_attach: (passport_attach.value) ? await convertFileToBase64(passport_attach.files[0]) : false

                });

            })
            go_next('personal_fieldset', 'personal2_fieldset')
        }
    })
    $('#personal2_next_btn').click(async function () {
        if (national_address.value.trim() === '') {
            setError(national_address, `${national_address.placeholder} is required`);
        } else if (national_address_attach.value.trim() === '') {
            setError(national_address_attach, `${national_address_attach.placeholder} is required`);
        } else if (email_from.value.trim() === '') {
            setError(email_from, `${email_from.placeholder} is required`);
        } else if (phone.value.trim() === '') {
            setError(phone, `${phone.placeholder} is required`);
        } else if (partner_mobile.value.trim() === '') {
            setError(partner_mobile, `${partner_mobile.placeholder} is required`);
        } else {
            db.personal.where("id").aboveOrEqual(0).modify({
                national_address: national_address.value.trim(),
                national_address_attach: await convertFileToBase64(national_address_attach.files[0]),
                phone: phone.value.trim(),
                partner_mobile: partner_mobile.value.trim(),
                country_of_birth: country_of_birth.options[country_of_birth.selectedIndex].value,
                place_of_birth: place_of_birth.value.trim(),
                religion: religion.options[religion.selectedIndex].value,
                email_from: email_from.value.trim(),
            });
            go_next('personal2_fieldset', 'education_fieldset')
        }
    })
    $('#education_next_btn').click(async function () {
        let next_page;
        if (graduate_date.value.trim() === '') {
            setError(graduate_date, `${graduate_date.placeholder} is required`);
        } else if (certificate.value.trim() === '') {
            setError(certificate, `${certificate.placeholder} is required`);
        } else if (study_field.value.trim() === '') {
            setError(study_field, `${study_field.placeholder} is required`);
        } else if (study_school.value.trim() === '') {
            setError(study_school, `${study_school.placeholder} is required`);
        } else if (certificate_attach.value.trim() === '') {
            setError(certificate_attach, `${certificate_attach.placeholder} is required`);
        } else {
            db.personal.where("id").aboveOrEqual(0).modify({
                graduate_date: graduate_date.value.trim(),
                certificate: certificate.options[certificate.selectedIndex].value,
                study_field: study_field.value.trim(),
                study_school: study_school.value.trim(),
                certificate_attach: await convertFileToBase64((certificate_attach.files[0]))
            });
            go_next('education_fieldset', 'gosi_fieldset')
        }
    })
    $('#gosi_next_btn').click(async function () {
        let next_page;
        if (sessionStorage.getItem('country_id') !== 'SA') {
            next_page = 'sponsor_fieldset'
        } else {
            next_page = 'bank_fieldset'
        }
        db.personal.where("id").aboveOrEqual(0).modify({
            gosi_number: (gosi_number.value) ? gosi_number.value.trim() : false,
            gosi_start_date: (gosi_start_date.value) ? gosi_start_date.value.trim() : false,
            gosi_attach: (gosi_attach.value) ? await convertFileToBase64(gosi_attach.files[0]) : false,
        });
        go_next('gosi_fieldset', next_page)

    })
    $('#gosi_skip_btn').click(async function () {
        let next_page;
        if (sessionStorage.getItem('country_id') !== 'SA') {
            next_page = 'sponsor_fieldset'
        } else {
            next_page = 'bank_fieldset'

        }
        go_next('gosi_fieldset', next_page)

    })
    $('#sponsor_next_btn').click(function () {
        if (sponsor_name.value.trim() === '') {
            setError(sponsor_name, `${sponsor_name.placeholder} is required`);
        } else if (sponsor_phone.value.trim() === '') {
            setError(sponsor_phone, `${sponsor_phone.placeholder} is required`);
        } else if (sponsor_address.value.trim() === '') {
            setError(sponsor_address, `${sponsor_address.placeholder} is required`);
        } else {
            db.personal.where("id").aboveOrEqual(0).modify({
                sponsor_name: sponsor_name.value.trim(),
                sponsor_phone: sponsor_phone.value.trim(),
                sponsor_address: sponsor_address.value.trim(),
            })
            go_next('sponsor_fieldset', 'residency_fieldset')
        }
    })
    $('#residency_next_btn').click(async function () {
        if (residency_number.value.trim() === '') {
            setError(residency_number, `${residency_number.placeholder} is required`);
        } else if (serial_number.value.trim() === '') {
            setError(serial_number, `${serial_number.placeholder} is required`);
        } else if (resid_job_title.value.trim() === '') {
            setError(resid_job_title, `${resid_job_title.placeholder} is required`);
        } else if (place_of_issuance.value.trim() === '') {
            setError(place_of_issuance, `${place_of_issuance.placeholder} is required`);
        } else if (expiration_date.value.trim() === '') {
            setError(expiration_date, `${expiration_date.placeholder} is required`);
        } else if (expiration_date_in_hijri.value.trim() === '') {
            setError(expiration_date_in_hijri, `${expiration_date_in_hijri.placeholder} is required`);
        } else if (arrival_date.value.trim() === '') {
            setError(arrival_date, `${arrival_date.placeholder} is required`);
        } else if (residency_attach.value.trim() === '') {
            setError(residency_attach, `${residency_attach.placeholder} is required`);
        } else {
            db.personal.where("id").aboveOrEqual(0).modify({
                residency_number: residency_number.value.trim(),
                serial_number: serial_number.value.trim(),
                resid_job_title: resid_job_title.value.trim(),
                place_of_issuance: place_of_issuance.value.trim(),
                expiration_date: expiration_date.value.trim(),
                expiration_date_in_hijri: expiration_date_in_hijri.value.trim(),
                arrival_date: arrival_date.value.trim(),
                resid_issuance_date: resid_issuance_date.value.trim(),
                residency_attach: await convertFileToBase64(residency_attach.files[0])
            })
            go_next('residency_fieldset', 'bank_fieldset')
        }
    })

    $('#bank_next_btn').click(function () {
        let next_bank_page;
        let can_next = false
        if (international_bank.checked) {

            if (bank_country_id.value.trim() === '') {
                setError(bank_country_id, `${bank_country_id.placeholder} is required`);
            } else if (bank_name.value.trim() === '') {
                setError(bank_name, `${bank_name.placeholder} is required`);
            } else if (branch_name_code.value.trim() === '') {
                setError(branch_name_code, `${branch_name_code.placeholder} is required`);
            } else if (iban_no.value.trim() === '') {
                setError(iban_no, `${iban_no.placeholder} is required`);
            } else if (reconfirm_iban_no.value.trim() === '') {
                setError(reconfirm_iban_no, `${reconfirm_iban_no.placeholder} is required`);
            } else if (reconfirm_iban_no.value.trim().length < 24 || iban_no.value.trim().length < 24) {
                setError(iban_no, `${iban_no.placeholder} not correct`);
            } else if (reconfirm_iban_no.value.trim() !== iban_no.value.trim()) {
                setError(reconfirm_iban_no, `${reconfirm_iban_no.placeholder} Not match ${reconfirm_iban_no.placeholder}`);
            } else {
                can_next = true
            }
        } else {
            if (bank_id.value.trim() === '') {
                setError(bank_id, `${bank_id.placeholder} is required`);
            } else if (iban_no.value.trim() === '') {
                setError(iban_no, `${iban_no.placeholder} is required`);
            } else if (reconfirm_iban_no.value.trim() === '') {
                setError(reconfirm_iban_no, `${reconfirm_iban_no.placeholder} is required`);
            } else if (reconfirm_iban_no.value.trim().slice(0, 2) !== 'SA' || iban_no.value.trim().slice(0, 2) !== 'SA') {
                setError(iban_no, `${iban_no.placeholder} Must Start With (SA)`);
            } else if (reconfirm_iban_no.value.trim().length < 24 || iban_no.value.trim().length < 24) {
                setError(iban_no, `${iban_no.placeholder} not correct`);
            } else if (reconfirm_iban_no.value.trim() !== iban_no.value.trim()) {
                setError(reconfirm_iban_no, `${reconfirm_iban_no.placeholder} Not match ${reconfirm_iban_no.placeholder}`);
            } else {
                can_next = true
            }
        }
        if (can_next) {
            if (international_bank.checked) {
                db.personal.where("id").aboveOrEqual(0).modify({
                    international_bank: true,
                    bank_id: false,
                    bank_country_id: bank_country_id.options[bank_country_id.selectedIndex].value,
                    bank_name: bank_name.value.trim(),
                    branch_name_code: branch_name_code.value.trim(),
                    iban_no: iban_no.value.trim(),
                })
            } else {

                db.personal.where("id").aboveOrEqual(0).modify({
                    international_bank: false,
                    bank_id: bank_id.options[bank_id.selectedIndex].value,
                    bank_country_id: false,
                    bank_name: false,
                    branch_name_code: false,
                    iban_no: iban_no.value.trim(),

                })

            }
            if (sessionStorage.getItem('country_id') !== 'SA' && sessionStorage.getItem('marital') === 'single') {
                next_bank_page = 'experience_fieldset'
            } else {
                next_bank_page = 'family_fieldset'
            }
            if (sessionStorage.getItem('marital') == 'single') {
                document.getElementById('spouse_div').hidden = true
                document.getElementById('children_div').hidden = true

            } else {
                document.getElementById('spouse_div').hidden = false
                document.getElementById('children_div').hidden = false

            }
            if (sessionStorage.getItem('country_id') != 'SA') {
                document.getElementById('parents_div').hidden = true

            }
            {
                document.getElementById('parents_div').hidden = false

            }
            go_next('bank_fieldset', next_bank_page)
        }

    })

    $('#family_next_btn').click(async function () {
        ex_done = true
        if (sessionStorage.getItem('country_id') === 'SA') {
            if (father_name.value.trim() === '') {
                setError(father_name, `${father_name.placeholder} is required`);
                ex_done = false
            } else if (father_id_number.value.trim() === '') {
                setError(father_id_number, `${father_id_number.placeholder} is required`);
                ex_done = false
            } else if (father_birthdate.value.trim() === '') {
                setError(father_birthdate, `${father_birthdate.placeholder} is required`);
                ex_done = false
            } else if (father_family_attach.value.trim() === '') {
                setError(father_family_attach, `${father_family_attach.placeholder} is required`);
                ex_done = false
            } else {
                db.father.clear()
                db.father.put({
                    father_name: father_name.value.trim(),
                    father_id_number: father_id_number.value.trim(),
                    father_birthdate: father_birthdate.value.trim(),
                    father_phone: father_phone.value.trim(),
                    father_family_attach: await convertFileToBase64(father_family_attach.files[0])
                })
                ex_done = true
            }
            if (mother_name.value.trim() === '') {
                setError(mother_name, `${mother_name.placeholder} is required`);
                ex_done = false
            } else if (mother_id_number.value.trim() === '') {
                setError(mother_id_number, `${mother_id_number.placeholder} is required`);
                ex_done = false
            } else if (mother_birthdate.value.trim() === '') {
                setError(mother_birthdate, `${mother_birthdate.placeholder} is required`);
                ex_done = false
            } else if (mother_family_attach.value.trim() === '') {
                setError(mother_family_attach, `${mother_family_attach.placeholder} is required`);
                ex_done = false
            } else {
                db.mother.clear()
                db.mother.put({
                    mother_name: mother_name.value.trim(),
                    mother_id_number: mother_id_number.value.trim(),
                    mother_birthdate: mother_birthdate.value.trim(),
                    mother_phone: mother_phone.value.trim(),
                    mother_family_attach: await convertFileToBase64(mother_family_attach.files[0])
                })
                ex_done = true
            }
        }
        execu = true

        if (sessionStorage.getItem('marital') !== 'single') {
            if (spouse_name.value.trim() === '') {
                setError(spouse_name, `${spouse_name.placeholder} is required`);
                ex_done = false
            } else if (spouse_id_number.value.trim() === '') {
                setError(spouse_id_number, `${spouse_id_number.placeholder} is required`);
                ex_done = false
            } else if (spouse_birthdate.value.trim() === '') {
                setError(spouse_birthdate, `${spouse_birthdate.placeholder} is required`);
                ex_done = false
            } else if (spouse_family_attach.value.trim() === '') {
                setError(spouse_family_attach, `${spouse_family_attach.placeholder} is required`);
                ex_done = false
            } else {
                db.spouse.clear()
                db.spouse.put({
                    spouse_name: spouse_name.value.trim(),
                    spouse_id_number: spouse_id_number.value.trim(),
                    spouse_birthdate: spouse_birthdate.value.trim(),
                    spouse_phone: spouse_phone.value.trim(),
                    spouse_family_attach: await convertFileToBase64(spouse_family_attach.files[0])
                })
                ex_done = true
            }
            let result = [];
            $("#family_info_table tbody tr").each(function () {
                var allValues = {};
                $(this).find("input").each(function (index) {

                    if ($(this).val() === '' && $(this).attr("name") !== 'phone') {

                        setError(this.parentElement, `${this.placeholder} is required`);
                        execu = false
                    } else {
                        const fieldName = $(this).attr("name");
                        allValues[fieldName] = $(this).val();
                        execu = true
                    }


                });
                $(this).find("select").each(function (index) {

                    if ($(this).val() === '') {
                        setError(this.parentElement, `${this.placeholder} is required`);
                        execu = false
                    } else {
                        const fieldName = $(this).attr("name");
                        allValues[fieldName] = $(this).val();
                        execu = true
                    }

                });
                result.push(allValues);
            })
            if (execu) {
                db.children.clear()
                for (const item of result) {
                    db.children.add({
                        child_name: item['name'],
                        child_id_number: item['id_number'],
                        child_birthdate: item['birthdate'],
                        child_gender: item['gender'],
                        child_phone: item['phone'],
                        child_family_attach: await convertFileToBase64(new File(["file"], item['family_attach']))
                    })
                }
            }
        }
        if (ex_done && execu) {
            go_next('family_fieldset', 'experience_fieldset')
        }


    })

    $('#experience_next_btn').click(async function () {
        let result = [];
        execu = true
        $("#experience_table tbody tr").each(function () {
            var allValues = {};
            $(this).find("input").each(function (index) {
                if ($(this).val() === '') {
                    setError(this.parentElement, `${this.placeholder} is required`);
                    execu = false
                } else {
                    const fieldName = $(this).attr("name");
                    allValues[fieldName] = $(this).val();
                    execu = true
                }

            });
            result.push(allValues);
        })
        if (execu) {
            for (const item of result) {
                const index = result.indexOf(item);
                db.experience.clear()
                db.experience.add({
                    job_name: item['job_name'],
                    employer_name: item['employer_name'],
                    date_from: item['date_from'],
                    date_to: item['date_to'],
                    service_certificate: await convertFileToBase64(new File(["file"], item['service_certificate']))
                })
            }
            db.transaction('r', db.tables, () => {
                return Promise.all(
                    db.tables.map(table => table.toArray()
                        .then(rows => ({table: table.name, rows: rows}))));
            }).then(function (jsondb) {
                $.ajax({
                    url: '/job/app/submit',
                    type: 'post',
                    dataType: 'json',
                    contentType: "application/json; charset=utf-8",
                    data: JSON.stringify({
                        'application_token': $('#application_token').val(),
                        'csrfmiddlewaretoken': '{{ csrf_token }}',
                        'db': JSON.stringify(jsondb)
                    }),
                    success: function (ress) {
                        go_next('experience_fieldset', 'success_fieldset')
                        console.log(ress)
                    }
                })
            });

        }


    })
    $('#export_next_btn').click(async function () {
        db.transaction('r', db.tables, () => {
            return Promise.all(
                db.tables.map(table => table.toArray()
                    .then(rows => ({table: table.name, rows: rows}))));
        }).then(function (jsondb) {
            $.ajax({
                url: '/job/app/submit',
                type: 'post',
                dataType: 'json',
                contentType: "application/json; charset=utf-8",
                data: JSON.stringify({
                    'application_token': $('#application_token').val(),
                    'csrfmiddlewaretoken': '{{ csrf_token }}',
                    'db': JSON.stringify(jsondb)
                }),
                success: function (ress) {
                    go_next('experience_fieldset', 'success_fieldset')
                    console.log(ress)
                }
            })
        });
    })

    function convertFileToBase64(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onload = () => resolve(reader.result);
            // Typescript users: use following line
            // reader.onload = () => resolve(reader.result as string);
            reader.onerror = reject;
        });
    }

    $('#birthday').datepicker({
        format: "dd-mm-yyyy",
        endDate: '-6575d',
        autoclose: true
    });
    $('#gosi_start_date').datepicker({
        format: "dd-mm-yyyy",
        endDate: '-1d',
        autoclose: true
    });
    $('#graduate_date').datepicker({
        format: "dd-mm-yyyy",
        endDate: '-3d',
        autoclose: true
    });

    $('#expiration_date').datepicker({
        format: "dd-mm-yyyy",
        endDate: '-3d',
        autoclose: true
    });

    $('#arrival_date').datepicker({
        format: "dd-mm-yyyy",
        endDate: '-3d',
        autoclose: true
    });
    $('#resid_issuance_date').datepicker({
        format: "dd-mm-yyyy",
        endDate: '-3d',
        autoclose: true
    });
    $('#expiration_date_in_hijri').datepicker({
        format: "dd-mm-yyyy",
        endDate: '-3d',
        autoclose: true
    });

    $('#father_birthdate').datepicker({
        format: "dd-mm-yyyy",
        endDate: '-6575d',
        autoclose: true
    });
    $('#mother_birthdate').datepicker({
        format: "dd-mm-yyyy",
        endDate: '-6575d',
        autoclose: true
    });
    $('#spouse_birthdate').datepicker({
        format: "dd-mm-yyyy",
        endDate: '-6575d',
        autoclose: true
    });
    $('#birthdate').datepicker({
        format: "dd-mm-yyyy",
        endDate: '-3d',
        autoclose: true
    });

});


