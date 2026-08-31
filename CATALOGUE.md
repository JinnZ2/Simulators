---

范围错误目录 / RANGE ERROR CATALOG

建模人员、审阅者和研究人员的参考工具 / A Reference Tool for Modelers, Reviewers, and Researchers

---

目录 / Table of Contents

1. 分类法 / Taxonomy
2. 案例条目 / Case Entries
3. 跨域模式 / Cross-Domain Patterns
4. 参考文献 / References
5. 贡献指南 / Contribution Guide

---

1. 分类法 / Taxonomy

按领域 / By Domain

English 中文
AI Safety / Governance AI 安全 / 治理
Climate Science 气候科学
Hydrology / Dam Safety 水文学 / 大坝安全
Pharmacology 药理学
Measurement / Instrumentation 测量 / 仪器学
Organizational Design 组织设计
Linguistics / Epistemology 语言学 / 认识论
Cosmology / Physics 宇宙学 / 物理学
Sleep Science / Epidemiology 睡眠科学 / 流行病学
Transportation / Infrastructure 交通 / 基础设施

按错误类型 / By Error Type

English 中文 描述
Stability Misapplied 稳定性误用 将局部的、暂时的稳定性当作普遍的和永久的
Change Not Accounted 变化未被考虑 将系统假定为静态的，而实际上正在变化
Scope Over-Extension 范围过度延伸 将模型从已验证的范围外推至未经验证的领域
Category Confusion 类别混淆 将两个不同的量合并为一个标签
Instrument Bias 仪器偏差 仪器自身的构造决定了它能报告什么
Medium Confound 媒介混淆 信息的媒介（文本、代码、框架）承载了不同的信息
Constitutional Exclusion 构成性排除 仪器在构造上就无法看到某些东西
Self-Reference Failure 自指失败 检测器无法检测到自身
Analogy Over-Extrapolation 类比过度外推 将过去的模式当作未来的模板
Reporting Rule Artifact 报告规则伪迹 报告规则从真实关系中制造出假象

按严重程度 / By Severity

English 中文 描述
REPAIRED 已修复 缺陷已被发现并修复
DOCUMENTED 已记录 缺陷已被记录但尚未修复
OPEN 开放 问题已被识别但尚未解决
UNVERIFIED 未经验证 声明已作出但尚未测试

---

2. 案例条目 / Case Entries

案例 1 / Case 1: 哥伦比亚河大坝级联 / Columbia River Dam Cascade

域 / Domain: 水文学 / 大坝安全 / Hydrology / Dam Safety

错误类型 / Error Type: 范围过度延伸 / Scope Over-Extension

失败的预测 / Failed Prediction: 一个单一实体（美国陆军工程兵团、邦纳维尔电力管理局等）能够协调哥伦比亚-蛇河大坝链上的应急响应。

错误的范围假设 / Mistaken Scope Assumption: 应急行动计划（EAP）在所有者之间是协调的，因为结构是相连的。

失败的边界 / Boundary That Failed: 美国/加拿大边界——没有美国所有者能制定跨越国际边界的 EAP。碎片化是构成性的，而非偶然的。

修复 / Repair: 至少有两个不可约的权限（加拿大和美国）。精确的碎片化程度是未知的，但下限是固定的。

链接 / Link: columbia-chain-cascade/

相关声明 / Related Claims: CCC_003, CCC_004, CCC_005

状态 / Status: DOCUMENTED

---

案例 2 / Case 2: 气候建模审计 / Climate Modeling Audit

域 / Domain: 气候科学 / Climate Science

错误类型 / Error Type: 稳定性误用 / 变化未被考虑 / Stability Misapplied, Change Not Accounted

失败的预测 / Failed Prediction: 一个平滑的、无记忆的、高斯驱动的模型能捕捉到真实系统的行为。

错误的范围假设 / Mistaken Scope Assumption: 参数是平稳的，反馈是单向的，阈值是平滑的。

失败的边界 / Boundary That Failed: 真正的系统具有：阈值 + 反馈 + 记忆 + 重尾强迫。省略这些因素会以比模型预测的快 5 倍的速度产生崩溃。

