-- Drop table created automatically by base update on 10.3.0
DROP TABLE IF EXISTS x_bi_sql_view_engagements;
-- Recreating the view deleted on 10.3.0
CREATE OR REPLACE VIEW "public".x_bi_sql_view_engagements AS
 SELECT row_number() OVER ()::integer AS id,
    NULL::timestamp without time zone AS create_date,
    NULL::integer AS create_uid,
    NULL::timestamp without time zone AS write_date,
    NULL::integer AS write_uid,
    my_query.x_doc_number,
    my_query.x_invoice_status,
    my_query.x_partner,
    my_query.x_ref_date,
    my_query.x_currency,
    my_query.x_doc_total,
    my_query.x_already_invoiced,
    my_query.x_engagements
   FROM ( SELECT eng.doc_number AS x_doc_number,
            eng.invoice_status AS x_invoice_status,
            eng.partner AS x_partner,
            eng.ref_date AS x_ref_date,
            eng.currency AS x_currency,
            eng.doc_total AS x_doc_total,
            eng.total_already_invoiced AS x_already_invoiced,
            eng.engagements AS x_engagements
           FROM ( SELECT so_line.doc_number,
                    so_line.invoice_status,
                    so_line.partner,
                    so_line.confirmation_date AS ref_date,
                    so_line.currency,
                    sum(so_line.line_total) AS doc_total,
                    sum(so_line.total_already_invoiced) AS total_already_invoiced,
                    sum(so_line.line_total) - sum(so_line.total_already_invoiced) AS engagements
                   FROM ( SELECT so.name AS doc_number,
                            so.invoice_status,
                            part.name AS partner,
                            so.confirmation_date,
                            cur.name AS currency,
                            sol.price_total AS line_total,
                            COALESCE(( SELECT sum(COALESCE(il.price_unit, 0::numeric) * COALESCE(il.quantity, 0::numeric)) AS sum
                                   FROM sale_order_line_invoice_rel lnk,
                                    account_invoice_line il
                                  WHERE sol.id = lnk.order_line_id AND lnk.invoice_line_id = il.id AND (EXISTS ( SELECT 1
   FROM account_invoice ai
  WHERE ai.id = il.invoice_id AND ai.state::text <> 'cancel'::text))), 0::numeric) AS total_already_invoiced
                           FROM sale_order so,
                            sale_order_line sol,
                            res_partner part,
                            res_currency cur
                          WHERE so.id = sol.order_id AND so.partner_id = part.id AND sol.currency_id = cur.id AND so.invoice_status::text <> 'no'::text) so_line
                  GROUP BY so_line.doc_number, so_line.invoice_status, so_line.partner, so_line.confirmation_date, so_line.currency
                UNION ALL
                 SELECT po_line.doc_number,
                    po_line.invoice_status,
                    po_line.partner,
                    po_line.date_planned AS ref_date,
                    po_line.currency,
                    - sum(po_line.line_total) AS doc_total,
                    sum(po_line.total_already_invoiced) AS total_already_invoiced,
                    - (sum(po_line.line_total) - sum(po_line.total_already_invoiced)) AS engagements
                   FROM ( SELECT po.name AS doc_number,
                            part.name AS partner,
                            po.date_planned,
                            cur.name AS currency,
                            pol.price_total AS line_total,
                            po.invoice_status,
                            COALESCE(( SELECT sum(COALESCE(il.price_unit, 0::numeric) * COALESCE(il.quantity, 0::numeric)) AS sum
                                   FROM account_invoice_line il,
                                    account_invoice_line_tax tax
                                  WHERE pol.id = il.purchase_line_id AND il.id = tax.invoice_line_id AND (EXISTS ( SELECT 1
   FROM account_invoice ai
  WHERE ai.id = il.invoice_id AND ai.state::text <> 'cancel'::text))), 0::numeric) AS total_already_invoiced
                           FROM purchase_order po,
                            purchase_order_line pol,
                            res_partner part,
                            res_currency cur
                          WHERE po.id = pol.order_id AND po.partner_id = part.id AND pol.currency_id = cur.id AND po.invoice_status::text <> 'no'::text) po_line
                  GROUP BY po_line.doc_number, po_line.partner, po_line.invoice_status, po_line.date_planned, po_line.currency) eng
          WHERE eng.engagements <> 0::numeric) my_query;
