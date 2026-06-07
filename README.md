<div align="center">

# arbx

**跨交易所套利扫描器 | Crypto Arbitrage Scanner**

[![Python](https://img.shields.io/badge/Python-3.8+-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.0.0-purple)](https://github.com/K2st0r/arbx)
[![Donate](https://img.shields.io/badge/Donate-USDT-red)](#donate)

</div>

### 🎯 扫描 Binance/Huobi 价格差，发现套利机会

```bash
python arbx.py
```

### 📊 输出示例

```
ARBX v1.0 — 2026-06-07 18:30
==================================================

 币种        Binance        Huobi      差价%
---------------------------------------------
 BTCUSDT    62528.00   62529.49   +0.00%
 ETHUSDT     1634.16    1635.69   +0.09%

📊 差价 <0.3%，暂无套利机会
```

### 🚀 用法

```bash
# 单次扫描
python arbx.py

# 定时扫描（每30分钟）
python -m time python arbx.py  # Linux/Mac
# Windows: 用任务计划程序
```

### 📦 输出

- 终端实时输出
- `arbx_log.json` — 结构化数据
- 机会发现时自动高亮

### 🔧 原理

| 交易所 | 数据源 | 延迟 |
|--------|--------|------|
| Binance | REST API | <100ms |
| Huobi | REST API | <200ms |

差价 >0.5% 时标记为套利机会，显示买卖方向。

## 💎 Donate

**USDT (ERC20):** `0xAfe9B67B1DF618FAeD32dC71E3458cf549f26697`

---

*MIT License · Made with ❤️ by [K2st0r](https://github.com/K2st0r)*
