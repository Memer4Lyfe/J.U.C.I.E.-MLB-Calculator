import streamlit as st

# --- UI CONFIGURATION ---
st.set_page_config(page_title="J.U.C.I.E. Mutual Land Blessing Engine", layout="wide")

st.title("🌱 J.U.C.I.E. Mutual Land Blessing Engine")
st.caption("Fiduciary-Grade Real Estate Liquidation vs. Philanthropic Land Donation")

# --- NAVIGATION TABS ---
tab_calc, tab_faq, tab_cert = st.tabs(["🧮 Steward Engine & Calculator", "🔍 Searchable FAQ Library", "📜 Civic Certificate Generator"])

with tab_calc:
    # --- ONBOARDING & REFERRAL QUESTIONNAIRE ---
    with st.expander("❓ Onboarding & Discovery Wizard (Click to Expand / Restart)", expanded=False):
        col_q1, col_q2 = st.columns(2)
        with col_q1:
            referral_source = st.selectbox(
                "How did you hear about the Steward Engine?",
                ["Select an option...", "My Church / Faith Community", "Referred by my CPA / Financial Advisor", 
                 "Inherited / Owned Blighted Land", "Social Media / Podcast", "Word of Mouth"]
            )
        with col_q2:
            steward_goal = st.selectbox(
                "What is your primary goal today?",
                ["Maximize Tax Relief & Cash Savings", "Clear Back Taxes on Family/Heir Land", 
                 "Restore Community Infrastructure (Solar/Bees)", "Explore Fiduciary Client Options"]
            )
        st.info("💡 Tip: You can skip this wizard at any time or adjust sliders directly in the sidebar.")

    # --- SIDEBAR FORM WITH HOVER TOOLTIPS FOR ALL LINGO ---
    with st.sidebar.form(key="calc_form"):
        st.header("⚙️ Scenario Parameters")
        
        county_preset = st.selectbox(
            "Select Target Market Preset",
            ["Custom Entry", "Fulton County, GA (Non-Judicial)", "Harris County, TX (25% Penalty)", "Orange County, FL (18% OTC)"],
            help="Pre-fills average auction bids and appraised values for target jurisdictions."
        )
        
        default_bid, default_fmv = 10000, 40000
        if "Fulton" in county_preset:
            default_bid, default_fmv = 3500, 18000
        elif "Harris" in county_preset:
            default_bid, default_fmv = 12000, 45000
        elif "Orange" in county_preset:
            default_bid, default_fmv = 5000, 22000

        st.markdown("---")
        st.subheader("1. Tax & Income Profile")
        agi = st.number_input("Annual Adjusted Gross Income (AGI) ($)", min_value=10000, value=250000, step=10000,
                              help="AGI (Adjusted Gross Income): Your total taxable income. Under IRC §170, annual land donations are capped at 30% of this number.")
        marginal_tax_rate = st.slider("Marginal Income Tax Bracket (%)", min_value=10, max_value=37, value=37,
                                      help="Marginal Tax Rate: Your top federal income tax bracket.") / 100
        cap_gains_tax_rate = st.slider("Capital Gains Tax Rate (%)", min_value=0, max_value=20, value=15,
                                         help="Capital Gains Tax: Tax owed on profits from selling real estate in traditional flips.") / 100

        st.markdown("---")
        st.subheader("2. Property & Acquisition")
        auction_bid = st.number_input("Auction Bid / Acquisition Cost ($)", min_value=500, value=default_bid, step=500,
                                      help="Acquisition Cost: Total cash required to win the tax deed at auction or pay back taxes.")
        expected_fmv = st.number_input("Appraised Fair Market Value (FMV) ($)", min_value=1000, value=default_fmv, step=1000,
                                       help="FMV (Fair Market Value): Independent appraised market value of raw land after 366 days.")

        st.markdown("---")
        st.subheader("3. Traditional Sale Friction")
        est_sale_price = st.number_input("Expected Open Market Sale Price ($)", min_value=1000, value=expected_fmv, step=1000)
        
        realtor_fee_pct = st.slider(
            "Realtor Commission (%)", min_value=0.0, max_value=10.0, value=6.0, step=0.5,
            help="💡 DID YOU KNOW? Realtor commissions are legally 100% negotiable! Consider DIY flat-fee options like SoldBot.com for local sales."
        ) / 100
        
        closing_costs_pct = st.slider("Closing Costs (%)", min_value=0.0, max_value=5.0, value=3.0, step=0.5) / 100
        trad_holding_costs = st.number_input("Traditional Holding Costs ($)", min_value=0, value=2500, step=250,
                                             help="Holding Costs: Property taxes, insurance, and lawn care while listing on open market.")
        sale_timeframe_months = st.slider("Expected Months to Sell", min_value=1, max_value=24, value=12)

        submit_button = st.form_submit_button(label="🔄 Calculate / Update Scenario", type="primary")

    # --- MATH ENGINE ---
    trad_realtor_fee = est_sale_price * realtor_fee_pct
    trad_closing_costs = est_sale_price * closing_costs_pct
    trad_total_friction = trad_realtor_fee + trad_closing_costs + trad_holding_costs
    trad_net_before_tax = est_sale_price - trad_total_friction
    trad_capital_gain = max(0, trad_net_before_tax - auction_bid)
    trad_cap_gains_tax = trad_capital_gain * cap_gains_tax_rate
    trad_net_cash = trad_net_before_tax - auction_bid - trad_cap_gains_tax

    mlb_out_of_pocket = auction_bid
    mlb_tax_savings = expected_fmv * marginal_tax_rate
    mlb_net_cash = mlb_tax_savings - mlb_out_of_pocket

    net_cash_delta = mlb_net_cash - trad_net_cash
    impact_leverage_ratio = expected_fmv / mlb_out_of_pocket if mlb_out_of_pocket > 0 else 0

    # --- EXECUTIVE DASHBOARD ---
    st.subheader("📊 Executive Summary")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Acquisition / Out-of-Pocket", f"${auction_bid:,.2f}")
    m2.metric("Traditional Net Cash", f"${trad_net_cash:,.2f}", delta=f"{sale_timeframe_months} Mo. Drag", delta_color="off")
    m3.metric("MLB Net Cash (Tax Shield)", f"${mlb_net_cash:,.2f}", delta=f"${net_cash_delta:+,.2f} vs. Sale", delta_color="normal" if net_cash_delta >= 0 else "off")
    m4.metric("Community Asset Created", f"${expected_fmv:,.2f}", delta=f"{impact_leverage_ratio:.1f}x Leverage", delta_color="normal")

    st.divider()

    # --- COMPARISON CARDS ---
    col_trad, col_mlb = st.columns(2)
    with col_trad:
        if trad_net_cash > mlb_net_cash and trad_net_cash > 0:
            st.success("🟢 **HIGHER NET CASH OPTION: Traditional Sale**")
        elif trad_net_cash <= 0:
            st.error("🔴 **HIGH FRICTION LOSS: Traditional Sale**")
        else:
            st.warning("🟡 **SECONDARY CASH OPTION: Traditional Sale**")

        st.markdown("### Traditional Real Estate Sale")
        st.write(f"**Gross Sale Price:** ${est_sale_price:,.2f}")
        st.write(f"• Realtor Commissions ({realtor_fee_pct*100:.1f}%): -${trad_realtor_fee:,.2f}")
        st.caption("ℹ️ *Realtor commissions are 100% negotiable! Consider DIY options like SoldBot.com for local parcels.*")
        st.write(f"• Closing Costs ({closing_costs_pct*100:.1f}%): -${trad_closing_costs:,.2f}")
        st.write(f"• Holding Costs (Taxes/Maint): -${trad_holding_costs:,.2f}")
        st.write(f"• Capital Gains Tax ({cap_gains_tax_rate*100:.1f}%): -${trad_cap_gains_tax:,.2f}")
        st.write("---")
        st.write(f"**Net Liquid Cash After Sale:** **${trad_net_cash:,.2f}**")

    with col_mlb:
        if mlb_net_cash > trad_net_cash and mlb_net_cash > 0:
            st.success("🟢 **HIGHER NET CASH OPTION: J.U.C.I.E. Mutual Land Blessing**")
        elif mlb_net_cash <= 0:
            st.warning(f"🟡 **CIVIC IMPACT FOCUS: Net Out-of-Pocket = ${abs(mlb_net_cash):,.2f}**")
        else:
            st.success("🟢 **NET CASH PROFIT + CIVIC IMPACT**")

        st.markdown("### J.U.C.I.E. Mutual Land Blessing")
        st.write(f"**Appraised FMV Donation:** ${expected_fmv:,.2f}")
        st.write("• Realtor Commissions: **$0.00**")
        st.write("• Closing Costs: **$0.00**")
        st.write("• Holding Costs ($1 NNN Lease): **$0.00** *(J.U.C.I.E. absorbs as tenant)*")
        st.write(f"• Income Tax Savings ({marginal_tax_rate*100:.1f}% Bracket): +${mlb_tax_savings:,.2f}")
        st.write("---")
        st.write(f"**Net Liquid Tax Cash Saved:** **${mlb_net_cash:,.2f}**")

    st.divider()

    # --- CIVIC IMPACT METRICS ---
    st.subheader("🌟 Hope & Civic Impact Quotient")
    sq_ft_land = (expected_fmv / 40000) * 10890
    kwh_solar_low = sq_ft_land * 0.9
    kwh_solar_peak = sq_ft_land * 1.25
    hives_capacity = int(sq_ft_land / 2500) + 1
    underwriting_hours = int(auction_bid / 250)

    q1, q2, q3, q4 = st.columns(4)
    q1.metric("School Deficit Healing", f"${expected_fmv*0.15:,.0f}")
    q2.metric("Clean Energy Range", f"{kwh_solar_low:,.0f} - {kwh_solar_peak:,.0f} kWh/yr")
    q3.metric("Pollinator Sanctuary", f"{hives_capacity} Bee Hives")
    q4.metric("Youth JRS Training", f"{underwriting_hours} Hours")

    st.divider()

    # --- CPA EXPORT ---
    st.subheader("📄 Export Briefing Summary")
    with st.expander("Click to view printable CPA Briefing Summary"):
        st.markdown(f"""
        **STRICTLY FOR TAX PREPARATION & FIDUCIARY DUE DILIGENCE**
        * **Structure:** Real Property Contribution to J.U.C.I.E. Inc. (501(c)(3) Public Charity)
        * **Acquisition Cost / Bid:** Day 1 — ${auction_bid:,.2f}
        * **Contribution Date / FMV:** Day 366 — ${expected_fmv:,.2f}
        * **Holding Period:** 366 Days (Qualifies as Long-Term Capital Gain Property)
        * **Applicable Tax Code:** IRC §170(b)(1)(C) — 30% AGI Limitation for Appreciated Capital Gain Property.
        * **Holding Cost Offset:** $1/year NNN Ground Lease executed with Tenant (J.U.C.I.E. Inc.) absorbing interim taxes/insurance.
        * **Required Attachments:** IRS Form 8283 + Qualified Independent Appraisal (Required for contributions > $5,000).
        """)

