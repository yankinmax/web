-- UPDATE mtsmte_reports.report_analysis_doc noupdate to false
UPDATE ir_model_data
    SET noupdate = false
    WHERE name ='report_analysis_doc'
      AND module ='mtsmte_reports'
      AND model ='ir.ui.view';
