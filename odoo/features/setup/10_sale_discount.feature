# -*- coding: utf-8 -*-
@depiltech @setup @sale_config

Feature: Parameter the new database
  In order to have a coherent installation
  I've automated the manual steps.

  @order_line_discount
  Scenario: Active discount on sale order line
    Given I set "Discount" to "Allow discounts on sales order lines" in "Sales" settings menu

  @&
  Scenario: Create discount pricelist
    Given I need a "product.pricelist" with oid: scenario.pricelist_sponsorship
      And having:
         | key          | value                     |
         | name         | Parrainage                |

    Given I need a "product.pricelist.item" with oid: scenario.pricelist_sponsorship_item1
      And having:
         | key           | value                                  |
         | pricelist_id  | by oid: scenario.pricelist_sponsorship |
         | applied_on    | 3_global                               |
         | compute_price | percentage                             |
         | percent_price | 10                                     |

    Given I need a "product.pricelist" with oid: scenario.pricelist_code_promo
      And having:
         | key          | value                     |
         | name         | Code promo                |

    Given I need a "product.pricelist.item" with oid: scenario.pricelist_code_promo_item1
      And having:
         | key           | value                                  |
         | pricelist_id  | by oid: scenario.pricelist_code_promo |
         | applied_on    | 3_global                               |
         | compute_price | percentage                             |
         | percent_price | 10                                     |

  @discount_config
  Scenario: setup of program discount config
    Given I need a "ir.config_parameter" with key: force_discount_apply
    And having:
      | key   | value                    |
      | key   | force_discount_apply     |
      | value | True                     |

    Given I need a "ir.config_parameter" with key: voucher_default_validity
    And having:
      | key   | value                    |
      | key   | voucher_default_validity |
      | value | 10                       |

    Given I need a "ir.config_parameter" with key: voucher_max_count
    And having:
      | key   | value                 |
      | key   | voucher_max_count     |
      | value | 2                     |

    Given I need a "ir.config_parameter" with key: voucher_max_amount
    And having:
      | key   | value                 |
      | key   | voucher_max_amount    |
      | value | 100                   |

    Given I need a "ir.config_parameter" with key: voucher_percent
    And having:
      | key   | value              |
      | key   | voucher_percent    |
      | value | 10                 |