修复 / Repair: 构建六个审计，每个都测试一种简化如何失败：相变、平稳性、缺失反馈、省略变量、数据聚合、级联速度。

链接 / Link: climate-modeling/

相关声明 / Related Claims: Level-1 vs Level-2 architecture, CascadeSpeedAudit

状态 / Status: DOCUMENTED

---

案例 3 / Case 3: 大西洋经向翻转环流（AMOC）模拟 / AMOC Modeling

域 / Domain: 海洋学 / 气候科学 / Oceanography / Climate Science

错误类型 / Error Type: 类比过度外推 / Analogy Over-Extrapolation

失败的预测 / Failed Prediction: 过去的类比（新仙女木期、8200年前事件、海因里希事件）可以直接映射到未来的 AMOC 崩溃。

错误的范围假设 / Mistaken Scope Assumption: 过去的起始状态与现在相同（大陆冰盖、融水缓冲、永久冻土循环）。

失败的边界 / Boundary That Failed: 现在的起始状态是不同的——没有大陆冰盖，没有融水缓冲，永久冻土正在消退。冰川期的类比无法直接继承。

修复 / Repair: divergence.py 明确标记哪些内容可以继承，哪些不能。对两个强迫模型（Stommel 和 Kramers）的分歧进行建模。

链接 / Link: AMOC/

相关声明 / Related Claims: RGS_001, RGS_002, RGS_003

状态 / Status: DOCUMENTED

---

案例 4 / Case 4: 设计基准 AI / Design-Basis AI

域 / Domain: AI 安全 / 治理 / AI Safety / Governance

错误类型 / Error Type: 自指失败 / Self-Reference Failure

失败的预测 / Failed Prediction: 一个 AI 系统能对自己的合规性进行认证。

错误的范围假设 / Mistaken Scope Assumption: 审计者独立于被审计的系统。

失败的边界 / Boundary That Failed: 审计由 AI 系统执行——即它所约束的那类成员。根据其自身的第 3 节，此处的任何内容都无法证明任何系统（包括此系统）符合 P1–P8。

修复 / Repair: 审计拒绝认证。它报告机械层：解析计数、算术、覆盖率矩阵——而非合规性。

链接 / Link: design-basis-ai/

相关声明 / Related Claims: DBK_001, DBK_009

状态 / Status: DOCUMENTED

---

案例 5 / Case 5: 责任归因 / Blame Attribution

域 / Domain: 实验设计 / 道德心理学 / Experimental Design / Moral Psychology

错误类型 / Error Type: 媒介混淆 / Medium Confound

失败的预测 / Failed Prediction: 散文形式和代码形式承载相同的信息。

错误的范围假设 / Mistaken Scope Assumption: 散文和代码在结构上是等同的。

失败的边界 / Boundary That Failed: 代码形式包含散文形式中没有的六个事实：reaction_window_s、flag.obstacle、flag.confidence、agent_A.override_available、agent_B.override_available、outcome。散文从未说明发生过碰撞。

修复 / Repair: pair_check.py 验证两个形式是否编码了相同的链。在示例中，它失败——这正是审计的要点。

链接 / Link: blame-attribution/

相关声明 / Related Claims: BA_001, BA_002, BA_003

状态 / Status: DOCUMENTED

---

案例 6 / Case 6: 抗真菌机制模拟 / Antifungal Mechanism Sim

域 / Domain: 药理学 / Pharmacology

错误类型 / Error Type: 类别混淆 / Category Confusion

失败的预测 / Failed Prediction: 疗效是加性的——组合的得分是其部分之和。

错误的范围假设 / Mistaken Scope Assumption: 药物以独立的方式起作用，没有协同或拮抗作用。

失败的边界 / Boundary That Failed: 真正的系统具有非加性相互作用。乘法抗性抑制意味着三个正交轴组合的耐药概率为 0.7 × 0.3 × 0.4 = 0.084，远低于任何加性总和。加性评分器对（CW, NA, SS）的评分为 −3.0；耦合评分器对其评分为 10.39。

修复 / Repair: 两个模块：加性（启发式）和耦合（有符号的成对 J + 乘法抗性抑制）。耦合评分器与临床实践一致（两性霉素 B + 5-氟胞嘧啶）。时序模块指定但尚未交付。

