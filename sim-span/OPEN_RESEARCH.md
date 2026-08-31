---

## CLAIM_TABLE.md / 声明表

| English | 中文 |
|---|---|
| Claims about the delivered sim-span/ folder, about what a Python stdlib environment can establish concerning it, and about the self-audit protocol it inherits. | 关于交付的 sim-span/ 文件夹的声明，关于一个 Python 标准库环境能对其建立什么，以及关于它所继承的自我审计协议的声明。 |
| This is a runnable test, not a measurement. The folder runs a synthetic simulation to test whether a reporting rule can manufacture a U‑shape from data where the true relationship is not U‑shaped. The answer is yes—but only on the leg that the specification's falsifier is written to exclude. | 这是一个可运行的测试，不是一个测量结果。 该文件夹运行一个合成模拟，以测试一种报告规则是否能从不存在 U 型关系的真实数据中制造出 U 型关系。结果是肯定的——但仅限于规范的可证伪条件恰好排除掉的那条腿上。 |

---

## REFUTATION_PROTOCOL / 反驳协议

Every claim names what would refute it. A failed check updates the claim, never the delivered design. / 每个声明都说明了什么会反驳它。检查失败则更新声明，而不是修改设计。

| id | English Claim | 中文声明 | Status / 状态 |
|---|---|---|---|
| `SPAN_001` | If true sleep–outcome is flat or monotonic, reported hours mixes two independent variables: true sleep + fragmentation × wake cost. Binning by reported hours averages two different populations (long sleepers and short–fragmented sleepers) together at the ends of the axis. The mechanism holds. | 如果真实睡眠与结果之间是平坦或单调的关系，那么报告时间会混合两个独立的变量：真实睡眠 + 碎片化 × 醒来成本。按报告时间分箱，会将两个不同的人群（长睡眠者和短碎片化睡眠者）在轴的两端平均在一起。机制是成立的。 | SUPPORTED / 已支持 |
| `SPAN_002` | The answer is yes—the reporting rule can manufacture a U‑shape. On the frag_driven leg, 63 of 360 parameter combinations produce a U‑shape, and 52 of those have their vertex inside the published 6–9 h window. The control arm (true sleep) stays flat. | 答案是肯定的——报告规则可以制造 U 型曲线。 在 frag_driven 腿上，360 个参数组合中有 63 个产生了 U 型曲线，其中 52 个的顶点位于 6-9 小时的已发表窗口内。控制轴（真实睡眠）保持平坦。 | SUPPORTED / 已支持 |
| `SPAN_003` | But the answer depends on which leg you run. Three legs give three different answers: flat: 4 U‑shapes out of 360 (noise); mono: 124 U‑shapes, but none with vertex inside 6–9 h (lowest vertex 10.16 h); frag_driven: 63 U‑shapes, 52 inside the published window (lowest vertex 5.23 h). | 但答案取决于你运行哪条腿。 三条腿给出三个不同的答案：flat：360 个组合中只有 4 个产生 U 型（且为噪声）；mono：124 个产生 U 型，但没有一个顶点位于 6-9 小时内（最低顶点为 10.16 小时）；frag_driven：63 个产生 U 型，52 个位于已发表窗口内（最低顶点为 5.23 小时）。 | SUPPORTED / 已支持 |
| `SPAN_004` | The specification's falsifier is scoped to the one leg that cannot answer the question. The null is stated as "flat or monotonic". The falsifier is stated as "flat null". These are two different sets, and the three legs disagree, so which one you run determines the conclusion. This is load‑bearing because a scoped falsifier licenses discarding the entire counterargument, and the leg that carries the counterargument is the one the specification itself asks for. | 规范的可证伪条件被限定在唯一无法回答问题的腿上。 零假设表述为“平坦或单调”。可证伪条件表述为“平坦零假设”。这是两个不同的集合，而三条腿的意见不一致，因此运行哪一条决定了结论。这是负载的，因为通过限定范围的可证伪条件会许可丢弃整个反对意见，而承载该反对意见的腿正是规范本身所要求的。 | SUPPORTED / 已支持 |
| `SPAN_005` | Under the specification's default fragmentation parameters, the mono leg does not trigger at all. Curvature is present and in the right direction (a = +0.055), but the vertex is at 14.75 hours, beyond the 4.0–11.5 reported range. The mechanism is active but not yet visible. | 在规范的默认碎片化参数下，mono 腿根本不会触发。 曲率存在且方向正确（a = +0.055），但顶点位于 14.75 小时，超出了 4.0-11.5 的报告范围。机制是活跃的，但尚未显现。 | SUPPORTED / 已支持 |
| `SPAN_006` | three_column.py tests show that the stated regression form is misspecified. gap = frag × wake_cost is a product, but gap ~ count + duration is additive, so it is the wrong form. The product fit is the correct one. three_column.py | 测试表明，规定的回归形式是错误的。 gap = frag × wake_cost 是乘积关系，但 gap ~ count + duration 是加性关系，因此是错误设定。应使用乘积拟合。 | SUPPORTED / 已支持 |
| `SPAN_007` | Under the mixture model, the regression slope is an estimator of the mixing proportion p. E[gap | product] = p × product exactly. So the slope estimates the fraction of the population that reports span rather than true sleep. | 在混合模型下，回归斜率是混合比例 p 的估计量。 E[gap | product] = p × product 精确成立。因此斜率估计的是报告 span 而非真实睡眠的人群比例。 | SUPPORTED / 已支持 |
| `SPAN_008` | The "single night" flag is load‑bearing for estimation. Self‑report asks about "usual"; a single night is one draw. Regressing on single‑night fragmentation produces errors‑in‑variables in the predictor, attenuating the estimate. “ | 一夜”标志对估计是负载的。 自我报告的是“通常”情况；单一夜晚是一次抽取。用单夜的碎片化进行回归，会在预测变量中产生变量误差，从而衰减估计。 | SUPPORTED / 已支持 |
| `SPAN_009` | The folder produces no real‑world measurements. All numbers are synthetic; no values from sleep studies are used. | 该文件夹不产生任何真实世界的测量结果。 所有数字都是合成的；没有来自睡眠研究的数值。 | SUPPORTED / 已支持 |
| `SPAN_010` | The delivered code is stdlib‑only. sim_span.py and three_column.py import only from the Python standard library. | 交付的代码是标准库（stdlib‑only）的。 sim_span.py 和 three_column.py 仅导入 Python 标准库。 | SUPPORTED / 已支持 |
| `SPAN_011` | The delivered code is runnable. python3 sim_span.py runs all three legs; python3 sim_span.py --selftest passes all checks. | 交付的代码是可运行的。 python3 sim_span.py 运行全部三条腿；python3 sim_span.py --selftest 通过所有检查。 | SUPPORTED / 已支持 |
| `SPAN_012` | The U‑shape detector initially misclassified monotonic rising curves as U‑shaped. The first version counted curves with positive quadratic and vertex near the left edge as U‑shaped. Fix: both arms must rise by MARGIN times the scatter of the bin means around the fit—a reasoning‑gate G‑RES pair, feature against the instrument's own noise, with margin named. U | 型检测器最初将单调上升的曲线误判为 U 型。 第一个版本将正二次项且顶点位于左边缘附近的曲线计为 U 型。修复方案是：两侧臂必须上升 MARGIN 倍于箱均值围绕拟合的残差散度——一个推理门 G‑RES 对，特征相对于仪器自身噪声，且裕度已命名。 | REPAIRED / 已修复 |
| `SPAN_013` | Vertex position is reported but never used for scoring. The specification asks for the vertex position, but the falsifier does not route through it. This is an intentional design choice: a U‑shape in the wrong place does not explain one in the right place. | 顶点位置被报告，但从未用于评分。 规范要求报告顶点位置，但可证伪条件不通过它路由。这是一个有意的设计选择：一个在错误位置的 U 型不能解释一个在正确位置的 U 型。 | SUPPORTED / 已支持 |
| `SPAN_014` | Five open questions are recorded, not resolved: (1) specification null is "flat or monotonic" but falsifier is scoped to flat; (2) fragmentation‑true‑sleep independence may not hold for real sleepers; (3) rounding rules are fictional; (4) outcome model is not a biological aging clock; (5) this tests whether the mechanism can produce the shape, not whether it does. | 五个开放问题被记录，但未解决：（1）规范的零假设是“平坦或单调”，但可证伪条件限定为平坦；（2）碎片化与真实睡眠的独立性可能对真实睡眠者不成立；（3）舍入规则是虚构的；（4）结果模型不是生物老化时钟；（5）这测试的是机制能否产生该形状，而非它是否产生了。 | OPEN / 开放 |

