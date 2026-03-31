# Compiled AI Optimization Findings

This document contains the detailed fractional trades, constraints, and AI time-series forecasting metrics for every portfolio processed across all three (Conservative, Moderate, Aggressive) risk settings.

---

## Portfolio: High Risk Portfolio | Risk Profile: Conservative

**Total Initial Value:** $9,693.47 | **Target ETF Allocation:** 40.0%

### Initial vs Target Weights
- **SHOP.TO**: Current: 11.9% -> Target: 2.0%
- **CLS.TO**: Current: 8.0% -> Target: 40.0%
- **DSG.TO**: Current: 8.2% -> Target: 2.0%
- **KXS.TO**: Current: 11.6% -> Target: 2.0%
- **MDA.TO**: Current: 9.7% -> Target: 6.0%
- **OTEX.TO**: Current: 12.1% -> Target: 2.0%
- **DCBO.TO**: Current: 9.8% -> Target: 2.0%
- **LSPD.TO**: Current: 10.1% -> Target: 40.0%
- **NVDA.TO**: Current: 6.4% -> Target: 2.0%
- **AMD.TO**: Current: 12.2% -> Target: 2.0%

### Required Trades (5% Drift Threshold)
- **SELL** 5 shares of SHOP.TO (Account: TFSA, Expected Gain/Loss: $48.20)
- **BUY** 8 shares of CLS.TO (Account: TFSA, Expected Gain/Loss: $0.00)
- **SELL** 6 shares of DSG.TO (Account: RRSP, Expected Gain/Loss: $-82.50)
- **SELL** 6 shares of KXS.TO (Account: TFSA, Expected Gain/Loss: $23.52)
- **SELL** 31 shares of OTEX.TO (Account: RRSP, Expected Gain/Loss: $-1.86)
- **SELL** 31 shares of DCBO.TO (Account: RRSP, Expected Gain/Loss: $-36.58)
- **BUY** 234 shares of LSPD.TO (Account: TFSA, Expected Gain/Loss: $0.00)
- **SELL** 26 shares of AMD.TO (Account: TFSA, Expected Gain/Loss: $-1.56)

### 30-Day Value Forecast (AI Model)
- Exponential Smoothing Target: **$9,978** (2.94%)
- Auto-ARIMA Target: **$9,691** (-0.02%)
- *Best ARIMA Order Selected by AIC: (p=2, d=1, q=2)*

---

## Portfolio: High Risk Portfolio | Risk Profile: Moderate

**Total Initial Value:** $9,693.47 | **Target ETF Allocation:** 40.0%

### Initial vs Target Weights
- **SHOP.TO**: Current: 11.9% -> Target: 2.0%
- **CLS.TO**: Current: 8.0% -> Target: 40.0%
- **DSG.TO**: Current: 8.2% -> Target: 2.0%
- **KXS.TO**: Current: 11.6% -> Target: 2.0%
- **MDA.TO**: Current: 9.7% -> Target: 6.0%
- **OTEX.TO**: Current: 12.1% -> Target: 2.0%
- **DCBO.TO**: Current: 9.8% -> Target: 2.0%
- **LSPD.TO**: Current: 10.1% -> Target: 40.0%
- **NVDA.TO**: Current: 6.4% -> Target: 2.0%
- **AMD.TO**: Current: 12.2% -> Target: 2.0%

### Required Trades (5% Drift Threshold)
- **SELL** 5 shares of SHOP.TO (Account: TFSA, Expected Gain/Loss: $48.20)
- **BUY** 8 shares of CLS.TO (Account: TFSA, Expected Gain/Loss: $0.00)
- **SELL** 6 shares of DSG.TO (Account: RRSP, Expected Gain/Loss: $-82.50)
- **SELL** 6 shares of KXS.TO (Account: TFSA, Expected Gain/Loss: $23.52)
- **SELL** 31 shares of OTEX.TO (Account: RRSP, Expected Gain/Loss: $-1.86)
- **SELL** 31 shares of DCBO.TO (Account: RRSP, Expected Gain/Loss: $-36.58)
- **BUY** 234 shares of LSPD.TO (Account: TFSA, Expected Gain/Loss: $0.00)
- **SELL** 26 shares of AMD.TO (Account: TFSA, Expected Gain/Loss: $-1.56)

