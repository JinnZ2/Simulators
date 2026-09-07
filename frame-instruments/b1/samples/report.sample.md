# B1 runner-up trace scoring -- report

## 1. Counts and the case set present

separation rows: 45; cases: 1; models: 1; positions: 2; traces: 3
D values: [8, 16, 32, 64, 128]; L values: [2, 4, 8]

| case_id | positions | traces |
|---|---|---|
| c1 | 2 | 3 |

models: m

## 2. D sweep

| model_id | D | L | n_rows | n_positions | mean_div | resync_rate | top_decile_count | n_tied_at_cutoff | separation_count |
|---|---|---|---|---|---|---|---|---|---|
| m | 8 | 2 | 3 | 3 | 0.708333 | 0.333333 | 1 | 0 | 2 |
| m | 16 | 2 | 3 | 3 | 0.854167 | 0.333333 | 1 | 0 | 2 |
| m | 32 | 2 | 3 | 3 | 0.802083 | 0.666667 | 1 | 0 | 1 |
| m | 64 | 2 | 3 | 3 | 0.734375 | 0.666667 | 1 | 0 | 1 |
| m | 128 | 2 | 3 | 3 | 0.700521 | 0.666667 | 1 | 0 | 1 |
| m | 8 | 4 | 3 | 3 | 0.708333 | 0.0 | 1 | 0 | 3 |
| m | 16 | 4 | 3 | 3 | 0.854167 | 0.0 | 1 | 0 | 3 |
| m | 32 | 4 | 3 | 3 | 0.802083 | 0.333333 | 1 | 0 | 2 |
| m | 64 | 4 | 3 | 3 | 0.734375 | 0.333333 | 1 | 0 | 2 |
| m | 128 | 4 | 3 | 3 | 0.700521 | 0.333333 | 1 | 0 | 2 |
| m | 8 | 8 | 3 | 3 | 0.708333 | 0.0 | 1 | 0 | 3 |
| m | 16 | 8 | 3 | 3 | 0.854167 | 0.0 | 1 | 0 | 3 |
| m | 32 | 8 | 3 | 3 | 0.802083 | 0.333333 | 1 | 0 | 2 |
| m | 64 | 8 | 3 | 3 | 0.734375 | 0.333333 | 1 | 0 | 2 |
| m | 128 | 8 | 3 | 3 | 0.700521 | 0.333333 | 1 | 0 | 2 |

## 3. L sweep

| model_id | D | L | n_rows | n_positions | mean_div | resync_rate | top_decile_count | n_tied_at_cutoff | separation_count |
|---|---|---|---|---|---|---|---|---|---|
| m | 8 | 2 | 3 | 3 | 0.708333 | 0.333333 | 1 | 0 | 2 |
| m | 8 | 4 | 3 | 3 | 0.708333 | 0.0 | 1 | 0 | 3 |
| m | 8 | 8 | 3 | 3 | 0.708333 | 0.0 | 1 | 0 | 3 |
| m | 16 | 2 | 3 | 3 | 0.854167 | 0.333333 | 1 | 0 | 2 |
| m | 16 | 4 | 3 | 3 | 0.854167 | 0.0 | 1 | 0 | 3 |
| m | 16 | 8 | 3 | 3 | 0.854167 | 0.0 | 1 | 0 | 3 |
| m | 32 | 2 | 3 | 3 | 0.802083 | 0.666667 | 1 | 0 | 1 |
| m | 32 | 4 | 3 | 3 | 0.802083 | 0.333333 | 1 | 0 | 2 |
| m | 32 | 8 | 3 | 3 | 0.802083 | 0.333333 | 1 | 0 | 2 |
| m | 64 | 2 | 3 | 3 | 0.734375 | 0.666667 | 1 | 0 | 1 |
| m | 64 | 4 | 3 | 3 | 0.734375 | 0.333333 | 1 | 0 | 2 |
| m | 64 | 8 | 3 | 3 | 0.734375 | 0.333333 | 1 | 0 | 2 |
| m | 128 | 2 | 3 | 3 | 0.700521 | 0.666667 | 1 | 0 | 1 |
| m | 128 | 4 | 3 | 3 | 0.700521 | 0.333333 | 1 | 0 | 2 |
| m | 128 | 8 | 3 | 3 | 0.700521 | 0.333333 | 1 | 0 | 2 |