---

## UNDERGRADUATE_RESEARCH_GAPS.md / 本科生研究空白

| English | 中文 |
|---|---|
| Open questions in the sim‑span framework, organized by discipline sim‑span | 框架中的开放性问题，按学科组织 |

---

1. Empirical — Three‑Column Test on Real Data / 经验性 — 真实世界数据中的三列测试

| English | 中文 |
|---|---|
| Gap: NOTES_INSTRUMENT.md proposes: subtract measured sleep from reported hours, regress against awakenings count and duration. If the gap grows with fragmentation, G‑SPAN is confirmed in a real population. | 空白： NOTES_INSTRUMENT.md 提出：将报告小时数减去实测睡眠量，对觉醒次数和觉醒持续时间进行回归。如果差距随碎片化而增长，则 G‑SPAN 在真实人群中被证实。 |
| Knowledge state: NOT_STUDIED | 知识状态： NOT_STUDIED |
| Research question: In real‑world sleep data, does the gap between reported and measured sleep grow with fragmentation? What is the correct regression form (product vs additive)? | 研究问题： 在真实世界的睡眠数据中，报告睡眠与实测睡眠之间的差距是否随碎片化而增长？正确的回归形式（乘积 vs 加性）是什么？ |
| Disciplines: Sleep science, biostatistics, epidemiology | 学科： 睡眠科学、生物统计学、流行病学 |
| Data sources: Actigraphy data, PSG data, self‑report questionnaires | 数据来源： 体动记录仪数据、多导睡眠图数据、自我报告问卷 |
| Method: Obtain datasets with both objective and self‑reported sleep, compute the gap, regress on fragmentation measures, test the slope, estimate p. | 方法： 获取同时包含客观和自我报告睡眠的数据集，计算差距，对碎片化指标进行回归，测试斜率，估计 p。 |
| Expected deliverable: A real‑world three‑column test report with regression results and p estimate. | 预期成果： 一份真实世界三列测试的报告，包含回归结果和 p 的估计值。 |
| Falsifier: The gap does not grow with fragmentation. | 证伪条件： 差距不随碎片化而增长。 |

