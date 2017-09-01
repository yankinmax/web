-- Clean bad translation
-- which will recreate correctly when the module will be updated

DELETE FROM
    ir_translation
WHERE
    module = 'specific_payment_mode'
AND lang = 'fr_FR'
AND value = 'Mode de paiement';

DELETE FROM
    ir_translation
WHERE
    module = 'specific_payment_mode'
AND lang = 'fr_FR'
AND value LIKE 'L''apport doit être%';

-- Update XMLID from discount_program_report module data

UPDATE ir_model_data
SET name = 'voucher_config_template_fr',
    noupdate = true
WHERE module = 'discount_program_report'
AND name = 'config_template_fr'
AND model = 'sale.discount.program.report.config';

UPDATE ir_model_data
SET name = 'gift_card_to_create'
WHERE module = 'discount_program_report'
AND name = 'gift_card'
AND model = 'product.product';

UPDATE ir_model_data
SET name = 'gift_card_to_create_template'
WHERE module = 'discount_program_report'
AND name = 'gift_card_template'
AND model = 'product.template';
