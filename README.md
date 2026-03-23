# 💊 DisNet DrugSlayer

A command-line application for programmatic access to the **DisNet** (Disease Network) database, enabling querying, management and modification of data on drugs, diseases, phenotypic effects and molecular targets.

> Developed by **Paula de Blas Rioja** and **Lucía de Lamadrid Ordóñez** — Database Systems, 2023–2024.

---

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation & Usage](#installation--usage)
- [Main Menu](#main-menu)
- [SQL Queries](#sql-queries)
- [Design Decisions](#design-decisions)
- [Authors](#authors)

---

## Overview

DisNet DrugSlayer is a Python terminal application that connects to a MySQL database containing biomedical information. It allows the user to:

- Query general statistics about the database.
- Look up detailed drug information (synonyms, ATC codes, chemical structure).
- Explore disease–drug associations and their inference scores.
- Browse phenotypic effects: indications and side effects.
- Analyse molecular targets by type and organism.
- Safely delete, insert and update records.

---

## Project Structure

```
disnet-drugslayer/
│
├── main.py              # Entry point: connects to DB and launches the menu
├── conexion_bd.py       # BD class: MySQL connection management
├── menu_principal.py    # Menu class: interactive main menu
├── submenus.py          # Submenu class: submenus for each option
│
├── opcion_1.py          # General database information
├── opcion_2.py          # Drug information
├── opcion_3.py          # Disease information
├── opcion_4.py          # Phenotypic effects
├── opcion_5.py          # Molecular targets
├── opcion_6_7_8.py      # Delete, insert and modify operations
│
├── requirements.txt     # Project dependencies
└── docs/
    └── queries.md       # Full SQL query reference
```

---

## Requirements

- Python 3.8+
- MySQL Server (with the `disnet_drugslayer` database set up)
- Python dependencies (see `requirements.txt`):

```
tabulate
mysql-connector-python
```

---

## Installation & Usage

### 1. Clone the repository

```bash
git clone https://github.com/username/disnet-drugslayer.git
cd disnet-drugslayer
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure the database connection

Make sure MySQL is running with the correct credentials. The connection config lives in `conexion_bd.py`:

```python
config = {
    'user': 'disnet_user',
    'password': 'disnet_pwd',
    'host': 'localhost',
    'database': 'disnet_drugslayer',
}
```

Update these values to match your local environment if needed.

### 4. Run the application

```bash
python main.py
```

---

## Main Menu

On launch, the following interactive menu is displayed in the terminal:

```
              WELCOME TO
  ____  _                _     ____  ____ 
 |  _ \(_)___ _ __   ___| |_  | __ )|  _ \ 
 | | | | / __| '_ \ / _ \ __| |  _ \| | | |
 | |_| | \__ \ | | |  __/ |_  | |_) | |_| |
 |____/|_|___/_| |_|\___|\__| |____/|____/ 

----------------------------------------
1. General database information
2. Drug information
3. Disease information
4. Phenotypic effect information
5. Target information
6. Delete an association
7. Insert drug encodings
8. Modify score
----------------------------------------
9. Exit
```

### Available submenus

| Option | Sub | Description |
|--------|-----|-------------|
| **1** | a | Total count of drugs, diseases, phenotypic effects and targets |
| **1** | b | First 10 instances of each entity |
| **2** | a | Drug information by ChEMBL ID |
| **2** | b | Synonyms of a drug by name |
| **2** | c | ATC code of a drug by ChEMBL ID |
| **3** | a | Drugs associated with a given disease |
| **3** | b | Drug–disease pair with the highest association score |
| **3** | c | Drug with the highest association score for a given disease *(extra)* |
| **4** | a | Indications for a given drug |
| **4** | b | Side effects for a given drug (ordered by score) |
| **5** | a | First 20 targets of a given type (alphabetical order) |
| **5** | b | Organism with the highest number of distinct targets |
| **6** | — | Delete one of the 10 associations with the lowest score |
| **7** | — | Insert a new encoding for a drug |
| **8** | — | Set to 0 all side effect scores below a given threshold |
| **9** | — | Close connection and exit |

---

## SQL Queries

### Option 1a — General counts

```sql
SELECT
    (SELECT COUNT(*) FROM drug) AS NumDrugs,
    (SELECT COUNT(DISTINCT disease_id) FROM disease) AS NumDiseases,
    (SELECT COUNT(*) FROM phenotype_effect) AS NumPhenoEff,
    (SELECT COUNT(DISTINCT target_id) FROM target) AS NumTargets;
```

### Option 2b — Drug synonyms

```sql
SELECT s.synonymous_name AS synonym_name
FROM synonymous AS s
INNER JOIN drug AS d ON d.drug_id = s.drug_id
WHERE d.drug_name = %s;
```

### Option 3b — Highest association score (global)

```sql
SELECT disease_code.name AS disease_name,
       d.drug_name AS drug_name,
       dd.inferred_score AS association_score
FROM disease_code
JOIN drug_disease AS dd ON disease_code.code_id = dd.code_id
JOIN drug AS d ON dd.drug_id = d.drug_id
ORDER BY dd.inferred_score DESC
LIMIT 1;
```

### Option 6 — Delete association

```sql
DELETE FROM drug_disease
WHERE code_id = (SELECT code_id FROM disease_code WHERE name = %s)
  AND drug_id = (SELECT drug_id FROM drug WHERE drug_name = %s);
```

### Option 7 — Insert encoding

```sql
INSERT INTO drug_has_code (drug_id, code_id, vocabulary)
SELECT drug.drug_id, %s, %s
FROM drug
WHERE drug.drug_name = %s;
```

### Option 8 — Update scores

```sql
UPDATE drug_phenotype_effect
SET score = 0
WHERE score < %s
  AND phenotype_type = 'SIDE EFFECT';
```

> For the full SQL reference, see [`docs/queries.md`](docs/queries.md).

---

## Design Decisions

### Modularisation
The code is split across multiple files, each containing a class that groups related functions. To run the project, simply execute `main.py`.

### Circular imports
To avoid circular import errors between `Menu` and the option classes, **local imports are used inside functions** rather than at the top of each file.

### SQL injection prevention
All queries that accept user input use **`%s` placeholders** with the MySQL connector, instead of string concatenation. This prevents user input from being interpreted as part of the SQL statement.

```python
# ✅ Safe — parameterised query
cursor.execute("SELECT * FROM drug WHERE drug_name = %s;", (name,))

# ❌ Unsafe — vulnerable to SQL injection
cursor.execute(f"SELECT * FROM drug WHERE drug_name = '{name}';")
```

> Note: `opcion_2.py` (`dos_a`) still uses an f-string for one query. This should ideally be migrated to the parameterised format.

### Error handling
`try/except` blocks with two layers:
- `mysql.connector.Error` — MySQL-specific errors.
- `Exception` — any other unexpected error.

The database connection is only closed on database-related errors, not on general application errors.

### Navigation
After each query result, the user is offered the option to return to the main menu or repeat the operation, via `Menu.salir_menu(current_function)`.

---

## Authors

| Name | ID |
|------|----|
| Paula de Blas Rioja | 16629972Y |
| Lucía de Lamadrid Ordóñez | 09133993A |

---

*Database Systems — Academic Year 2023–2024*