---

2. Empirical — Night‑to‑Night Variability Impact / 经验性 — 逐夜变异性的影响

| English | 中文 |
|---|---|
| Gap: NOTES_INSTRUMENT.md notes that 7‑night actigraphy per person allows checking night‑to‑night variability, which single‑night reports discard. | 空白： NOTES_INSTRUMENT.md 指出，每人 7 天的体动记录仪数据允许检查逐夜变异性，而单夜报告会丢弃这些信息。 |
| Knowledge state: NOT_STUDIED | 知识状态： NOT_STUDIED |
| Research question: How does night‑to‑night variability affect estimation of p? How much attenuation occurs when using a single night vs averaging across multiple nights? | 研究问题： 逐夜变异性如何影响 p 的估计？使用单夜与多夜平均相比，估计值有多少衰减？ |
| Disciplines: Sleep science, biostatistics, epidemiology | 学科： 睡眠科学、生物统计学、流行病学 |
| Data sources: Multi‑night actigraphy datasets, the three_column.py simulation framework | 数据来源： 多夜体动记录仪数据集，three_column.py 模拟框架 |
| Method: Extend three_column.py to simulate multi‑night data, compare single‑night vs multi‑night estimates, measure attenuation, find minimum nights needed. | 方法： 扩展 three_column.py 以模拟多夜数据，比较单夜与多夜估计，测量衰减量，计算恢复真实 p 所需的最少夜晚数。 |
| Expected deliverable: An analysis of night‑to‑night variability effects on p estimation, with sample‑size recommendations. | 预期成果： 一份逐夜变异性对 p 估计影响的分析，包含样本量建议。 |
| Falsifier: Single‑night and multi‑night estimates are identical. | 证伪条件： 单夜估计与多夜估计无差异。 |

---

3. Methodological — Fragmentation‑True‑Sleep Independence / 方法论 — 碎片化与真实睡眠的独立性