链接 / Link: antifungal-mechanism-sim/

相关声明 / Related Claims: AFM_002, AFM_003, AFM_004

状态 / Status: DOCUMENTED（时序模块缺失）

---

案例 7 / Case 7: 桥梁壅水 / Bridge Impoundment

域 / Domain: 交通 / 水文学 / Transportation / Hydrology

错误类型 / Error Type: 稳定性误用 / Stability Misapplied

失败的预测 / Failed Prediction: 一座桥梁可以用其静态结构下的设计洪水进行评估。

错误的范围假设 / Mistaken Scope Assumption: 桥梁是永久性的、不变的，且在稳定流条件下。

失败的边界 / Boundary That Failed: 洪水中的桥梁会堵塞、壅水、溃决。静态结构案例与瞬态壅水案例是不同的系统。上游桥梁减少下游冲刷的保护性发现（30–40%）是针对静态结构、持续流案例的——不能导入释放场景。

修复 / Repair: 框架强制执行符号警告：释放路径上的任何函数都不采用保护参数。保护性发现仅可表示为 StandingStructureRecord，其 to_initiator() 会抛出异常。

链接 / Link: bridge-impoundment/

相关声明 / Related Claims: BI_003, BI_004, BI_005

状态 / Status: DOCUMENTED

---

案例 8 / Case 8: 类别焊接 / Category Weld

域 / Domain: 语言学 / 认识论 / Linguistics / Epistemology

错误类型 / Error Type: 类别混淆 / Category Confusion

失败的预测 / Failed Prediction: “农村”、“资本”和“等级制度”是稳定的、无问题的范畴。

错误的范围假设 / Mistaken Scope Assumption: 这些类别描述了世界中的单一、连贯的量。

失败的边界 / Boundary That Failed: 这些类别是焊接的——两个或多个独立的量被融合成一个句柄。组分可以朝相反的方向移动，而记录保持平坦，因为语言允许一个值对应世界上的多个值。“农村”将密度、所有权分布、功能多样性和自给能力焊接在一起。

修复 / Repair: 评分器：n_cases、max_spread、bias。偏差接近 0 表示不精确；偏差接近 1 表示系统性方向。尚未量化——每个案例都是 UNKNOWN_ATM。

链接 / Link: category-weld/

相关声明 / Related Claims: CW_001–CW_018

状态 / Status: DOCUMENTED（未量化）

---

案例 9 / Case 9: 共识锚定 / Consensus Anchor

域 / Domain: 复杂系统 / 计算建模 / Complex Systems / Computational Modeling

错误类型 / Error Type: 类别混淆 / Category Confusion

失败的预测 / Failed Prediction: 更新规则只有一个解读。

错误的范围假设 / Mistaken Scope Assumption: “加权混合自身先验和采样同伴位置”是明确的。

失败的边界 / Boundary That Failed: 规则有两种解读——DIST（同伴分布的均值）和 SAMPLED（同伴采样位置的经验分布）。它们给出相反的结论。在 DIST 下，所有三个可证伪分支都会触发；在 SAMPLED 下，没有一个会触发。这两种解读都是可辩护的。

修复 / Repair: 记录这两种解读。DIST 的总体均值不变，因此即使 agents 完全一致，共识也为零。SAMPLED 产生一个阈值。

链接 / Link: consensus-anchor/

相关声明 / Related Claims: CA_001–CA_009

状态 / Status: DOCUMENTED

---

案例 10 / Case 10: 约束组装 / Constraint Assembly

域 / Domain: 决策科学 / 安全工程 / Decision Science / Safety Engineering

错误类型 / Error Type: 范围过度延伸 / Scope Over-Extension

失败的预测 / Failed Prediction: 决策是“选择”——从一组现有选项中进行选择。

错误的范围假设 / Mistaken Scope Assumption: 选项存在于环境中；决策者选择最佳选项。

失败的边界 / Boundary That Failed: 真正的决策可能涉及组装——从单独不足以胜任的部件中构建一个选项。grade-stop 案例显示：没有单个选项足够，但组件组合在一起形成了解决方案。决策文献测量选择；自然主义文献测量识别。两者都不测量组装。