### 30-Day Value Forecast (AI Model)
- Exponential Smoothing Target: **$9,978** (2.94%)
- Auto-ARIMA Target: **$9,691** (-0.02%)
- *Best ARIMA Order Selected by AIC: (p=2, d=1, q=2)*

---

## Portfolio: High Risk Portfolio | Risk Profile: Aggressive

**Total Initial Value:** $9,693.47 | **Target ETF Allocation:** 20.0%

### Initial vs Target Weights
- **SHOP.TO**: Current: 11.9% -> Target: 2.0%
- **CLS.TO**: Current: 8.0% -> Target: 40.0%
- **DSG.TO**: Current: 8.2% -> Target: 2.0%
- **KXS.TO**: Current: 11.6% -> Target: 2.0%
- **MDA.TO**: Current: 9.7% -> Target: 26.0%
- **OTEX.TO**: Current: 12.1% -> Target: 2.0%
- **DCBO.TO**: Current: 9.8% -> Target: 2.0%
- **LSPD.TO**: Current: 10.1% -> Target: 20.0%
- **NVDA.TO**: Current: 6.4% -> Target: 2.0%
- **AMD.TO**: Current: 12.2% -> Target: 2.0%

### Required Trades (5% Drift Threshold)
- **SELL** 5 shares of SHOP.TO (Account: TFSA, Expected Gain/Loss: $48.20)
- **BUY** 8 shares of CLS.TO (Account: TFSA, Expected Gain/Loss: $0.00)
- **SELL** 6 shares of DSG.TO (Account: RRSP, Expected Gain/Loss: $-82.50)
- **SELL** 6 shares of KXS.TO (Account: TFSA, Expected Gain/Loss: $23.52)
- **BUY** 45 shares of MDA.TO (Account: TFSA, Expected Gain/Loss: $0.00)
- **SELL** 31 shares of OTEX.TO (Account: RRSP, Expected Gain/Loss: $-1.86)
- **SELL** 31 shares of DCBO.TO (Account: RRSP, Expected Gain/Loss: $-36.58)
- **BUY** 77 shares of LSPD.TO (Account: TFSA, Expected Gain/Loss: $0.00)
- **SELL** 26 shares of AMD.TO (Account: TFSA, Expected Gain/Loss: $-1.56)

### 30-Day Value Forecast (AI Model)
- Exponential Smoothing Target: **$10,021** (3.38%)
- Auto-ARIMA Target: **$9,646** (-0.49%)
- *Best ARIMA Order Selected by AIC: (p=2, d=1, q=2)*

---

## Portfolio: Low Risk Portfolio | Risk Profile: Conservative

**Total Initial Value:** $9,780.73 | **Target ETF Allocation:** 40.0%

### Initial vs Target Weights
- **ZLB.TO**: Current: 9.5% -> Target: 2.0%
- **XEI.TO**: Current: 10.4% -> Target: 2.0%
- **VDY.TO**: Current: 10.2% -> Target: 40.0%
- **ZWU.TO**: Current: 10.3% -> Target: 2.0%
- **XBB.TO**: Current: 10.0% -> Target: 2.0%
- **FTS.TO**: Current: 9.5% -> Target: 2.0%
- **TRP.TO**: Current: 9.7% -> Target: 36.5%
- **BMO.TO**: Current: 9.6% -> Target: 2.0%
- **MFC.TO**: Current: 10.7% -> Target: 2.0%
- **WN.TO**: Current: 10.0% -> Target: 9.5%

### Required Trades (5% Drift Threshold)
- **SELL** 12 shares of ZLB.TO (Account: TFSA, Expected Gain/Loss: $-13.68)
- **SELL** 22 shares of XEI.TO (Account: TFSA, Expected Gain/Loss: $26.40)
- **BUY** 43 shares of VDY.TO (Account: TFSA, Expected Gain/Loss: $0.00)
- **SELL** 66 shares of ZWU.TO (Account: RRSP, Expected Gain/Loss: $11.22)
- **SELL** 28 shares of XBB.TO (Account: RRSP, Expected Gain/Loss: $-5.88)
- **SELL** 9 shares of FTS.TO (Account: TFSA, Expected Gain/Loss: $-4.59)
- **BUY** 30 shares of TRP.TO (Account: RRSP, Expected Gain/Loss: $0.00)
- **SELL** 3 shares of BMO.TO (Account: RRSP, Expected Gain/Loss: $12.39)
- **SELL** 17 shares of MFC.TO (Account: TFSA, Expected Gain/Loss: $58.82)

