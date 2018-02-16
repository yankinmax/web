-- Drop this view before applying base update (we will recreate it afterwards)
DROP VIEW x_bi_sql_view_engagements;

-- Update XMLIDs of CSV imported taxes with wrong module name
UPDATE ir_model_data
SET "module" = '__import__'
WHERE "module" = 'l10n_ch'
AND model = 'account.tax';
