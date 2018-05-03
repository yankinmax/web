-- UPDATE mtsmte_accounting.board_management_dash_view noupdate to False
UPDATE ir_model_data
    SET noupdate = false
    WHERE name ='board_management_dash_view'
      AND module ='mtsmte_accounting'
      AND model ='ir.ui.view';