### 30-Day Value Forecast (AI Model)
- Exponential Smoothing Target: **$10,024** (2.49%)
- Auto-ARIMA Target: **$10,023** (2.47%)
- *Best ARIMA Order Selected by AIC: (p=2, d=2, q=3)*

---

## Portfolio: Low Risk Portfolio | Risk Profile: Moderate

**Total Initial Value:** $9,780.73 | **Target ETF Allocation:** 40.0%

### Initial vs Target Weights
- **ZLB.TO**: Current: 9.5% -> Target: 2.0%
- **XEI.TO**: Current: 10.4% -> Target: 2.0%
- **VDY.TO**: Current: 10.2% -> Target: 40.0%
- **ZWU.TO**: Current: 10.3% -> Target: 2.0%
- **XBB.TO**: Current: 10.0% -> Target: 2.0%
- **FTS.TO**: Current: 9.5% -> Target: 2.0%
- **TRP.TO**: Current: 9.7% -> Target: 40.0%
- **BMO.TO**: Current: 9.6% -> Target: 2.0%
- **MFC.TO**: Current: 10.7% -> Target: 2.0%
- **WN.TO**: Current: 10.0% -> Target: 6.0%

### Required Trades (5% Drift Threshold)
- **SELL** 12 shares of ZLB.TO (Account: TFSA, Expected Gain/Loss: $-13.68)
- **SELL** 22 shares of XEI.TO (Account: TFSA, Expected Gain/Loss: $26.40)
- **BUY** 43 shares of VDY.TO (Account: TFSA, Expected Gain/Loss: $0.00)
- **SELL** 66 shares of ZWU.TO (Account: RRSP, Expected Gain/Loss: $11.22)
- **SELL** 28 shares of XBB.TO (Account: RRSP, Expected Gain/Loss: $-5.88)
- **SELL** 9 shares of FTS.TO (Account: TFSA, Expected Gain/Loss: $-4.59)
- **BUY** 34 shares of TRP.TO (Account: RRSP, Expected Gain/Loss: $0.00)
- **SELL** 3 shares of BMO.TO (Account: RRSP, Expected Gain/Loss: $12.39)
- **SELL** 17 shares of MFC.TO (Account: TFSA, Expected Gain/Loss: $58.82)

### 30-Day Value Forecast (AI Model)
- Exponential Smoothing Target: **$10,023** (2.48%)
- Auto-ARIMA Target: **$10,030** (2.55%)
- *Best ARIMA Order Selected by AIC: (p=0, d=2, q=1)*

---

## Portfolio: Low Risk Portfolio | Risk Profile: Aggressive

**Total Initial Value:** $9,780.73 | **Target ETF Allocation:** 20.0%

### Initial vs Target Weights
- **ZLB.TO**: Current: 9.5% -> Target: 2.0%
- **XEI.TO**: Current: 10.4% -> Target: 2.0%
- **VDY.TO**: Current: 10.2% -> Target: 20.0%
- **ZWU.TO**: Current: 10.3% -> Target: 2.0%
- **XBB.TO**: Current: 10.0% -> Target: 2.0%
- **FTS.TO**: Current: 9.5% -> Target: 2.0%
- **TRP.TO**: Current: 9.7% -> Target: 40.0%
- **BMO.TO**: Current: 9.6% -> Target: 2.0%
- **MFC.TO**: Current: 10.7% -> Target: 2.0%
- **WN.TO**: Current: 10.0% -> Target: 26.0%

### Required Trades (5% Drift Threshold)
- **SELL** 12 shares of ZLB.TO (Account: TFSA, Expected Gain/Loss: $-13.68)
- **SELL** 22 shares of XEI.TO (Account: TFSA, Expected Gain/Loss: $26.40)
- **BUY** 14 shares of VDY.TO (Account: TFSA, Expected Gain/Loss: $0.00)
- **SELL** 66 shares of ZWU.TO (Account: RRSP, Expected Gain/Loss: $11.22)
- **SELL** 28 shares of XBB.TO (Account: RRSP, Expected Gain/Loss: $-5.88)
- **SELL** 9 shares of FTS.TO (Account: TFSA, Expected Gain/Loss: $-4.59)
- **BUY** 34 shares of TRP.TO (Account: RRSP, Expected Gain/Loss: $0.00)
- **SELL** 3 shares of BMO.TO (Account: RRSP, Expected Gain/Loss: $12.39)
- **SELL** 17 shares of MFC.TO (Account: TFSA, Expected Gain/Loss: $58.82)
- **BUY** 15 shares of WN.TO (Account: TFSA, Expected Gain/Loss: $0.00)

