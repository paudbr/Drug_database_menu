# SQL Query Reference — DisNet DrugSlayer

> Complete documentation of all SQL queries used in the project, organised by menu option.

---

## Option 1 — General Information

### 1a. Total counts

```sql
SELECT
    (SELECT COUNT(*) FROM drug) AS NumDrugs,
    (SELECT COUNT(DISTINCT disease_id) FROM disease) AS NumDiseases,
    (SELECT COUNT(*) FROM phenotype_effect) AS NumPhenoEff,
    (SELECT COUNT(DISTINCT target_id) FROM target) AS NumTargets;
```

### 1b. First 10 instances per entity

**Drugs:**
```sql
SELECT drug_id AS identifier, drug_name AS name,
       molecular_type, chemical_structure, inchi_key
FROM drug
WHERE COALESCE(drug_id, drug_name, molecular_type, chemical_structure, inchi_key) IS NOT NULL
LIMIT 10;
```

**Diseases:**
```sql
SELECT disease_id AS identifier, disease_name AS name
FROM disease
WHERE COALESCE(disease_id, disease_name) IS NOT NULL
LIMIT 10;
```

**Phenotypic effects:**
```sql
SELECT phenotype_id AS identifier, phenotype_name AS name
FROM phenotype_effect
WHERE COALESCE(phenotype_id, phenotype_name) IS NOT NULL
LIMIT 10;
```

**Targets:**
```sql
SELECT t.target_id AS identifier, t.target_name_pref AS name,
       t.target_type AS type, o.taxonomy_name AS organism_name
FROM target AS t
INNER JOIN organism AS o ON t.organism_id = o.taxonomy_id
WHERE COALESCE(t.target_id, t.target_name_pref, o.taxonomy_name) IS NOT NULL
LIMIT 10;
```

---

## Option 2 — Drug Information

### 2a. Drug info by ChEMBL ID

```sql
SELECT drug_name AS name, molecular_type,
       chemical_structure, inchi_key
FROM drug
WHERE COALESCE(drug_name, molecular_type, chemical_structure, inchi_key) IS NOT NULL
  AND drug_id = %s;
```

### 2b. Synonyms by drug name

```sql
SELECT s.synonymous_name AS synonym_name
FROM synonymous AS s
INNER JOIN drug AS d ON d.drug_id = s.drug_id
WHERE d.drug_name = %s;
```

### 2c. ATC code by ChEMBL ID

```sql
SELECT ATC_code_id
FROM atc_code
WHERE drug_id = %s;
```

---

## Option 3 — Disease Information

### 3a. Drugs associated with a disease

```sql
SELECT d.drug_id AS drug_id, d.drug_name AS drug_name
FROM disease_code
JOIN drug_disease AS dd ON disease_code.code_id = dd.code_id
JOIN drug AS d ON dd.drug_id = d.drug_id
WHERE disease_code.name = %s;
```

### 3b. Highest association score (global)

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

### 3c. Top-scoring drug for a given disease *(extra)*

> This query was added as an extension of 3b, allowing the user to specify a disease and retrieve the drug with the strongest association to it.

```sql
SELECT d.drug_id AS drug_id, d.drug_name AS drug_name,
       dd.inferred_score AS association_score
FROM disease_code
JOIN drug_disease AS dd ON disease_code.code_id = dd.code_id
JOIN drug AS d ON dd.drug_id = d.drug_id
WHERE disease_code.name = %s
ORDER BY dd.inferred_score DESC
LIMIT 1;
```

---

## Option 4 — Phenotypic Effects

### 4a. Indications for a drug

```sql
SELECT pe.phenotype_id, pe.phenotype_name
FROM phenotype_effect AS pe
JOIN drug_phenotype_effect AS dpe ON pe.phenotype_id = dpe.phenotype_id
JOIN drug AS d ON d.drug_id = dpe.drug_id
WHERE d.drug_id = %s
  AND dpe.phenotype_type = 'INDICATION';
```

### 4b. Side effects for a drug (ordered by score descending)

```sql
SELECT pe.phenotype_id AS phenotype_id,
       pe.phenotype_name AS phenotype_name
FROM phenotype_effect AS pe
JOIN drug_phenotype_effect AS dpe ON pe.phenotype_id = dpe.phenotype_id
JOIN drug AS d ON dpe.drug_id = d.drug_id
WHERE d.drug_id = %s
  AND dpe.phenotype_type = 'SIDE EFFECT'
ORDER BY dpe.score DESC;
```

---

## Option 5 — Molecular Targets

### 5a. First 20 targets of a given type (alphabetical)

```sql
SELECT target_name_pref
FROM target
WHERE target_type = %s
ORDER BY target_name_pref ASC
LIMIT 20;
```

### 5b. Organism with the most distinct targets

```sql
SELECT o.taxonomy_name AS organism,
       COUNT(DISTINCT t.target_id) AS target_count
FROM organism o
JOIN target t ON t.organism_id = o.taxonomy_id
GROUP BY o.taxonomy_name
ORDER BY target_count DESC
LIMIT 1;
```

---

## Option 6 — Delete Association

### Retrieve the 10 lowest-scoring associations

```sql
SELECT disease_code.name AS disease_name,
       d.drug_name AS drug_name,
       dd.inferred_score AS association_score
FROM disease_code
JOIN drug_disease AS dd ON disease_code.code_id = dd.code_id
JOIN drug AS d ON dd.drug_id = d.drug_id
WHERE dd.inferred_score IS NOT NULL
ORDER BY dd.inferred_score ASC
LIMIT 10;
```

### Delete the selected association

```sql
DELETE FROM drug_disease
WHERE code_id = (SELECT code_id FROM disease_code WHERE name = %s)
  AND drug_id = (SELECT drug_id FROM drug WHERE drug_name = %s);
```

---

## Option 7 — Insert Drug Encoding

```sql
INSERT INTO drug_has_code (drug_id, code_id, vocabulary)
SELECT drug.drug_id, %s, %s
FROM drug
WHERE drug.drug_name = %s;
```

---

## Option 8 — Modify Score

```sql
UPDATE drug_phenotype_effect
SET score = 0
WHERE score < %s
  AND phenotype_type = 'SIDE EFFECT';
```
