-- Standalone SQL Queries for Fraud Detection Analysis
-- These queries can be run directly in PostgreSQL

-- =====================================================
-- 1. TOP 100 HIGHEST EARLY MORNING TRANSACTIONS (7-9 AM)
-- =====================================================
SELECT 
    t.id as transaction_id,
    t.date as transaction_date,
    t.amount,
    t.card,
    ch.name as cardholder_name,
    m.name as merchant_name,
    mc.name as merchant_category,
    EXTRACT(HOUR FROM t.date) as hour_of_transaction
FROM transaction t
JOIN credit_card cc ON t.card = cc.card
JOIN card_holder ch ON cc.id_card_holder = ch.id
JOIN merchant m ON t.id_merchant = m.id
JOIN merchant_category mc ON m.id_merchant_category = mc.id
WHERE EXTRACT(HOUR FROM t.date) BETWEEN 7 AND 9
ORDER BY t.amount DESC
LIMIT 100;

-- =====================================================
-- 2. SMALL TRANSACTIONS (<$2) PER CARDHOLDER
-- =====================================================
SELECT 
    t.card,
    ch.name as cardholder_name,
    COUNT(*) as small_transaction_count,
    AVG(t.amount) as avg_small_amount,
    MIN(t.amount) as min_amount,
    MAX(t.amount) as max_amount,
    STRING_AGG(DISTINCT mc.name, ', ') as merchant_categories_used
FROM transaction t
JOIN credit_card cc ON t.card = cc.card
JOIN card_holder ch ON cc.id_card_holder = ch.id
JOIN merchant m ON t.id_merchant = m.id
JOIN merchant_category mc ON m.id_merchant_category = mc.id
WHERE t.amount < 2.00
GROUP BY t.card, ch.name
ORDER BY small_transaction_count DESC;

-- =====================================================
-- 3. TOP 5 MERCHANTS VULNERABLE TO SMALL TRANSACTION FRAUD
-- =====================================================
SELECT 
    m.id as merchant_id,
    m.name as merchant_name,
    mc.name as merchant_category,
    COUNT(*) as small_transaction_count,
    AVG(t.amount) as avg_small_amount,
    COUNT(DISTINCT t.card) as unique_cards_affected,
    COUNT(DISTINCT ch.id) as unique_cardholders_affected,
    MIN(t.amount) as min_transaction,
    MAX(t.amount) as max_transaction
FROM transaction t
JOIN merchant m ON t.id_merchant = m.id
JOIN merchant_category mc ON m.id_merchant_category = mc.id
JOIN credit_card cc ON t.card = cc.card
JOIN card_holder ch ON cc.id_card_holder = ch.id
WHERE t.amount < 2.00
GROUP BY m.id, m.name, mc.name
ORDER BY small_transaction_count DESC
LIMIT 5;

-- =====================================================
-- 4. TRANSACTION PATTERNS BY HOUR OF DAY
-- =====================================================
SELECT 
    EXTRACT(HOUR FROM date) as hour_of_day,
    COUNT(*) as transaction_count,
    AVG(amount) as avg_amount,
    SUM(amount) as total_amount,
    MIN(amount) as min_amount,
    MAX(amount) as max_amount,
    STDDEV(amount) as amount_stddev
FROM transaction
GROUP BY EXTRACT(HOUR FROM date)
ORDER BY hour_of_day;

-- =====================================================
-- 5. CARDHOLDER SPENDING ANALYSIS
-- =====================================================
SELECT 
    ch.id as cardholder_id,
    ch.name as cardholder_name,
    COUNT(t.id) as total_transactions,
    AVG(t.amount) as avg_transaction_amount,
    SUM(t.amount) as total_spent,
    MIN(t.amount) as min_transaction,
    MAX(t.amount) as max_transaction,
    STDDEV(t.amount) as amount_stddev,
    COUNT(DISTINCT m.id) as unique_merchants_used,
    COUNT(DISTINCT mc.name) as unique_categories_used,
    MIN(t.date) as first_transaction,
    MAX(t.date) as last_transaction
FROM card_holder ch
JOIN credit_card cc ON ch.id = cc.id_card_holder
JOIN transaction t ON cc.card = t.card
JOIN merchant m ON t.id_merchant = m.id
JOIN merchant_category mc ON m.id_merchant_category = mc.id
GROUP BY ch.id, ch.name
ORDER BY total_spent DESC;

-- =====================================================
-- 6. OUTLIER DETECTION USING STATISTICAL METHODS
-- =====================================================
WITH transaction_stats AS (
    SELECT 
        AVG(amount) as mean_amount,
        STDDEV(amount) as stddev_amount,
        PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY amount) as q1,
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY amount) as q3
    FROM transaction
),
outlier_bounds AS (
    SELECT 
        mean_amount,
        stddev_amount,
        q1,
        q3,
        q1 - 1.5 * (q3 - q1) as iqr_lower_bound,
        q3 + 1.5 * (q3 - q1) as iqr_upper_bound,
        mean_amount - 3 * stddev_amount as zscore_lower_bound,
        mean_amount + 3 * stddev_amount as zscore_upper_bound
    FROM transaction_stats
)
SELECT 
    t.id,
    t.date,
    t.amount,
    t.card,
    ch.name as cardholder_name,
    m.name as merchant_name,
    mc.name as merchant_category,
    CASE 
        WHEN t.amount < ob.iqr_lower_bound OR t.amount > ob.iqr_upper_bound THEN 'IQR_Outlier'
        WHEN t.amount < ob.zscore_lower_bound OR t.amount > ob.zscore_upper_bound THEN 'ZScore_Outlier'
        ELSE 'Normal'
    END as outlier_type,
    ob.mean_amount,
    ob.stddev_amount,
    ABS(t.amount - ob.mean_amount) / NULLIF(ob.stddev_amount, 0) as z_score,
    EXTRACT(HOUR FROM t.date) as hour_of_transaction,
    EXTRACT(DOW FROM t.date) as day_of_week
