```mermaid
erDiagram
    %% Fraud Detection Database - Entity Relationship Diagram
    
    MERCHANT_CATEGORY {
        int id PK "SERIAL PRIMARY KEY"
        varchar name "VARCHAR(50) NOT NULL"
    }
    
    CARD_HOLDER {
        int id PK "SERIAL PRIMARY KEY" 
        varchar name "VARCHAR(100) NOT NULL"
    }
    
    MERCHANT {
        int id PK "SERIAL PRIMARY KEY"
        varchar name "VARCHAR(200) NOT NULL"
        int id_merchant_category FK "INTEGER NOT NULL"
    }
    
    CREDIT_CARD {
        varchar card PK "VARCHAR(20) PRIMARY KEY"
        int id_card_holder FK "INTEGER NOT NULL"
    }
    
    TRANSACTION {
        int id PK "SERIAL PRIMARY KEY"
        timestamp date "TIMESTAMP NOT NULL"
        decimal amount "DECIMAL(10,2) NOT NULL"
        varchar card FK "VARCHAR(20) NOT NULL"
        int id_merchant FK "INTEGER NOT NULL"
    }
    
    %% Relationships
    MERCHANT_CATEGORY ||--o{ MERCHANT : "categorizes"
    CARD_HOLDER ||--o{ CREDIT_CARD : "owns"
    CREDIT_CARD ||--o{ TRANSACTION : "used_in"
    MERCHANT ||--o{ TRANSACTION : "processes"
    
    %% Fraud Detection Views (represented as entities for clarity)
    EARLY_MORNING_HIGH_TRANSACTIONS {
        int transaction_id
        timestamp date
        decimal amount
        varchar card
        varchar cardholder_name
        varchar merchant_name
        varchar merchant_category
    }
    
    SMALL_TRANSACTIONS {
        varchar card
        varchar cardholder_name
        int small_transaction_count
        decimal avg_small_amount
        decimal min_amount
        decimal max_amount
    }
    
    MERCHANT_VULNERABILITY_ANALYSIS {
        int merchant_id
        varchar merchant_name
        varchar merchant_category
        int small_transaction_count
        decimal avg_small_amount
        int unique_cards_affected
    }
    
    OUTLIER_TRANSACTIONS {
        int transaction_id
        timestamp date
        decimal amount
        varchar card
        varchar cardholder_name
        varchar merchant_name
        varchar merchant_category
        varchar outlier_type
        decimal z_score
    }
    
    %% View relationships (dotted lines to show they're derived)
    TRANSACTION ||..o{ EARLY_MORNING_HIGH_TRANSACTIONS : "filters_7_9am"
    TRANSACTION ||..o{ SMALL_TRANSACTIONS : "groups_small_amounts"
    MERCHANT ||..o{ MERCHANT_VULNERABILITY_ANALYSIS : "analyzes_vulnerability"
    TRANSACTION ||..o{ OUTLIER_TRANSACTIONS : "detects_outliers"
```

## Fraud Detection Database - ERD Explanation

### **Core Entities:**

1. **MERCHANT_CATEGORY** - Business type classifications (restaurant, coffee shop, bar, pub, food truck)
2. **CARD_HOLDER** - Individual customers who own credit cards
3. **MERCHANT** - Businesses that process transactions
4. **CREDIT_CARD** - Individual credit cards linked to cardholders
5. **TRANSACTION** - Individual purchase transactions

### **Key Relationships:**

- **One-to-Many**: Each merchant category can have multiple merchants
- **One-to-Many**: Each cardholder can have multiple credit cards
- **One-to-Many**: Each credit card can have multiple transactions
- **One-to-Many**: Each merchant can process multiple transactions

### **Fraud Detection Views:**

The diagram also shows the specialized views created for fraud detection:

- **EARLY_MORNING_HIGH_TRANSACTIONS**: Filters transactions between 7-9 AM
- **SMALL_TRANSACTIONS**: Groups cards with multiple small transactions (<$2)
- **MERCHANT_VULNERABILITY_ANALYSIS**: Analyzes merchants prone to fraud
- **OUTLIER_TRANSACTIONS**: Statistical outlier detection using IQR and Z-score

### **Data Integrity:**

- **Primary Keys**: Ensure unique identification of each record
- **Foreign Keys**: Maintain referential integrity between related tables
- **NOT NULL constraints**: Ensure critical data is always present
- **Indexes**: Optimize query performance for fraud detection queries

This ERD represents a normalized database design optimized for fraud detection analysis with proper relationships and constraints to ensure data integrity.
