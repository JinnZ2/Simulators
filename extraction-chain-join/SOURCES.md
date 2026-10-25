# extraction-chain-join -- sources

Search-index depth only. Searched 2026-10-25 through the session's web
search. No primary page was opened: publisher and data hosts are outside
this environment's egress allowlist. A row marked VERIFIED means the search
index returned the bibliographic record. It does not mean the paper's text
was read.

| item named by the order | state | what the search index returned | used for |
|---|---|---|---|
| Zhang et al. ~2020, multinational subsidiary emissions ("verify citation") | VERIFIED (record) | Zhang, Guan, Wang, Meng, Zheng, Zhu, Du, "Embodied carbon emissions in the supply chains of multinational enterprises", *Nature Climate Change* 10, 1096-1101 (2020), doi 10.1038/s41558-020-0895-9. Foreign-affiliate emissions 22% of the global total in 2011, 18.7% in 2016 (press summary of the paper). The paper proposes investment-based accounting: emissions assigned to the investing country. | `ECJ_009`: G3 has country-level prior art |
| Davis & Caldeira 2010, ~23% of global CO2 embedded in traded goods | RECORD VERIFIED, FIGURE CARRIED | Davis and Caldeira, "Consumption-based accounting of CO2 emissions", *PNAS* 107, 5687-5692 (2010), doi 10.1073/pnas.0906974107. The 23% (about 6.2 Gt) appears in press coverage attributed to the authors; the search results did not show it in the paper's text. | `ECJ_017`; not used in any computation |
| China post-2024 plateau | CARRIED, CONSISTENT | Carbon Brief / CREA analysis (Myllyvirta), 12 Feb 2026: China's CO2 "flat or falling" for 21 months from March 2024; 2025 estimated -0.3%, with a ~7% fall in cement CO2 offsetting a ~0.1% rise from fossil fuels. These are production-based (territorial) estimates. | `ECJ_015`: G7 compares this kind of series with a consumption-based one |
| ICIJ, Open Ownership, OCCRP, EITI, Trase, Carbon Majors, TJN FSI, OECD TiVA, World Bank IDS, IMF COFER, OpenSecrets, IDEA, GCP | NOT SEARCHED | named by the order as custodians; nothing here reads them | the instruments take records in the shape these sources publish; no row is copied from any of them |

Sources returned by the search index:

- https://www.nature.com/articles/s41558-020-0895-9
- https://discovery.ucl.ac.uk/id/eprint/10109801/
- https://www.ucl.ac.uk/news/2020/sep/multinationals-supply-chains-account-fifth-global-emissions
- https://www.sciencedaily.com/releases/2010/03/100308151041.htm
- https://www.eco-business.com/news/when-goods-get-traded-who-pays-co2/
- https://www.carbonbrief.org/analysis-chinas-co2-emissions-have-now-been-flat-or-falling-for-21-months/