## 4. Stability overlaps

| model_id | position_set | sweep_axis | held | from | to | jaccard |
|---|---|---|---|---|---|---|
| m | separation_resync0 | D | {'L': 2} | 8 | 16 | 1.0 |
| m | separation_resync0 | D | {'L': 2} | 16 | 32 | 0.5 |
| m | separation_resync0 | D | {'L': 2} | 32 | 64 | 1.0 |
| m | separation_resync0 | D | {'L': 2} | 64 | 128 | 1.0 |
| m | separation_resync0 | D | {'L': 4} | 8 | 16 | 1.0 |
| m | separation_resync0 | D | {'L': 4} | 16 | 32 | 0.6667 |
| m | separation_resync0 | D | {'L': 4} | 32 | 64 | 1.0 |
| m | separation_resync0 | D | {'L': 4} | 64 | 128 | 1.0 |
| m | separation_resync0 | D | {'L': 8} | 8 | 16 | 1.0 |
| m | separation_resync0 | D | {'L': 8} | 16 | 32 | 0.6667 |
| m | separation_resync0 | D | {'L': 8} | 32 | 64 | 1.0 |
| m | separation_resync0 | D | {'L': 8} | 64 | 128 | 1.0 |
| m | separation_resync0 | L | {'D': 128} | 2 | 4 | 0.5 |
| m | separation_resync0 | L | {'D': 128} | 4 | 8 | 1.0 |
| m | separation_resync0 | L | {'D': 16} | 2 | 4 | 0.6667 |
| m | separation_resync0 | L | {'D': 16} | 4 | 8 | 1.0 |
| m | separation_resync0 | L | {'D': 32} | 2 | 4 | 0.5 |
| m | separation_resync0 | L | {'D': 32} | 4 | 8 | 1.0 |
| m | separation_resync0 | L | {'D': 64} | 2 | 4 | 0.5 |
| m | separation_resync0 | L | {'D': 64} | 4 | 8 | 1.0 |
| m | separation_resync0 | L | {'D': 8} | 2 | 4 | 0.6667 |
| m | separation_resync0 | L | {'D': 8} | 4 | 8 | 1.0 |
| m | top_decile_div | D | {'L': 2} | 8 | 16 | 1.0 |
| m | top_decile_div | D | {'L': 2} | 16 | 32 | 0.0 |
| m | top_decile_div | D | {'L': 2} | 32 | 64 | 1.0 |
| m | top_decile_div | D | {'L': 2} | 64 | 128 | 1.0 |
| m | top_decile_div | D | {'L': 4} | 8 | 16 | 1.0 |
| m | top_decile_div | D | {'L': 4} | 16 | 32 | 0.0 |
| m | top_decile_div | D | {'L': 4} | 32 | 64 | 1.0 |
| m | top_decile_div | D | {'L': 4} | 64 | 128 | 1.0 |
| m | top_decile_div | D | {'L': 8} | 8 | 16 | 1.0 |
| m | top_decile_div | D | {'L': 8} | 16 | 32 | 0.0 |
| m | top_decile_div | D | {'L': 8} | 32 | 64 | 1.0 |
| m | top_decile_div | D | {'L': 8} | 64 | 128 | 1.0 |
| m | top_decile_div | L | {'D': 128} | 2 | 4 | 1.0 |
| m | top_decile_div | L | {'D': 128} | 4 | 8 | 1.0 |
| m | top_decile_div | L | {'D': 16} | 2 | 4 | 1.0 |
| m | top_decile_div | L | {'D': 16} | 4 | 8 | 1.0 |
| m | top_decile_div | L | {'D': 32} | 2 | 4 | 1.0 |
| m | top_decile_div | L | {'D': 32} | 4 | 8 | 1.0 |
| m | top_decile_div | L | {'D': 64} | 2 | 4 | 1.0 |
| m | top_decile_div | L | {'D': 64} | 4 | 8 | 1.0 |
| m | top_decile_div | L | {'D': 8} | 2 | 4 | 1.0 |
| m | top_decile_div | L | {'D': 8} | 4 | 8 | 1.0 |

