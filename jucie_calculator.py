import streamlit as st

# --- UI Configuration ---
st.set_page_config(page_title="J.U.C.I.E. Leverage & Comparison Engine", layout="wide")
st.title("🌱 J.U.C.I.E. Leverage & Comparison Engine")
st.markdown("Compare **Traditional Real Estate Liquidation** vs. **The Mutual Land Blessing (MLB) Donation** side-by-side.")

# --- Sidebar Inputs ---
st.sidebar.header("1. Investor & Tax Profile")
agi = st.sidebar.number_input("Annual Adjusted Gross Income (AGI) ($)", min_value=10000, value=250000, step=10000)
marginal_tax_rate = st.sidebar.slider("Marginal Income Tax Bracket (%)", min_value=10, max_value=37, value=37) / 100
cap_gains_tax_rate = st.sidebar.slider("Capital Gains Tax Rate (%)", min_value=0, max_value=20, value=15) / 100

st.sidebar.header("2. Property & Acquisition")
auction_bid = st.sidebar.number_input("Auction Bid / Acquisition Cost ($)", min_value=500, value=10000, step=500)
expected_fmv = st.sidebar.number_input("Appraised Fair Market Value (FMV) ($)", min_value=1000, value=40000, step=1000)

st.sidebar.header("3. Traditional Sale Friction Assumptions")
est_sale_price = st.sidebar.number_input("Expected Open Market Sale Price ($)", min_value=1000, value=expected_fmv, step=1000)
realtor_fee_pct = st.sidebar.slider("Realtor Commission (%)", min_value=0.0, max_value=10.0, value=6.0, step=0.5) / 100
closing_costs_pct = st.sidebar.slider("Closing Costs / Title / Escrow (%)", min_value=0.0, max_value=5.0, value=3.0, step=0.5) / 100
trad_holding_costs = st.sidebar.number_input("Est. Traditional Holding Costs (Taxes, Insurance, Repairs) ($)", min_value=0, value=2500, step=250)
sale_timeframe_months = st.sidebar.slider("Expected Months to Sell & Close", min_value=1, max_value=24, value=12)

# --- MATH ENGINE ---

# --- A. Traditional Sale Calculation ---
trad_realtor_fee = est_sale_price * realtor_fee_pct
trad_closing_costs = est_sale_price * closing_costs_pct
trad_total_friction = trad_realtor_fee + trad_closing_costs + trad_holding_costs
trad_net_before_tax = est_sale_price - trad_total_friction
trad_capital_gain = max(0, trad_net_before_tax - auction_bid)
trad_cap_gains_tax = trad_capital_gain * cap_gains_tax_rate
trad_net_cash = trad_net_before_tax - auction_bid - trad_cap_gains_tax

# --- B. MLB Donation Calculation ---
# Under $1 NNN Lease, J.U.C.I.E. covers holding costs. Total Out-of-Pocket = Auction Bid
mlb_out_of_pocket = auction_bid 
mlb_tax_savings = expected_fmv * marginal_tax_rate
mlb_net_cash = mlb_tax_savings - mlb_out_of_pocket

# IRS 30% AGI Cap
max_deduction_yr1 = agi * 0.30
usable_deduction_yr1 = min(expected_fmv, max_deduction_yr1)
tax_savings_yr1 = usable_deduction_yr1 * marginal_tax_rate
carryforward_amt = max(0, expected_fmv - max_deduction_yr1)

# Comparison Delta
net_cash_delta = mlb_net_cash - trad_net_cash
impact_leverage_ratio = expected_fmv / mlb_out_of_pocket if mlb_out_of_pocket > 0 else 0

# --- MAIN DISPLAY ---

# Top Line Metrics
m1, m2, m3, m4 = st.columns(4)
m1.metric("Acquisition Cost", f"${auction_bid:,.2f}")
m2.metric("Traditional Net Cash", f"${trad_net_cash:,.2f}", delta=f"{sale_timeframe_months} Mo. Friction", delta_color="off")
m3.metric("MLB Net Cash (Tax Shield)", f"${mlb_net_cash:,.2f}", delta=f"${net_cash_delta:+,.2f} vs. Sale", delta_color="normal" if net_cash_delta >= 0 else "off")
m4.metric("Community Impact Created", f"${expected_fmv:,.2f}", delta=f"{impact_leverage_ratio:.1f}x Leverage", delta_color="normal")