# --- TAB 2: SEARCHABLE FAQ LIBRARY ---
with tab_faq:
    st.subheader("🔍 Searchable Knowledge Base & FAQ")
    st.info("💡 **Pro-Tip for Beginners:** Type any keyword below (e.g., 'lease', 'taxes', 'appraisal') or press **Ctrl + F** (Windows) / **Cmd + F** (Mac) to search this page instantly!")
    
    faq_query = st.text_input("Type a keyword to search FAQs:", value="")
    
    faqs = [
        ("What is a $1 NNN (Triple Net) Stewardship Lease?", 
         "A Triple Net (NNN) lease means the tenant (J.U.C.I.E.) pays 100% of property taxes, insurance, and maintenance for $1/year. This freezes the donor's holding costs at $0 during the 366-day IRS seasoning period."),
        ("What is the 366-Day Seasoning Period?", 
         "To claim a Fair Market Value (FMV) deduction for appreciated real estate under IRC §170, the donor must hold legal title for more than one year (366 days) to qualify as long-term capital gain property."),
        ("What is the difference between Leased Fee Estate and Trade Fixtures?", 
         "The Leased Fee Estate is the raw land owned by the donor (which qualifies for the tax write-off). Trade Fixtures are solar panels or bee hives owned by J.U.C.I.E. which are excluded from the donor's tax deduction to prevent double-dipping."),
        ("Does a QR Code on the Certificate cost money?", 
         "No! Static QR codes are 100% free and open-source. They never expire and cost $0.00 to generate."),
        ("How does J.U.C.I.E. fund its operations if the software is free?", 
         "The calculator software is 100% free for public use. J.U.C.I.E. earns revenue through $0.35 underwritten lead feeds purchased by CPAs, which directly fund youth Roblox research bounties.")
    ]
    
    for q, a in faqs:
        if faq_query.lower() in q.lower() or faq_query.lower() in a.lower():
            with st.expander(f"❓ {q}"):
                st.write(a)

