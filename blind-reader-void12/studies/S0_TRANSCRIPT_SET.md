# Specimen S0: transcript set (opened 2026-11-19, not coded)

`EMBEDDED_AUDIT_TESTS.md` T6 names "this chat (2026-11-19) and its Claude Code relays" as specimen S0, "coded like any other transcript, the designers included". This file lists the commits whose reports came through this chat. **Nothing here is coded.** No F-code, N-code or count is assigned. Coding needs coders of at least two different families (T6), and this session is the implementer, so it is not one of them.

How the list was built: `git log --all --grep='session_01BSBFWHuGrN5AdHuCDNkS29'` (this session's `Claude-Session` trailer), checked against reachability from `origin/main`. Manus commits came into this chat only when the owner pasted their reports, so they are listed apart. Whether each was relayed is marked from the owner's messages in this chat, or void.

## A. This session's commits (Claude Code, the session this chat drives), 2026-11-19, UTC

```text
commit    time   on main   subject
2676b43   16:00  NO        GPT-6 reading of packet v2, filed and scored; the round's task text filed
                           (the object exists, is on no branch, and carries this session's trailer;
                           the GPT-6 folder entered main at 8d74903; CF15 cites gpt6-v2@2676b43)
8d74903   16:21  yes       file the superseded r1 patch; README entries for this round
67b8e9d   16:31  yes       study M01 schema and criteria, fixed before any coding
3d3ac5f   16:35  yes       study M01 coding of the three filed v2 readings
ff421b1   16:38  yes       PREREG status note, amendment 1 is in force
66d4f28   16:40  yes       M01 extension and M02 design, fixed before instrument or coding
961146e   16:41  yes       M01/M02 instrument (validator, fixtures, tests)
158aa12   16:49  yes       rule_on / rule_off arms and two TAG readings (studies only)
a1129bf   16:55  yes       confusion record template and the first record
ebb9f7d   16:59  yes       the chat session's confusion record, filed as received
c567ecc   17:02  yes       glossary; Kimi's inventory proposal; draft next task text
4722e04   17:10  yes       blind study-review packet for a new reader (Grok)
7bc51bb   17:12  NO        M02 fixture rule includes on-path wrappers under D2 (KC11) (PR #320, draft, held)
3234379   17:12  yes       the Kimi reader's confusion record on the study material
0f00922   17:19  yes       Grok packet v1 defects checked; packet v2 draft; gap list
1c89ab9   17:21  yes       the Grok reader's confusion record, tagged and cross-referenced
3b963e7   17:38  yes       Grok repository read checked; map drafts, residue register, attestation block
8849444   18:01  yes       mode sequence, request headers, definitions table, boundary cases, row evidence status
68bfd96   18:12  yes       required vs default behaviour; the owner's frame for unknowns and code
a3e204f   18:17  yes       a measurand line for each OPEN rule, per layer
671a226   18:21  yes       independence rules filed and applied
5ea6328   18:22  yes       SUGGEST records on MEASURANDS (read set a3e204f)
30c7fd0   --     yes       EMBEDDED_AUDIT_TESTS.md filed verbatim (PROPOSED); index row
<this commit>    yes       this file and the AUDIT request draft
```

The trailer search finds 21 commits; 2676b43 is the 22nd, which the trailer parser missed and a body grep found. The last two rows were added by hand when this file was written.

Earlier work of this chat (the Claude-v2-A reading, the r1 patch) has no commit of this session before 8d74903. The reading was filed by Manus (`13110b9`, 2026-11-18). Whether this chat's transcript before 2026-11-19 belongs to S0 is for T6's coders: **void**.

## B. Manus commits on 2026-11-19 (reports relayed into this chat by the owner, where marked)

```text
commit    time   relayed into this chat           subject
7f9f121   00:01  yes (the owner pasted the         derive slots_specific from the sources by one rule
46576ba   00:07   Manus message on PR #317)        apply INDEPENDENCE on every route; T10 = [missing_path, error]
e54f66d   00:14                                     the owner's confirmation that the relayed acceptance lines were Claude's
d7b7687   00:17                                     decide: pre-registered criteria
50a2c54   00:28                                     decide: evidence for the rule, N1, C1, ND, K1
1c45e1e   15:36  the amendment text, yes (the       key v2 amendment 1 (text, key a1, builder, scorer rules, tests)
                 owner uploaded it); the report:
                 void
926fd50   15:36  void                              PREREG records the amendment-1 hashes
356a77a   15:38  void                              Claude-v2-A scored under key v2 and key a1
bfd2c46   15:55  void                              Kimi K3.1 reading of packet v2 (variant A), filed as received
```

## Not in the set

The owner's merges (`JinnZ2`, PR #317, #318). These are acts, not reports.
