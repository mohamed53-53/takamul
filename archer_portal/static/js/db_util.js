var db = new Dexie("employee_app");

db.version(1).stores({
    personal: '++id,name_en,name_ar,birthday,country,civil_id,civil_id_attach,passport,passport_attach,marital,gender,national_address,' +
        'gosi_number,gosi_start_date,gosi_attach,' +
        'national_address_attach,email_from,phone,partner_mobile,country_of_birth,place_of_birth,religion,graduate_date,' +
        'certificate,study_field,study_school,certificate_attach,' +
        'sponsor_name,sponsor_phone,sponsor_address,' +
        'residency_number,serial_number,resid_job_title,place_of_issuance,expiration_date,expiration_date_in_hijri,arrival_date,residency_attach,' +
        'international_bank,bank_id,bank_country_id,bank_name,branch_name_code,iban_no,reconfirm_iban_no',
    father:'++id,father_name,father_id_number,father_birthdate,father_phone,father_family_attach',
    mother:'++id,mother_name,mother_id_number,mother_birthdate,mother_phone,mother_family_attach',
    spouse:'++id,spouse_name,spouse_id_number,spouse_birthdate,spouse_phone,spouse_family_attach',
    children:'++id,child_name,child_id_number,child_gender,child_birthdate,child_phone,child_family_attach',
    experience:'++id,job_name,employer_name,date_from,date_to,service_certificate',
    attaches:'++id,dbid,name,attach'
});