### 30-Day Value Forecast (AI Model)
- Exponential Smoothing Target: **$10,028** (2.53%)
- Auto-ARIMA Target: **$10,031** (2.56%)
- *Best ARIMA Order Selected by AIC: (p=0, d=2, q=1)*

---

## Portfolio: Meme stock portfolio | Risk Profile: Conservative

**Total Initial Value:** $10,479.98 | **Target ETF Allocation:** 40.0%

### Initial vs Target Weights
- **BB.TO**: Current: 4.4% -> Target: 2.0%
- **WEED.TO**: Current: 29.8% -> Target: 2.0%
- **ACB.TO**: Current: 12.5% -> Target: 2.0%
- **LSPD.TO**: Current: 8.9% -> Target: 40.0%
- **OGI.TO**: Current: 1.6% -> Target: 2.0%
- **TAL.TO**: Current: 1.6% -> Target: 2.0%
- **GRN.TO**: Current: 0.6% -> Target: 26.3%
- **DIAM.TO**: Current: 18.7% -> Target: 13.4%
- **TSND.TO**: Current: 9.6% -> Target: 2.0%
- **LAR.TO**: Current: 12.3% -> Target: 8.3%

### Required Trades (5% Drift Threshold)
- **SELL** 2222 shares of WEED.TO (Account: TFSA, Expected Gain/Loss: $177.76)
- **SELL** 240 shares of ACB.TO (Account: TFSA, Expected Gain/Loss: $24.00)
- **BUY** 263 shares of LSPD.TO (Account: TFSA, Expected Gain/Loss: $0.00)
- **BUY** 11448 shares of GRN.TO (Account: RRSP, Expected Gain/Loss: $0.00)
- **SELL** 18371 shares of DIAM.TO (Account: RRSP, Expected Gain/Loss: $-0.00)
- **SELL** 908 shares of TSND.TO (Account: RRSP, Expected Gain/Loss: $90.80)

### 30-Day Value Forecast (AI Model)
- Exponential Smoothing Target: **$10,722** (2.31%)
- Auto-ARIMA Target: **$10,742** (2.50%)
- *Best ARIMA Order Selected by AIC: (p=2, d=2, q=3)*

---

## Portfolio: Meme stock portfolio | Risk Profile: Moderate

**Total Initial Value:** $10,479.98 | **Target ETF Allocation:** 40.0%

### Initial vs Target Weights
- **BB.TO**: Current: 4.4% -> Target: 2.0%
- **WEED.TO**: Current: 29.8% -> Target: 2.0%
- **ACB.TO**: Current: 12.5% -> Target: 2.0%
- **LSPD.TO**: Current: 8.9% -> Target: 40.0%
- **OGI.TO**: Current: 1.6% -> Target: 2.0%
- **TAL.TO**: Current: 1.6% -> Target: 2.0%
- **GRN.TO**: Current: 0.6% -> Target: 27.2%
- **DIAM.TO**: Current: 18.7% -> Target: 13.4%
- **TSND.TO**: Current: 9.6% -> Target: 2.0%
- **LAR.TO**: Current: 12.3% -> Target: 7.4%

### Required Trades (5% Drift Threshold)
- **SELL** 2222 shares of WEED.TO (Account: TFSA, Expected Gain/Loss: $177.76)
- **SELL** 240 shares of ACB.TO (Account: TFSA, Expected Gain/Loss: $24.00)
- **BUY** 263 shares of LSPD.TO (Account: TFSA, Expected Gain/Loss: $0.00)
- **BUY** 11878 shares of GRN.TO (Account: RRSP, Expected Gain/Loss: $0.00)
- **SELL** 18479 shares of DIAM.TO (Account: RRSP, Expected Gain/Loss: $-0.00)
- **SELL** 908 shares of TSND.TO (Account: RRSP, Expected Gain/Loss: $90.80)

### 30-Day Value Forecast (AI Model)
- Exponential Smoothing Target: **$10,726** (2.35%)
- Auto-ARIMA Target: **$10,743** (2.51%)
- *Best ARIMA Order Selected by AIC: (p=2, d=2, q=3)*

