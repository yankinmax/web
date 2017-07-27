-- Clean bad translation
-- which will recreate correctly when the module will be updated

DELETE FROM
    ir_translation
WHERE
    module = 'sale_discount_program'
AND lang = 'fr_FR'
AND src = 'Quantity is the sum of matching products quantities';