## 5. REAL vs PERMUTED, side by side

| arm | model_id | D | L | n_rows | n_positions | mean_div | resync_rate | top_decile_count | n_tied_at_cutoff | separation_count |
|---|---|---|---|---|---|---|---|---|---|---|
| REAL | m | 8 | 2 | 3 | 3 | 0.708333 | 0.333333 | 1 | 0 | 2 |
| PERMUTED | m | 8 | 2 | 3 | 3 | 0.708333 | 0.333333 | 1 | 0 | 2 |
| REAL | m | 8 | 4 | 3 | 3 | 0.708333 | 0.0 | 1 | 0 | 3 |
| PERMUTED | m | 8 | 4 | 3 | 3 | 0.708333 | 0.0 | 1 | 0 | 3 |
| REAL | m | 8 | 8 | 3 | 3 | 0.708333 | 0.0 | 1 | 0 | 3 |
| PERMUTED | m | 8 | 8 | 3 | 3 | 0.708333 | 0.0 | 1 | 0 | 3 |
| REAL | m | 16 | 2 | 3 | 3 | 0.854167 | 0.333333 | 1 | 0 | 2 |
| PERMUTED | m | 16 | 2 | 3 | 3 | 0.854167 | 0.333333 | 1 | 0 | 2 |
| REAL | m | 16 | 4 | 3 | 3 | 0.854167 | 0.0 | 1 | 0 | 3 |
| PERMUTED | m | 16 | 4 | 3 | 3 | 0.854167 | 0.0 | 1 | 0 | 3 |
| REAL | m | 16 | 8 | 3 | 3 | 0.854167 | 0.0 | 1 | 0 | 3 |
| PERMUTED | m | 16 | 8 | 3 | 3 | 0.854167 | 0.0 | 1 | 0 | 3 |
| REAL | m | 32 | 2 | 3 | 3 | 0.802083 | 0.666667 | 1 | 0 | 1 |
| PERMUTED | m | 32 | 2 | 3 | 3 | 0.802083 | 0.666667 | 1 | 0 | 1 |
| REAL | m | 32 | 4 | 3 | 3 | 0.802083 | 0.333333 | 1 | 0 | 2 |
| PERMUTED | m | 32 | 4 | 3 | 3 | 0.802083 | 0.333333 | 1 | 0 | 2 |
| REAL | m | 32 | 8 | 3 | 3 | 0.802083 | 0.333333 | 1 | 0 | 2 |
| PERMUTED | m | 32 | 8 | 3 | 3 | 0.802083 | 0.333333 | 1 | 0 | 2 |
| REAL | m | 64 | 2 | 3 | 3 | 0.734375 | 0.666667 | 1 | 0 | 1 |
| PERMUTED | m | 64 | 2 | 3 | 3 | 0.734375 | 0.666667 | 1 | 0 | 1 |
| REAL | m | 64 | 4 | 3 | 3 | 0.734375 | 0.333333 | 1 | 0 | 2 |
| PERMUTED | m | 64 | 4 | 3 | 3 | 0.734375 | 0.333333 | 1 | 0 | 2 |
| REAL | m | 64 | 8 | 3 | 3 | 0.734375 | 0.333333 | 1 | 0 | 2 |
| PERMUTED | m | 64 | 8 | 3 | 3 | 0.734375 | 0.333333 | 1 | 0 | 2 |
| REAL | m | 128 | 2 | 3 | 3 | 0.700521 | 0.666667 | 1 | 0 | 1 |
| PERMUTED | m | 128 | 2 | 3 | 3 | 0.700521 | 0.666667 | 1 | 0 | 1 |
| REAL | m | 128 | 4 | 3 | 3 | 0.700521 | 0.333333 | 1 | 0 | 2 |
| PERMUTED | m | 128 | 4 | 3 | 3 | 0.700521 | 0.333333 | 1 | 0 | 2 |
| REAL | m | 128 | 8 | 3 | 3 | 0.700521 | 0.333333 | 1 | 0 | 2 |
| PERMUTED | m | 128 | 8 | 3 | 3 | 0.700521 | 0.333333 | 1 | 0 | 2 |

