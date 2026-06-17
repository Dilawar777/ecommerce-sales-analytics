# Business Memo: Brazilian E-Commerce Performance Analysis

**To:** Operations & Strategy Leadership
**From:** Dilawar Mahar, Data Analyst
**Date:** June 2026
**Re:** Key findings and recommendations from 2016–2018 sales data analysis

---

## Summary

An analysis of 96,426 delivered orders (R$19.8M in revenue) from the Olist marketplace reveals three structural issues limiting growth: a severe regional logistics gap, inconsistent product quality in specific categories, and a heavy revenue concentration in a single state. Addressing these could meaningfully improve both revenue and customer satisfaction without requiring new market entry.

## Key Findings

**1. Delivery speed is the strongest driver of customer satisfaction.**
Orders delivered within 7 days average a 4.33/5 review score, while orders taking 22+ days average just 3.01/5 — a 1.3 point drop. Delivery time is a stronger predictor of satisfaction than product category or price.

**2. Remote states are underserved and underperforming.**
The 10 lowest-revenue states (including RR, AP, AC, AM) show average delivery times of 17–25 days, nearly double the fastest delivery bucket. This is very likely suppressing demand rather than reflecting genuinely lower interest in these regions.

**3. Revenue is heavily concentrated in São Paulo.**
São Paulo alone generates more revenue than the next four highest states combined, indicating an over-reliance on a single regional market.

**4. office_furniture underperforms on quality despite reasonable volume.**
Among categories with 100+ orders, office_furniture has the lowest average review score (3.52/5), suggesting packaging, durability, or shipping damage issues specific to this category.

**5. May is the peak revenue month.**
Demand consistently peaks in May across the dataset, useful for inventory and marketing planning.

**6. Data limitation.**
Olist assigns a unique customer ID per order, making true repeat-purchase analysis impossible with this dataset alone. Any retention figures derived from this data should be treated as directional, not exact.

## Recommendations

1. **Prioritize logistics investment in the 10 lowest-revenue states.** Even a partial reduction in delivery time (from 20+ days toward the 14-day mark) could improve both order volume and review scores in these regions, based on the strong correlation observed.

2. **Audit the office_furniture supply chain.** Investigate packaging standards and carrier handling specifically for this category before considering broader product-line changes.

3. **Diversify regional marketing investment.** Reduce dependency on São Paulo by testing targeted promotions in mid-tier states (RJ, MG, RS) where revenue is meaningful but has room to grow.

4. **Plan inventory and staffing around the May peak.** Ensure adequate stock levels for top categories (bed_bath_table, health_beauty, computers_accessories) ahead of this period.

5. **Invest in proper customer-level tracking** to enable accurate repeat-purchase and lifetime-value analysis going forward.

---

*Analysis based on Olist's public e-commerce dataset (2016–2018). Full methodology, code, and interactive dashboard available at: github.com/Dilawar777/ecommerce-sales-analytics*