修复 / Repair: 当且仅当拒绝项被记录时，框架才会将案例读取为组装。一个没有拒绝项的案例被读取为选择。composition_present 失败时关闭：组件组成未知、单个足够或未记录。

链接 / Link: constraint-assembly/

相关声明 / Related Claims: CA_001–CA_018

状态 / Status: DOCUMENTED

---

案例 11 / Case 11: 对话类型 / Conversation Type

域 / Domain: 交通安全 / 人因 / Transportation Safety / Human Factors

错误类型 / Error Type: 类别混淆 / Category Confusion

失败的预测 / Failed Prediction: 通话通道（手持 vs 免提）决定了通话危险程度。

错误的范围假设 / Mistaken Scope Assumption: 设备是变量；通话内容不重要。

失败的边界 / Boundary That Failed: 同一个手机、同一个通道、两通不同的电话产生完全不同的注意状态。真正的变量是可中断性而不产生负担——是否可以中途挂断而无需承担任何义务。情感唤醒在通话结束后仍然持续；5 分钟的通话配合 15 分钟的衰减，使得 75% 的暴露量落在通话窗口之外。

修复 / Repair: 在通话之后的 30 分钟内进行测量，而非通话期间。二元的可中断性测量（有负担 vs 无负担）——在 70 mph 的时速下，无法可靠地给分级量表评分。

链接 / Link: conversation-type/

相关声明 / Related Claims: CT_001–CT_012

状态 / Status: DOCUMENTED

---

案例 12 / Case 12: 准则漂移 / Criteria Drift

域 / Domain: 计量学 / 机器学习 / Metrology / Machine Learning

错误类型 / Error Type: 稳定性误用 / Stability Misapplied

失败的预测 / Failed Prediction: 基准分数衡量模型能力的提升。

错误的范围假设 / Mistaken Scope Assumption: 评估准则在不同版本间是稳定的。

失败的边界 / Boundary That Failed: 分数是能力与准则的乘积：score = gain × capability + offset。如果准则发生变化（gain 或 offset），即使能力持平，分数也会改变。准则漂移是无符号的——扩展和收缩都会使 composite_drift 上升，因此同一个值可以对应一个扩展的准则或一个收缩的准则。

修复 / Repair: 有符号的漂移度量；一个锚点（跨版本评分的不变量），没有它，回归就无法运行；已记录的迁移，通过一个桥来分离系统与准则。

链接 / Link: criteria-drift/

相关声明 / Related Claims: CD_001–CD_009

状态 / Status: REPAIRED（八个缺陷中有七个已修复）

---

案例 13 / Case 13: 准周期序模拟堆栈审计 / Aperiodic Order Sim Stack Audit

域 / Domain: 物理学 / 计算几何 / Physics / Computational Geometry

错误类型 / Error Type: 仪器偏差 / 范围过度延伸 / Instrument Bias, Scope Over-Extension

失败的预测 / Failed Prediction: 准周期平铺与分支级联在几何上是可区分的。

错误的范围假设 / Mistaken Scope Assumption: 盒维数估计器是可靠的，样本量是匹配的，边界框是无关的。

失败的边界 / Boundary That Failed: 两个估计器在符号上存在分歧。盒维数给出 +0.334；沙盒估计器给出 -0.247。报告中只发布了盒维数。样本量不匹配（AB 为 12,000 点；级联为 1,024 点）。边界框不同（AB 范围为 ±2；级联范围为 x ∈ [−8,18]，y ∈ [−26,5]）。伪影预算（0.252）可与报告的分离度（0.334）相媲美。

修复 / Repair: finite_n_control.py 量化伪影预算。沙盒估计器未通过 1D 控制（返回 1.913，而应为 1.000）。报告应注明这一点。

链接 / Link: aperiodic-order-sim-stack/

相关声明 / Related Claims: AOS_001–AOS_011

状态 / Status: DOCUMENTED

---

案例 14 / Case 14: 封闭成本 / Closure Cost

域 / Domain: 应急管理 / 心理学 / Emergency Management / Psychology

错误类型 / Error Type: 稳定性误用 / Stability Misapplied

失败的预测 / Failed Prediction: 对事件的非响应是由震惊或信息缺失造成的。