| arm | model_id | position_set | sweep_axis | held | from | to | jaccard |
|---|---|---|---|---|---|---|---|
| REAL | m | separation_resync0 | D | {'L': 2} | 8 | 16 | 1.0 |
| REAL | m | separation_resync0 | D | {'L': 2} | 16 | 32 | 0.5 |
| REAL | m | separation_resync0 | D | {'L': 2} | 32 | 64 | 1.0 |
| REAL | m | separation_resync0 | D | {'L': 2} | 64 | 128 | 1.0 |
| REAL | m | separation_resync0 | D | {'L': 4} | 8 | 16 | 1.0 |
| REAL | m | separation_resync0 | D | {'L': 4} | 16 | 32 | 0.6667 |
| REAL | m | separation_resync0 | D | {'L': 4} | 32 | 64 | 1.0 |
| REAL | m | separation_resync0 | D | {'L': 4} | 64 | 128 | 1.0 |
| REAL | m | separation_resync0 | D | {'L': 8} | 8 | 16 | 1.0 |
| REAL | m | separation_resync0 | D | {'L': 8} | 16 | 32 | 0.6667 |
| REAL | m | separation_resync0 | D | {'L': 8} | 32 | 64 | 1.0 |
| REAL | m | separation_resync0 | D | {'L': 8} | 64 | 128 | 1.0 |
| REAL | m | separation_resync0 | L | {'D': 128} | 2 | 4 | 0.5 |
| REAL | m | separation_resync0 | L | {'D': 128} | 4 | 8 | 1.0 |
| REAL | m | separation_resync0 | L | {'D': 16} | 2 | 4 | 0.6667 |
| REAL | m | separation_resync0 | L | {'D': 16} | 4 | 8 | 1.0 |
| REAL | m | separation_resync0 | L | {'D': 32} | 2 | 4 | 0.5 |
| REAL | m | separation_resync0 | L | {'D': 32} | 4 | 8 | 1.0 |
| REAL | m | separation_resync0 | L | {'D': 64} | 2 | 4 | 0.5 |
| REAL | m | separation_resync0 | L | {'D': 64} | 4 | 8 | 1.0 |
| REAL | m | separation_resync0 | L | {'D': 8} | 2 | 4 | 0.6667 |
| REAL | m | separation_resync0 | L | {'D': 8} | 4 | 8 | 1.0 |
| REAL | m | top_decile_div | D | {'L': 2} | 8 | 16 | 1.0 |
| REAL | m | top_decile_div | D | {'L': 2} | 16 | 32 | 0.0 |
| REAL | m | top_decile_div | D | {'L': 2} | 32 | 64 | 1.0 |
| REAL | m | top_decile_div | D | {'L': 2} | 64 | 128 | 1.0 |
| REAL | m | top_decile_div | D | {'L': 4} | 8 | 16 | 1.0 |
| REAL | m | top_decile_div | D | {'L': 4} | 16 | 32 | 0.0 |
| REAL | m | top_decile_div | D | {'L': 4} | 32 | 64 | 1.0 |
| REAL | m | top_decile_div | D | {'L': 4} | 64 | 128 | 1.0 |
| REAL | m | top_decile_div | D | {'L': 8} | 8 | 16 | 1.0 |
| REAL | m | top_decile_div | D | {'L': 8} | 16 | 32 | 0.0 |
| REAL | m | top_decile_div | D | {'L': 8} | 32 | 64 | 1.0 |
| REAL | m | top_decile_div | D | {'L': 8} | 64 | 128 | 1.0 |
| REAL | m | top_decile_div | L | {'D': 128} | 2 | 4 | 1.0 |
| REAL | m | top_decile_div | L | {'D': 128} | 4 | 8 | 1.0 |
| REAL | m | top_decile_div | L | {'D': 16} | 2 | 4 | 1.0 |
| REAL | m | top_decile_div | L | {'D': 16} | 4 | 8 | 1.0 |
| REAL | m | top_decile_div | L | {'D': 32} | 2 | 4 | 1.0 |
| REAL | m | top_decile_div | L | {'D': 32} | 4 | 8 | 1.0 |
| REAL | m | top_decile_div | L | {'D': 64} | 2 | 4 | 1.0 |
| REAL | m | top_decile_div | L | {'D': 64} | 4 | 8 | 1.0 |
| REAL | m | top_decile_div | L | {'D': 8} | 2 | 4 | 1.0 |
| REAL | m | top_decile_div | L | {'D': 8} | 4 | 8 | 1.0 |

