# 货币银行学核心公式速查

所有公式均给出符号含义、适用条件与计算脚本命令。**计算题必须用 `scripts/calc.py` 验证。**

---

## 1. 货币乘数（M2 型）

$$m = \frac{1 + c + t}{c + rr + e + t \cdot rr_t}$$

| 符号 | 含义 |
|---|---|
| $c$ | 现金漏损率（现金/活期存款） |
| $rr$ | 活期存款法定准备金率 |
| $rr_t$ | 定期存款法定准备金率 |
| $e$ | 超额准备金率 |
| $t$ | 定期存款/活期存款 |

**简化版**（忽略定期存款）：$m = \dfrac{1}{rr + e + c}$

```bash
python3 scripts/calc.py money_multiplier --rr 0.1 --c 0.05 --e 0.02 --t 0.3 --rt 0.05
```

> 适用条件：广义货币 M2 口径。若教材使用 M1 口径，去掉 $t$ 项。

---

## 2. 货币供应量

$$M_s = m \times B$$

$B$ = 基础货币 = 流通中现金 $C$ + 准备金存款 $R$。

---

## 3. 简单存款派生模型

$$D = \frac{R}{rr}, \quad \text{派生倍数} = \frac{1}{rr}$$

```bash
python3 scripts/calc.py deposit_expansion --reserve 0.2 --base 1000
```

> 适用条件：无现金漏损、无超额准备金的理想情形；为简化乘数（理论上限）。

---

## 4. 费雪方程式（交易方程式）

$$M \cdot V = P \cdot T$$

$M$ 货币量、$V$ 流通速度、$P$ 物价水平、$T$ 交易量。

**费雪效应**（名义与实际利率）：

$$(1+i) = (1+r)(1+\pi) \Rightarrow r \approx i - \pi$$

```bash
python3 scripts/calc.py fisher --nominal 0.06 --inflation 0.02
```

> 精确式与近似式的误差随通胀率上升而扩大；高通胀时应使用精确式。

---

## 5. 现值与终值

$$PV = \frac{FV}{(1+r)^n}, \qquad FV = PV(1+r)^n$$

**复利（每年 m 次计息）**：$FV = PV\left(1+\dfrac{r}{m}\right)^{mn}$

**有效年利率**：$EAR = \left(1+\dfrac{r}{m}\right)^m - 1$

```bash
python3 scripts/calc.py present_value --fv 1000 --rate 0.05 --years 3
python3 scripts/calc.py compound --pv 1000 --rate 0.05 --years 3 --freq 12
```

---

## 6. 年金现值

$$PV_{annuity} = A \cdot \frac{1 - (1+r)^{-n}}{r}$$

---

## 7. 债券价格与到期收益率

$$P = \sum_{t=1}^{n} \frac{C}{(1+y)^t} + \frac{F}{(1+y)^n}$$

$C$ 年利息、$F$ 面值、$y$ 到期收益率。
债券价格与到期收益率**反向变动**。

---

## 8. 久期

**麦考利久期**：

$$D_{mac} = \frac{\sum_{t=1}^{n} t \cdot \dfrac{CF_t}{(1+y)^t}}{P}$$

**修正久期**：$D^* = \dfrac{D_{mac}}{1+y}$

**价格变动近似**：$\dfrac{\Delta P}{P} \approx -D^* \cdot \Delta y$

```bash
python3 scripts/calc.py duration --face 1000 --coupon 0.05 --ytm 0.06 --years 3
```

> 久期越长，利率风险越大。零息债的麦考利久期 = 到期期限。

---

## 9. 外汇与汇率

**直接标价法**：1 单位外币 = 若干本币。
**间接标价法**：1 单位本币 = 若干外币。

**掉期率**：$\dfrac{\text{掉期点}}{\text{即期汇率}}$

```bash
python3 scripts/calc.py exchange_swap --buy 6.45 --sell 6.50 --amount 1000000
```

**购买力平价**（PPP）：$e = \dfrac{P_d}{P_f}$（绝对形式）

**利率平价**（IRP）：$\dfrac{F-S}{S} = i_d - i_f$

---

## 10. 菲利普斯曲线

$$\pi = \pi^e - \beta(u - u_n) + \varepsilon$$

$u_n$ 自然失业率。长期中预期被完全调整，$\pi = \pi^e$，曲线垂直。

---

## 11. 商业银行流动性指标

- **流动性覆盖率 LCR** = 优质流动性资产 / 未来30日净现金流出 ≥ 100%
- **净稳定资金比例 NSFR** = 可用稳定资金 / 所需稳定资金 ≥ 100%

---

## 12. 通胀率计算

$$\pi_t = \frac{P_t - P_{t-1}}{P_{t-1}} \times 100\%$$

**实际利率**（事后）$r = i - \pi$；**事前**用预期通胀。

---

## 计算题通用解题步骤

1. **整理已知**：把题目条件逐条列出，统一量纲（百分数转小数）。
2. **选公式**：写出公式并**说明适用条件**（这一步最容易丢分）。
3. **代入计算**：用脚本计算，保留 4 位小数。
4. **解释含义**：说明结果的现实意义（如"货币乘数为 7.3，意味着基础货币每增加 1 元，货币供应量增加 7.3 元"）。
5. **检查量纲**：率对率、金额对金额。
