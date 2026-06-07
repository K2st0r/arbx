#!/usr/bin/env python3
"""
arbx — 跨交易所套利扫描器
比较 Binance / Huobi 价格，发现套利机会。
依赖: 系统代理已开启
"""
import subprocess, json, sys, os, time
from datetime import datetime
sys.stdout.reconfigure(encoding="utf-8")

WALLET = "0xAfe9B67B1DF618FAeD32dC71E3458cf549f26697"
COINS = ["BTCUSDT","ETHUSDT","BNBUSDT","SOLUSDT","XRPUSDT","DOGEUSDT","ADAUSDT","AVAXUSDT"]

def ps(cmd):
    """Run PowerShell and return parsed JSON"""
    full = f'$r=Invoke-WebRequest -Uri "{cmd}" -TimeoutSec 10 -UseBasicParsing; $r.Content'
    r = subprocess.run(["powershell","-Command",full], capture_output=True, text=True, timeout=15)
    return json.loads(r.stdout)

def get_binance():
    try:
        r = ps("https://api.binance.com/api/v3/ticker/price")
        return {i["symbol"]: float(i["price"]) for i in r if i["symbol"] in COINS}
    except: return {}

def get_huobi():
    try:
        r = ps("https://api.huobi.pro/market/tickers")
        result = {}
        for t in r.get("data", []):
            sym = t["symbol"].upper()  # huobi returns "btcusdt"
            if sym in COINS:
                result[sym] = t.get("close", 0)
        return result
    except: return {}

now = datetime.now().strftime("%Y-%m-%d %H:%M")
b = get_binance()
h = get_huobi()

print(f"\n  ARBX v1.0 — {now}")
print(f"  {'='*50}")

if not b:
    print("  ❌ 无法获取Binance数据")
    sys.exit(1)

print(f"\n  {'币种':<10} {'Binance':>12} {'Huobi':>12} {'差价%':>8}")
print(f"  {'-'*45}")

opps = []
for c in COINS:
    bp = b.get(c)
    hp = h.get(c)
    if bp and hp:
        d = (hp - bp) / bp * 100
        m = "⚠️" if abs(d) > 0.3 else " "
        print(f"  {m} {c:<8} {bp:>10.2f} {hp:>10.2f} {d:>+7.2f}%")
        if abs(d) > 0.3:
            direction = "←买Binance卖Huobi" if d > 0 else "→买Huobi卖Binance"
            opps.append(f"  💰 {c}: {abs(d):.2f}% {direction}")
    elif bp:
        print(f"    {c:<8} {bp:>10.2f} {'N/A':>12}")

if opps:
    print(f"\n  🚀 套利机会 ({len(opps)})")
    for o in opps: print(o)
else:
    print(f"\n  📊 差价 <0.3%，暂无套利机会")

print(f"\n  {'='*50}")
print(f"  Donate: {WALLET}")
print()

# 保存结果
out = {"time": now, "binance": b, "huobi": h, "opportunities": opps}
with open(os.path.join(os.path.dirname(__file__), "arbx_log.json"), "w") as f:
    json.dump(out, f)
