# PDF reader — known-answer set, registered before the reader works

The answer key comes from **outside the reader**: the operator pasted the
document's text, and the reader must recover it from the PDF. Same
arrangement as `xlsreader` and `docreader`, where every known answer was
the real file's own number.

Target: `b07a5e8f-companyresearchpdfcompanyresearchpaloaltonetworkspdf.pdf`
(`Company Research - Palo Alto Networks.docx`, converted 2024-11).

## The four figures — the ones that matter

A reader that gets prose right and numbers wrong is worse than one that
refuses (`FM_032`). These must come out **whole**:

| figure | as pasted |
|---|---|
| stock price | `$374.83` |
| market cap | `$122.04 Billion` |
| revenue 2023 | `$7.52 Billion` |
| net income 2023 | `$227.7 Million` |

**None of the four appears in the inflated bytes as literal ASCII or as
UTF-16BE.** They are in the Identity-H font as glyph IDs, so recovering
them requires the `/ToUnicode` CMap. That is the test: a reader that
skips CMaps cannot pass it, and one that concatenates string literals
produces `$754` / `$32` / `$00`, which are artifacts.

## Nineteen strings

`Nikesh Arora`, `Amit Singh`, `Fortinet`, `Check Point`, `Prisma`,
`Cortex`, `Trent Weber`, `Kirk Skeeles`, `Rob Dominguez`,
`Economic Logic`, `Published Values`, `Real Values`, `Zero Trust`,
`Ransomware`, `Dallen Moody`, `374.83`, `122.04`, `7.52`, `227.7`.

The naive extractor already committed gets **6 of 19 and 0 of 4**.

## What the file contains, measured before building

| | |
|---|---|
| streams inflating with zlib | 28 of 29 |
| image XObjects | **0** — real text, no OCR needed |
| ToUnicode CMaps | 5, `beginbfchar` only, no `beginbfrange` |
| font encodings | 4 WinAnsi + 1 Identity-H |
| xref streams / object streams | 1 / 7 |

## The refusal that makes it worth building

A number is emitted only if its digits come from one contiguous show
operation, or from adjacent ones whose kerning offset is below a stated
threshold. Otherwise it emits `FRAGMENTED` and is refused. That converts
the dangerous failure — silently wrong figures — into a declared one.

A font with no `/ToUnicode` and a non-standard encoding is unrecoverable
in principle; that is refused rather than guessed at, as `read_doc` does.
An image-only PDF has no text at all and is refused outright.
