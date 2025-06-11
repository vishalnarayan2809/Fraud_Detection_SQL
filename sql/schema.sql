-- Fraud Detection Database Schema
-- PostgreSQL DDL for creating tables and relationships

-- Drop tables if they exist (for clean setup)
DROP TABLE IF EXISTS transaction CASCADE;
DROP TABLE IF EXISTS credit_card CASCADE;
DROP TABLE IF EXISTS card_holder CASCADE;
DROP TABLE IF EXISTS merchant CASCADE;
DROP TABLE IF EXISTS merchant_category CASCADE;

-- Create merchant_category table
CREATE TABLE merchant_category (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

-- Create card_holder table
CREATE TABLE card_holder (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

-- Create merchant table
CREATE TABLE merchant (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    id_merchant_category INTEGER NOT NULL,
    FOREIGN KEY (id_merchant_category) REFERENCES merchant_category(id)
);

-- Create credit_card table
CREATE TABLE credit_card (
    card VARCHAR(20) PRIMARY KEY,
    id_card_holder INTEGER NOT NULL,
    FOREIGN KEY (id_card_holder) REFERENCES card_holder(id)
);

-- Create transaction table
CREATE TABLE transaction (
    id SERIAL PRIMARY KEY,
    date TIMESTAMP NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    card VARCHAR(20) NOT NULL,
    id_merchant INTEGER NOT NULL,
    FOREIGN KEY (card) REFERENCES credit_card(card),
    FOREIGN KEY (id_merchant) REFERENCES merchant(id)
);

-- Create indexes for better query performance
CREATE INDEX idx_transaction_date ON transaction(date);
CREATE INDEX idx_transaction_amount ON transaction(amount);
CREATE INDEX idx_transaction_card ON transaction(card);
CREATE INDEX idx_transaction_merchant ON transaction(id_merchant);
CREATE INDEX idx_credit_card_holder ON credit_card(id_card_holder);
CREATE INDEX idx_merchant_category ON merchant(id_merchant_category);

-- Create views for fraud detection

-- View 1: High early morning transactions (7-9 AM)
CREATE VIEW early_morning_high_transactions AS
SELECT 
    t.id,
    t.date,
    t.amount,
    t.card,
    ch.name as cardholder_name,
    m.name as merchant_name,
    mc.name as merchant_category
FROM transaction t
JOIN credit_card cc ON t.card = cc.card
JOIN card_holder ch ON cc.id_card_holder = ch.id
JOIN merchant m ON t.id_merchant = m.id
JOIN merchant_category mc ON m.id_merchant_category = mc.id
WHERE EXTRACT(HOUR FROM t.date) BETWEEN 7 AND 9
ORDER BY t.amount DESC;

-- View 2: Small transactions (potential card testing)
CREATE VIEW small_transactions AS
SELECT 
    t.card,
    ch.name as cardholder_name,
    COUNT(*) as small_transaction_count,
    AVG(t.amount) as avg_small_amount,
    MIN(t.amount) as min_amount,
    MAX(t.amount) as max_amount
FROM transaction t
JOIN credit_card cc ON t.card = cc.card
JOIN card_holder ch ON cc.id_card_holder = ch.id
WHERE t.amount < 2.00
GROUP BY t.card, ch.name
ORDER BY small_transaction_count DESC;

-- View 3: Merchant vulnerability analysis
CREATE VIEW merchant_small_transaction_analysis AS
SELECT 
    m.id as merchant_id,
    m.name as merchant_name,
    mc.name as merchant_category,
    COUNT(*) as small_transaction_count,
    AVG(t.amount) as avg_small_amount,
    COUNT(DISTINCT t.card) as unique_cards_affected
FROM transaction t
JOIN merchant m ON t.id_merchant = m.id
JOIN merchant_category mc ON m.id_merchant_category = mc.id
WHERE t.amount < 2.00
GROUP BY m.id, m.name, mc.name
ORDER BY small_transaction_count DESC;

-- View 4: Transaction patterns by hour
CREATE VIEW hourly_transaction_patterns AS
SELECT 
    EXTRACT(HOUR FROM date) as hour_of_day,
    COUNT(*) as transaction_count,
    AVG(amount) as avg_amount,
    SUM(amount) as total_amount,
    MIN(amount) as min_amount,
    MAX(amount) as max_amount
FROM transaction
GROUP BY EXTRACT(HOUR FROM date)
ORDER BY hour_of_day;

-- View 5: Card holder transaction summary
CREATE VIEW cardholder_transaction_summary AS
SELECT 
    ch.id,
    ch.name as cardholder_name,
    COUNT(t.id) as total_transactions,
    AVG(t.amount) as avg_transaction_amount,
    SUM(t.amount) as total_spent,
    MIN(t.amount) as min_transaction,
    MAX(t.amount) as max_transaction,
    STDDEV(t.amount) as amount_stddev
FROM card_holder ch
JOIN credit_card cc ON ch.id = cc.id_card_holder
JOIN transaction t ON cc.card = t.card
GROUP BY ch.id, ch.name
ORDER BY total_spent DESC;

-- View 6: Outlier transactions using statistical methods
CREATE VIEW outlier_transactions AS
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
    ABS(t.amount - ob.mean_amount) / ob.stddev_amount as z_score
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
ORDER BY ABS(t.amount - ob.mean_amount) / ob.stddev_amount DESC;
