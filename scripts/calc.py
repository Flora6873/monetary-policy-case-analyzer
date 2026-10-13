#!/usr/bin/env python3
"""货币银行学常用计算器。

用法示例:
    python3 calc.py money_multiplier --rr 0.1 --c 0.05 --e 0.02 --t 0.03
    python3 calc.py deposit_expansion --reserve 0.2 --base 1000
    python3 calc.py present_value --fv 1000 --rate 0.05 --years 3
    python3 calc.py compound --pv 1000 --rate 0.05 --years 3 --freq 12
    python3 calc.py fisher --nominal 0.06 --inflation 0.02
    python3 calc.py duration --face 1000 --coupon 0.05 --ytm 0.06 --years 3
    python3 calc.py exchange_swap --buy 6.45 --sell 6.50 --amount 1000000

所有结果同时输出"过程+结果"，便于直接写入解析。
"""

import argparse
import json
import sys


def _round(x, n=4):
    return round(x, n)


# ---------- 货币乘数 ----------
def money_multiplier(rr, c, e, t, rt=None):
    """M2 型货币乘数。

    rr: 法定准备金率 (required reserve ratio)
    c : 现金漏损率 (currency/deposit ratio)
    e : 超额准备金率 (excess reserve ratio)
    t : 定期存款占活期存款比率
    rt: 定期存款法定准备金率，默认等于 rr
    """
    if rt is None:
        rt = rr
    denom = c + rr + e + t * rt
    if denom <= 0:
        raise ValueError("分母必须为正，请检查输入参数")
    m = (1 + c + t) / denom
    simple = 1.0 / (rr + c + e) if (rr + c + e) > 0 else float("inf")
    return {
        "货币乘数 m": _round(m),
        "分母 (c+rr+e+t*rt)": _round(denom),
        "简化乘数 1/(rr+c+e)": _round(simple),
        "过程": f"m = (1 + {c} + {t}) / ({c} + {rr} + {e} + {t}*{rt}) = {_round(1 + c + t)} / {_round(denom)} = {_round(m)}",
    }


# ---------- 存款派生 ----------
def deposit_expansion(reserve, base):
    """简单存款乘数模型：存款总额 = 准备金 / 准备金率。"""
    if reserve <= 0 or reserve >= 1:
        raise ValueError("准备金率应在 (0,1) 区间")
    total = base / reserve
    multiplier = 1.0 / reserve
    return {
        "总存款 D": _round(total, 2),
        "派生倍数": _round(multiplier),
        "新增派生存款": _round(total - base, 2),
        "过程": f"D = 准备金 / rr = {base} / {reserve} = {_round(total, 2)}；派生倍数 = 1/{reserve} = {_round(multiplier)}",
    }


# ---------- 现值 / 终值 ----------
def present_value(fv, rate, years):
    pv = fv / ((1 + rate) ** years)
    return {
        "现值 PV": _round(pv, 2),
        "贴现因子": _round(1 / ((1 + rate) ** years), 6),
        "过程": f"PV = {fv} / (1+{rate})^{years} = {_round(pv, 2)}",
    }


def compound(pv, rate, years, freq):
    fv = pv * ((1 + rate / freq) ** (freq * years))
    eff = (1 + rate / freq) ** freq - 1
    return {
        "终值 FV": _round(fv, 2),
        "有效年利率 EAR": _round(eff, 6),
        "过程": f"FV = {pv} * (1+{rate}/{freq})^({freq}*{years}) = {_round(fv, 2)}",
    }


# ---------- 费雪方程 ----------
def fisher(nominal, inflation):
    real = (1 + nominal) / (1 + inflation) - 1
    approx = nominal - inflation
    return {
        "精确实际利率": _round(real, 6),
        "近似实际利率 (i-π)": _round(approx, 6),
        "误差": _round(real - approx, 6),
        "过程": f"r = (1+{nominal})/(1+{inflation}) - 1 = {_round(real, 6)}；近似 = {nominal} - {inflation} = {_round(approx, 6)}",
    }


