-- Drop this view before applying base update (we will recreate it afterwards)
DROP VIEW x_bi_sql_view_engagements;

-- Update XMLIDs of CSV imported taxes, tags and report lines with wrong
-- module name and nopupdate flag
UPDATE ir_model_data
SET module = '__setup__'
, noupdate = true
WHERE module = 'l10n_ch'
AND model = 'account.tax';

UPDATE ir_model_data
SET module = '__setup__'
, noupdate = true
WHERE module = 'l10n_ch'
AND name IN ('vat_tag_302'
,'vat_tag_302b'
,'vat_tag_342'
,'vat_tag_342b');

UPDATE ir_model_data
SET module = '__setup__'
, noupdate = true
WHERE module = 'l10n_ch_reports'
AND name IN (
'financial_report_line_chtax_302a'
,'financial_report_line_chtax_342a'
,'financial_report_line_chtax_302b'
,'financial_report_line_chtax_342b'
);
