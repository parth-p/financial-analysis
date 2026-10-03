#!/usr/bin/env python3
"""
financial_calculator.py — Deterministic Financial Analysis Engine
Implements the quantitative and forensic framework of src/company/listed/checklists/5-financials.md.

Accepts structured financial time-series data via JSON on stdin (or file argument).
Outputs verified GitHub-flavored Markdown tables, ratio decompositions, and forensic screens.

Zero external dependencies (pure Python standard library).
Execute using project virtualenv: .venv/bin/python src/company/listed/scripts/financial_calculator.py
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import sys
from typing import Any, Dict, List, Optional


def safe_div(num: Optional[float], den: Optional[float], default: float = 0.0) -> float:
    """Safe division handling zero and None values."""
    if num is None or den is None:
        return default
    try:
        return num / den if den != 0 else default
    except (ZeroDivisionError, OverflowError):
        return default


def cagr(start: Optional[float], end: Optional[float], periods: int) -> Optional[float]:
    """Compound Annual Growth Rate calculation in percentage."""
    if start is None or end is None or periods <= 0 or start <= 0 or end <= 0:
        return None
    try:
        return (((end / start) ** (1.0 / periods)) - 1.0) * 100.0
    except (ValueError, ZeroDivisionError, OverflowError):
        return None


def pct_change(prev: Optional[float], curr: Optional[float]) -> Optional[float]:
    """Percentage change calculation."""
    if prev is None or curr is None or prev == 0:
        return None
    return ((curr - prev) / abs(prev)) * 100.0


def fmt_num(val: Optional[float], decimals: int = 1, prefix: str = "", suffix: str = "") -> str:
    """Format float numbers cleanly."""
    if val is None or math.isnan(val):
        return "-"
    if decimals == 0:
        return f"{prefix}{val:,.0f}{suffix}"
    return f"{prefix}{val:,.{decimals}f}{suffix}"


def fmt_pct(val: Optional[float], decimals: int = 2) -> str:
    """Format percentages."""
    if val is None or math.isnan(val):
        return "-"
    return f"{val:.{decimals}f}%"


class FinancialModel:
    """Processes financial series and computes all metrics from 5-financials.md."""

    def __init__(self, data: Dict[str, Any]):
        self.data = data
        self.years: List[str] = data.get("years", [])
        self.n: int = len(self.years)
        if self.n == 0:
            raise ValueError("Input data must contain a non-empty 'years' list.")

        # P&L series
        self.revenue = self._get_series("revenue")
        self.cogs = self._get_series("cogs", fallback_key="material_costs")
        self.ebitda = self._get_series("ebitda", fallback_key="operating_profit")
        self.other_income = self._get_series("other_income")
        self.depreciation = self._get_series("depreciation")
        self.interest = self._get_series("interest", fallback_key="finance_costs")
        self.pbt = self._get_series("pbt")
        self.tax = self._get_series("tax")
        self.pat = self._get_series("pat", fallback_key="net_income")
        self.exceptional = self._get_series("exceptional_items")

        # Balance Sheet series
        self.net_worth = self._get_series("net_worth", fallback_key="equity")
        self.total_debt = self._get_series("total_debt", fallback_key="borrowings")
        self.total_assets = self._get_series("total_assets")
        self.fixed_assets = self._get_series("fixed_assets", fallback_key="net_block")
        self.inventories = self._get_series("inventories")
        self.receivables = self._get_series("receivables")
        self.payables = self._get_series("payables", fallback_key="trade_payables")
        self.cash = self._get_series("cash", fallback_key="cash_and_equivalents")
        self.current_assets = self._get_series("current_assets")
        self.current_liabilities = self._get_series("current_liabilities")
        self.goodwill = self._get_series("goodwill")
        self.intangibles = self._get_series("intangibles")
        self.reserves = self._get_series("reserves", fallback_key="retained_earnings")
        self.sga = self._get_series("sga", fallback_key="other_expenses")

        # Cash Flow series
        self.cfo = self._get_series("cfo", fallback_key="operating_cash_flow")
        self.capex = self._get_series("capex")

        # Qualitative / Overrides
        self.wacc: float = float(data.get("wacc", 13.0))
        self.default_tax_rate: float = float(data.get("tax_rate", 0.25))
        self.volume = self._get_series("volume")
        self.related_party_revenue = self._get_series("related_party_revenue")
        self.contingent_liabilities = data.get("contingent_liabilities")
        self.promoter_pledge_pct = data.get("promoter_pledge_pct")

        # Precompute derived rows
        self._precompute()

    def _get_series(self, key: str, fallback_key: Optional[str] = None) -> List[Optional[float]]:
        vals = self.data.get(key)
        if vals is None and fallback_key:
            vals = self.data.get(fallback_key)
        if vals is None:
            return [None] * self.n
        # Pad or truncate to self.n
        cleaned: List[Optional[float]] = []
        for i in range(self.n):
            if i < len(vals):
                v = vals[i]
                if v is None or v == "" or v == "-":
                    cleaned.append(None)
                else:
                    try:
                        cleaned.append(float(v))
                    except (ValueError, TypeError):
                        cleaned.append(None)
            else:
                cleaned.append(None)
        return cleaned

    def _precompute(self):
        # Gross profit
        self.gross_profit: List[Optional[float]] = []
        for i in range(self.n):
            rev, cg = self.revenue[i], self.cogs[i]
            if rev is not None and cg is not None:
                self.gross_profit.append(rev - cg)
            else:
                self.gross_profit.append(None)

        # Total EBIT (PBT + Interest) for Solvency / Interest Coverage & Altman Z
        self.total_ebit: List[Optional[float]] = []
        for i in range(self.n):
            pbt_val, int_val = self.pbt[i], self.interest[i]
            if pbt_val is not None:
                self.total_ebit.append(pbt_val + (int_val or 0.0))
            elif self.ebitda[i] is not None and self.depreciation[i] is not None:
                self.total_ebit.append(self.ebitda[i] - self.depreciation[i] + (self.other_income[i] or 0.0))
            else:
                self.total_ebit.append(None)

        # Operating EBIT (excludes non-operating Other Income) for Core NOPAT / ROIC
        self.operating_ebit: List[Optional[float]] = []
        for i in range(self.n):
            op, dep = self.ebitda[i], self.depreciation[i]
            pbt_val, int_val, o_inc = self.pbt[i], self.interest[i], self.other_income[i]
            if pbt_val is not None:
                self.operating_ebit.append(pbt_val + (int_val or 0.0) - (o_inc or 0.0))
            elif op is not None and dep is not None:
                self.operating_ebit.append(op - dep)
            elif op is not None:
                self.operating_ebit.append(op)
            else:
                self.operating_ebit.append(None)
        self.ebit = self.operating_ebit

        # Tax rate per year
        self.tax_rates: List[float] = []
        for i in range(self.n):
            p, t = self.pbt[i], self.tax[i]
            if p and t and p > 0 and t >= 0:
                tr = t / p
                self.tax_rates.append(min(max(tr, 0.0), 0.50))
            else:
                self.tax_rates.append(self.default_tax_rate)

        # NOPAT
        self.nopat: List[Optional[float]] = []
        for i in range(self.n):
            eb = self.ebit[i]
            if eb is not None:
                self.nopat.append(eb * (1.0 - self.tax_rates[i]))
            else:
                self.nopat.append(None)

        # Free Cash Flow
        self.fcf: List[Optional[float]] = []
        for i in range(self.n):
            cf, cx = self.cfo[i], self.capex[i]
            if cf is not None:
                self.fcf.append(cf - (cx or 0.0))
            else:
                self.fcf.append(None)

        # Capital Employed & Invested Capital
        self.capital_employed: List[Optional[float]] = []
        self.invested_capital: List[Optional[float]] = []
        for i in range(self.n):
            nw, debt, cs = self.net_worth[i], self.total_debt[i], self.cash[i]
            if nw is not None:
                ce = nw + (debt or 0.0)
                self.capital_employed.append(ce)
                self.invested_capital.append(ce - (cs or 0.0))
            else:
                self.capital_employed.append(None)
                self.invested_capital.append(None)

    # =========================================================================
    # Section 1: System, Trends & Common-Size
    # =========================================================================
    def build_system_and_trends(self) -> str:
        lines = []
        lines.append("## 1. Read the Three Statements as One System, Across Time\n")
        lines.append("### Point 1.1 & 1.2: Multi-Year Trend Analysis & Compound Growth\n")

        headers = ["Metric / Line Item"] + self.years + ["3-Yr CAGR", "Full CAGR"]
        table_rows = []

        metrics_to_track = [
            ("Revenue from Operations", self.revenue),
            ("EBITDA / Operating Profit", self.ebitda),
            ("Profit Before Tax (PBT)", self.pbt),
            ("Profit After Tax (PAT)", self.pat),
            ("Operating Cash Flow (CFO)", self.cfo),
            ("Free Cash Flow (FCF)", self.fcf),
            ("Tangible Net Worth", self.net_worth),
            ("Total Assets", self.total_assets),
            ("Gross Borrowings (Debt)", self.total_debt),
        ]

        for label, series in metrics_to_track:
            if not any(v is not None for v in series):
                continue
            row = [label]
            for v in series:
                row.append(fmt_num(v, decimals=1))

            # 3-Yr CAGR
            c3 = None
            if self.n >= 4 and series[-4] is not None and series[-1] is not None:
                c3 = cagr(series[-4], series[-1], 3)
            row.append(fmt_pct(c3) if c3 is not None else "-")

            # Full CAGR
            first_idx = next((i for i, x in enumerate(series) if x is not None), None)
            c_full = None
            if first_idx is not None and first_idx < self.n - 1 and series[-1] is not None:
                c_full = cagr(series[first_idx], series[-1], (self.n - 1 - first_idx))
            row.append(fmt_pct(c_full) if c_full is not None else "-")
            table_rows.append(row)

        lines.append(self._render_table(headers, table_rows))
        lines.append("")

        # Common-Size Income Statement
        lines.append("### Point 1.3: Common-Size Income Statement (% of Revenue)\n")
        cs_is_headers = ["Income Statement Line"] + self.years
        cs_is_rows = []
        is_lines = [
            ("Revenue from Operations", self.revenue, True),
            ("Cost of Materials / COGS", self.cogs, False),
            ("Operating Profit (EBITDA)", self.ebitda, False),
            ("Other Income", self.other_income, False),
            ("Depreciation & Amortization", self.depreciation, False),
            ("Finance Costs / Interest", self.interest, False),
            ("Profit Before Tax (PBT)", self.pbt, False),
            ("Income Tax Expense", self.tax, False),
            ("Profit After Tax (PAT)", self.pat, False),
        ]
        for label, series, is_base in is_lines:
            if not any(v is not None for v in series):
                continue
            row = [label]
            for i in range(self.n):
                rev = self.revenue[i]
                v = series[i]
                if is_base:
                    row.append("100.00%")
                elif rev and v is not None:
                    row.append(fmt_pct(safe_div(v, rev) * 100.0, 2))
                else:
                    row.append("-")
            cs_is_rows.append(row)
        lines.append(self._render_table(cs_is_headers, cs_is_rows))
        lines.append("")

        # Common-Size Balance Sheet
        lines.append("### Common-Size Balance Sheet (% of Total Assets)\n")
        cs_bs_headers = ["Balance Sheet Component"] + self.years
        cs_bs_rows = []
        bs_lines = [
            ("Total Assets / Liabilities (₹)", self.total_assets, True),
            ("Net Fixed Assets (PPE)", self.fixed_assets, False),
            ("Inventories", self.inventories, False),
            ("Trade Receivables", self.receivables, False),
            ("Cash & Equivalents", self.cash, False),
            ("Tangible Net Worth", self.net_worth, False),
            ("Total Borrowings (Debt)", self.total_debt, False),
            ("Trade Payables", self.payables, False),
            ("Current Liabilities", self.current_liabilities, False),
        ]
        for label, series, is_base in bs_lines:
            if not any(v is not None for v in series):
                continue
            row = [label]
            for i in range(self.n):
                ta = self.total_assets[i]
                v = series[i]
                if is_base:
                    row.append(fmt_num(ta, 1))
                elif ta and v is not None:
                    row.append(fmt_pct(safe_div(v, ta) * 100.0, 2))
                else:
                    row.append("-")
            cs_bs_rows.append(row)
        lines.append(self._render_table(cs_bs_headers, cs_bs_rows))
        lines.append("\n---\n")
        return "\n".join(lines)

    # =========================================================================
    # Section 2: Earnings Quality & Accruals
    # =========================================================================
    def build_earnings_quality(self) -> str:
        lines = []
        lines.append("## 2. Earnings Quality — Reconcile Earnings to Cash (The Central Test)\n")
        lines.append("### Point 2.1 & 2.2: Net Income vs. Cash Flow & Conversion Ratios\n")

        headers = ["Earnings Quality Metric"] + self.years + ["Cumulative"]
        rows = []

        pat_row = ["Reported Net Income (PAT)"]
        cfo_row = ["Operating Cash Flow (CFO)"]
        gap_row = ["Cash Gap (CFO − PAT)"]
        fcf_row = ["Free Cash Flow (FCF)"]
        ocf_conv_row = ["OCF / PAT Conversion (%)"]
        fcf_conv_row = ["FCF / PAT Conversion (%)"]
        accrual_row = ["Total Accruals (PAT − CFO)"]
        accrual_ratio_row = ["Sloan Accrual Ratio (% of Assets)"]

        cum_pat = 0.0
        cum_cfo = 0.0
        cum_fcf = 0.0
        cum_gap = 0.0
        has_cfo = any(x is not None for x in self.cfo)

        for i in range(self.n):
            p = self.pat[i]
            c = self.cfo[i]
            f = self.fcf[i]
            ta = self.total_assets[i]

            pat_row.append(fmt_num(p, 1))
            cfo_row.append(fmt_num(c, 1))
            fcf_row.append(fmt_num(f, 1))

            if p is not None and c is not None:
                gap = c - p
                gap_row.append(fmt_num(gap, 1))
                acc = p - c
                accrual_row.append(fmt_num(acc, 1))
                acc_r = safe_div(acc, ta) * 100.0 if ta else None
                accrual_ratio_row.append(fmt_pct(acc_r, 1) if acc_r is not None else "-")
                ocf_conv_row.append(fmt_pct(safe_div(c, p) * 100.0, 1))
                fcf_conv_row.append(fmt_pct(safe_div(f, p) * 100.0, 1) if f is not None else "-")

                cum_pat += p
                cum_cfo += c
                if f is not None:
                    cum_fcf += f
                cum_gap += gap
            else:
                gap_row.append("-")
                accrual_row.append("-")
                accrual_ratio_row.append("-")
                ocf_conv_row.append("-")
                fcf_conv_row.append("-")

        if has_cfo:
            pat_row.append(fmt_num(cum_pat, 1))
            cfo_row.append(fmt_num(cum_cfo, 1))
            gap_row.append(fmt_num(cum_gap, 1))
            fcf_row.append(fmt_num(cum_fcf, 1))
            ocf_conv_row.append(fmt_pct(safe_div(cum_cfo, cum_pat) * 100.0, 1))
            fcf_conv_row.append(fmt_pct(safe_div(cum_fcf, cum_pat) * 100.0, 1))
            accrual_row.append(fmt_num(-cum_gap, 1))
            last_ta = self.total_assets[-1]
            accrual_ratio_row.append(fmt_pct(safe_div(-cum_gap, last_ta) * 100.0, 1) if last_ta else "-")

        rows.extend([pat_row, cfo_row, gap_row, fcf_row, ocf_conv_row, fcf_conv_row, accrual_row, accrual_ratio_row])
        lines.append(self._render_table(headers, rows))

        # Forensic evaluation comment
        if has_cfo and cum_pat > 0:
            conv = safe_div(cum_cfo, cum_pat) * 100.0
            if conv < 50.0:
                lines.append(f"\n> ⚠️ **RED FLAG (Earnings Quality):** Cumulative OCF/PAT conversion is severely depressed at **{conv:.1f}%**. Over **{100 - conv:.1f}%** of reported earnings did not convert to operating cash.\n")
            elif conv < 80.0:
                lines.append(f"\n> ⚡ **CAUTION (Earnings Quality):** Cumulative OCF/PAT conversion is moderate at **{conv:.1f}%**.\n")
            else:
                lines.append(f"\n> ✅ **PASS (Earnings Quality):** Robust cumulative cash conversion of **{conv:.1f}%**.\n")
        lines.append("---\n")
        return "\n".join(lines)

    # =========================================================================
    # Section 3: Returns on Capital (DuPont & ROIC)
    # =========================================================================
    def build_returns_on_capital(self) -> str:
        lines = []
        lines.append("## 3. Returns on Capital — The Moat's Fingerprint\n")
        lines.append("### Point 3.1 & 3.2: 3-Stage DuPont ROE Decomposition\n")

        dupont_headers = ["DuPont Component"] + self.years
        dupont_rows = []

        npm_row = ["1. Net Profit Margin (%)"]
        ato_row = ["2. Asset Turnover (x)"]
        lev_row = ["3. Financial Leverage (x)"]
        roe_row = ["**DuPont ROE (%)**"]

        for i in range(self.n):
            s = self.revenue[i]
            p = self.pat[i]
            ta = self.total_assets[i]
            nw = self.net_worth[i]

            if s and p is not None and ta and nw is not None:
                npm = safe_div(p, s)
                ato = safe_div(s, ta)
                npm_row.append(fmt_pct(npm * 100.0, 2))
                ato_row.append(f"{ato:.2f}x")

                if nw <= 0:
                    lev_row.append(f"{safe_div(ta, nw):.2f}x (Neg NW)")
                    roe_row.append("Negative NW")
                else:
                    lev = safe_div(ta, nw)
                    roe = npm * ato * lev * 100.0
                    lev_row.append(f"{lev:.2f}x")
                    roe_row.append(fmt_pct(roe, 1))
            else:
                npm_row.append("-")
                ato_row.append("-")
                lev_row.append("-")
                roe_row.append("-")

        dupont_rows.extend([npm_row, ato_row, lev_row, roe_row])
        lines.append(self._render_table(dupont_headers, dupont_rows))
        lines.append("")

        # Capital Employed & Returns
        lines.append("### Returns on Invested Capital & Incremental ROIC (ROIIC)\n")
        ret_headers = ["Return Metric"] + self.years
        ret_rows = []

        ce_row = ["Total Capital Employed (₹)"]
        ic_row = ["Invested Capital (Net of Cash) (₹)"]
        nopat_row = ["NOPAT (₹)"]
        roce_row = ["ROCE (%)"]
        roic_row = ["Net ROIC (%)"]
        spread_row = [f"ROIC − WACC Spread ({self.wacc:.1f}%)"]
        roiic_row = ["Incremental ROIC (YoY ROIIC)"]

        for i in range(self.n):
            ce = self.capital_employed[i]
            ic = self.invested_capital[i]
            nop = self.nopat[i]
            eb = self.ebit[i]

            ce_row.append(fmt_num(ce, 1))
            ic_row.append(fmt_num(ic, 1))
            nopat_row.append(fmt_num(nop, 1))

            if eb is not None and ce and ce > 0:
                roce_val = safe_div(eb, ce) * 100.0
                roce_row.append(fmt_pct(roce_val, 1))
            else:
                roce_row.append("-")

            if nop is not None and ic and ic > 0:
                roic_val = safe_div(nop, ic) * 100.0
                roic_row.append(fmt_pct(roic_val, 1))
                spread_row.append(fmt_pct(roic_val - self.wacc, 1))
            else:
                roic_row.append("-")
                spread_row.append("-")

            # Incremental ROIC YoY
            if i > 0:
                prev_ic = self.invested_capital[i - 1]
                prev_nop = self.nopat[i - 1]
                if ic is not None and prev_ic is not None and nop is not None and prev_nop is not None:
                    d_ic = ic - prev_ic
                    d_nop = nop - prev_nop
                    if d_ic > 0.01:
                        roiic_val = (d_nop / d_ic) * 100.0
                        roiic_row.append(fmt_pct(roiic_val, 1))
                    elif d_ic < -0.01:
                        if d_nop >= 0:
                            roiic_row.append("Cap Released (NOPAT +)")
                        else:
                            roiic_row.append("Cap Reduced (NOPAT -)")
                    else:
                        roiic_row.append("N/A (ΔIC ~ 0)")
                else:
                    roiic_row.append("-")
            else:
                roiic_row.append("-")

        ret_rows.extend([ce_row, ic_row, nopat_row, roce_row, roic_row, spread_row, roiic_row])
        lines.append(self._render_table(ret_headers, ret_rows))
        lines.append("\n---\n")
        return "\n".join(lines)

    # =========================================================================
    # Section 4 & 5: Margins, Operating Leverage & Growth
    # =========================================================================
    def build_margins_and_growth(self) -> str:
        lines = []
        lines.append("## 4 & 5. Margins, Operating Leverage & Growth Quality\n")

        headers = ["Margin & Growth Metric"] + self.years
        rows = []

        rev_g_row = ["Revenue YoY Growth (%)"]
        gm_row = ["Gross Margin (%)"]
        opm_row = ["EBITDA / Operating Margin (%)"]
        npm_row = ["Net Profit Margin (%)"]
        dol_row = ["Degree of Operating Leverage (DOL)"]
        inc_opm_row = ["Incremental EBITDA Margin (%)"]

        for i in range(self.n):
            rev = self.revenue[i]
            gp = self.gross_profit[i]
            op = self.ebitda[i]
            p = self.pat[i]

            # Margins
            gm_row.append(fmt_pct(safe_div(gp, rev) * 100.0, 2) if rev and gp is not None else "-")
            opm_row.append(fmt_pct(safe_div(op, rev) * 100.0, 2) if rev and op is not None else "-")
            npm_row.append(fmt_pct(safe_div(p, rev) * 100.0, 2) if rev and p is not None else "-")

            if i > 0:
                p_rev = self.revenue[i - 1]
                p_op = self.ebitda[i - 1]
                g_rev = pct_change(p_rev, rev)
                g_op = pct_change(p_op, op)

                rev_g_row.append(fmt_pct(g_rev, 1) if g_rev is not None else "-")

                # DOL
                if g_rev is not None and g_op is not None and abs(g_rev) > 0.01:
                    dol = safe_div(g_op, g_rev)
                    dol_row.append(f"{dol:.2f}x")
                else:
                    dol_row.append("-")

                # Incremental EBITDA Margin
                if rev is not None and p_rev is not None and op is not None and p_op is not None:
                    d_rev = rev - p_rev
                    d_op = op - p_op
                    inc_opm_row.append(fmt_pct(safe_div(d_op, d_rev) * 100.0, 2) if abs(d_rev) > 0.01 else "-")
                else:
                    inc_opm_row.append("-")
            else:
                rev_g_row.append("-")
                dol_row.append("-")
                inc_opm_row.append("-")

        rows.extend([rev_g_row, gm_row, opm_row, npm_row, dol_row, inc_opm_row])
        lines.append(self._render_table(headers, rows))
        lines.append("\n---\n")
        return "\n".join(lines)

    # =========================================================================
    # Section 6: Solvency & Liquidity
    # =========================================================================
    def build_solvency_and_liquidity(self) -> str:
        lines = []
        lines.append("## 6. Balance Sheet Strength & Solvency\n")

        headers = ["Solvency / Liquidity Metric"] + self.years
        rows = []

        debt_row = ["Gross Debt (₹)"]
        cash_row = ["Cash & Equivalents (₹)"]
        net_debt_row = ["Net Debt / (Net Cash) (₹)"]
        de_row = ["Gross Debt / Equity (x)"]
        nd_ebitda_row = ["Net Debt / EBITDA (x)"]
        icr_row = ["Interest Coverage Ratio (x)"]
        cr_row = ["Current Ratio (x)"]
        qr_row = ["Quick Ratio (x)"]

        for i in range(self.n):
            d = self.total_debt[i] or 0.0
            cs = self.cash[i] or 0.0
            nd = d - cs
            nw = self.net_worth[i]
            op = self.ebitda[i]
            eb = self.total_ebit[i] if self.total_ebit[i] is not None else self.ebit[i]
            intr = self.interest[i]
            ca = self.current_assets[i]
            cl = self.current_liabilities[i]
            inv = self.inventories[i] or 0.0

            debt_row.append(fmt_num(d, 1))
            cash_row.append(fmt_num(cs, 1))
            net_debt_row.append(fmt_num(nd, 1))

            de_row.append(f"{safe_div(d, nw):.2f}x" if nw else "-")
            nd_ebitda_row.append(f"{safe_div(nd, op):.2f}x" if op and op > 0 else ("Net Cash" if nd < 0 else "-"))
            icr_row.append(f"{safe_div(eb, intr):.1f}x" if intr and intr > 0 and eb is not None else ">100x")

            cr_row.append(f"{safe_div(ca, cl):.2f}x" if ca and cl else "-")
            qr_row.append(f"{safe_div(ca - inv, cl):.2f}x" if ca and cl else "-")

        rows.extend([debt_row, cash_row, net_debt_row, de_row, nd_ebitda_row, icr_row, cr_row, qr_row])
        lines.append(self._render_table(headers, rows))
        lines.append("\n---\n")
        return "\n".join(lines)

    # =========================================================================
    # Section 7: Working Capital & Cash Conversion Cycle
    # =========================================================================
    def build_working_capital(self) -> str:
        lines = []
        lines.append("## 7. Working Capital & Cash Conversion Cycle\n")

        headers = ["Working Capital Metric"] + self.years
        rows = []

        dso_row = ["Debtor Days (DSO)"]
        dio_row = ["Inventory Days (DIO)"]
        dpo_row = ["Payable Days (DPO)"]
        ccc_row = ["**Cash Conversion Cycle (CCC)**"]
        scale_mult_row = ["1-Day Sales Value (₹)"]

        for i in range(self.n):
            s = self.revenue[i]
            cg = self.cogs[i] or s
            rec = self.receivables[i]
            inv = self.inventories[i]
            pay = self.payables[i]

            dso = (safe_div(rec, s) * 365.0) if s and rec is not None else None
            dio = (safe_div(inv, cg) * 365.0) if cg and inv is not None else None
            dpo = (safe_div(pay, cg) * 365.0) if cg and pay is not None else None

            dso_row.append(f"{dso:.1f} d" if dso is not None else "-")
            dio_row.append(f"{dio:.1f} d" if dio is not None else "-")
            dpo_row.append(f"{dpo:.1f} d" if dpo is not None else "-")

            if dso is not None and dio is not None:
                ccc = dso + dio - (dpo or 0.0)
                ccc_row.append(f"**{ccc:.1f} d**")
            else:
                ccc_row.append("-")

            scale_mult_row.append(fmt_num(safe_div(s, 365.0), 1) if s else "-")

        rows.extend([dso_row, dio_row, dpo_row, ccc_row, scale_mult_row])
        lines.append(self._render_table(headers, rows))
        lines.append("\n---\n")
        return "\n".join(lines)

    # =========================================================================
    # Section 8 & 9: Statistical Forensics (Altman Z & Beneish M)
    # =========================================================================
    def build_forensics(self) -> str:
        lines = []
        lines.append("## 8 & 9. Forensic Red Flags & Statistical Screens\n")

        # Altman Z''-Score (Emerging Market / Non-manufacturing 4-variable model)
        # Z'' = 6.56*X1 + 3.26*X2 + 6.72*X3 + 1.05*X4
        # X1 = (CA - CL) / TA
        # X2 = Retained Earnings / TA (approx Net Worth / TA if retained earnings not separated)
        # X3 = EBIT / TA
        # X4 = Net Worth / Total Liabilities
        altman_scores = []
        for i in range(self.n):
            ta = self.total_assets[i]
            ca = self.current_assets[i]
            cl = self.current_liabilities[i]
            nw = self.net_worth[i]
            re = self.reserves[i] if self.reserves[i] is not None else nw
            eb = self.total_ebit[i] if self.total_ebit[i] is not None else self.ebit[i]
            tl = (ta - nw) if ta and nw is not None else cl

            if ta and ca and cl and nw is not None and eb is not None and tl and tl > 0:
                x1 = safe_div(ca - cl, ta)
                x2 = safe_div(re, ta)
                x3 = safe_div(eb, ta)
                x4 = safe_div(nw, tl)
                z = 6.56 * x1 + 3.26 * x2 + 6.72 * x3 + 1.05 * x4
                altman_scores.append(z)
            else:
                altman_scores.append(None)

        # Beneish M-Score (8-variable model) for latest year
        beneish_str = self._compute_beneish_m()

        lines.append("### Statistical Models Summary\n")
        z_headers = ["Forensic Model"] + self.years
        z_row = ["Altman Z''-Score (EM Safe > 2.60)"]
        for z in altman_scores:
            if z is not None:
                z_row.append(f"{z:.2f}")
            else:
                z_row.append("-")
        lines.append(self._render_table(z_headers, [z_row]))
        lines.append("")
        lines.append(beneish_str)
        lines.append("\n---\n")
        return "\n".join(lines)

    def _compute_beneish_m(self) -> str:
        if self.n < 2:
            return "*Beneish M-Score requires at least 2 consecutive fiscal years.*"

        t = self.n - 1
        p = t - 1

        s_t, s_p = self.revenue[t], self.revenue[p]
        r_t, r_p = self.receivables[t], self.receivables[p]
        c_t, c_p = self.cogs[t], self.cogs[p]
        ta_t, ta_p = self.total_assets[t], self.total_assets[p]
        fa_t, fa_p = self.fixed_assets[t], self.fixed_assets[p]
        ca_t, ca_p = self.current_assets[t], self.current_assets[p]
        dep_t, dep_p = self.depreciation[t], self.depreciation[p]
        d_t, d_p = self.total_debt[t], self.total_debt[p]
        pat_t = self.pat[t]
        cfo_t = self.cfo[t]

        if not (s_t and s_p and ta_t and ta_p):
            return "*Insufficient data for Beneish M-Score.*"

        # 1. DSRI: Days Sales in Receivables Index
        dsri = safe_div(safe_div(r_t, s_t), safe_div(r_p, s_p), default=1.0)

        # 2. GMI: Gross Margin Index (with fallback to operating margin for service firms)
        if c_t is not None and c_p is not None:
            gm_t = safe_div(s_t - c_t, s_t)
            gm_p = safe_div(s_p - c_p, s_p)
        elif self.ebitda[t] is not None and self.ebitda[p] is not None:
            gm_t = safe_div(self.ebitda[t], s_t)
            gm_p = safe_div(self.ebitda[p], s_p)
        else:
            gm_t = 1.0
            gm_p = 1.0
        gmi = safe_div(gm_p, gm_t, default=1.0)

        # 3. AQI: Asset Quality Index (bounded non-negative)
        aq_t = max(0.0, 1.0 - safe_div((fa_t or 0.0) + (ca_t or 0.0), ta_t))
        aq_p = max(0.0, 1.0 - safe_div((fa_p or 0.0) + (ca_p or 0.0), ta_p))
        aqi = safe_div(aq_t, aq_p, default=1.0) if aq_p > 0 else 1.0

        # 4. SGI: Sales Growth Index
        sgi = safe_div(s_t, s_p, default=1.0)

        # 5. DEPI: Depreciation Index
        dr_p = safe_div(dep_p, (fa_p or 0.0) + (dep_p or 0.0))
        dr_t = safe_div(dep_t, (fa_t or 0.0) + (dep_t or 0.0))
        depi = safe_div(dr_p, dr_t, default=1.0)

        # 6. SGAI: SGA Expense Index (proxy 1.0 if not separated)
        sg_t, sg_p = self.sga[t], self.sga[p]
        if sg_t is not None and sg_p is not None and s_t and s_p:
            sgai = safe_div(safe_div(sg_t, s_t), safe_div(sg_p, s_p), default=1.0)
        else:
            sgai = 1.0

        # 7. TATA: Total Accruals to Total Assets
        tata = safe_div((pat_t or 0.0) - (cfo_t or 0.0), ta_t, default=0.0)

        # 8. LVGI: Leverage Index
        lev_t = safe_div(d_t or 0.0, ta_t)
        lev_p = safe_div(d_p or 0.0, ta_p)
        lvgi = safe_div(lev_t, lev_p, default=1.0) if lev_p > 0 else 1.0

        m_score = (
            -4.84
            + 0.920 * dsri
            + 0.528 * gmi
            + 0.404 * aqi
            + 0.892 * sgi
            + 0.115 * depi
            - 0.172 * sgai
            + 4.037 * tata
            + 0.0327 * lvgi
        )

        flag_str = "**FLAGGED (High Manipulation Probability)**" if m_score > -1.78 else "**CLEAN (Low Manipulation Probability)**"

        out = []
        out.append(f"### Beneish M-Score ({self.years[t]} vs. {self.years[p]}): {m_score:.2f} → {flag_str}\n")
        out.append("| Parameter | Value | Interpretation |")
        out.append("| :--- | :---: | :--- |")
        out.append(f"| **DSRI (Receivables Index)** | {dsri:.2f} | {'Receivables grew faster than sales' if dsri > 1.2 else 'Normal collection pattern'} |")
        out.append(f"| **GMI (Gross Margin Index)** | {gmi:.2f} | {'Gross margins contracted' if gmi > 1.05 else 'Gross margins stable/expanding'} |")
        out.append(f"| **AQI (Asset Quality Index)**| {aqi:.2f} | {'Potential non-current cost capitalization' if aqi > 1.2 else 'Normal asset composition'} |")
        out.append(f"| **SGI (Sales Growth Index)** | {sgi:.2f} | {'Rapid top-line expansion' if sgi > 1.2 else 'Moderate growth'} |")
        out.append(f"| **TATA (Total Accruals/Assets)**| {tata:+.3f} | {'High positive accruals (NI > OCF)' if tata > 0.05 else 'Normal accrual level'} |")
        out.append(f"| **LVGI (Leverage Index)**    | {lvgi:.2f} | {'Leverage increased' if lvgi > 1.1 else 'Leverage stable/declining'} |")
        return "\n".join(out)

    # =========================================================================
    # Helpers
    # =========================================================================
    def _render_table(self, headers: List[str], rows: List[List[str]]) -> str:
        lines = []
        lines.append("| " + " | ".join(headers) + " |")
        sep = ["| :--- "] + [":---:"] * (len(headers) - 1)
        lines.append(" | ".join(sep) + " |")
        for row in rows:
            lines.append("| " + " | ".join(row) + " |")
        return "\n".join(lines)

    def run_all(self) -> str:
        sections = [
            self.build_system_and_trends(),
            self.build_earnings_quality(),
            self.build_returns_on_capital(),
            self.build_margins_and_growth(),
            self.build_solvency_and_liquidity(),
            self.build_working_capital(),
            self.build_forensics(),
        ]
        return "\n".join(sections)


def get_template_json() -> Dict[str, Any]:
    """Returns a clean documented JSON template for model input."""
    return {
        "_comment": "Input template for financial_calculator.py (Step 5 Financials Framework). All currency values in ₹ Crore or uniform unit.",
        "years": ["FY21", "FY22", "FY23", "FY24", "FY25"],
        "revenue": [100.0, 120.0, 150.0, 180.0, 220.0],
        "cogs": [50.0, 60.0, 72.0, 85.0, 100.0],
        "ebitda": [20.0, 25.0, 32.0, 40.0, 52.0],
        "other_income": [2.0, 2.5, 3.0, 3.5, 4.0],
        "depreciation": [5.0, 6.0, 7.0, 8.0, 9.0],
        "interest": [3.0, 3.0, 2.5, 2.0, 1.5],
        "pbt": [14.0, 18.5, 25.5, 33.5, 45.5],
        "tax": [3.5, 4.6, 6.4, 8.4, 11.4],
        "pat": [10.5, 13.9, 19.1, 25.1, 34.1],
        "exceptional_items": [0.0, 0.0, 0.0, 0.0, 0.0],
        "net_worth": [60.0, 72.0, 88.0, 110.0, 140.0],
        "total_debt": [30.0, 28.0, 25.0, 20.0, 15.0],
        "total_assets": [110.0, 125.0, 145.0, 170.0, 205.0],
        "fixed_assets": [45.0, 50.0, 55.0, 60.0, 65.0],
        "inventories": [15.0, 18.0, 22.0, 25.0, 30.0],
        "receivables": [12.0, 15.0, 18.0, 22.0, 26.0],
        "payables": [10.0, 12.0, 14.0, 16.0, 18.0],
        "cash": [10.0, 12.0, 18.0, 25.0, 38.0],
        "current_assets": [45.0, 52.0, 65.0, 80.0, 105.0],
        "current_liabilities": [20.0, 25.0, 32.0, 40.0, 50.0],
        "reserves": [50.0, 62.0, 78.0, 100.0, 130.0],
        "sga": [10.0, 12.0, 15.0, 18.0, 22.0],
        "cfo": [15.0, 18.0, 24.0, 30.0, 42.0],
        "capex": [8.0, 10.0, 12.0, 14.0, 15.0],
        "wacc": 13.0,
        "tax_rate": 0.25,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Deterministic Financial Analysis Engine for src/company/listed/checklists/5-financials.md"
    )
    parser.add_argument("file", nargs="?", type=str, help="Optional path to input JSON file. If omitted, reads from stdin.")
    parser.add_argument(
        "--section",
        type=str,
        choices=["all", "system", "earnings", "returns", "margins", "solvency", "working_capital", "forensics"],
        default="all",
        help="Select checklist section to output.",
    )
    parser.add_argument("--wacc", type=float, default=13.0, help="Custom WACC percentage (default: 13.0)")
    parser.add_argument("--output", "-o", type=str, help="Optional path to write generated Markdown file.")
    parser.add_argument("--template", action="store_true", help="Print a documented sample JSON template and exit.")
    args = parser.parse_args()

    if args.template:
        print(json.dumps(get_template_json(), indent=2))
        sys.exit(0)

    # Load JSON
    if args.file and args.file != "-":
        with open(args.file, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
    else:
        if sys.stdin.isatty():
            print("Error: No input provided. Pipe JSON data via stdin, provide a file path, or run with --template.", file=sys.stderr)
            parser.print_help(sys.stderr)
            sys.exit(1)
        raw_data = json.load(sys.stdin)

    if args.wacc != 13.0:
        raw_data["wacc"] = args.wacc

    model = FinancialModel(raw_data)

    if args.section == "all":
        output_content = model.run_all()
    elif args.section == "system":
        output_content = model.build_system_and_trends()
    elif args.section == "earnings":
        output_content = model.build_earnings_quality()
    elif args.section == "returns":
        output_content = model.build_returns_on_capital()
    elif args.section == "margins":
        output_content = model.build_margins_and_growth()
    elif args.section == "solvency":
        output_content = model.build_solvency_and_liquidity()
    elif args.section == "working_capital":
        output_content = model.build_working_capital()
    elif args.section == "forensics":
        output_content = model.build_forensics()
    else:
        output_content = model.run_all()

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(output_content, encoding="utf-8")
        print(f"Markdown tables saved to {out_path.resolve()}", file=sys.stderr)
    else:
        print(output_content)


if __name__ == "__main__":
    main()
