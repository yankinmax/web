-- Clean bad translation
-- which will recreate correctly when the module will be updated

DELETE FROM
    ir_translation
WHERE
    module = 'discount_program_report'
AND lang = 'fr_FR'
AND value = 'Valable jusqu''au';

DELETE FROM
    ir_translation
WHERE
    module = 'fields_regex_validation'
AND lang = 'fr_FR'
AND value = 'Validation Regular Expression';

DELETE FROM
    ir_translation
WHERE
    module = 'specific_discount_program'
AND lang = 'fr_FR'
AND value = 'source_sale_id can be filled only for voucher';