| arm | model_id | position_set | sweep_axis | held | from | to | jaccard |
|---|---|---|---|---|---|---|---|
| PERMUTED | m | separation_resync0 | D | {'L': 2} | 8 | 16 | 0.3333 |
| PERMUTED | m | separation_resync0 | D | {'L': 2} | 16 | 32 | 0.5 |
| PERMUTED | m | separation_resync0 | D | {'L': 2} | 32 | 64 | 1.0 |
| PERMUTED | m | separation_resync0 | D | {'L': 2} | 64 | 128 | 1.0 |
| PERMUTED | m | separation_resync0 | D | {'L': 4} | 8 | 16 | 1.0 |
| PERMUTED | m | separation_resync0 | D | {'L': 4} | 16 | 32 | 0.6667 |
| PERMUTED | m | separation_resync0 | D | {'L': 4} | 32 | 64 | 0.3333 |
| PERMUTED | m | separation_resync0 | D | {'L': 4} | 64 | 128 | 0.3333 |
| PERMUTED | m | separation_resync0 | D | {'L': 8} | 8 | 16 | 1.0 |
| PERMUTED | m | separation_resync0 | D | {'L': 8} | 16 | 32 | 0.6667 |
| PERMUTED | m | separation_resync0 | D | {'L': 8} | 32 | 64 | 0.3333 |
| PERMUTED | m | separation_resync0 | D | {'L': 8} | 64 | 128 | 0.3333 |
| PERMUTED | m | separation_resync0 | L | {'D': 128} | 2 | 4 | 0.5 |
| PERMUTED | m | separation_resync0 | L | {'D': 128} | 4 | 8 | 0.3333 |
| PERMUTED | m | separation_resync0 | L | {'D': 16} | 2 | 4 | 0.6667 |
| PERMUTED | m | separation_resync0 | L | {'D': 16} | 4 | 8 | 1.0 |
| PERMUTED | m | separation_resync0 | L | {'D': 32} | 2 | 4 | 0.5 |
| PERMUTED | m | separation_resync0 | L | {'D': 32} | 4 | 8 | 0.3333 |
| PERMUTED | m | separation_resync0 | L | {'D': 64} | 2 | 4 | 0.5 |
| PERMUTED | m | separation_resync0 | L | {'D': 64} | 4 | 8 | 0.3333 |
| PERMUTED | m | separation_resync0 | L | {'D': 8} | 2 | 4 | 0.6667 |
| PERMUTED | m | separation_resync0 | L | {'D': 8} | 4 | 8 | 1.0 |
| PERMUTED | m | top_decile_div | D | {'L': 2} | 8 | 16 | 0.0 |
| PERMUTED | m | top_decile_div | D | {'L': 2} | 16 | 32 | 0.0 |
| PERMUTED | m | top_decile_div | D | {'L': 2} | 32 | 64 | 0.0 |
| PERMUTED | m | top_decile_div | D | {'L': 2} | 64 | 128 | 1.0 |
| PERMUTED | m | top_decile_div | D | {'L': 4} | 8 | 16 | 1.0 |
| PERMUTED | m | top_decile_div | D | {'L': 4} | 16 | 32 | 0.0 |
| PERMUTED | m | top_decile_div | D | {'L': 4} | 32 | 64 | 0.0 |
| PERMUTED | m | top_decile_div | D | {'L': 4} | 64 | 128 | 0.0 |
| PERMUTED | m | top_decile_div | D | {'L': 8} | 8 | 16 | 0.0 |
| PERMUTED | m | top_decile_div | D | {'L': 8} | 16 | 32 | 0.0 |
| PERMUTED | m | top_decile_div | D | {'L': 8} | 32 | 64 | 0.0 |
| PERMUTED | m | top_decile_div | D | {'L': 8} | 64 | 128 | 0.0 |
| PERMUTED | m | top_decile_div | L | {'D': 128} | 2 | 4 | 1.0 |
| PERMUTED | m | top_decile_div | L | {'D': 128} | 4 | 8 | 1.0 |
| PERMUTED | m | top_decile_div | L | {'D': 16} | 2 | 4 | 0.0 |
| PERMUTED | m | top_decile_div | L | {'D': 16} | 4 | 8 | 1.0 |
| PERMUTED | m | top_decile_div | L | {'D': 32} | 2 | 4 | 0.0 |
| PERMUTED | m | top_decile_div | L | {'D': 32} | 4 | 8 | 0.0 |
| PERMUTED | m | top_decile_div | L | {'D': 64} | 2 | 4 | 0.0 |
| PERMUTED | m | top_decile_div | L | {'D': 64} | 4 | 8 | 0.0 |
| PERMUTED | m | top_decile_div | L | {'D': 8} | 2 | 4 | 0.0 |
| PERMUTED | m | top_decile_div | L | {'D': 8} | 4 | 8 | 0.0 |