st.divider()

# Side-by-Side Comparison Table
col_trad, col_mlb = st.columns(2)

with col_trad:
    st.subheader("🔴 Traditional Real Estate Sale")
    st.write(f"**Gross Selling Price:** ${est_sale_price:,.2f}")
    st.write(f"• Realtor Commissions ({realtor_fee_pct*100:.1f}%): -${trad_realtor_fee:,.2f}")
    st.write(f"• Closing Costs ({closing_costs_pct*100:.1f}%): -${trad_closing_costs:,.2f}")
    st.write(f"• Holding Costs (Taxes/Maint/Ins): -${trad_holding_costs:,.2f}")
    st.write(f"• Capital Gains Tax ({cap_gains_tax_rate*100:.1f}%): -${trad_cap_gains_tax:,.2f}")
    st.write("---")
    st.write(f"**Total Friction & Expense:** -${(trad_total_friction + trad_cap_gains_tax):,.2f}")
    st.write(f"**Estimated Timeframe:** {sale_timeframe_months} Months")
    st.write("**Operational Friction:** High (Landlord hassle, buyer negotiations, appraisal drops, market volatility)")

with col_mlb:
    st.subheader("🟢 J.U.C.I.E. Mutual Land Blessing")
    st.write(f"**Appraised FMV Donation:** ${expected_fmv:,.2f}")
    st.write("• Realtor Commissions: **$0.00**")
    st.write("• Closing Costs: **$0.00**")
    st.write("• Holding Costs ($1 NNN Lease to J.U.C.I.E.): **$0.00**")
    st.write(f"• Ordinary Income Tax Savings ({marginal_tax_rate*100:.1f}% Bracket): +${mlb_tax_savings:,.2f}")
    st.write("---")
    st.write(f"**Total Direct Out-of-Pocket:** -${mlb_out_of_pocket:,.2f}")
    st.write("**Estimated Timeframe:** 366 Days (Silent Holding Period)")
    st.write("**Operational Friction:** Zero (J.U.C.I.E. handles site cleanup, holding costs, and title transfer)")

st.divider()

# --- Exhaustive Data Points & Donor Guidance ---
st.subheader("🧠 Donor Value Strategy & Impact Analysis")

if mlb_net_cash > 0:
    st.success(f"🎉 **LITERAL CASH PROFIT DETECTED:** This deal generates **${mlb_net_cash:,.2f}** in net liquid tax savings above your acquisition cost. You are profiting while restoring the community!")
elif mlb_net_cash == 0:
    st.info("⚖️ **PERFECT BREAKEVEN:** You receive a 100% full cash recovery of your acquisition bid while gifting 100% of the land's value to the community.")
else:
    net_cost = abs(mlb_net_cash)
    st.warning(f"💡 **IMPACT VALUE PROPOSITION (Slight Net Out-of-Pocket):** Your net out-of-pocket after tax savings is **${net_cost:,.2f}**. "
               f"However, this single transaction unlocks **${expected_fmv:,.2f}** in real community asset value—a **{impact_leverage_ratio:.1f}x Civic Leverage Multiplier**!")

# IRS Guardrails & Carryforward
st.markdown("### ⚖️ IRS Deduction Limits & Tax Arbitrage")
c1, c2 = st.columns(2)
with c1:
    st.write(f"**Year 1 Deduction Limit (30% of AGI):** ${max_deduction_yr1:,.2f}")
    st.write(f"**Year 1 Usable Tax Deduction:** ${usable_deduction_yr1:,.2f}")
    st.write(f"**Year 1 Immediate Tax Cash Back:** ${tax_savings_yr1:,.2f}")
with c2:
    if carryforward_amt > 0:
        st.write(f"**Carryforward Amount:** ${carryforward_amt:,.2f}")
        st.write("*(This unused deduction carries forward for up to 5 additional tax years to shield future income.)*")
    else:
        st.write("**Carryforward Amount:** $0.00 *(100% of deduction absorbed in Year 1)*")

st.caption("*Disclaimer: This software is an estimation tool based on IRS Section 170 long-term capital gains property donation rules. Always consult a licensed CPA or tax attorney for official filing guidance.*")