FROM transaction t
JOIN credit_card cc ON t.card = cc.card
JOIN card_holder ch ON cc.id_card_holder = ch.id
JOIN merchant m ON t.id_merchant = m.id
JOIN merchant_category mc ON m.id_merchant_category = mc.id
CROSS JOIN outlier_bounds ob
WHERE t.amount < ob.iqr_lower_bound 
   OR t.amount > ob.iqr_upper_bound 
   OR t.amount < ob.zscore_lower_bound 
   OR t.amount > ob.zscore_upper_bound
ORDER BY ABS(t.amount - ob.mean_amount) / NULLIF(ob.stddev_amount, 0) DESC;

-- =====================================================
-- 7. RAPID SUCCESSIVE TRANSACTIONS (WITHIN 5 MINUTES)
-- =====================================================
WITH transaction_with_lag AS (
    SELECT 
        t.*,
        ch.name as cardholder_name,
        m.name as merchant_name,
        mc.name as merchant_category,
        LAG(t.date) OVER (PARTITION BY t.card ORDER BY t.date) as prev_transaction_date,
        LEAD(t.date) OVER (PARTITION BY t.card ORDER BY t.date) as next_transaction_date
    FROM transaction t
    JOIN credit_card cc ON t.card = cc.card
    JOIN card_holder ch ON cc.id_card_holder = ch.id
    JOIN merchant m ON t.id_merchant = m.id
    JOIN merchant_category mc ON m.id_merchant_category = mc.id
),
rapid_transactions AS (
    SELECT 
        *,
        CASE 
            WHEN prev_transaction_date IS NOT NULL 
            THEN EXTRACT(EPOCH FROM (date - prev_transaction_date))/60 
            ELSE NULL 
        END as minutes_since_prev,
        CASE 
            WHEN next_transaction_date IS NOT NULL 
            THEN EXTRACT(EPOCH FROM (next_transaction_date - date))/60 
            ELSE NULL 
        END as minutes_to_next
    FROM transaction_with_lag
)
SELECT 
    id,
    date,
    amount,
    card,
    cardholder_name,
    merchant_name,
    merchant_category,
    minutes_since_prev,
    minutes_to_next
FROM rapid_transactions
WHERE (minutes_since_prev IS NOT NULL AND minutes_since_prev <= 5)
   OR (minutes_to_next IS NOT NULL AND minutes_to_next <= 5)
ORDER BY card, date;

-- =====================================================
-- 8. MERCHANT CATEGORY ANALYSIS
-- =====================================================
SELECT 
    mc.name as merchant_category,
    COUNT(t.id) as total_transactions,
    AVG(t.amount) as avg_transaction_amount,
    SUM(t.amount) as total_volume,
    MIN(t.amount) as min_amount,
    MAX(t.amount) as max_amount,
    COUNT(DISTINCT t.card) as unique_cards,
    COUNT(DISTINCT m.id) as number_of_merchants
FROM merchant_category mc
JOIN merchant m ON mc.id = m.id_merchant_category
JOIN transaction t ON m.id = t.id_merchant
GROUP BY mc.id, mc.name
ORDER BY total_volume DESC;

-- =====================================================
-- 9. WEEKEND VS WEEKDAY TRANSACTION PATTERNS
-- =====================================================
SELECT 
    CASE 
        WHEN EXTRACT(DOW FROM date) IN (0, 6) THEN 'Weekend'
        ELSE 'Weekday'
    END as day_type,
    COUNT(*) as transaction_count,
    AVG(amount) as avg_amount,
    SUM(amount) as total_volume,
    MIN(amount) as min_amount,
    MAX(amount) as max_amount
FROM transaction
GROUP BY CASE 
    WHEN EXTRACT(DOW FROM date) IN (0, 6) THEN 'Weekend'
    ELSE 'Weekday'
END
ORDER BY day_type;

-- =====================================================
-- 10. MONTHLY TRANSACTION TRENDS
-- =====================================================
SELECT 
    EXTRACT(YEAR FROM date) as transaction_year,
    EXTRACT(MONTH FROM date) as transaction_month,
    COUNT(*) as transaction_count,
    AVG(amount) as avg_amount,
    SUM(amount) as total_volume,
    COUNT(DISTINCT card) as unique_cards_used
FROM transaction
GROUP BY EXTRACT(YEAR FROM date), EXTRACT(MONTH FROM date)
ORDER BY transaction_year, transaction_month;