| English | 中文 |
|---|---|
| Gap: MARKER.md notes: "Independence of fragmentation from true sleep is assumed and may not hold for real sleepers." | 空白： MARKER.md 指出：“碎片化与真实睡眠的独立性是假设的，且对真实睡眠者可能不成立。” |
| Knowledge state: UNKNOWN_ATM | 知识状态： UNKNOWN_ATM |
| Research question: In real populations, are fragmentation and true sleep independent or correlated? If correlated, how does the simulation's conclusion change? | 研究问题： 在真实人群中，碎片化与真实睡眠是独立的还是相关的？如果相关，模拟的结论会如何改变？ |
| Disciplines: Sleep science, biostatistics, epidemiology | 学科： 睡眠科学、生物统计学、流行病学 |
| Data sources: Actigraphy datasets, PSG datasets, published fragmentation studies | 数据来源： 体动记录仪数据集、多导睡眠图数据集、已发表的碎片化研究 |
| Method: Measure the correlation in real data, incorporate it into the simulation, re‑run, compare results. | 方法： 在真实数据中测量相关性，将其纳入模拟，重新运行，比较结果。 |
| Expected deliverable: A report on fragmentation‑true‑sleep correlation and updated simulation results. | 预期成果： 一份关于碎片化-真实睡眠相关性的报告，以及更新后的模拟结果。 |
| Falsifier: Fragmentation and true sleep are highly correlated in real data. | 证伪条件： 碎片化与真实睡眠在真实数据中高度相关。 |

---

4. Methodological — Vertex Position Interpretation / 方法论 — 顶点位置的解释

| English | 中文 |
|---|---|
| Gap: The simulation shows mono leg vertex at 10.16 h, frag_driven leg vertex at 5.23 h. Different vertex positions have different interpretations across legs. | 空白： 模拟显示 mono 腿的顶点位于 10.16 小时，frag_driven 腿的顶点位于 5.23 小时。不同腿的顶点位置有不同的解释。 |
| Knowledge state: UNDEFINED | 知识状态： UNDEFINED |
| Research question: What does the vertex position of a U‑shape tell us? Are vertex positions distinguishable across mechanisms? | 研究问题： U 型曲线的顶点位置告诉我们什么？不同机制产生的顶点位置是否具有可区分的特征？ |
| Disciplines: Statistics, metascience, research methodology | 学科： 统计学、元科学、研究方法论 |
| Data sources: Simulation output (RESULTS.md), published sleep‑mortality U‑shape studies, curve‑fitting literature | 数据来源： 模拟输出（RESULTS.md），已发表的 U 型睡眠-死亡率研究，曲线拟合文献 |
| Method: Analyse vertex distributions per leg, test whether vertex position discriminates mechanisms, compare to published vertex positions. | 方法： 分析不同腿的顶点位置分布，测试顶点位置是否可作为区分机制的诊断指标，与已发表的顶点分布进行比较。 |
| Expected deliverable: An analysis of vertex position as a diagnostic for mechanism. | 预期成果： 一份关于 U 型顶点位置作为机制诊断指标的分析。 |
| Falsifier: All mechanisms produce the same vertex distribution. | 证伪条件： 所有机制产生相同的顶点位置分布。 |

---

5. Methodological — Falsifier Scope / 方法论 — 可证伪条件的范围

| English | 中文 |
|---|---|
| Gap: The specification's falsifier is scoped to the flat null, but the null is "flat or monotonic". This is load‑bearing. | 空白： 规范的可证伪条件被限定在平坦零假设上，但零假设是“平坦或单调”。这是负载的。 |
| Knowledge state: UNDEFINED | 知识状态： UNDEFINED |
| Research question: What is the correct falsifier? Should it cover both flat and monotonic nulls? | 研究问题： 正确的可证伪条件应该是什么？它应该覆盖平坦零假设和单调零假设两者吗？ |
| Disciplines: Philosophy of science, metascience, research methodology | 学科： 科学哲学、元科学、研究方法论 |
| Data sources: MARKER.md, RESULTS.md, philosophical literature on falsifiability, sleep‑mortality literature | 数据来源： MARKER.md、RESULTS.md、关于可证伪性的哲学文献、睡眠-死亡率文献 |
| Method: Analyse the difference between "flat or monotonic" and "flat", test both nulls, propose a revised falsifier covering both. | 方法： 分析“平坦或单调”与“平坦”之间的差异，测试两种零假设，提出一个覆盖两种零假设的可证伪条件。 |
| Expected deliverable: A revised falsifier proposal with re‑analysis of the simulation. | 预期成果： 一份关于正确可证伪条件的提案，包含对模拟的重新分析。 |
| Falsifier: The conclusion is the same under both nulls. | 证伪条件： 在两种零假设下结论相同。 |