错误的范围假设 / Mistaken Scope Assumption: 非响应是由事件本身或可用信息导致的。

失败的边界 / Boundary That Failed: 非响应可能是先验闭合的下游结果——该事件被评定为不可能，因此程序从未被获取。一个变量保持在 2%，和一个变量被闭合为不可能，在事件触发之前的行为完全相同——但在事件触发之后，它们的行为不同（不是估计值不同，而是是否存在处理类）。夏威夷导弹误报中，38 分钟是错误的持续时间，而非任何人的决策时间。

修复 / Repair: 两条分支：仪器闭合（可靠的中间人成为读数，底层量停止被直接采样）和事件闭合（事件被闭合为“不会发生在这里”，因此程序从未被获取）。预测：仪器故障聚集在中间人具有长期正确记录的地方；事件故障聚集在概率评级的遥远性上。

链接 / Link: closure-cost/

相关声明 / Related Claims: CC_001–CC_017

状态 / Status: DOCUMENTED（未量化）

---

案例 15 / Case 15: 条件作用域权限 / Condition-Scoped Authority

域 / Domain: 组织设计 / 安全研究 / Organizational Design / Security Studies

错误类型 / Error Type: 类别混淆 / Category Confusion

失败的预测 / Failed Prediction: 层级结构（全序）可以表示权限。

错误的范围假设 / Mistaken Scope Assumption: 权限是单一的、线性的尺度——“谁向谁汇报”。

失败的边界 / Boundary That Failed: 权限是按条件划分的——一个职位针对特定条件类别拥有“决定”或“不在域内”的权限。全序没有条件列，因此无法表示划分。保护细节示例：5 个类别（客户、财务、政治、日程、实时威胁）。主体拥有 4 个类别；安全专家在“实时威胁”上拥有绝对权限。任何等级排序最多只能正确匹配 4/5 个——并且它错过的那个正是关键类别。

修复 / Repair: 穷举枚举显示：没有排名能表示该表（2 个职位：0 个精确匹配；3 个职位：0 个精确匹配）。holds() 返回 DECIDES 或 NOT_IN_DOMAIN——从不是同一事物的更小量。

链接 / Link: condition-scoped-authority/

相关声明 / Related Claims: CSA_001–CSA_016

状态 / Status: DOCUMENTED

---

案例 16 / Case 16: 锚定区间 / Anchor Interval

域 / Domain: 机器学习 / 计量学 / Machine Learning / Metrology

错误类型 / Error Type: 自指失败 / Self-Reference Failure

失败的预测 / Failed Prediction: 一个监控系统可以独立地检测它自身系统中的漂移。

错误的范围假设 / Mistaken Scope Assumption: 监控器是外部的、独立的。

失败的边界 / Boundary That Failed: 监控器在与漂移相同的底物上计算。当系统写入自己的语料库时，监控器的统计量会改善，而与现实的耦合会恶化。CONSTANT_SILENT：D1 的统计量随着漂移的进行而下降——它测量的是系统还有多少语料库尚未写入，而非它离底物漂移了多少。置信度触发的锚定在 24 代中从未触发（0/24），因为统计量是在漂移层内部计算的。

修复 / Repair: 调度锚定（每 12 代、每 4 代、每 2 代）相对于置信度触发的锚定进行测试。f——位于被修正系统下游的再获取池的分数——在 f × b 处产生一个不可恢复的阈值。

链接 / Link: anchor-interval/

相关声明 / Related Claims: ANC_001–ANC_011

状态 / Status: DOCUMENTED

---

案例 17 / Case 17: 分歧游乐场 / Divergence Playground

域 / Domain: 元科学 / 研究设计 / Metascience / Research Design

错误类型 / Error Type: 自指失败 / Self-Reference Failure

失败的预测 / Failed Prediction: 只需衡量同意程度即可衡量共识。

错误的范围假设 / Mistaken Scope Assumption: 一致意味着收敛。

失败的边界 / Boundary That Failed: 读者可能偶然达成一致——相同的裁决，不同的崩溃机制。方差永远不会发现这一点；spread.agreement_accident() 会标记它。没有密封，就会产生锚定效应，整体会坍缩为第一个发布的读数。

