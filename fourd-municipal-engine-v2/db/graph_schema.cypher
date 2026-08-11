// =====================================================================
// GRAPH CONSTRAINTS & INDEXES
// =====================================================================

CREATE CONSTRAINT unique_donor_id IF NOT EXISTS FOR (d:Donor) REQUIRE d.donor_id IS UNIQUE;
CREATE CONSTRAINT unique_official_id IF NOT EXISTS FOR (o:Official) REQUIRE o.official_id IS UNIQUE;
CREATE CONSTRAINT unique_entity_id IF NOT EXISTS FOR (e:CorporateEntity) REQUIRE e.entity_id IS UNIQUE;
CREATE CONSTRAINT unique_app_id IF NOT EXISTS FOR (a:VarianceApplication) REQUIRE a.application_id IS UNIQUE;

CREATE INDEX idx_donor_name IF NOT EXISTS FOR (d:Donor) ON (d.cleaned_name);
CREATE INDEX idx_entity_name IF NOT EXISTS FOR (e:CorporateEntity) ON (e.entity_name);

// =====================================================================
// GRAPH PATH MODELING EXAMPLE
// =====================================================================

// Node Types:
// (:Donor), (:Official), (:CorporateEntity), (:Person), (:VarianceApplication), (:Parcel)

// Relationships:
// (:Donor)-[:CONTRIBUTED {amount: 5000, date: '2026-03-15'}]->(:Official)
// (:Person)-[:OFFICER_OF {role: 'Managing Member'}]->(:CorporateEntity)
// (:CorporateEntity)-[:FILED_APPLICATION]->(:VarianceApplication)
// (:VarianceApplication)-[:TARGETS_PARCEL]->(:Parcel)
// (:Official)-[:VOTED_ON {vote: 'YES', recusal: false}]->(:VarianceApplication)
// (:Donor)-[:SAME_ENTITY_AS {confidence: 0.94}]->(:Person)

// Query: Detect 2-Hop Hidden Pay-to-Play Paths
MATCH (donor:Donor)-[c:CONTRIBUTED]->(official:Official)
MATCH (donor)-[s:SAME_ENTITY_AS|OFFICER_OF*1..2]-(entity:CorporateEntity)
MATCH (entity)-[:FILED_APPLICATION]->(app:VarianceApplication)
MATCH (official)-[v:VOTED_ON]->(app)
WHERE v.vote = 'YES'
  AND v.recusal = false
  AND duration.between(c.date, v.vote_date).days <= 90
RETURN official.name AS Official,
       donor.cleaned_name AS Donor,
       entity.entity_name AS Developer_LLC,
       c.amount AS Contribution_USD,
       c.date AS Contribution_Date,
       v.vote_date AS Vote_Date,
       app.application_id AS Application_ID;