---

## Portfolio: Meme stock portfolio | Risk Profile: Aggressive

**Total Initial Value:** $10,479.98 | **Target ETF Allocation:** 20.0%

### Initial vs Target Weights
- **BB.TO**: Current: 4.4% -> Target: 9.1%
- **WEED.TO**: Current: 29.8% -> Target: 2.0%
- **ACB.TO**: Current: 12.5% -> Target: 2.0%
- **LSPD.TO**: Current: 8.9% -> Target: 20.0%
- **OGI.TO**: Current: 1.6% -> Target: 2.0%
- **TAL.TO**: Current: 1.6% -> Target: 2.0%
- **GRN.TO**: Current: 0.6% -> Target: 31.0%
- **DIAM.TO**: Current: 18.7% -> Target: 14.4%
- **TSND.TO**: Current: 9.6% -> Target: 2.4%
- **LAR.TO**: Current: 12.3% -> Target: 15.2%

### Required Trades (5% Drift Threshold)
- **SELL** 2222 shares of WEED.TO (Account: TFSA, Expected Gain/Loss: $177.76)
- **SELL** 240 shares of ACB.TO (Account: TFSA, Expected Gain/Loss: $24.00)
- **BUY** 94 shares of LSPD.TO (Account: TFSA, Expected Gain/Loss: $0.00)
- **BUY** 13560 shares of GRN.TO (Account: RRSP, Expected Gain/Loss: $0.00)
- **SELL** 864 shares of TSND.TO (Account: RRSP, Expected Gain/Loss: $86.40)

### 30-Day Value Forecast (AI Model)
- Exponential Smoothing Target: **$10,796** (3.02%)
- Auto-ARIMA Target: **$10,833** (3.37%)
- *Best ARIMA Order Selected by AIC: (p=0, d=2, q=1)*

---

## Portfolio: portfolio | Risk Profile: Conservative

**Total Initial Value:** $53,674.79 | **Target ETF Allocation:** 80.0%

### Initial vs Target Weights
- **ZSP.TO**: Current: 28.3% -> Target: 20.7%
- **ZNQ.TO**: Current: 7.9% -> Target: 25.6%
- **TD.TO**: Current: 7.5% -> Target: 2.0%
- **RY.TO**: Current: 6.9% -> Target: 2.0%
- **BNS.TO**: Current: 4.7% -> Target: 2.0%
- **VFV.TO**: Current: 12.6% -> Target: 2.0%
- **XIC.TO**: Current: 8.6% -> Target: 2.0%
- **ENB.TO**: Current: 7.7% -> Target: 2.0%
- **BCE.TO**: Current: 2.0% -> Target: 2.0%
- **CNR.TO**: Current: 3.4% -> Target: 2.0%
- **XEQT.TO**: Current: 4.6% -> Target: 33.7%
- **XIU.TO**: Current: 4.2% -> Target: 2.0%
- **QQC.TO**: Current: 1.7% -> Target: 2.0%

### Required Trades (5% Drift Threshold)
- **SELL** 41 shares of ZSP.TO (Account: TFSA, Expected Gain/Loss: $438.70)
- **BUY** 89 shares of ZNQ.TO (Account: TFSA, Expected Gain/Loss: $0.00)
- **SELL** 22 shares of TD.TO (Account: TFSA, Expected Gain/Loss: $1019.04)
- **SELL** 35 shares of VFV.TO (Account: RRSP, Expected Gain/Loss: $1671.60)
- **SELL** 67 shares of XIC.TO (Account: RRSP, Expected Gain/Loss: $1191.26)
- **SELL** 40 shares of ENB.TO (Account: RRSP, Expected Gain/Loss: $1088.40)
- **BUY** 392 shares of XEQT.TO (Account: FHSA, Expected Gain/Loss: $0.00)

### 30-Day Value Forecast (AI Model)
- Exponential Smoothing Target: **$54,450** (1.44%)
- Auto-ARIMA Target: **$53,675** (0.00%)
- *Best ARIMA Order Selected by AIC: (p=0, d=1, q=0)*

---

## Portfolio: portfolio | Risk Profile: Moderate

**Total Initial Value:** $53,674.79 | **Target ETF Allocation:** 60.0%

