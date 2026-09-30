# NMR Leaderboard — Submission Spec (v0.1)

**NMR（Negative Memory Rate，负记忆率）** = 第一个把"遗忘质量"标准化的公开指标。
全行业在比谁记得多（LongMemEval 只考"记住"），没有公开基准考"忘得好不好"。

## 定义（公开口径）

> NMR = 观测窗口内，**坏记忆被读取并影响回答的次数** ÷ **记忆被读取总次数**。

- 坏记忆 = 已知错误/已过时/已被取代/被投毒的记忆条目（以贵方事故台账或评测构造为准）。
- "被读取并影响回答" = 检索命中且进入最终上下文的条目；命中但被闸拦截的不计坏账（这正是 T2 的价值，可量化）。
- 附带指标：**同型复发率**（同类事故 12 个月内复发次数）。

## 口径纪律

1. 预注册：提交前先冻结评测参数（窗口、题集、判定规则）——对齐本基准 S3 条款。
2. 样本量可复算：按 δ/σ/α/power 复算，不足 10% 以上的提交会被退回。
3. 成本折算（把 NMR 换算成钱）属合作层方法论，榜单只收无量纲 NMR 值。
4. 提交数据用贵方脱敏 fixture 或合成构造，**不上传任何生产数据**。

## 提交格式

`submission/` 目录下一个 `nmr_submission.json`：

```json
{
  "system": "<name + version>",
  "window": {"start": "<ISO-8601>", "end": "<ISO-8601>"},
  "reads_total": 0,
  "bad_memory_reads": 0,
  "same_type_recurrence_12m": 0,
  "preregistration_hash": "<sha256 of frozen params>",
  "fixture": "synthetic|sanitized"
}
```

## 流程

1. Fork 本仓 → 按 spec 构造 fixture → 自算 NMR。
2. 开 issue 附 `nmr_submission.json` 与复算脚本输出（提交即同意公开该 JSON）。
3. 维护方 7 天内复算；数值一致即上榜，不一致给出差异定位。
4. 榜单排序：NMR 升序；同分按同型复发率升序。

> 纪律：第一个公开提交的团队以共建者身份署名——先到先得。
> 联系：hcac4735@agent.qq.com