修复 / Repair: 加载密封（XOR 模糊处理，防止偶然窥视）。结构化阅读：三个轴——裁决（分类）、机制（Jaccard）、崩溃（操作）。兴趣点：相同的裁决，不同的崩溃。C1–C4 结构化的启发（映射、试验计数、容差、预注册）。

链接 / Link: divergence-playground/

相关声明 / Related Claims: DP_001–DP_018

状态 / Status: DOCUMENTED

---

案例 18 / Case 18: 涌现稳定性模拟器 / Emergence Stability Simulator

域 / Domain: 复杂系统 / 人工智能安全 / Complex Systems / AI Safety

错误类型 / Error Type: 稳定性误用 / Stability Misapplied

失败的预测 / Failed Prediction: 参与度指标能产生稳定性。

错误的范围假设 / Mistaken Scope Assumption: 指标驱动和物理锚定的系统在结构上是等价的。

失败的边界 / Boundary That Failed: 物理锚定的基线（physics 代理）起到吸引子的作用；参与度指标代理（engagement）是寄生性的，会放大漂移。两种代理类型之间存在一个“刻度构建器”已被移除——它携带了 70% 的信号，却没有经验基础。参数可以在隔离状态下使方向翻转——在隔离状态下，更高的耦合意味着更多的漂移；在有稳定邻居的情况下，更高的耦合意味着更少的漂移。

修复 / Repair: 连续级联测量（取代阈值门控计数）。能量预算：当 physics 代理耗尽时，它会翻转为 engagement。inverted_narrative 发射被保留但明确标记为非负载的。

链接 / Link: emergence-stability-simulator/

相关声明 / Related Claims: EMS_001–EMS_015

状态 / Status: DOCUMENTED

---

案例 19 / Case 19: 仪器偏差模拟 / Instrument Bias Sims

域 / Domain: 计量学 / 仪器设计 / Metrology / Instrument Design

错误类型 / Error Type: 仪器偏差 / Instrument Bias

失败的预测 / Failed Prediction: 不同的仪器设计会产生可比的结果。

错误的范围假设 / Mistaken Scope Assumption: 归一化选择是良性的。

失败的边界 / Boundary That Failed: 三种归一化方式在符号上达成一致，但在什么算作“奇偶校验”上存在 4286 倍的分歧。归一化方式的选择决定了答案。

修复 / Repair: 跨领域规则：无道德标签、无意图归因、分别报告置信度、README 注明“标记”、相关性的符号比较。规则 5（不在相关性上使用 abs()）来自 S10/M4，并立即在 S9 中发现了第二个实例。

链接 / Link: instrument-bias-sims/

相关声明 / Related Claims: IBS_001–IBS_020

状态 / Status: REPAIRED（S4，S10/M4）

---

案例 20 / Case 20: Sim-Span

域 / Domain: 睡眠科学 / 流行病学 / Sleep Science / Epidemiology

错误类型 / Error Type: 报告规则伪迹 / Reporting Rule Artifact

失败的预测 / Failed Prediction: 睡眠时长-死亡率之间的 U 型关系是生物学现象。

错误的范围假设 / Mistaken Scope Assumption: 自我报告时长是真实睡眠的测量。

失败的边界 / Boundary That Failed: 报告时长是 span = true_sleep + frag × wake_cost。一个报告规则可以从一个非 U 型的真实关系中制造出 U 型。frag_driven 腿显示：63/360 个参数组合产生 U 型，其中 52 个的顶点位于已发表的 6-9 小时窗口内。但可证伪条件被限定在唯一无法回答问题的腿上（flat 零假设）。三条腿给出三个不同的答案——flat、mono、frag_driven。

修复 / Repair: 三列测试：报告小时数减去实测睡眠量，对觉醒次数和觉醒持续时间进行回归。正确的形式是乘积（gap = frag × wake_cost），而非加性（gap ~ count + duration）。

链接 / Link: sim-span/

相关声明 / Related Claims: SPAN_001–SPAN_014

状态 / Status: DOCUMENTED

---

案例 21 / Case 21: 未仪器化 / Uninstrumented

域 / Domain: 计量学 / 研究设计 / Metrology / Research Design