### Initial vs Target Weights
- **ZSP.TO**: Current: 28.3% -> Target: 2.0%
- **ZNQ.TO**: Current: 7.9% -> Target: 18.0%
- **TD.TO**: Current: 7.5% -> Target: 2.4%
- **RY.TO**: Current: 6.9% -> Target: 6.7%
- **BNS.TO**: Current: 4.7% -> Target: 2.0%
- **VFV.TO**: Current: 12.6% -> Target: 2.0%
- **XIC.TO**: Current: 8.6% -> Target: 2.0%
- **ENB.TO**: Current: 7.7% -> Target: 16.9%
- **BCE.TO**: Current: 2.0% -> Target: 2.0%
- **CNR.TO**: Current: 3.4% -> Target: 2.0%
- **XEQT.TO**: Current: 4.6% -> Target: 40.0%
- **XIU.TO**: Current: 4.2% -> Target: 2.0%
- **QQC.TO**: Current: 1.7% -> Target: 2.0%

### Required Trades (5% Drift Threshold)
- **SELL** 142 shares of ZSP.TO (Account: TFSA, Expected Gain/Loss: $1519.40)
- **BUY** 51 shares of ZNQ.TO (Account: TFSA, Expected Gain/Loss: $0.00)
- **SELL** 21 shares of TD.TO (Account: TFSA, Expected Gain/Loss: $972.72)
- **SELL** 35 shares of VFV.TO (Account: RRSP, Expected Gain/Loss: $1671.60)
- **SELL** 67 shares of XIC.TO (Account: RRSP, Expected Gain/Loss: $1191.26)
- **BUY** 66 shares of ENB.TO (Account: RRSP, Expected Gain/Loss: $0.00)
- **BUY** 476 shares of XEQT.TO (Account: FHSA, Expected Gain/Loss: $0.00)

### 30-Day Value Forecast (AI Model)
- Exponential Smoothing Target: **$54,609** (1.74%)
- Auto-ARIMA Target: **$53,637** (-0.07%)
- *Best ARIMA Order Selected by AIC: (p=2, d=1, q=2)*

---

## Portfolio: portfolio | Risk Profile: Aggressive

**Total Initial Value:** $53,674.79 | **Target ETF Allocation:** 20.0%

### Initial vs Target Weights
- **ZSP.TO**: Current: 28.3% -> Target: 2.0%
- **ZNQ.TO**: Current: 7.9% -> Target: 2.0%
- **TD.TO**: Current: 7.5% -> Target: 12.6%
- **RY.TO**: Current: 6.9% -> Target: 28.4%
- **BNS.TO**: Current: 4.7% -> Target: 2.0%
- **VFV.TO**: Current: 12.6% -> Target: 2.0%
- **XIC.TO**: Current: 8.6% -> Target: 2.0%
- **ENB.TO**: Current: 7.7% -> Target: 25.0%
- **BCE.TO**: Current: 2.0% -> Target: 2.0%
- **CNR.TO**: Current: 3.4% -> Target: 2.0%
- **XEQT.TO**: Current: 4.6% -> Target: 16.0%
- **XIU.TO**: Current: 4.2% -> Target: 2.0%
- **QQC.TO**: Current: 1.7% -> Target: 2.0%

### Required Trades (5% Drift Threshold)
- **SELL** 142 shares of ZSP.TO (Account: TFSA, Expected Gain/Loss: $1519.40)
- **SELL** 29 shares of ZNQ.TO (Account: TFSA, Expected Gain/Loss: $294.64)
- **BUY** 20 shares of TD.TO (Account: TFSA, Expected Gain/Loss: $0.00)
- **BUY** 51 shares of RY.TO (Account: TFSA, Expected Gain/Loss: $0.00)
- **SELL** 35 shares of VFV.TO (Account: RRSP, Expected Gain/Loss: $1671.60)
- **SELL** 67 shares of XIC.TO (Account: RRSP, Expected Gain/Loss: $1191.26)
- **BUY** 124 shares of ENB.TO (Account: RRSP, Expected Gain/Loss: $0.00)
- **BUY** 153 shares of XEQT.TO (Account: FHSA, Expected Gain/Loss: $0.00)

### 30-Day Value Forecast (AI Model)
- Exponential Smoothing Target: **$54,849** (2.19%)
- Auto-ARIMA Target: **$53,675** (0.00%)
- *Best ARIMA Order Selected by AIC: (p=0, d=1, q=0)*

---

