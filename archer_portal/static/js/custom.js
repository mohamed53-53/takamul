

/* This method will add a new row */
function addFamilyRelationNewRow() {
    var table = document.getElementById("family_info_table");
    var rowCount = table.rows.length;
    var cellCount = table.rows[0].cells.length;
    var row = table.insertRow(rowCount);
    for (var i = 0; i < cellCount; i++) {
        var cell = row.insertCell(i);
        if (i < cellCount - 1) {
            if (i == 0) {
                cell.innerHTML = '<input type="text" class="form-control" name="name"/>'
            }
            if (i == 1) {
                cell.innerHTML = '<input type="text" class="form-control" name="id_number"/>'
            }
            if (i == 2) {
                cell.innerHTML = '<select class="form-control" name="relation">\n' +
                    '                                                    <option></option>\n' +
                    '                                                    <option value="spouse">Spouse</option>\n' +
                    '                                                    <option value="child">Child</option>\n' +
                    '                                                </select>'
            }
            if (i == 3) {
                cell.innerHTML = '<select class="form-control gender" name="gender" >\n' +
                    '                                                    <option ></option>\n' +
                    '                                                    <option value="male">Male</option>\n' +
                    '                                                    <option value="female">Female</option>\n' +
                    '                                                </select>'
            }
            if (i == 4) {
                cell.innerHTML = '<input type="date" class="form-control" name="birthdate"/>'
            }
            if (i == 5) {
                cell.innerHTML = '<input type="text" class="form-control" name="phone"/>'
            }

        } else {
            cell.innerHTML = '<input type="button" class="btn btn-danger family_delete_btn" value="delete" />';
        }
    }
    $('.gender').click(function (ev) {
        table = document.getElementById("family_info_table");
        for (let i in table.rows) {
            let row = table.rows[i]
            for (let j in row.cells) {
                let spouse_col = row.cells['2']
                let meal_col = row.cells['3']
                if (spouse_col.nodeName === 'TD' && meal_col.nodeName === 'TD') {
                    e_spouse = spouse_col.children[0]
                    e_meal = meal_col.children[0]
                    if (e_spouse.options[e_spouse.selectedIndex].value === 'spouse') {
                        if (e_meal.options[e_meal.selectedIndex].value === 'male') {
                            if (ev.currentTarget.options[ev.currentTarget.selectedIndex].value === 'female') {
                                alert("This Relation can\'t added")
                                ev.currentTarget.parentNode.parentNode.remove();
                                break
                            }
                        }
                        if (e_meal.options[e_meal.selectedIndex].value === 'female') {
                            if (ev.currentTarget.options[ev.currentTarget.selectedIndex].value === 'male') {
                                alert("This Relation can\'t added")
                                ev.currentTarget.parentNode.parentNode.remove();
                                break
                            }
                        }
                    }
                    if (e_spouse.options[e_spouse.selectedIndex].value === 'spouse' && e_meal.options[e_meal.selectedIndex].value === 'male') {
                        if (ev.currentTarget.options[ev.currentTarget.selectedIndex].value === 'name') {
                            alert("This Relation can\'t added")
                            ev.currentTarget.parentNode.parentNode.remove();
                            break
                        }
                    }
                }
            }
        }


    })
    /* This method will delete a row */
    function deleteFamilyRelationRow(ele) {
        var table = document.getElementById('family_info_table');
        var rowCount = table.rows.length;

        if (ele) {
            //delete specific row
            ele.parentNode.parentNode.remove();
            document.getElementById('family_delete').value += ele.getAttribute('data') + ','
        } else {
            //delete last row
            table.deleteRow(rowCount - 1);
        }
    }
    $('.family_delete_btn').click(function (eb) {
        deleteFamilyRelationRow(this)
    })

}

/* This method will add a new row */
function addExperienceNewRow() {
    var table = document.getElementById("experience_table");
    var rowCount = table.rows.length;
    var cellCount = table.rows[0].cells.length;
    var row = table.insertRow(rowCount);
    for (var i = 0; i < cellCount; i++) {
        var cell = row.insertCell(i);
        if (i < cellCount - 1) {
            if (i == 0) {
                cell.innerHTML = '<input type="text" class="form-control" name="job_name"/>'
            }
            if (i == 1) {
                cell.innerHTML = '<input type="text" class="form-control" name="employer_name"/>'
            }
            if (i == 2) {
                cell.innerHTML = '<input type="date" class="form-control" name="date_from"/>'
            }
            if (i == 3) {
                cell.innerHTML = '<input type="date" class="form-control" name="date_to"/>'
            }
            if (i == 4) {
                cell.innerHTML = '<input type="file" class="form-control" name="service_certificate" multiple="true"/>'
            }


        } else {
            cell.innerHTML = '<input type="button" t-att-data="experience.id" class="btn btn-danger experience_delete_btn" value="delete"   />';
        }
    }
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

$(document).ready(function () {
    if($('.data_state').val() != 'return' && $('.data_state').val() != 'employee_entry'){

        $("#employee_form :input").prop("disabled", true);
    }else {
        $("#employee_form :input").prop("disabled", false);

    }
    /* This method will delete a row */
    function deleteFamilyRelationRow(ele) {
        var table = document.getElementById('family_info_table');
        var rowCount = table.rows.length;
        if (ele) {
            //delete specific row
            ele.parentNode.parentNode.remove();
            document.getElementById('family_delete').value += ele.getAttribute('data') + ','
        } else {
            //delete last row
            table.deleteRow(rowCount - 1);
        }
    }
    $('.family_delete_btn').click(function (eb) {
        deleteFamilyRelationRow(this)
    })

    /* This method will delete a row */
    function deleteExperienceRow(ele) {
        var table = document.getElementById('experience_table');
        var rowCount = table.rows.length;

        if (ele) {
            //delete specific row
            debugger
            ele.parentNode.parentNode.remove();
            debugger;
            document.getElementById('experience_delete').value += ele.getAttribute('data') + ','

        } else {
            //delete last row
            table.deleteRow(rowCount - 1);
        }
    }
    $('.experience_delete_btn').click(function (eb) {
        deleteExperienceRow(this)
    })


})