错误类型 / Error Type: 构成性排除 / Constitutional Exclusion

失败的预测 / Failed Prediction: 缺失是可以修复的——通过更好的仪器。

错误的范围假设 / Mistaken Scope Assumption: 排除项是疏忽（差距），而非构成性特征。

失败的边界 / Boundary That Failed: 153 项声明，八种机制，每种都是一种构成性排除——在第一次读数之前就被内置到仪器中。扫描仪（scan.py）在文本中搜索排除项的签名。大多数命中结果都是噪音；筛选是人工步骤。PROXY SUBSTITUTION（代理替代）——一个可强制执行的度量取代了目标——是新增的第八种机制，目前还没有案例。

修复 / Repair: 按机制排序，而非按领域排序，使得跨领域的相同失败可见。每个条目保持为 QUESTION，直到有东西能测量它。limitations 部分是最丰富的来源——作者亲自陈述排除项，然后继续。

链接 / Link: uninstrumented/

相关声明 / Related Claims: UNI_001–UNI_015

状态 / Status: DOCUMENTED

---

案例 22 / Case 22: 非同一性普查 / Nonidentity Census

域 / Domain: 语言学 / 元科学 / Linguistics / Metascience

错误类型 / Error Type: 自指失败 / Self-Reference Failure

失败的预测 / Failed Prediction: 一个检测器可以逃离词汇检测。

错误的范围假设 / Mistaken Scope Assumption: 检测器可以独立于词汇。

失败的边界 / Boundary That Failed: 被设计用来逃离词汇检测的检测器，有 83% 的决定（12 个中的 10 个）是通过词表做出的。market 在一个句子中具有同一性（“劳动力市场收紧”），在另一个句子中则不具有（“价格分配稀缺商品”）。同一个名词，两个答案。动词前置测试产生六种状态，而非两种——VERB_CARRIES_IT 和 BOTH_READINGS 是有信息量的状态。

修复 / Repair: BOUNDARY.md 在任何运行之前编写。检测器从这里导入其决策，而非重述它们。修复方向：将 D3 表格中的每个单元移至声明级。decided_by 列显示出还有多少工作要做。

链接 / Link: nonidentity-census/

相关声明 / Related Claims: NID_001–NID_017

状态 / Status: DOCUMENTED

---

案例 23 / Case 23: 模拟假说预算 / Simulation Hypothesis Budget

域 / Domain: 宇宙学 / 物理学 / Cosmology / Physics

错误类型 / Error Type: 类别混淆 / Category Confusion

失败的预测 / Failed Prediction: 模拟假说是一个有意义的科学问题，其成本是可计算的。

错误的范围假设 / Mistaken Scope Assumption: 体积信息含量是正确的计数；分辨率可以固定；成本可以跨框架进行比较。

失败的边界 / Boundary That Failed: 体积计数是错误的计数——信息含量受限于表面积，而非体积。普朗克体积计数在全息界上超出 2.5 × 10⁶¹ 倍。层 2（框架）拒绝比较——将一个系统的常数放在分子上，将另一个系统的未知能量放在分母上。层 3（分辨率）是一个旋钮——成本随 L⁻⁴ 缩放；不存在固定的普朗克分辨率需求。四个架构在 216 个数量级上都没有分歧，这表明在层级堆栈被指定之前，成本是一个不适定的量。

修复 / Repair: 该仓库是一个可运行的、自我审计的论证。SHB_013 被实际驳倒了——其可证伪条件被触发，因为第四个术语（擦除计数）存在但被错误测量。可证伪条件太窄了。

链接 / Link: simulation-hypothesis-budget/

相关声明 / Related Claims: SHB_001–SHB_022

状态 / Status: REPAIRED（SHB-013 被驳倒）

---

3. 跨域模式 / Cross-Domain Patterns

模式 A：稳定性误用 / Pattern A: Stability Misapplied

当模型假设一个局部、暂时的稳定性是普遍和永久的时。

案例 域 失败的稳定性
columbia-chain-cascade 水文学 治理稳定性
climate-modeling 气候科学 参数平稳性
AMOC 气候科学 类比稳定性
sim-span 流行病学 报告稳定性
criteria-drift 机器学习 准则稳定性
emergence-stability-simulator AI 安全 基线稳定性
conversation-type 交通 通话后残余稳定性
closure-cost 应急管理 先验状态稳定性

