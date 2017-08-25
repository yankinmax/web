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