# ---------- 麦考利久期 ----------
def duration(face, coupon, ytm, years):
    """年付息债券的麦考利久期与修正久期。"""
    p = 0.0
    weighted = 0.0
    for t in range(1, years + 1):
        cf = face * coupon
        if t == years:
            cf += face
        pv_cf = cf / ((1 + ytm) ** t)
        p += pv_cf
        weighted += t * pv_cf
    d_mac = weighted / p
    d_mod = d_mac / (1 + ytm)
    return {
        "债券价格 P": _round(p, 2),
        "麦考利久期 D": _round(d_mac, 4),
        "修正久期 D*": _round(d_mod, 4),
        "利率上升1%的价格变动": f"{-_round(d_mod * 0.01 * 100, 3)}%",
        "过程": f"D = Σ(t·PV(CFt))/P = {_round(d_mac, 4)}；D* = D/(1+y) = {_round(d_mod, 4)}",
    }


# ---------- 外汇掉期 ----------
def exchange_swap(buy, sell, amount):
    """掉期点与掉期率。"""
    points = sell - buy
    rate = points / buy
    ann = rate * (360 / 30) if amount else rate  # 默认按1个月掉期年化
    return {
        "掉期点数": _round(points, 4),
        "掉期率(期)": _round(rate * 100, 4),
        "掉期率(年化,1月)": _round(ann * 100, 4),
        "过程": f"掉期点 = {sell} - {buy} = {_round(points, 4)}；掉期率 = {_round(points, 4)}/{buy} = {_round(rate * 100, 4)}%",
    }


def main():
    parser = argparse.ArgumentParser(
        description="货币银行学常用计算器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("money_multiplier", help="货币乘数")
    p.add_argument("--rr", type=float, required=True, help="法定准备金率")
    p.add_argument("--c", type=float, default=0.0, help="现金漏损率")
    p.add_argument("--e", type=float, default=0.0, help="超额准备金率")
    p.add_argument("--t", type=float, default=0.0, help="定期存款比率")
    p.add_argument("--rt", type=float, default=None, help="定期存款准备金率")

    p = sub.add_parser("deposit_expansion", help="存款派生")
    p.add_argument("--reserve", type=float, required=True, help="准备金率")
    p.add_argument("--base", type=float, required=True, help="基础货币/准备金")

    p = sub.add_parser("present_value", help="现值")
    p.add_argument("--fv", type=float, required=True)
    p.add_argument("--rate", type=float, required=True)
    p.add_argument("--years", type=float, required=True)

    p = sub.add_parser("compound", help="复利终值")
    p.add_argument("--pv", type=float, required=True)
    p.add_argument("--rate", type=float, required=True)
    p.add_argument("--years", type=float, required=True)
    p.add_argument("--freq", type=int, default=1, help="每年计息次数")

    p = sub.add_parser("fisher", help="费雪方程")
    p.add_argument("--nominal", type=float, required=True)
    p.add_argument("--inflation", type=float, required=True)

    p = sub.add_parser("duration", help="久期")
    p.add_argument("--face", type=float, default=1000)
    p.add_argument("--coupon", type=float, required=True)
    p.add_argument("--ytm", type=float, required=True)
    p.add_argument("--years", type=int, required=True)

    p = sub.add_parser("exchange_swap", help="外汇掉期")
    p.add_argument("--buy", type=float, required=True)
    p.add_argument("--sell", type=float, required=True)
    p.add_argument("--amount", type=float, default=0)

    args = parser.parse_args()
    kwargs = {k: v for k, v in vars(args).items() if k != "cmd"}

    try:
        if args.cmd == "money_multiplier":
            res = money_multiplier(**kwargs)
        elif args.cmd == "deposit_expansion":
            res = deposit_expansion(**kwargs)
        elif args.cmd == "present_value":
            res = present_value(**kwargs)
        elif args.cmd == "compound":
            res = compound(**kwargs)
        elif args.cmd == "fisher":
            res = fisher(**kwargs)
        elif args.cmd == "duration":
            res = duration(**kwargs)
        elif args.cmd == "exchange_swap":
            res = exchange_swap(**kwargs)
        else:
            parser.error("未知命令")
    except ValueError as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False, indent=2))
        sys.exit(1)

    print(json.dumps(res, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