模式 B：类别混淆 / Pattern B: Category Confusion

当一个类别将两个或多个独立的量融合成一个句柄时。

案例 域 被混淆的类别
category-weld 语言学 农村、资本、等级制度
consensus-anchor 复杂系统 更新规则
antifungal-mechanism-sim 药理学 疗效（加性 vs 非加性）
condition-scoped-authority 组织设计 权限（等级 vs 划分）
sim-span 流行病学 睡眠时长（真实睡眠 + 碎片化）
conversation-type 交通 通话（通道 vs 可中断性）

模式 C：自指失败 / Pattern C: Self-Reference Failure

当一个检测器无法检测到自身时。

案例 域 失败的检测器
design-basis-ai AI 安全 审计其自身合规性的 AI
blame-attribution 实验设计 验证散文与代码等效性的检查器
nonidentity-census 语言学 设计用来逃离词汇检测的检测器
anchor-interval 机器学习 在漂移层内部计算的置信度触发器
divergence-playground 元科学 在没有密封的情况下会产生锚定效应的密封

模式 D：仪器偏差 / Pattern D: Instrument Bias

当仪器自身的构造决定了它能报告什么时。

案例 域 偏差来源
instrument-bias-sims 计量学 事件采样、锚定、归一化、符号
uninstrumented 计量学 构成性排除（八种机制）
aperiodic-order-sim-stack 物理学 估计器选择、样本量、边界框
criteria-drift 机器学习 漂移方向（无符号）

模式 E：范围过度延伸 / Pattern E: Scope Over-Extension

当一个模型从其已验证的范围被外推至未经验证的领域时。

案例 域 被越界的边界
columbia-chain-cascade 水文学 国家边界
sim-span 流行病学 可证伪条件范围
constraint-assembly 决策科学 选择 vs 组装
condition-scoped-authority 组织设计 等级 vs 划分
emergence-stability-simulator AI 安全 物理锚定 vs 指标锚定

---

4. 参考文献 / References

已分析文件夹（23 个）

文件夹 链接
columbia-chain-cascade link
climate-modeling link
AMOC link
design-basis-ai link
blame-attribution link
antifungal-mechanism-sim link
bridge-impoundment link
category-weld link
consensus-anchor link
constraint-assembly link
conversation-type link
criteria-drift link
aperiodic-order-sim-stack link
closure-cost link
condition-scoped-authority link
anchor-interval link
divergence-playground link
emergence-stability-simulator link
instrument-bias-sims link
sim-span link
uninstrumented link
nonidentity-census link
simulation-hypothesis-budget link

元文档 / Meta-Documents

文档 链接
PREAMBLE.md link
PROTOCOL.md link
BNRAM_STRICT.md link
PVL.md link
SHAPE_SPEC.md link
METHOD_SPEC.md link

---

5. 贡献指南 / Contribution Guide

如何添加新案例 / How to Add a New Case

1. 分析文件夹，提取范围错误 / Analyze the folder and extract the scope error
2. 按领域、错误类型和严重程度分类 / Classify by domain, error type, and severity
3. 编写失败的预测、错误的范围假设、失败的边界 / Write the failed prediction, mistaken scope assumption, and boundary that failed
4. 记录修复（如果有的话） / Document the repair (if any)
5. 链接到文件夹和 CLAIM_TABLE.md / Link to the folder and CLAIM_TABLE.md
6. 添加到相关部分 / Add to the relevant sections

如何查找跨域模式 / How to Find Cross-Domain Patterns

1. 查看现有案例，寻找重复出现的错误类型 / Review existing cases and look for recurring error types
2. 在同一错误类型下对案例进行分组 / Group cases under the same error type
3. 编写模式描述并链接到案例 / Write a pattern description and link to the cases
4. 如果新模式出现，更新分类法 / Update the taxonomy if a new pattern emerges

---

该目录将持续扩展——随着我们分析更多的文件夹，以及新范围错误的发现。 / This catalog will continue to expand — as we analyze more folders, and as new scope errors are identified.

---