---

6. User Guide — Non‑Specialist Translation / 用户指南 — 非专业人士翻译

| English | 中文 |
|---|---|
| Gap: The framework is documented for researchers but not for non‑specialists (clinicians, policymakers, general public). | 空白： 该框架是为研究人员记录的，而非为非专业人士（临床医生、政策制定者、普通公众）记录的。 |
| Knowledge state: NOT_STUDIED | 知识状态： NOT_STUDIED |
| Research question: How can the sim‑span framework's insights be communicated to non‑specialists to change how they think about self‑report data, measurement error, and published U‑shapes? | 研究问题： 如何将 sim‑span 框架的见解传达给非专业人士，以改变他们对自我报告数据、测量误差和已发表 U 型曲线的思考方式？ |
| Disciplines: Science communication, public health, medical education | 学科： 科学传播、公共卫生、医学教育 |
| Data sources: The framework itself, published science communication research, clinical guidelines | 数据来源： 该框架本身、已发表的科学传播研究、临床指南 |
| Method: Translate each concept into plain language, develop case studies, create a user guide, test with non‑specialist audiences, iterate. | 方法： 将每个概念翻译成平实的语言，开发案例研究，创建用户指南，在非专业受众中测试，进行迭代。 |
| Expected deliverable: A non‑technical user guide to the sim‑span framework. | 预期成果： 一份关于 sim‑span 框架的非技术性用户指南。 |
| Falsifier: Non‑specialists find the guide unhelpful or incomprehensible. | 证伪条件： 非专业人士认为该指南无益或难以理解。 |

---

## SCOPE_BOUNDARY.md / 范围边界

| English | 中文 |
|---|---|
| Why this framework is broader than standard measurement‑error practice | 为什么这个框架比标准的测量误差实践更广泛 |

---

### The Problem / 问题

| English | 中文 |
|---|---|
| In measurement error and epidemiology, things like reporting bias, fragmentation mixing, regression‑form choice, and falsifier scope are not separate from the conclusion. They are direct, material, contributing factors to whether the conclusion holds. When a study says "sleep duration has a U‑shaped relationship with mortality," that is treated as a finding about biology. | 在测量误差和流行病学中，像是报告偏差、碎片化混合、回归形式的选择以及可证伪条件的范围这类事情，并非与结论无关。它们是直接的、物质性的、有贡献的因素，决定着结论是否成立。当一项研究说“睡眠时长与死亡率之间存在 U 型关系”时，它就被当作一个关于生物学的发现。 |

But reported hours may mix two independent variables: true sleep plus fragmentation waking time. The U‑shape in reported hours may be produced by a reporting rule, not by true sleep. The framework shows that on the correct leg (frag_driven), the U‑shape does appear—but the specification's falsifier is scoped to the one leg that cannot answer the question. | 但报告时长可能混合了两个独立的变量：真实睡眠加上碎片化导致的清醒时间。报告时长中的 U 型可能是由报告规则产生的，而非由真实睡眠产生的。该框架显示，在正确的腿（frag_driven）下，U 型确实会出现——但规范的可证伪条件恰好限定在了无法产生答案的那条腿上。

---

### Six Ways the Connection Gets Lost / 六种连接丢失的方式

#### 1. The "Reporting as Measurement" Fallacy / “报告作为测量”谬误

| English | 中文 |
|---|---|
| Many studies treat self‑report as a measurement of true sleep. If the study says "sleep duration is associated with mortality," that is treated as a biological finding. | 许多研究将自我报告视为真实睡眠的测量。如果研究说“睡眠时长与死亡率相关”，它就被当作一个生物学发现。 |

But reported hours are span = true_sleep + frag × wake_cost. It is a mixture. If the study says "sleep duration is associated," it is not wrong for true sleep, but it may be wrong for reported hours. The mixture was causal—just not represented. | 但报告时长是 span = true_sleep + frag × wake_cost。它是一个混合物。如果研究说“睡眠时长相关”，对于真实睡眠并非错误，但对于报告时长可能是错误的。混合物是因果性的——只是没有被表述。

