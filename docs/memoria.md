# Memoria técnica — DisNet DrugSlayer

> Documentación completa de todas las consultas SQL del proyecto.

---

## Opción 1 — Información general

### 1a. Conteos totales

```sql
SELECT
    (SELECT COUNT(*) FROM drug) AS NumDrugs,
    (SELECT COUNT(DISTINCT disease_id) FROM disease) AS NumDiseases,
    (SELECT COUNT(*) FROM phenotype_effect) AS NumPhenoEff,
    (SELECT COUNT(DISTINCT target_id) FROM target) AS NumTargets;
```

### 1b. Primeras 10 instancias por entidad

**Fármacos:**
```sql
SELECT drug_id AS identificador, drug_name AS nombre,
       molecular_type AS tipo_molecular,
       chemical_structure AS estructura_quimica, inchi_key
FROM drug
WHERE COALESCE(drug_id, drug_name, molecular_type, chemical_structure, inchi_key) IS NOT NULL
LIMIT 10;
```

**Enfermedades:**
```sql
SELECT disease_id AS identificador, disease_name AS nombre
FROM disease
WHERE COALESCE(disease_id, disease_name) IS NOT NULL
LIMIT 10;
```

**Fenotipos:**
```sql
SELECT phenotype_id AS identificador, phenotype_name AS nombre
FROM phenotype_effect
WHERE COALESCE(phenotype_id, phenotype_name) IS NOT NULL
LIMIT 10;
```

**Dianas:**
```sql
SELECT t.target_id AS identificador, t.target_name_pref AS nombre,
       t.target_type AS tipo, o.taxonomy_name AS nombre_organismo
FROM target AS t
INNER JOIN organism AS o ON t.organism_id = o.taxonomy_id
WHERE COALESCE(t.target_id, t.target_name_pref, o.taxonomy_name) IS NOT NULL
LIMIT 10;
```

---

## Opción 2 — Información de fármacos

### 2a. Información por ID ChEMBL

```sql
SELECT drug_name AS nombre, molecular_type AS tipo_molecular,
       chemical_structure AS estructura_quimica, inchi_key
FROM drug
WHERE COALESCE(drug_name, molecular_type, chemical_structure, inchi_key) IS NOT NULL
  AND drug_id = %s;
```

### 2b. Sinónimos por nombre

```sql
SELECT s.synonymous_name AS nombre_sinonimo
FROM synonymous AS s
INNER JOIN drug AS d ON d.drug_id = s.drug_id
WHERE d.drug_name = %s;
```

### 2c. Código ATC por ID ChEMBL

```sql
SELECT ATC_code_id
FROM atc_code
WHERE drug_id = %s;
```

---

## Opción 3 — Información de enfermedades

### 3a. Fármacos asociados a una enfermedad

```sql
SELECT d.drug_id AS id_farmaco, d.drug_name AS nombre_farmaco
FROM disease_code
JOIN drug_disease AS dd ON disease_code.code_id = dd.code_id
JOIN drug AS d ON dd.drug_id = d.drug_id
WHERE disease_code.name = %s;
```

### 3b. Máximo score de asociación global

```sql
SELECT disease_code.name AS nombre_enfermedad,
       d.drug_name AS nombre_farmaco,
       dd.inferred_score AS score_asociacion
FROM disease_code
JOIN drug_disease AS dd ON disease_code.code_id = dd.code_id
JOIN drug AS d ON dd.drug_id = d.drug_id
ORDER BY dd.inferred_score DESC
LIMIT 1;
```

### 3c. Fármaco de mayor asociación para una enfermedad (consulta extra)

```sql
SELECT d.drug_id AS id_farmaco, d.drug_name AS nombre_farmaco,
       dd.inferred_score AS score_asociacion
FROM disease_code
JOIN drug_disease AS dd ON disease_code.code_id = dd.code_id
JOIN drug AS d ON dd.drug_id = d.drug_id
WHERE disease_code.name = %s
ORDER BY dd.inferred_score DESC
LIMIT 1;
```

---

## Opción 4 — Efectos fenotípicos

### 4a. Indicaciones de un fármaco

```sql
SELECT pe.phenotype_id, pe.phenotype_name
FROM phenotype_effect AS pe
JOIN drug_phenotype_effect AS dpe ON pe.phenotype_id = dpe.phenotype_id
JOIN drug AS d ON d.drug_id = dpe.drug_id
WHERE d.drug_id = %s
  AND dpe.phenotype_type = 'INDICATION';
```

### 4b. Efectos secundarios (ordenados por score)

```sql
SELECT pe.phenotype_id AS identificador_fenotipo,
       pe.phenotype_name AS nombre_fenotipo
FROM phenotype_effect AS pe
JOIN drug_phenotype_effect AS dpe ON pe.phenotype_id = dpe.phenotype_id
JOIN drug AS d ON dpe.drug_id = d.drug_id
WHERE d.drug_id = %s
  AND dpe.phenotype_type = 'SIDE EFFECT'
ORDER BY dpe.score DESC;
```

---

## Opción 5 — Dianas moleculares

### 5a. 20 primeras dianas de un tipo (orden alfabético)

```sql
SELECT target_name_pref
FROM target
WHERE target_type = %s
ORDER BY target_name_pref ASC
LIMIT 20;
```

### 5b. Organismo con más dianas distintas

```sql
SELECT o.taxonomy_name AS organismo,
       COUNT(DISTINCT t.target_id) AS numero_dianas
FROM organism o
JOIN target t ON t.organism_id = o.taxonomy_id
GROUP BY o.taxonomy_name
ORDER BY numero_dianas DESC
LIMIT 1;
```

---

## Opción 6 — Borrado de asociación

### Consulta de las 10 asociaciones con menor score

```sql
SELECT disease_code.name AS nombre_enfermedad,
       d.drug_name AS nombre_farmaco,
       dd.inferred_score AS score_asociacion
FROM disease_code
JOIN drug_disease AS dd ON disease_code.code_id = dd.code_id
JOIN drug AS d ON dd.drug_id = d.drug_id
WHERE dd.inferred_score IS NOT NULL
ORDER BY dd.inferred_score ASC
LIMIT 10;
```

### Borrado de la asociación seleccionada

```sql
DELETE FROM drug_disease
WHERE code_id = (SELECT code_id FROM disease_code WHERE name = %s)
  AND drug_id = (SELECT drug_id FROM drug WHERE drug_name = %s);
```

---

## Opción 7 — Inserción de codificación

```sql
INSERT INTO drug_has_code (drug_id, code_id, vocabulary)
SELECT drug.drug_id, %s, %s
FROM drug
WHERE drug.drug_name = %s;
```

---

## Opción 8 — Modificación de score

```sql
UPDATE drug_phenotype_effect
SET score = 0
WHERE score < %s
  AND phenotype_type = 'SIDE EFFECT';
```
