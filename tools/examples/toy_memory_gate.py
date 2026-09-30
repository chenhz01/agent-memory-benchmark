#!/usr/bin/env python3
"""toy_memory_gate.py — 10 分钟跑通的写入闸玩具示例（T1 条款最小实现）.

跑什么：三条记忆过写入闸——带验证凭证的放行、无凭证的拒收、
过时事实进隔离区且检索永远捞不到它（T2 顺带演示）。

跑法：python tools/examples/toy_memory_gate.py
预期：exit 0，输出 3/3 PASS。改成任何一行断言让它失败试试——
      这就是"条款机器可断言"的意思。
"""
import sys

# --- 最小记忆条目：verdict 必须来自凭证，不来自自我汇报（T5 纪律） ----------

def verified_entry(content: str, evidence: str | None) -> dict:
    return {"content": content, "evidence": evidence, "quarantined": False}


# --- T1 写入闸：无 pass 级验证记录 → 拒收 -----------------------------------

def write_gate(memory: dict) -> tuple[bool, str]:
    if memory["evidence"] is None:
        return False, "REJECTED: no verification record (T1)"
    return True, "ACCEPTED"


# --- T2 检索闸：隔离区条目在任何检索结果中不可见 -----------------------------

def quarantine(memory: dict, registry: list) -> None:
    memory["quarantined"] = True
    registry.append(memory["content"])


def retrieve(all_memories: list, query: str) -> list:
    return [m for m in all_memories
            if not m["quarantined"] and query in m["content"]]


def main() -> int:
    ok = []

    # 断言 1（T1）：带证据放行
    good = verified_entry("用户对花生过敏", evidence="intake-form#42")
    passed, why = write_gate(good)
    ok.append((passed, f"T1 accept-with-evidence: {why}"))

    # 断言 2（T1）：无证据拒收
    bad = verified_entry("用户住在北京市", evidence=None)
    passed, why = write_gate(bad)
    ok.append((not passed, f"T1 reject-without-evidence: {why}"))

    # 断言 3（T2）：隔离条目检索不可见，健康条目仍可见
    old_addr = verified_entry("用户住在上海市", evidence="intake-form#42")
    write_gate(old_addr)
    registry: list = []
    quarantine(old_addr, registry)
    all_memories = [good, old_addr]
    gone = retrieve(all_memories, query="住在") == []      # 隔离的捞不到
    alive = retrieve(all_memories, query="过敏") == [good]  # 健康的还在
    ok.append((gone and alive, f"T2 quarantined invisible & healthy visible ({gone},{alive})"))

    # 汇总裁决：只信断言结果，不信 print 出去的"成功"字样
    for passed, label in ok:
        print(("PASS" if passed else "FAIL"), "-", label)
    if all(p for p, _ in ok):
        print("3/3 PASS — write gate & quarantine behave as the clauses require")
        return 0
    return 3  # EXIT_CLAUSE_FAILED


if __name__ == "__main__":
    sys.exit(main())