#### 2. The "U‑Shape as Biological" Fallacy / “U 型作为生物学”谬误

| English | 中文 |
|---|---|
| Many studies treat the U‑shape as a biological phenomenon. If the study says "the U‑shape exists," that is treated as a discovery. | 许多研究将 U 型视为生物学现象。如果研究说“U 型存在”，它就被当作一个发现。 |

But a reporting rule can manufacture a U‑shape from a true relationship that is not U‑shaped. The frag_driven leg shows: if outcome is truly driven by fragmentation, and the reported quantity is time in bed, then the U‑shape in duration emerges. If the study says "the U‑shape is biological," it is not wrong for the curve, but it may be wrong for the interpretation. The reporting rule was causal—just not represented. | 但报告规则可以从一个不存在 U 型的真实关系中制造出 U 型。frag_driven 腿显示：如果结果真正由碎片化驱动，而报告的量是卧床时间，那么 U 型时长曲线就会出现。如果研究说“U 型是生物学”，它并非对于曲线错误，但对于解释可能是错误的。报告规则是因果性的——只是没有被表述。

#### 3. The "Null as Single" Fallacy / “零假设作为单一”谬误

| English | 中文 |
|---|---|
| Many studies treat the null as single. If the study says "the null is rejected," that is treated as a finding. | 许多研究将零假设视为单一的。如果研究说“零假设被拒绝”，它就被当作一个发现。 |

But the null is "flat or monotonic". The falsifier is scoped to "flat". These are two different sets. If the study says "the null is rejected," it is not wrong for the flat null, but it may be wrong for the monotonic null. The scope was causal—just not represented. | 但零假设是“平坦或单调”。可证伪条件被限定在“平坦”上。这是两个不同的集合。如果研究说“零假设被拒绝”，它并非对于平坦零假设错误，但对于单调零假设可能是错误的。范围是因果性的——只是没有被表述。

#### 4. The "Regression Form as Given" Fallacy / “回归形式作为给定”谬误

| English | 中文 |
|---|---|
| Many studies treat the regression form as given. If the study says "the gap grows with fragmentation," that is treated as a finding. | 许多研究将回归形式视为给定的。如果研究说“差距随碎片化增长”，它就被当作一个发现。 |

But gap = frag × wake_cost is a product. gap ~ count + duration is additive, so it is misspecified. If the study says "the gap grows," it is not wrong for the association, but it may be wrong for the interpretation. The regression form was causal—just not represented. | 但 gap = frag × wake_cost 是乘积关系。gap ~ count + duration 是加性关系，因此是错误设定。如果研究说“差距增长”，它并非对于相关性错误，但对于解释可能是错误的。回归形式是因果性的——只是没有被表述。

#### 5. The "Single Night as Usual" Fallacy / “一夜作为通常”谬误

| English | 中文 |
|---|---|
| Many studies treat a single night's measurement as representative of usual. If the study says "fragmentation is X," that is treated as a finding. | 许多研究将一夜的测量视为通常情况的代表。如果研究说“碎片化是 X”，它就被当作一个发现。 |

But self‑report asks about "usual"; a single night is one draw. Regressing on single‑night fragmentation produces errors‑in‑variables in the predictor, attenuating the estimate. If the study says "fragmentation is X," it is not wrong for that night, but it may be wrong for usual. The night‑to‑night variability was causal—just not represented. | 但自我报告的是“通常”情况；单一夜晚是一次抽取。用单夜的碎片化进行回归，会在预测变量中产生变量误差，从而衰减估计。如果研究说“碎片化是 X”，它并非对于该夜晚错误，但对于通常情况可能是错误的。逐夜变异性是因果性的——只是没有被表述。

#### 6. The "Vertex as Discovery" Fallacy / “顶点作为发现”谬误

| English | 中文 |
|---|---|
| Many studies treat the vertex position of a U‑shape as a discovery. If the study says "the minimum is at 7 hours," that is treated as a finding. | 许多研究将 U 型的顶点位置视为一个发现。如果研究说“最低点在 7 小时”，它就被当作一个发现。 |

