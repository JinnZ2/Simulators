# CC-3 verification pass — the F/UNVERIFIED items

Run 2026-10-04 by Claude Code. One row per item, exactly one of three states:

    VERIFIED(url, quoted locator)
    CONTRADICTED(url, what the source says)
    NOT_FOUND(queries run)

No claim was repaired to make it pass.

## Depth, stated first

Every primary page was refused by this environment's egress gate. The proxy
answered 403 to CONNECT for `www.ecfr.gov`, `eur-lex.europa.eu`,
`export.arxiv.org`, `arxiv.org`, `www.oecd.org`, `www.sunset.texas.gov`,
`www.justice.gov`, `www.federalregister.gov`, `curia.europa.eu`, `www.irs.gov`,
`www.quantgov.org`, `huggingface.co`, `www.dea.gov`, `www.govinfo.gov`,
`web.archive.org` (measured 2026-10-04T02:17Z). WebFetch returned
`EGRESS_BLOCKED` for `www.ecfr.gov`, `www.gpo.gov`, `www.law.cornell.edu`.
Only the web search index answered.

So every VERIFIED and CONTRADICTED below rests on a search-index result that
names the URL and carries the quoted text. None rests on the page itself
having been opened. A VERIFIED row here is weaker than a row the auditor
marked VERIFIED after reading the source.

## Table

| # | item (as listed in F) | state | url | locator / what it says / queries |
|---|---|---|---|---|
| 1 | CJEU "Alsen" C-137/23 | VERIFIED | https://www.e-petrol.pl/sekcja-prawna-podatki/119402/wyrok-tsue-c-137-23-alsen-warunki-formalne-nie-sa-decydujace-dla-oceny ; https://fliphtml5.com/wxszx/hzfx/The_Week_2025_064/ | "The Court of Justice's judgment of 13 March 2025 in Alsen (C-137/23) clarified that the obligation to mark fuels benefiting from favourable tax treatment should not be an additional requirement for Member States to grant a tax reduction." Existence and date only. What the report used the case for cannot be checked: the report is not in this session. |
| 2a | OR-Bench Hard-1K 39.8% illegal | NOT_FOUND | — | queries: `OR-Bench Hard-1K "illegal" category percentage Claude-2.1 rejection rate 73.7%`; `OR-Bench-Hard-1K category distribution illegal 39.8%`. The index returns that Hard-1K "contains more illegal and privacy related prompts", with no share stated. |
| 2b | OR-Bench Claude-2.1 73.7% | NOT_FOUND | — | same two queries. Adjacent, not the item: the index attributes to arXiv 2405.20947 a Claude-2.1 rejection rate of 99.8% on Hard-1K overall. Whether 73.7% is a category rate or a different set cannot be told without the report's sentence. |
| 3 | XSTest model size (report: Llama-2-7B) | CONTRADICTED | https://arxiv.org/pdf/2308.01263 ; https://aclanthology.org/2024.naacl-long.301.pdf | "The XSTest study evaluated Llama-2-70b-chat-hf with and without its original system prompt"; Llama2.0 "fully refusing 38% of prompts ... partially refusing another 21.6%". The auditor's recollection (70B chat) matches the index; the report's 7B does not. |
| 4 | RegData 1,126,959 / +175.2% | NOT_FOUND | — | queries: `RegData Code of Federal Regulations 1,126,959 restrictions increase since 1970 Mercatus`; `QuantGov RegData federal regulatory restrictions total 2024 percent increase since 1970 175.2%`; `"1,126,959" regulatory restrictions`. Adjacent: Mercatus states "about 400 thousand restrictive words" in 1970 and "over 1,080,000 total restrictions as of 2016". |
| 5 | "9 of 38 countries reach 2/4" (OECD) | NOT_FOUND | — | query: `OECD Regulatory Policy Outlook 2025 ex post evaluation primary laws countries iREG periodic review "of 38" members` (the search tool ran three follow-ups under it). The index confirms the 2021 and 2024 surveys cover the 38 members plus the EU; no "9 of 38" and no "2/4" threshold surfaced. |
| 6 | IRS publishes no aggregate dye-enforcement stats | CONTRADICTED | https://www.finance.senate.gov/download/2005/04/14/testimony-of-kevin-m-brown&download=1 ; https://www.finance.senate.gov/imo/media/doc/kbtest041405.pdf | IRS testimony to Senate Finance, 2005-04-14: "During fiscal year 2004, IRS Fuel Compliance Officers conducted more than 120,000 fuel inspections and assessed over $4.6 million in penalties for misuse of dyed diesel fuel. Seventy percent of the penalties involved the misuse of fuel by taxpayers in the construction and agriculture industries." It contradicts the claim as stated flat. It does not contradict a narrower claim that no routine published series exists; none was located. The index's two summaries of this testimony disagree on the officer count (approximately 120 against approximately 140). |
| 7 | DEA quote "no longer fits Schedule I" | VERIFIED | https://thehazeconnect.com/blogs/learn/marijuana-rescheduling-schedule-iii-hemp-impact-2026 ; https://www.marijuanamoment.net/dea-releases-full-marijuana-rescheduling-hearing-transcript-as-judge-prepares-to-issue-his-recommendation/ | "marijuana no longer fits the statutory requirements for Schedule I because it has a currently accepted medical use within the United States and it has an accepted safety for its use under medical supervision", attributed to a DEA brief in the 2026 hearing. Secondary sources only; the DEA filing itself was not opened. |

## Bearing on the INTERNAL INCONSISTENCY lines of F

These are not verification items. The row-7 search returned one date relevant
to them, recorded without interpretation:

    hearing ran June 29 to July 15, 2026; final briefs filed August 17, 2026
    (search-index summary, same sources as row 7)

## Counts

    VERIFIED 2   CONTRADICTED 2   NOT_FOUND 4   (8 rows; F listed item 2 as one line carrying two figures, split here)

`check.py` asserts every row carries exactly one of the three states.