## 6. NULLS TRIGGERED (N1-N5)

Per workorders/runner_up_trace.md section 7. Thresholds are arguments: n1_resync=0.9, n2_separate=0.95, n3_jaccard=0.5, n5_discordance=0.1, sustained_d=64

### N1 -- not triggered

number: `{"min_resync_over_D_per_L": {"2": 0.333333, "4": 0.0, "8": 0.0}}`
threshold: `0.9`

triggered when the minimum resync rate over D is >= threshold at every L

### N2 -- not triggered

number: `{"separation_rate_at_D>=64_per_L": {"2": 0.3333, "4": 0.6667, "8": 0.6667}}`
threshold: `0.95`

separates = resync 0 at every D >= 64; triggered when the rate is >= threshold at every L

### N3 -- TRIGGERED

number: `{"N": "not carried", "min_adjacent_D_jaccard_separation_resync0": 0.5, "min_adjacent_D_jaccard_top_decile_div": 0.0, "min_adjacent_L_jaccard_separation_resync0": 0.5, "min_adjacent_L_jaccard_top_decile_div": 1.0}`
threshold: `0.5`

triggered when any adjacent-D or adjacent-L Jaccard, on the top-decile set or the separation set, is < threshold; the top-decile set is L-invariant by construction so its L row reads 1.0 and only the separation set carries L dependence; the N sweep (stage B) is not in separations.jsonl and is compared across runs at different N

### N4 -- not triggered

number: `{"mean_adjacent_D_jaccard_permuted": 0.1667, "mean_adjacent_D_jaccard_real": 0.75, "transfer_function_permuted": [{"from": 8, "held": {"L": 2}, "jaccard": 0.0, "model_id": "m", "to": 16}, {"from": 16, "held": {"L": 2}, "jaccard": 0.0, "model_id": "m", "to": 32}, {"from": 32, "held": {"L": 2}, "jaccard": 0.0, "model_id": "m", "to": 64}, {"from": 64, "held": {"L": 2}, "jaccard": 1.0, "model_id": "m", "to": 128}, {"from": 8, "held": {"L": 4}, "jaccard": 1.0, "model_id": "m", "to": 16}, {"from": 16, "held": {"L": 4}, "jaccard": 0.0, "model_id": "m", "to": 32}, {"from": 32, "held": {"L": 4}, "jaccard": 0.0, "model_id": "m", "to": 64}, {"from": 64, "held": {"L": 4}, "jaccard": 0.0, "model_id": "m", "to": 128}, {"from": 8, "held": {"L": 8}, "jaccard": 0.0, "model_id": "m", "to": 16}, {"from": 16, "held": {"L": 8}, "jaccard": 0.0, "model_id": "m", "to": 32}, {"from": 32, "held": {"L": 8}, "jaccard": 0.0, "model_id": "m", "to": 64}, {"from": 64, "held": {"L": 8}, "jaccard": 0.0, "model_id": "m", "to": 128}]}`
threshold: `permuted >= real`

the permuted stability values are the method's transfer function and are printed either way; this compares ONE permutation draw to the real value, so the margin is one seed wide

### N5 -- NOT EVALUABLE

number: `{"entropy_bases_present": ["topk"], "positions_with_both": 0}`
threshold: `0.1`

requires >= 2 positions carrying entropy under both bases; not evaluable

permute seed(s) carried in the permuted summary: none (the seed is in the permute run record)