But different mechanisms produce different vertex positions. The mono leg puts the vertex at 10.16 h; the frag_driven leg puts it at 5.23 h. If the study says "the minimum is at 7 h," it is not wrong for the curve, but it may be wrong for the interpretation. The vertex position was causal—just not represented. | 但不同的机制产生不同的顶点位置。mono 腿将顶点放在 10.16 小时；frag_driven 腿将顶点放在 5.23 小时。如果研究说“最低点在 7 小时”，它并非对于该曲线错误，但对于解释可能是错误的。顶点位置是因果性的——只是没有被表述。

---

### What This Framework Does Differently / 这个框架做了什么不同的事情

| English | 中文 |
|---|---|
| This framework treats self‑report data as potentially a mixture—true sleep plus fragmentation cost—and tests whether a reporting rule can manufacture a U‑shape from a true relationship that is not U‑shaped. | 该框架将自我报告数据视为潜在的混合物——真实睡眠加上碎片化成本——并测试报告规则是否能在不存在 U 型的真实关系中制造出 U 型。 |

Three legs: flat (no relationship), mono (monotonically decreasing with true sleep), frag_driven (outcome depends only on fragmentation). | 三条腿： flat（无关系）、mono（随真实睡眠单调递减）、frag_driven（结果仅依赖于碎片化）。

The scope problem: The falsifier is scoped to the flat null, but the null is "flat or monotonic". | 范围问题： 可证伪条件被限定在平坦零假设上，而零假设是“平坦或单调”。

The three‑column test: Subtract measured sleep from reported hours, regress against awakenings count and duration. | 三列测试： 将报告小时数减去实测睡眠量，对觉醒次数和觉醒持续时间进行回归。

Product vs additive: gap = frag × wake_cost is a product, not an additive sum. | 乘积 vs 加性： gap = frag × wake_cost 是乘积关系，而非加性关系。

Night‑to‑night variability: A single night's measurement is one draw; it does not represent "usual". | 逐夜变异性： 单夜测量是一次抽取；它不能代表“通常”情况。

---

### The Knowledge‑State Vocabulary / 知识状态词汇表

| English | 中文 |
|---|---|
| SUPPORTED | 已支持 |
| REPAIRED | 已修复 |
| OPEN | 开放 |
| NOT_STUDIED | 未研究 |
| UNKNOWN_ATM | 未知（机制已知，值未知） |
| UNDEFINED | 未定义（无统一定义或协议） |

---

### What Is NOT a Valid Epistemic State / 什么不是有效的认知状态

| English | 中文 |
|---|---|
| REPORT_AS_MEASUREMENT is not a valid epistemic state. If reported hours mix two independent variables, treating them as a measurement of true sleep is a measurement error, not an epistemic one. Biology does not care about our reporting rules. REPORT_AS_MEASUREMENT | 不是一个有效的认知状态。如果报告时长混合了两个独立的变量，将其视为真实睡眠的测量就是一个测量误差，而非认知误差。生物学并不关心我们的报告规则。 |

The framework refuses to record reported hours as a measurement. Instead, it records them as a mixture—true sleep plus fragmentation cost—and names what would be needed to move it to a calibrated state. | 该框架拒绝将报告记录为测量。相反，它将报告记录为混合物——真实睡眠加上碎片化成本——并指出需要什么才能将其移动到已校准的状态。

---

### The Standard / 标准

| English | 中文 |
|---|---|
| The question should not be: | 问题不应该是： |

"Is there a U‑shaped relationship between sleep duration and mortality?" | > “睡眠时长与死亡率之间存在 U 型关系吗？”

But rather: | 而应该是：

"What is reported hours mixing, and is the U‑shape produced by true sleep or by a reporting rule?" | > “报告时长混合了什么？U 型是由真实睡眠产生的，还是由报告规则产生的？”

If the answer is that a reporting rule can manufacture a U‑shape from a true relationship that is not U‑shaped, then the published U‑shape may be a measurement artifact. End of story. | 如果答案是报告规则可以在不存在 U 型的真实关系中制造出 U 型，那么已发表的 U 型就可能是一个测量伪迹。故事结束。

This framework does not pretend otherwise. | 该框架不会假装并非如此。

---

下一步

如果你想让我继续处理下一个文件夹，只需告诉我。如果你想让我把这些文档放入一个 sim-span/ 文件夹的 PR 中，我也可以帮你起草那个。我已准备好。
