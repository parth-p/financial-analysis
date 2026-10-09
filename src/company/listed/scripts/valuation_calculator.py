#!/usr/bin/env python3
"""
valuation_calculator.py — Deterministic 3-Year Multiples Valuation Engine
Implements the practical relative valuation & return framework for Indian equities.

Key Principles:
- Strictly 3-year investment horizon.
- Zero speculative assumptions: only growth rate and exit multiple.
- Multiples supported: P/E, EV/EBITDA, P/S (and P/B).
- Constant Net Debt treatment for enterprise value multiples.
- Inversion analysis: Implied growth for hurdle rate & Breakeven exit multiple.
- 2D Sensitivity Grid: Growth Rate vs. Exit Multiple (CAGR returns).

Pure Python standard library (zero external dependencies).
Execute via project virtualenv: .venv/bin/python src/company/listed/scripts/valuation_calculator.py
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import sys
from typing import Any, Dict, List, Optional, Tuple


def safe_div(num: Optional[float], den: Optional[float], default: float = 0.0) -> float:
    """Safe division handling zero and None values."""
    if num is None or den is None:
        return default
    try:
        return num / den if den != 0 else default
    except (ZeroDivisionError, OverflowError):
        return default


def cagr_3y(start_price: float, end_price: float) -> Optional[float]:
    """Calculate 3-year compound annual growth rate in percentage."""
    if start_price <= 0 or end_price <= 0:
        return None
    try:
        return (((end_price / start_price) ** (1.0 / 3.0)) - 1.0) * 100.0
    except (ValueError, ZeroDivisionError, OverflowError):
        return None


def fmt_num(val: Optional[float], decimals: int = 1, prefix: str = "", suffix: str = "") -> str:
    """Format float numbers cleanly."""
    if val is None or math.isnan(val):
        return "-"
    if decimals == 0:
        return f"{prefix}{val:,.0f}{suffix}"
    return f"{prefix}{val:,.{decimals}f}{suffix}"


def fmt_pct(val: Optional[float], decimals: int = 1, show_plus: bool = True) -> str:
    """Format percentage cleanly with optional sign."""
    if val is None or math.isnan(val):
        return "-"
    sign = "+" if show_plus and val > 0 else ""
    return f"{sign}{val:.{decimals}f}%"


class ValuationEngine:
    """Processes 3-year multiples-based valuation, scenarios, and sensitivity."""

    def __init__(self, data: Dict[str, Any], hurdle_rate: float = 15.0):
        self.data = data
        self.hurdle_rate = float(data.get("hurdle_rate", hurdle_rate))
        self.company = data.get("company", "Company")
        self.ticker = data.get("ticker", "")
        self.cmp = float(data.get("cmp", 0.0))
        self.shares_cr = float(data.get("shares_cr", 0.0))

        if self.cmp <= 0:
            raise ValueError("Input data must contain a valid positive 'cmp' (Current Market Price).")
        if self.shares_cr <= 0:
            raise ValueError("Input data must contain a valid positive 'shares_cr' (Shares Outstanding in Crore).")

        # Current Market Cap
        self.mcap_cr = self.cmp * self.shares_cr

        # Current metrics
        metrics = data.get("current_metrics", {})
        self.eps = self._get_float(metrics, "eps")
        self.ebitda_cr = self._get_float(metrics, "ebitda_cr", fallback_key="ebitda")
        self.sales_cr = self._get_float(metrics, "sales_cr", fallback_key="revenue")
        self.bvps = self._get_float(metrics, "bvps", fallback_key="book_value_per_share")
        self.net_debt_cr = self._get_float(metrics, "net_debt_cr", default=0.0)
        self.dividend_yield_pct = self._get_float(metrics, "dividend_yield_pct", default=0.0)

        # Current Enterprise Value
        self.current_ev_cr = self.mcap_cr + self.net_debt_cr

        # Current valuation multiples
        self.current_pe = safe_div(self.cmp, self.eps) if self.eps and self.eps > 0 else None
        self.current_ev_ebitda = safe_div(self.current_ev_cr, self.ebitda_cr) if self.ebitda_cr and self.ebitda_cr > 0 else None
        self.current_ps = safe_div(self.mcap_cr, self.sales_cr) if self.sales_cr and self.sales_cr > 0 else None
        self.current_pb = safe_div(self.cmp, self.bvps) if self.bvps and self.bvps > 0 else None

        # Historical & Peer Benchmarks
        self.benchmarks = data.get("benchmarks", {})
        self.hist_pe = self._get_float(self.benchmarks, "pe_5y_median", fallback_key="pe_historical_median")
        self.hist_ev_ebitda = self._get_float(self.benchmarks, "ev_ebitda_5y_median", fallback_key="ev_ebitda_historical_median")
        self.hist_ps = self._get_float(self.benchmarks, "ps_5y_median", fallback_key="ps_historical_median")
        self.hist_pb = self._get_float(self.benchmarks, "pb_5y_median", fallback_key="pb_historical_median")

        self.peer_pe = self._get_float(self.benchmarks, "peer_pe_median")
        self.peer_ev_ebitda = self._get_float(self.benchmarks, "peer_ev_ebitda_median")

        # Scenarios
        self.scenarios = data.get("scenarios_3y", {})

    def _get_float(self, d: Dict[str, Any], key: str, fallback_key: Optional[str] = None, default: Optional[float] = None) -> Optional[float]:
        val = d.get(key)
        if val is None and fallback_key:
            val = d.get(fallback_key)
        if val is None:
            return default
        try:
            return float(val)
        except (ValueError, TypeError):
            return default

    # =========================================================================
    # Section 1: Current Valuation Context
    # =========================================================================
    def build_current_valuation_table(self) -> str:
        lines = []
        name_str = f"{self.company} ({self.ticker})" if self.ticker else self.company
        lines.append(f"## 1. Current Valuation Snapshot — {name_str}\n")
        lines.append(f"- **Current Market Price (CMP):** ₹{self.cmp:,.2f}")
        lines.append(f"- **Market Capitalisation:** ₹{self.mcap_cr:,.1f} Cr ({self.shares_cr:,.2f} Cr shares)")
        debt_label = "Net Cash" if self.net_debt_cr < 0 else "Net Debt"
        lines.append(f"- **{debt_label}:** ₹{abs(self.net_debt_cr):,.1f} Cr | **Enterprise Value (EV):** ₹{self.current_ev_cr:,.1f} Cr")
        if self.dividend_yield_pct > 0:
            lines.append(f"- **Trailing Dividend Yield:** {self.dividend_yield_pct:.2f}%")
        lines.append("")

        headers = ["Valuation Metric", "Current Value", "5-Yr Historical Median", "Peer Median", "Current Status vs. History"]
        rows = []

        # P/E
        pe_curr = f"{self.current_pe:.1f}x" if self.current_pe else "-"
        pe_hist = f"{self.hist_pe:.1f}x" if self.hist_pe else "-"
        pe_peer = f"{self.peer_pe:.1f}x" if self.peer_pe else "-"
        pe_status = self._calc_premium_label(self.current_pe, self.hist_pe)
        rows.append(["**P/E (Price-to-Earnings)**", pe_curr, pe_hist, pe_peer, pe_status])

        # EV/EBITDA
        eve_curr = f"{self.current_ev_ebitda:.1f}x" if self.current_ev_ebitda else "-"
        eve_hist = f"{self.hist_ev_ebitda:.1f}x" if self.hist_ev_ebitda else "-"
        eve_peer = f"{self.peer_ev_ebitda:.1f}x" if self.peer_ev_ebitda else "-"
        eve_status = self._calc_premium_label(self.current_ev_ebitda, self.hist_ev_ebitda)
        rows.append(["**EV/EBITDA**", eve_curr, eve_hist, eve_peer, eve_status])

        # P/S
        ps_curr = f"{self.current_ps:.2f}x" if self.current_ps else "-"
        ps_hist = f"{self.hist_ps:.2f}x" if self.hist_ps else "-"
        ps_status = self._calc_premium_label(self.current_ps, self.hist_ps)
        rows.append(["**P/S (Price-to-Sales)**", ps_curr, ps_hist, "-", ps_status])

        # P/B
        if self.current_pb or self.hist_pb:
            pb_curr = f"{self.current_pb:.2f}x" if self.current_pb else "-"
            pb_hist = f"{self.hist_pb:.2f}x" if self.hist_pb else "-"
            pb_status = self._calc_premium_label(self.current_pb, self.hist_pb)
            rows.append(["**P/B (Price-to-Book)**", pb_curr, pb_hist, "-", pb_status])

        lines.append(self._render_table(headers, rows))
        lines.append("\n---\n")
        return "\n".join(lines)

    def _calc_premium_label(self, current: Optional[float], benchmark: Optional[float]) -> str:
        if current is None or benchmark is None or benchmark <= 0:
            return "No historical benchmark"
        gap_pct = ((current - benchmark) / benchmark) * 100.0
        if gap_pct > 20.0:
            return f"⚠️ **Premium of +{gap_pct:.1f}%**"
        elif gap_pct < -20.0:
            return f"✅ **Discount of {gap_pct:.1f}%**"
        else:
            return f"In-line ({gap_pct:+.1f}%)"

    # =========================================================================
    # Section 2: 3-Year Scenario Projections & Return Table
    # =========================================================================
    def build_scenarios_table(self) -> str:
        lines = []
        lines.append("## 2. 3-Year Forward Scenario Projections & Return (CAGR)\n")
        lines.append("> Assumes business grows over 3 years at the scenario rate and exits at the specified multiple.")
        lines.append("> For enterprise multiples, Net Debt is held constant to avoid speculative balance sheet forecasting.\n")

        # P/E Scenarios
        if self.eps and self.eps > 0:
            lines.append("### A. P/E Multiple Scenarios (Earnings-Driven)\n")
            pe_headers = [
                "Scenario",
                "3Y EPS CAGR",
                f"Year 3 EPS (Base: ₹{self.eps:.1f})",
                "Exit P/E",
                "Year 3 Target Price",
                "Price 3Y CAGR",
                "Total 3Y CAGR (+Div)",
                "Multiple Expansion/Contraction",
            ]
            pe_rows = []
            for name in ["bear", "base", "bull"]:
                sc = self.scenarios.get(name, {})
                g = self._get_float(sc, "eps_growth_pct", fallback_key="growth_pct")
                exit_m = self._get_float(sc, "exit_pe")
                if g is None or exit_m is None:
                    continue

                y3_eps = self.eps * ((1.0 + (g / 100.0)) ** 3)
                target_price = y3_eps * exit_m
                price_cagr = cagr_3y(self.cmp, target_price)
                tot_cagr = (price_cagr + self.dividend_yield_pct) if price_cagr is not None else None

                mult_impact = ""
                if self.current_pe and self.current_pe > 0:
                    mult_chg = ((exit_m - self.current_pe) / self.current_pe) * 100.0
                    mult_impact = f"{mult_chg:+.1f}% vs CMP P/E"

                row = [
                    f"**{name.capitalize()}**",
                    f"{g:.1f}%",
                    f"₹{y3_eps:,.2f}",
                    f"{exit_m:.1f}x",
                    f"₹{target_price:,.2f}",
                    f"**{fmt_pct(price_cagr)}**",
                    f"**{fmt_pct(tot_cagr)}**" if self.dividend_yield_pct > 0 else fmt_pct(price_cagr),
                    mult_impact,
                ]
                pe_rows.append(row)

            if pe_rows:
                lines.append(self._render_table(pe_headers, pe_rows))
                lines.append("")

        # EV/EBITDA Scenarios
        if self.ebitda_cr and self.ebitda_cr > 0:
            lines.append("### B. EV/EBITDA Multiple Scenarios (Cash Flow / Capital Structure Driven)\n")
            eve_headers = [
                "Scenario",
                "3Y EBITDA CAGR",
                f"Year 3 EBITDA (₹ Cr)",
                "Exit EV/EBITDA",
                "Year 3 Target EV (₹ Cr)",
                "Net Debt (Held Constant)",
                "Target Price",
                "Price 3Y CAGR",
            ]
            eve_rows = []
            for name in ["bear", "base", "bull"]:
                sc = self.scenarios.get(name, {})
                g = self._get_float(sc, "ebitda_growth_pct", fallback_key="growth_pct")
                exit_m = self._get_float(sc, "exit_ev_ebitda")
                if g is None or exit_m is None:
                    continue

                y3_ebitda = self.ebitda_cr * ((1.0 + (g / 100.0)) ** 3)
                target_ev = y3_ebitda * exit_m
                target_equity = target_ev - self.net_debt_cr
                target_price = safe_div(target_equity, self.shares_cr)
                price_cagr = cagr_3y(self.cmp, target_price)

                debt_str = f"-₹{abs(self.net_debt_cr):,.1f} Cr (Cash)" if self.net_debt_cr < 0 else f"+₹{self.net_debt_cr:,.1f} Cr"

                row = [
                    f"**{name.capitalize()}**",
                    f"{g:.1f}%",
                    f"₹{y3_ebitda:,.1f}",
                    f"{exit_m:.1f}x",
                    f"₹{target_ev:,.1f}",
                    debt_str,
                    f"₹{target_price:,.2f}",
                    f"**{fmt_pct(price_cagr)}**",
                ]
                eve_rows.append(row)

            if eve_rows:
                lines.append(self._render_table(eve_headers, eve_rows))
                lines.append("")

        # P/S Scenarios
        has_ps_scenarios = any("exit_ps" in self.scenarios.get(k, {}) for k in ["bear", "base", "bull"])
        if self.sales_cr and self.sales_cr > 0 and has_ps_scenarios:
            lines.append("### C. P/S Multiple Scenarios (Sales-Driven)\n")
            ps_headers = [
                "Scenario",
                "3Y Sales CAGR",
                f"Year 3 Sales (₹ Cr)",
                "Exit P/S",
                "Year 3 Target Mcap",
                "Target Price",
                "Price 3Y CAGR",
            ]
            ps_rows = []
            for name in ["bear", "base", "bull"]:
                sc = self.scenarios.get(name, {})
                g = self._get_float(sc, "sales_growth_pct", fallback_key="growth_pct")
                exit_m = self._get_float(sc, "exit_ps")
                if g is None or exit_m is None:
                    continue

                y3_sales = self.sales_cr * ((1.0 + (g / 100.0)) ** 3)
                target_mcap = y3_sales * exit_m
                target_price = safe_div(target_mcap, self.shares_cr)
                price_cagr = cagr_3y(self.cmp, target_price)

                row = [
                    f"**{name.capitalize()}**",
                    f"{g:.1f}%",
                    f"₹{y3_sales:,.1f}",
                    f"{exit_m:.2f}x",
                    f"₹{target_mcap:,.1f} Cr",
                    f"₹{target_price:,.2f}",
                    f"**{fmt_pct(price_cagr)}**",
                ]
                ps_rows.append(row)

            if ps_rows:
                lines.append(self._render_table(ps_headers, ps_rows))
                lines.append("")

        lines.append("---\n")
        return "\n".join(lines)

    # =========================================================================
    # Section 3: Inversion Analysis (Reverse Math)
    # =========================================================================
    def build_inversion_analysis(self) -> str:
        lines = []
        lines.append("## 3. Inversion Analysis (What Must Happen to Justify Price?)\n")
        lines.append(f"> Rather than forecasting the future, this inverts the formula to identify the breakeven conditions and required growth rates against a **{self.hurdle_rate:.1f}% hurdle rate**.\n")

        if not self.eps or self.eps <= 0:
            lines.append("*EPS is zero or negative; inversion analysis requires positive earnings base.*\n---\n")
            return "\n".join(lines)

        # 1. Growth needed for hurdle rate at different exit multiples
        # Formula: CMP * (1 + hurdle)^3 = EPS_0 * (1 + g)^3 * Exit_PE
        # => (1 + g)^3 = (CMP / (EPS_0 * Exit_PE)) * (1 + hurdle)^3
        # => (1 + g) = (1 + hurdle) * [ (CMP / (EPS_0 * Exit_PE))^(1/3) ]
        hurdle_dec = self.hurdle_rate / 100.0
        target_cmp_y3 = self.cmp * ((1.0 + hurdle_dec) ** 3)

        lines.append(f"### A. Required 3-Year EPS Growth to Achieve {self.hurdle_rate:.1f}% CAGR\n")
        headers = ["Exit P/E Multiple Assumed", "Implied Year 3 EPS Needed", "Required 3Y EPS Growth (CAGR)", "Verdict"]
        rows = []

        test_multiples: List[Tuple[str, float]] = []
        if self.current_pe:
            test_multiples.append((f"At Current P/E ({self.current_pe:.1f}x)", self.current_pe))
        if self.hist_pe and (not self.current_pe or abs(self.hist_pe - self.current_pe) > 0.5):
            test_multiples.append((f"At 5-Yr Historical Median ({self.hist_pe:.1f}x)", self.hist_pe))
        if self.peer_pe and (not self.hist_pe or abs(self.peer_pe - self.hist_pe) > 0.5):
            test_multiples.append((f"At Peer Median ({self.peer_pe:.1f}x)", self.peer_pe))

        # Add 2 conservative de-rating multiples
        base_ref = self.hist_pe or self.current_pe or 25.0
        de_rate_1 = round(base_ref * 0.8, 1)
        de_rate_2 = round(base_ref * 0.65, 1)
        test_multiples.append((f"De-rating to {de_rate_1:.1f}x (-20%)", de_rate_1))
        test_multiples.append((f"Severe De-rating to {de_rate_2:.1f}x (-35%)", de_rate_2))

        for label, m in test_multiples:
            if m <= 0:
                continue
            req_eps_y3 = target_cmp_y3 / m
            req_g = (((req_eps_y3 / self.eps) ** (1.0 / 3.0)) - 1.0) * 100.0

            if req_g > 30.0:
                verdict = "🔴 **Heroic / Improbable (>30% CAGR)**"
            elif req_g > 20.0:
                verdict = "⚡ **High Bar (20–30% CAGR)**"
            elif req_g > 10.0:
                verdict = "✅ **Reasonable (10–20% CAGR)**"
            else:
                verdict = "🟢 **Easy Bar (<10% CAGR)**"

            rows.append([label, f"₹{req_eps_y3:,.2f}", f"**{req_g:+.1f}%**", verdict])

        lines.append(self._render_table(headers, rows))
        lines.append("")

        # 2. Breakeven Multiple Analysis (0% return / capital preservation floor)
        # At base scenario growth, what exit multiple results in Target Price == CMP?
        base_sc = self.scenarios.get("base", {})
        base_g = self._get_float(base_sc, "eps_growth_pct", fallback_key="growth_pct")

        if base_g is not None:
            lines.append("### B. Capital Preservation Floor (Breakeven Multiple)\n")
            y3_base_eps = self.eps * ((1.0 + (base_g / 100.0)) ** 3)
            breakeven_pe = self.cmp / y3_base_eps
            pe_cushion = ((self.current_pe - breakeven_pe) / self.current_pe) * 100.0 if self.current_pe else 0.0

            lines.append(f"- **Assuming Base EPS Growth of {base_g:.1f}% CAGR**, Year 3 EPS will be **₹{y3_base_eps:,.2f}**.")
            lines.append(f"- To protect capital (**0% return / breakeven at ₹{self.cmp:,.2f}**), P/E can fall to: **{breakeven_pe:.1f}x**.")
            if self.current_pe:
                lines.append(f"- **Downside Multiple Cushion:** P/E can contract by **{pe_cushion:.1f}%** (from {self.current_pe:.1f}x to {breakeven_pe:.1f}x) before you lose money.")
            lines.append("")

        lines.append("---\n")
        return "\n".join(lines)

    # =========================================================================
    # Section 4: 2D Sensitivity Grid (Growth vs. Exit Multiple)
    # =========================================================================
    def build_sensitivity_grid(self) -> str:
        lines = []
        lines.append("## 4. 2D Sensitivity Payoff Grid (3-Year Annualized CAGR Return)\n")
        lines.append(f"> Displays 3-year Price CAGR across varying growth rates and exit multiples. Values meeting or exceeding the **{self.hurdle_rate:.1f}% hurdle rate** are highlighted (**★**).\n")

        if not self.eps or self.eps <= 0:
            lines.append("*EPS is zero or negative; sensitivity grid requires positive earnings base.*\n")
            return "\n".join(lines)

        # Determine reasonable range of growth rates
        base_g = 15.0
        if "base" in self.scenarios:
            sc_g = self._get_float(self.scenarios["base"], "eps_growth_pct", fallback_key="growth_pct")
            if sc_g:
                base_g = sc_g

        growth_steps = [
            max(0.0, round(base_g - 10.0, 1)),
            max(2.0, round(base_g - 5.0, 1)),
            round(base_g, 1),
            round(base_g + 5.0, 1),
            round(base_g + 10.0, 1),
        ]
        growth_steps = sorted(list(set(growth_steps)))

        # Determine reasonable range of exit multiples
        anchor_pe = self.hist_pe or self.current_pe or 30.0
        multiples = [
            round(anchor_pe * 0.70, 1),
            round(anchor_pe * 0.85, 1),
            round(anchor_pe, 1),
            round(anchor_pe * 1.15, 1),
            round(anchor_pe * 1.30, 1),
        ]
        # Ensure current P/E is present if distinct
        if self.current_pe and round(self.current_pe, 1) not in multiples:
            multiples.append(round(self.current_pe, 1))
        multiples = sorted(list(set(multiples)))

        # Build table
        headers = ["3Y EPS CAGR \\ Exit P/E"] + [f"{m:.1f}x" for m in multiples]
        rows = []

        for g in growth_steps:
            row = [f"**{g:.1f}%**"]
            y3_eps = self.eps * ((1.0 + (g / 100.0)) ** 3)
            for m in multiples:
                target_p = y3_eps * m
                cagr = cagr_3y(self.cmp, target_p)
                if cagr is None:
                    row.append("-")
                elif cagr >= self.hurdle_rate:
                    row.append(f"**{cagr:+.1f}% ★**")
                else:
                    row.append(f"{cagr:+.1f}%")
            rows.append(row)

        lines.append(self._render_table(headers, rows))
        lines.append("")
        return "\n".join(lines)

    # =========================================================================
    # Master Runner
    # =========================================================================
    def run_all(self) -> str:
        sections = [
            self.build_current_valuation_table(),
            self.build_scenarios_table(),
            self.build_inversion_analysis(),
            self.build_sensitivity_grid(),
        ]
        return "\n".join(sections)

    def _render_table(self, headers: List[str], rows: List[List[str]]) -> str:
        lines = []
        lines.append("| " + " | ".join(headers) + " |")
        sep = ["| :--- "] + [":---:"] * (len(headers) - 1)
        lines.append(" | ".join(sep) + " |")
        for row in rows:
            lines.append("| " + " | ".join(row) + " |")
        return "\n".join(lines)


def get_template_json() -> Dict[str, Any]:
    """Returns a clean documented JSON template for valuation_calculator input."""
    return {
        "_comment": "Input template for valuation_calculator.py (Strict 3-Year Multiples Framework). All currency values in ₹ Crore or uniform unit.",
        "company": "Polycab India Ltd",
        "ticker": "POLYCAB",
        "cmp": 5400.0,
        "shares_cr": 15.03,
        "hurdle_rate": 15.0,

        "current_metrics": {
            "eps": 120.0,
            "ebitda_cr": 2492.0,
            "sales_cr": 18039.0,
            "bvps": 520.0,
            "net_debt_cr": -1550.0,
            "dividend_yield_pct": 0.6
        },

        "benchmarks": {
            "pe_5y_median": 38.0,
            "ev_ebitda_5y_median": 26.0,
            "ps_5y_median": 3.2,
            "peer_pe_median": 45.0,
            "peer_ev_ebitda_median": 30.0
        },

        "scenarios_3y": {
            "bear": {
                "growth_pct": 10.0,
                "exit_pe": 28.0,
                "exit_ev_ebitda": 20.0,
                "exit_ps": 2.4
            },
            "base": {
                "growth_pct": 16.0,
                "exit_pe": 38.0,
                "exit_ev_ebitda": 26.0,
                "exit_ps": 3.2
            },
            "bull": {
                "growth_pct": 22.0,
                "exit_pe": 45.0,
                "exit_ev_ebitda": 30.0,
                "exit_ps": 4.0
            }
        }
    }


def main():
    parser = argparse.ArgumentParser(
        description="Deterministic 3-Year Multiples Valuation Engine for Listed Indian Equities"
    )
    parser.add_argument("file", nargs="?", type=str, help="Optional path to input JSON file. If omitted, reads from stdin.")
    parser.add_argument("--hurdle", type=float, default=15.0, help="Target hurdle return CAGR in %% (default: 15.0)")
    parser.add_argument("--output", "-o", type=str, help="Optional path to write generated Markdown report.")
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

    if args.hurdle != 15.0:
        raw_data["hurdle_rate"] = args.hurdle

    engine = ValuationEngine(raw_data, hurdle_rate=args.hurdle)
    output_content = engine.run_all()

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(output_content, encoding="utf-8")
        print(f"Valuation report saved to {out_path.resolve()}", file=sys.stderr)
    else:
        print(output_content)


if __name__ == "__main__":
    main()