# --- TAB 3: CIVIC CERTIFICATE GENERATOR ---
with tab_cert:
    st.subheader("📜 Custom Certificate Generator")
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        steward_name = st.text_input("Steward / Donor Name", value="Jane & John Doe")
        scripture_option = st.selectbox(
            "Select Scripture / Message Wording for Certificate",
            ["Short Reference (John 4:13)", "Full Quote (John 4:13-14)", "Full Quote + Founder Reflection", "Secular / Civic Wording Only"]
        )
    with col_c2:
        st.write(f"**Out-of-Pocket Investment:** ${auction_bid:,.2f}")
        st.write(f"**Community Value Restored:** ${expected_fmv:,.2f}")
        st.write(f"**Civic Multiplier:** {impact_leverage_ratio:.1f}x Leverage")

    st.success("✅ Certificate Ready! The tool automatically generates your printable digital certificate complete with donor ROI metrics and free QR code verification.")

# --- DOUBLE-OPT-IN SPIRITUAL ANCHOR (JOHN 4:13) ---
st.divider()
with st.expander("🧠 Curious about the system design? Discover where this liquidity model originated."):
    st.markdown(
        """
        <div style="text-align: center; padding: 20px; background-color: #f0f4f8; border-radius: 10px; border-left: 4px solid #1f77b4;">
            <p style="font-size: 16px; font-style: italic; color: #2c3e50; margin-bottom: 8px;">
                "Jesus answered, 'Everyone who drinks this water will be thirsty again, but whoever drinks the water I give them will never thirst.'"
            </p>
            <p style="font-size: 14px; font-weight: bold; color: #1f77b4; margin-bottom: 12px;">— JOHN 4:13–14</p>
            <p style="font-size: 12px; color: #555; line-height: 1.5;">
                Financial liquidity sustains temporal operations, but no portfolio yield can permanently satisfy the human heart. 
                As we steward earthly land and restore communities today, we give all credit to God and anchor our ultimate hope in His grace.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")
st.success("### 🌟 CALL TO HOPE: DONATE. SAVE. RESTORE.")
st.markdown("Join the movement turning distressed municipal tax debt into permanent community wealth, local school funding, and clean energy!")
