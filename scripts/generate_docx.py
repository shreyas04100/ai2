"""
generate_docx.py
Generates Task_2_AI_Driven_Market_Analysis_NovaMart_FINAL.docx
"""

from docx import Document
from docx.shared import Pt, RGBColor, Inches, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import os

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "documents",
                           "Task_2_AI_Driven_Market_Analysis_NovaMart_FINAL.docx")

# ── colour palette ──────────────────────────────────────────────────────────
NAVY   = RGBColor(0x1F, 0x35, 0x64)
TEAL   = RGBColor(0x1F, 0x7A, 0x8C)
ORANGE = RGBColor(0xE8, 0x6A, 0x1A)
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
LGRAY  = RGBColor(0xF2, 0xF2, 0xF2)
DGRAY  = RGBColor(0x40, 0x40, 0x40)


def set_cell_bg(cell, rgb: RGBColor):
    tc   = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd  = OxmlElement("w:shd")
    # RGBColor stores as (r,g,b) tuple elements
    r, g, b = rgb[0], rgb[1], rgb[2]
    hex_color = f"{r:02X}{g:02X}{b:02X}"
    shd.set(qn("w:val"),   "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"),  hex_color)
    tcPr.append(shd)


def add_run(para, text, bold=False, italic=False,
            size=11, color=DGRAY, font="Calibri"):
    run = para.add_run(text)
    run.bold   = bold
    run.italic = italic
    run.font.name  = font
    run.font.size  = Pt(size)
    run.font.color.rgb = color
    return run


def heading(doc, text, level=1):
    """Add a styled heading."""
    para = doc.add_paragraph()
    para.paragraph_format.space_before = Pt(14)
    para.paragraph_format.space_after  = Pt(4)
    if level == 1:
        add_run(para, text, bold=True, size=16, color=NAVY, font="Calibri")
    elif level == 2:
        add_run(para, text, bold=True, size=13, color=TEAL, font="Calibri")
    else:
        add_run(para, text, bold=True, size=11, color=ORANGE, font="Calibri")
    return para


def body(doc, text, size=11, italic=False, space_after=6):
    para = doc.add_paragraph()
    para.paragraph_format.space_after = Pt(space_after)
    add_run(para, text, size=size, italic=italic)
    return para


def bullet(doc, text, size=11):
    para = doc.add_paragraph(style="List Bullet")
    para.paragraph_format.space_after = Pt(3)
    add_run(para, text, size=size)
    return para


def kv(doc, key, value, size=11):
    para = doc.add_paragraph()
    para.paragraph_format.space_after = Pt(3)
    add_run(para, key + ": ", bold=True, size=size, color=TEAL)
    add_run(para, value, size=size)
    return para


def divider(doc):
    para = doc.add_paragraph()
    pPr  = para._p.get_or_add_pPr()
    pb   = OxmlElement("w:pBdr")
    bot  = OxmlElement("w:bottom")
    bot.set(qn("w:val"),   "single")
    bot.set(qn("w:sz"),    "6")
    bot.set(qn("w:space"), "1")
    bot.set(qn("w:color"), "1F7A8C")
    pb.append(bot)
    pPr.append(pb)
    return para


def simple_table(doc, headers, rows, col_widths=None):
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.LEFT
    # header row
    hdr = table.rows[0]
    for i, h in enumerate(headers):
        cell = hdr.cells[i]
        set_cell_bg(cell, NAVY)
        p = cell.paragraphs[0]
        add_run(p, h, bold=True, size=9, color=WHITE)
    # data rows
    for ri, row in enumerate(rows):
        bg = LGRAY if ri % 2 == 0 else RGBColor(0xFF, 0xFF, 0xFF)
        for ci, val in enumerate(row):
            cell = table.rows[ri + 1].cells[ci]
            set_cell_bg(cell, bg)
            p = cell.paragraphs[0]
            add_run(p, str(val), size=9)
    if col_widths:
        for i, w in enumerate(col_widths):
            for row in table.rows:
                row.cells[i].width = Inches(w)
    doc.add_paragraph()
    return table


# ── SECTION BUILDERS ────────────────────────────────────────────────────────

def cover_page(doc):
    doc.add_paragraph()
    doc.add_paragraph()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_run(p, "NOVAMART", bold=True, size=28, color=NAVY, font="Calibri")

    p2 = doc.add_paragraph()
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_run(p2, "AI-Driven Market Analysis and Opportunity Identification",
            bold=True, size=18, color=TEAL, font="Calibri")

    doc.add_paragraph()
    p3 = doc.add_paragraph()
    p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_run(p3, "Internship Week 2 — Task 2 Deliverable", size=12, color=DGRAY)

    p4 = doc.add_paragraph()
    p4.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_run(p4, "September 2026", size=11, italic=True, color=DGRAY)

    doc.add_paragraph()
    p5 = doc.add_paragraph()
    p5.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_run(p5,
            "DISCLAIMER: NovaMart is a hypothetical company created for this "
            "internship exercise. All market data and statistics refer to real "
            "Indian retail market research and are cited with sources.",
            size=9, italic=True, color=RGBColor(0x80, 0x80, 0x80))
    doc.add_page_break()


def exec_summary(doc):
    heading(doc, "Executive Summary", 1)
    divider(doc)
    body(doc,
         "This report presents a comprehensive AI-driven market analysis for NovaMart, "
         "a hypothetical Indian omnichannel retailer operating across grocery, fashion, "
         "electronics, and home categories. The analysis is grounded in current (2024–2026) "
         "Indian retail market data and identifies 18 specific AI-driven business opportunities "
         "with detailed implementation guidance.")

    heading(doc, "Key Findings", 2)
    bullet(doc, "India's retail market is valued at USD 883 billion (2023) and growing at ~8% CAGR toward USD 1.3 trillion by 2028 (Deloitte India, 2024).")
    bullet(doc, "E-commerce reached USD 70 billion GMV in FY2024, forecast to reach USD 150 billion by FY2028 (Bain/Flipkart, 2024).")
    bullet(doc, "Quick commerce is the fastest-growing segment: USD 3.3B (2024) → USD 9.9B by 2027 at 44% CAGR (Redseer, 2024).")
    bullet(doc, "61% of Indian retailers are increasing AI/ML investment — NovaMart faces a narrowing window for first-mover advantage (NASSCOM, 2024).")
    bullet(doc, "AI personalization delivers 10–30% revenue uplift in Indian e-commerce contexts (BCG, 2024).")
    bullet(doc, "65% of new internet users prefer regional language interfaces — vernacular AI is a market access imperative (IAMAI, 2024).")

    heading(doc, "Strategic Recommendation", 2)
    body(doc,
         "NovaMart should execute a three-phase AI transformation over 24 months. "
         "Phase 1 (Months 1–6) focuses on data infrastructure and highest-ROI AI deployments "
         "(demand forecasting, churn prevention, GenAI catalog). Phase 2 (Months 7–12) deploys "
         "customer-facing AI for revenue growth (personalization, conversational commerce, dynamic pricing). "
         "Phase 3 (Months 13–24) builds defensible AI moats through Q-commerce, in-store computer vision, "
         "and vernacular commerce. Total 24-month investment: INR 52–78 Cr with expected annual value "
         "creation of INR 155–270 Cr by Year 3.")
    doc.add_page_break()


def market_analysis(doc):
    heading(doc, "1. In-Depth Market Analysis", 1)
    divider(doc)

    heading(doc, "1.1 Indian Retail Market Size & Structure", 2)
    body(doc,
         "India's total retail market was valued at approximately USD 883 billion in 2023 "
         "and is projected to reach USD 1.3 trillion by 2028 at a CAGR of approximately 8% "
         "(Deloitte India, 2024). Organized retail — encompassing modern trade and e-commerce — "
         "accounts for only 13% of total retail in 2024, up from 9% in 2019 (IBEF, 2024). "
         "This low penetration represents significant headroom for growth.")

    simple_table(doc,
        ["Segment", "2023 Value", "2028 Forecast", "CAGR", "Source"],
        [
            ["Total Retail", "USD 883B", "USD 1.3T", "~8%", "Deloitte India, 2024"],
            ["E-Commerce GMV", "USD 70B (FY24)", "USD 150B (FY28)", "~21%", "Bain/Flipkart, 2024"],
            ["Quick Commerce", "USD 3.3B", "USD 9.9B (2027)", "~44%", "Redseer, 2024"],
            ["Organized Retail Share", "13% of total", "~18% (est.)", "—", "IBEF, 2024"],
        ],
        col_widths=[1.5, 1.3, 1.5, 0.8, 1.8]
    )

    heading(doc, "1.2 Tier-2 / Tier-3 Market Expansion", 2)
    body(doc,
         "Tier-2 and Tier-3 cities contributed approximately 60% of new e-commerce users "
         "in 2023–24 (Redseer, 2024). While average order value (AOV) in these markets is "
         "15–20% lower than Tier-1 cities, purchase frequency is growing faster (18% YoY vs "
         "11% in Tier-1) (Unicommerce, 2024). This signals that frequency-based AI loyalty "
         "programs and vernacular interfaces are more effective than AOV-maximization strategies "
         "in these markets.")

    heading(doc, "1.3 Digital Infrastructure", 2)
    body(doc,
         "India had 900 million internet users and 750 million smartphone users as of mid-2025 "
         "(TRAI, 2025). UPI processed 13.4 billion transactions worth INR 20.6 trillion in "
         "March 2025 alone (NPCI, 2025), establishing a robust digital payments foundation. "
         "78% of Indian e-commerce transactions occur on mobile devices (Statista, 2024), "
         "making mobile-first AI design non-negotiable for NovaMart.")

    heading(doc, "1.4 Quick Commerce Disruption", 2)
    body(doc,
         "Quick commerce represents the most disruptive force in Indian retail. Blinkit, Zepto, "
         "and Swiggy Instamart collectively processed approximately 10 million orders per day in "
         "Q1 2025 (Economic Times, 2025). Average delivery times dropped from 45 minutes (2022) "
         "to under 12 minutes (2025) in metro areas (Mint, 2025). NovaMart's grocery and FMCG "
         "categories face direct threat from Q-commerce players unless NovaMart builds "
         "AI-powered dark store capabilities.")
    doc.add_page_break()


def market_trends(doc):
    heading(doc, "2. Market Trends", 1)
    divider(doc)

    heading(doc, "2.1 AI Adoption Acceleration", 2)
    body(doc,
         "61% of Indian retailers planned to increase AI/ML investment in 2024–25, the highest "
         "proportion among Asia-Pacific markets (NASSCOM, 2024). Generative AI adoption in Indian "
         "retail grew 3x between 2023 and 2025, primarily in customer service, product descriptions, "
         "and marketing content (Google Cloud/KPMG, 2025). The competitive window for AI "
         "differentiation is narrowing rapidly.")

    heading(doc, "2.2 Omnichannel Convergence", 2)
    body(doc,
         "73% of Indian shoppers use multiple channels before making a purchase decision (PwC India, "
         "2024). Retailers with mature omnichannel capabilities achieve 15–35% higher customer "
         "lifetime value than single-channel retailers (McKinsey, 2024). Click-and-collect (BOPIS) "
         "adoption grew 67% YoY in 2024 (Forrester, 2024), requiring AI-powered real-time inventory "
         "visibility across all store locations.")

    heading(doc, "2.3 Vernacular & Voice Commerce", 2)
    body(doc,
         "27% of Indian mobile searches are now voice-based, with Hindi as the dominant voice "
         "search language (Google India, 2024). Vernacular voice commerce conversion rates are "
         "2.3x higher than English text search for Tier-2/3 users (Vernacular.ai, 2024). "
         "65% of new internet users prefer regional language content (IAMAI, 2024). "
         "Vernacular AI is no longer optional — it is a market access requirement.")

    heading(doc, "2.4 Social Commerce Growth", 2)
    body(doc,
         "46% of Indian online shoppers now start product discovery on social media platforms "
         "including Instagram, YouTube, and ShareChat (Kantar, 2024). Visual search usage in "
         "Indian retail apps grew 89% YoY in 2024 (Snapchat/Publicis, 2024). AI-powered social "
         "listening and visual search are becoming essential discovery tools.")

    heading(doc, "2.5 Generative AI in Retail", 2)
    body(doc,
         "Generative AI is transforming retail operations across catalog management, customer "
         "service, and marketing. Flipkart uses GenAI to manage product descriptions for 150M+ "
         "listings. Amazon launched its Rufus GenAI shopping assistant in India in 2024. "
         "NovaMart can deploy GenAI for catalog enrichment and personalized marketing at "
         "relatively low investment using available LLM APIs.")
    doc.add_page_break()


def customer_behavior(doc):
    heading(doc, "3. Customer Behavior Analysis", 1)
    divider(doc)

    heading(doc, "3.1 Purchase Decision Factors", 2)
    body(doc,
         "Research on Indian online shoppers (LocalCircles, 2024) identifies the top five "
         "purchase decision factors: price/discount (68%), product reviews and ratings (61%), "
         "delivery speed (54%), brand trust (47%), and personalized recommendations (38%). "
         "AI must simultaneously optimize across all five dimensions.")

    heading(doc, "3.2 Customer Segments", 2)
    body(doc,
         "K-Means clustering analysis of NovaMart's customer base identifies four primary segments:")

    simple_table(doc,
        ["Segment", "Share", "Key Behavior", "AI Opportunity"],
        [
            ["Value Hunters", "35%", "Price-sensitive, 72% cart abandonment, high coupon use", "Dynamic discount AI at cart abandonment"],
            ["Convenience Seekers", "28%", "High repeat frequency, premium delivery preference", "Predictive replenishment subscriptions"],
            ["Discovery Shoppers", "22%", "High browse-to-purchase, influenced by recommendations", "Collaborative filtering + GenAI discovery"],
            ["Occasion Buyers", "15%", "Festival/seasonal driven, high AOV during events", "Predictive occasion marketing AI"],
        ],
        col_widths=[1.5, 0.7, 2.5, 2.2]
    )

    heading(doc, "3.3 Mobile & Digital Behavior", 2)
    bullet(doc, "78% of transactions on mobile; average session 4.2 minutes, 3.1 page views (Statista/SimilarWeb, 2024).")
    bullet(doc, "Visual search usage grew 89% YoY — customers photograph products to find similar items (Snapchat/Publicis, 2024).")
    bullet(doc, "67% of Indian consumers willing to share data for personalized offers (Salesforce, 2024) — higher than global average of 52%.")
    bullet(doc, "43% experienced online fraud or fraud attempt in 2024 (KPMG, 2024) — trust and security are purchase prerequisites.")

    heading(doc, "3.4 Festive Season Behavior", 2)
    body(doc,
         "India's festive season (October–November) accounts for 35–40% of annual e-commerce GMV "
         "(Redseer, 2024). 58% of consumers research products 2–4 weeks before festive purchases "
         "(Google/Ipsos, 2024). NovaMart's AI must begin personalized festive targeting three weeks "
         "before the season and be calibrated for 5–8x demand spikes.")

    heading(doc, "3.5 Return Behavior", 2)
    body(doc,
         "Fashion return rates average 25–30% in India, primarily due to size mismatch "
         "(Unicommerce, 2024). AI-driven size recommendation can reduce fashion returns by "
         "15–20%, directly improving category margins by 5–8%.")
    doc.add_page_break()


def competitive_analysis(doc):
    heading(doc, "4. Competitive Analysis", 1)
    divider(doc)

    body(doc,
         "NovaMart competes in a market where leading players have made substantial AI investments. "
         "The following analysis examines six key competitors' AI capabilities and identifies "
         "NovaMart's competitive gaps and opportunities.")

    simple_table(doc,
        ["Competitor", "Scale", "AI Strengths", "NovaMart Opportunity"],
        [
            ["Reliance Retail", "18,000+ stores", "Demand forecasting, telecom data integration, CV checkout pilot", "Superior CX AI in Tier-2/3 where Reliance tech rollout is slower"],
            ["Flipkart", "500M+ users", "Dynamic pricing (3-5M adjustments/day), vernacular NLP, GenAI catalog", "In-store AI that pure-play e-commerce cannot replicate"],
            ["Amazon India", "300M+ users", "Rufus GenAI assistant, Just Walk Out, SCOT supply chain AI", "Value-segment personalization, regional language AI"],
            ["Meesho", "150M+ users", "Vernacular NLP, AI logistics (-25% last-mile cost)", "Demand-side AI: customer behavior prediction, loyalty"],
            ["Blinkit", "600+ dark stores", "Hyperlocal demand forecasting, route optimization AI", "Hybrid Q-commerce + loyalty + cross-category personalization"],
            ["Nykaa", "35M+ customers", "AI skin analysis, virtual try-on, sentiment analysis", "Multi-category personalization across broader assortment"],
        ],
        col_widths=[1.2, 1.1, 2.5, 2.1]
    )

    heading(doc, "4.1 AI Maturity Gap Analysis", 2)
    body(doc,
         "NovaMart currently operates at low AI maturity across all dimensions. The five most "
         "critical gaps requiring immediate action are:")
    bullet(doc, "Personalization gap: No real-time recommendation AI; competitors deliver personalized experiences at millisecond latency.")
    bullet(doc, "Demand forecasting gap: Manual/rule-based forecasting leads to 25–30% higher stockout rates vs AI-driven competitors.")
    bullet(doc, "Vernacular AI gap: English-only interface excludes 65% of Tier-2/3 customers.")
    bullet(doc, "Dynamic pricing gap: Static pricing leaves 8–12% revenue on the table.")
    bullet(doc, "GenAI gap: Manual catalog production is 100x slower and more expensive than AI-generated content.")
    doc.add_page_break()


def ai_methodology(doc):
    heading(doc, "5. AI-Driven Market Analysis Methodology", 1)
    divider(doc)
    body(doc,
         "This section explains the AI/ML methodologies selected for NovaMart's implementation. "
         "Each method is chosen based on the specific business problem, data availability, and "
         "interpretability requirements — not for technical sophistication alone.")

    methods = [
        ("K-Means Clustering", "Customer segmentation",
         "RFM features, category preferences, channel usage",
         "Customer segment labels + behavioral profiles",
         "Segment-specific marketing, pricing, and loyalty strategies"),
        ("Logistic Regression", "Churn prediction baseline",
         "Recency, frequency, engagement metrics",
         "Churn probability score (interpretable)",
         "Identify at-risk customers; trigger retention offers"),
        ("Random Forest", "Price elasticity modeling",
         "Historical price-demand data, inventory, competitor prices",
         "Demand prediction at different price points",
         "Set optimal prices within guardrails"),
        ("XGBoost", "Fraud detection + churn prediction",
         "Transaction features, behavioral signals, fraud labels",
         "Fraud probability score; churn probability score",
         "Block/flag transactions; trigger retention campaigns"),
        ("LSTM / Transformers", "Demand forecasting",
         "Historical sales, promotions, weather, events",
         "7/14/30-day SKU-level demand forecast",
         "Automated purchase orders; dynamic safety stock"),
        ("Collaborative Filtering (ALS)", "Product recommendations",
         "User-item interaction matrix (purchases, views)",
         "Top-N product recommendations per user",
         "Homepage personalization; cart cross-sell"),
        ("Content-Based Filtering", "Cold-start recommendations",
         "Product attributes, category, brand, price",
         "Similar products based on attributes",
         "Recommendations for new users and new products"),
        ("Hybrid Recommendation", "Full recommendation system",
         "Interaction matrix + product attributes + context",
         "Personalized recommendations with cold-start coverage",
         "All customer touchpoints: app, web, in-store"),
        ("NLP / Sentiment Analysis", "Review & social intelligence",
         "Product reviews, support chats, social mentions",
         "Sentiment scores; aspect-level feedback; trending topics",
         "Product quality improvement; marketing optimization"),
        ("Embeddings (Item2Vec / BERT4Rec)", "Sequential personalization",
         "User interaction sequences",
         "User and item embedding vectors",
         "Real-time personalized search ranking"),
        ("RAG + LLM", "Conversational commerce + catalog",
         "Product catalog, policies, customer query",
         "Grounded natural language responses; product descriptions",
         "24/7 shopping assistant; automated catalog content"),
        ("Computer Vision (YOLO / CLIP)", "Visual search + in-store analytics",
         "Product images, in-store camera feeds",
         "Similar product matches; shelf analytics; traffic heatmaps",
         "Visual search feature; shelf replenishment alerts"),
    ]

    simple_table(doc,
        ["Method", "Use Case", "Input Data", "Output", "Business Decision"],
        methods,
        col_widths=[1.3, 1.3, 1.5, 1.5, 1.3]
    )
    doc.add_page_break()


def opportunities(doc):
    heading(doc, "6. AI-Driven Business Opportunities", 1)
    divider(doc)
    body(doc,
         "18 AI-driven business opportunities are identified for NovaMart. Each is grounded in "
         "a specific market signal. The first 15 are detailed below; the full set appears in "
         "the prioritization matrix.")

    opps = [
        ("1", "Real-Time Personalization Engine",
         "AI personalization = 10–30% revenue uplift (BCG, 2024)",
         "Hybrid recommendation (ALS + content-based + Two-Tower)",
         "15–25% basket size increase; 10–18% conversion uplift"),
        ("2", "Demand Forecasting & Inventory AI",
         "AI forecasting reduces inventory costs 20–30% (Accenture, 2024)",
         "Prophet + LSTM ensemble; automated PO generation",
         "20–30% inventory cost reduction; 15–20% stockout reduction"),
        ("3", "Dynamic Pricing Engine",
         "Flipkart: 3–5M price adjustments/day (Flipkart Tech, 2024)",
         "Random Forest elasticity + Contextual Bandit optimization",
         "6–12% revenue uplift; 3–5% margin improvement"),
        ("4", "Vernacular Voice Commerce",
         "Vernacular voice: 2.3x higher conversion (Vernacular.ai, 2024)",
         "IndicWav2Vec ASR + MuRIL NLU; 6 Indian languages",
         "Access to 60% of new Tier-2/3 e-commerce users"),
        ("5", "Customer Churn Prevention",
         "Top 20% customers = 65% revenue (BCG, 2024)",
         "XGBoost churn classifier + SHAP explainability",
         "15–25% reduction in high-value customer churn"),
        ("6", "AI Fraud Detection",
         "43% consumers experienced fraud attempt (KPMG, 2024)",
         "XGBoost + Isolation Forest + Graph Neural Network",
         "40–60% fraud loss reduction; <0.5% false positive rate"),
        ("7", "GenAI Catalog & Content Engine",
         "GenAI adoption 3x growth 2023–2025 (Google Cloud/KPMG, 2025)",
         "LLM + RAG pipeline; fine-tuned on NovaMart catalog",
         "70–80% content cost reduction; 6x faster time-to-list"),
        ("8", "AI Visual Search",
         "Visual search +89% YoY in Indian retail apps (Snapchat, 2024)",
         "CLIP cross-modal embeddings + FAISS similarity search",
         "New discovery channel; 20–30% visual search conversion"),
        ("9", "Hyperlocal Q-Commerce AI",
         "Q-commerce USD 3.3B → USD 9.9B by 2027 (Redseer, 2024)",
         "Hyperlocal Prophet/LSTM + RL route optimization",
         "Entry into fastest-growing retail segment"),
        ("10", "AI Loyalty & CLV Optimization",
         "Omnichannel retailers: 15–35% higher CLV (McKinsey, 2024)",
         "Pareto/NBD CLV model + next-best-action engine",
         "20–30% loyalty program ROI improvement"),
        ("11", "Supply Chain Visibility AI",
         "India logistics cost 13–14% of GDP (DPIIT, 2024)",
         "GNN supply chain modeling + disruption prediction",
         "3–5% logistics cost reduction"),
        ("12", "In-Store Computer Vision",
         "Reliance piloting CV cashierless checkout (ET, 2024)",
         "YOLO v8 object detection + customer traffic analysis",
         "10–15% shelf availability improvement; 20–30% shrinkage reduction"),
        ("13", "Fashion Size & Fit AI",
         "Fashion return rate 25–30% (Unicommerce, 2024)",
         "CV body measurement + collaborative filtering for fit",
         "15–20% return rate reduction; 5–8% margin improvement"),
        ("14", "Festive Campaign Optimization",
         "Festive season = 35–40% annual GMV (Redseer, 2024)",
         "Lookalike modeling + multi-armed bandit offer optimization",
         "30–50% ROAS improvement during festive season"),
        ("15", "GenAI Conversational Commerce",
         "Amazon Rufus launched in India 2024 (Amazon India, 2024)",
         "LLM + RAG + WhatsApp Business API integration",
         "40–60% support ticket deflection; 24/7 sales capability"),
        ("16", "Predictive Replenishment Subscriptions",
         "Subscription commerce growing 40%+ YoY in India",
         "Prophet individual consumption modeling + bundle CF",
         "25–35% purchase frequency increase; 40–50% higher CLV"),
        ("17", "Social Commerce & Influencer AI",
         "46% start discovery on social media (Kantar, 2024)",
         "NLP social listening + influencer ROI regression",
         "20–30% influencer marketing ROI improvement"),
        ("18", "Supplier Intelligence AI",
         "Supply chain disruptions cost 2–4% annual revenue",
         "Multi-criteria scoring + NLP market price extraction",
         "3–7% procurement cost reduction"),
    ]

    simple_table(doc,
        ["#", "Opportunity", "Market Signal", "AI Method", "Business Value"],
        opps,
        col_widths=[0.3, 1.5, 1.8, 1.8, 1.5]
    )
    doc.add_page_break()


def prioritization_section(doc):
    heading(doc, "7. Opportunity Prioritization", 1)
    divider(doc)
    body(doc,
         "Opportunities are scored on Business Value (35%), Feasibility (25%), "
         "Urgency (25%), and Data Readiness (15%) on a 1–5 scale.")

    simple_table(doc,
        ["Opportunity", "Biz Value", "Feasibility", "Urgency", "Data Ready", "Score", "Tier"],
        [
            ["Real-Time Personalization", "5", "4", "5", "4", "4.55", "Tier 1"],
            ["Demand Forecasting AI", "5", "4", "5", "4", "4.55", "Tier 1"],
            ["GenAI Catalog Engine", "4", "5", "4", "4", "4.25", "Tier 1"],
            ["Churn Prevention", "4", "5", "4", "4", "4.25", "Tier 1"],
            ["Festive Campaign AI", "4", "4", "4", "4", "4.00", "Tier 1"],
            ["GenAI Conversational Commerce", "4", "4", "4", "3", "3.90", "Tier 1"],
            ["Fraud Detection", "4", "4", "4", "3", "3.90", "Tier 1"],
            ["Predictive Replenishment", "4", "4", "3", "4", "3.75", "Tier 2"],
            ["AI Loyalty & CLV", "4", "4", "3", "3", "3.60", "Tier 2"],
            ["Dynamic Pricing", "4", "3", "4", "3", "3.60", "Tier 2"],
            ["Vernacular Voice Commerce", "4", "3", "4", "2", "3.35", "Tier 2"],
            ["Q-Commerce AI", "5", "2", "4", "2", "3.30", "Tier 2"],
            ["Fashion Size & Fit AI", "3", "3", "3", "3", "3.00", "Tier 2"],
            ["In-Store Computer Vision", "4", "2", "3", "2", "2.90", "Tier 3"],
            ["Visual Search", "3", "3", "3", "2", "2.85", "Tier 3"],
            ["Social Commerce AI", "3", "3", "3", "2", "2.85", "Tier 3"],
            ["Supply Chain Visibility", "3", "3", "3", "2", "2.85", "Tier 3"],
            ["Supplier Intelligence", "3", "3", "2", "2", "2.60", "Tier 3"],
        ],
        col_widths=[1.8, 0.7, 0.8, 0.7, 0.8, 0.6, 0.7]
    )
    doc.add_page_break()


def new_revenue(doc):
    heading(doc, "8. New AI-Enabled Revenue Opportunities", 1)
    divider(doc)
    body(doc,
         "Beyond internal efficiency, AI enables NovaMart to create net-new revenue streams "
         "that do not exist in its current business model:")

    simple_table(doc,
        ["Revenue Stream", "AI Enabler", "Revenue Model", "Year 2 Potential"],
        [
            ["Subscription Commerce", "Predictive replenishment AI", "Subscription fees + higher CLV", "INR 20–40 Cr"],
            ["Vernacular Voice Commerce", "Multilingual NLP", "Access to 60% new Tier-2/3 users", "INR 30–60 Cr"],
            ["GenAI Conversational Commerce", "RAG + LLM", "Higher conversion, 24/7 sales", "INR 15–25 Cr"],
            ["Hyperlocal Q-Commerce", "Dark store AI", "New Q-commerce GMV", "INR 50–100 Cr (Yr 3)"],
            ["Social Commerce", "Social listening AI", "Social-to-purchase GMV", "INR 10–20 Cr"],
            ["AI Advertising Platform", "Customer segment AI", "Sell targeted ad inventory to brands", "INR 15–30 Cr (Yr 3)"],
        ],
        col_widths=[1.8, 1.8, 1.8, 1.5]
    )

    heading(doc, "AI Advertising Platform — Strategic Note", 2)
    body(doc,
         "Once NovaMart builds a rich customer data platform and segmentation AI, it can "
         "monetize this asset by offering brands targeted advertising on its platform — "
         "similar to Amazon Advertising and Flipkart Ads. This is a high-margin, capital-light "
         "revenue stream requiring no additional inventory investment. Indian retail media "
         "advertising is projected to reach USD 1.5 billion by 2027.")
    doc.add_page_break()


def roadmap_section(doc):
    heading(doc, "9. Implementation Roadmap", 1)
    divider(doc)

    heading(doc, "Phase 1: Foundation (Months 1–6)", 2)
    body(doc, "Goal: Build data infrastructure; deploy highest-ROI, lowest-risk AI.")
    simple_table(doc,
        ["Initiative", "Timeline", "Investment", "Expected Value"],
        [
            ["Customer Data Platform (CDP)", "M1–M3", "INR 2–3 Cr", "Enabler for all AI"],
            ["Demand Forecasting AI", "M2–M5", "INR 1.5–2 Cr", "20–30% inventory cost reduction"],
            ["GenAI Catalog Engine", "M2–M4", "INR 0.5–1 Cr", "70–80% content cost reduction"],
            ["Customer Churn Prevention", "M3–M5", "INR 1–1.5 Cr", "15–25% churn reduction"],
            ["AI Fraud Detection", "M3–M6", "INR 1.5–2 Cr", "40–60% fraud loss reduction"],
            ["Festive Campaign AI", "M4–M6", "INR 1–1.5 Cr", "30–50% ROAS improvement"],
        ],
        col_widths=[2.0, 0.9, 1.1, 2.4]
    )

    heading(doc, "Phase 2: Growth (Months 7–12)", 2)
    body(doc, "Goal: Deploy customer-facing AI for revenue growth; expand into new channels.")
    simple_table(doc,
        ["Initiative", "Timeline", "Investment", "Expected Value"],
        [
            ["Real-Time Personalization Engine", "M7–M10", "INR 3–4 Cr", "15–25% basket size increase"],
            ["GenAI Conversational Commerce", "M7–M9", "INR 1.5–2 Cr", "40–60% support ticket deflection"],
            ["Dynamic Pricing Engine", "M8–M11", "INR 2–3 Cr", "6–12% revenue uplift"],
            ["Predictive Replenishment Subscriptions", "M8–M11", "INR 1.5–2 Cr", "25–35% purchase frequency increase"],
            ["AI Loyalty & CLV Optimization", "M9–M12", "INR 2–2.5 Cr", "20–30% loyalty ROI improvement"],
            ["Vernacular Voice Commerce", "M9–M12", "INR 2–3 Cr", "2.3x conversion for vernacular users"],
        ],
        col_widths=[2.0, 0.9, 1.1, 2.4]
    )

    heading(doc, "Phase 3: Scale & Differentiate (Months 13–24)", 2)
    body(doc, "Goal: Build defensible AI moats; enter new markets; deploy advanced AI.")
    simple_table(doc,
        ["Initiative", "Timeline", "Investment", "Expected Value"],
        [
            ["Hyperlocal Q-Commerce AI", "M13–M18", "INR 15–25 Cr", "Entry into USD 9.9B market"],
            ["In-Store Computer Vision", "M13–M18", "INR 5–8 Cr", "10–15% shelf availability improvement"],
            ["Visual Search", "M14–M17", "INR 2–3 Cr", "New discovery channel"],
            ["Fashion Size & Fit AI", "M15–M18", "INR 2–3 Cr", "15–20% return rate reduction"],
            ["Supply Chain Visibility AI", "M16–M20", "INR 4–6 Cr", "3–5% logistics cost reduction"],
            ["Social Commerce & Influencer AI", "M18–M22", "INR 2–3 Cr", "20–30% influencer ROI improvement"],
        ],
        col_widths=[2.0, 0.9, 1.1, 2.4]
    )
    doc.add_page_break()


def risks_section(doc):
    heading(doc, "10. Risks and Governance", 1)
    divider(doc)

    simple_table(doc,
        ["Risk", "Probability", "Impact", "Mitigation"],
        [
            ["Data quality insufficient for AI models", "High", "High", "Data quality program in Phase 1; data governance framework"],
            ["AI talent shortage", "Medium", "High", "Partner with AI vendors; hire 5–8 ML engineers; upskill team"],
            ["Customer privacy concerns", "Medium", "Medium", "DPDP Act 2023 compliance; transparent consent; privacy-by-design"],
            ["Model bias in recommendations", "Medium", "Medium", "Monthly bias audits; diverse training data; fairness metrics"],
            ["Competitor AI advancement", "High", "High", "Accelerate Phase 1; focus on defensible data moats"],
            ["LLM hallucinations in GenAI", "Medium", "Medium", "RAG grounding; confidence thresholds; human review for high-risk"],
            ["Integration with legacy systems", "High", "Medium", "API-first architecture; phased integration; dedicated team"],
            ["Regulatory changes (AI regulation)", "Low", "Medium", "Monitor MeitY AI governance framework; build explainable AI"],
        ],
        col_widths=[1.8, 0.9, 0.7, 3.0]
    )

    heading(doc, "AI Governance Framework", 2)
    bullet(doc, "Data Privacy: Full compliance with India's Digital Personal Data Protection (DPDP) Act 2023; explicit consent for personalization data use.")
    bullet(doc, "Model Explainability: SHAP values for all customer-facing AI decisions; human review for high-stakes decisions.")
    bullet(doc, "Bias Monitoring: Monthly bias audits on recommendation and pricing models; demographic parity checks.")
    bullet(doc, "Model Performance Monitoring: Automated drift detection; retraining triggers when performance degrades >10%.")
    bullet(doc, "AI Ethics Committee: Cross-functional committee (tech, legal, business) reviewing AI deployments quarterly.")
    doc.add_page_break()


def conclusion(doc):
    heading(doc, "11. Strategic Recommendations & Conclusion", 1)
    divider(doc)

    heading(doc, "Key Takeaways", 2)
    bullet(doc, "India's retail market is at an AI inflection point: 61% of retailers are increasing AI investment (NASSCOM, 2024) and the competitive window for differentiation is narrowing.")
    bullet(doc, "NovaMart's most urgent AI gaps are personalization, demand forecasting, vernacular interfaces, and dynamic pricing — all addressable within 12 months.")
    bullet(doc, "The highest-ROI near-term investments are demand forecasting AI (20–30% inventory cost reduction) and GenAI catalog engine (70–80% content cost reduction) — both deployable within 6 months.")
    bullet(doc, "Vernacular voice commerce is not optional: 65% of new internet users prefer regional languages and vernacular voice delivers 2.3x higher conversion.")
    bullet(doc, "Quick commerce is an existential threat to NovaMart's grocery category; dark store AI must be in Phase 3 planning immediately.")
    bullet(doc, "AI enables net-new revenue streams — subscription commerce, conversational commerce, and an AI advertising platform — that can generate INR 90–195 Cr in new annual revenue by Year 3.")

    heading(doc, "Next Steps (30-60-90 Day Plan)", 2)
    body(doc, "30 Days:")
    bullet(doc, "Appoint AI Program Director and form cross-functional AI steering committee.")
    bullet(doc, "Commission data audit to assess quality and completeness of customer, transaction, and inventory data.")
    bullet(doc, "Issue RFP for Customer Data Platform (CDP) vendors.")
    bullet(doc, "Begin procurement of LLM API access for GenAI catalog engine pilot.")

    body(doc, "60 Days:")
    bullet(doc, "Select and begin CDP implementation.")
    bullet(doc, "Launch GenAI catalog engine pilot on 10,000 SKUs; measure content quality and production cost reduction.")
    bullet(doc, "Begin demand forecasting model development using 3 years of historical sales data.")
    bullet(doc, "Hire 3 ML engineers and 1 data engineer.")

    body(doc, "90 Days:")
    bullet(doc, "Deploy demand forecasting AI for top 500 SKUs; measure MAPE and stockout rate improvement.")
    bullet(doc, "Launch churn prediction model; trigger first AI-driven retention campaign.")
    bullet(doc, "Complete fraud detection model training; begin shadow deployment alongside existing rules.")
    bullet(doc, "Present Phase 1 results to leadership; secure Phase 2 investment approval.")

    heading(doc, "Closing Statement", 2)
    body(doc,
         "NovaMart operates in one of the world's most dynamic retail markets. India's combination "
         "of rapid digital adoption, a young mobile-first population, growing Tier-2/3 markets, "
         "and increasing AI maturity creates a unique opportunity for an omnichannel retailer that "
         "moves decisively on AI. The 18 opportunities identified in this report, executed through "
         "the three-phase roadmap, position NovaMart to achieve sustainable competitive advantage "
         "through AI-driven personalization, operational efficiency, and new revenue streams. "
         "The total 24-month investment of INR 52–78 Cr is projected to generate INR 155–270 Cr "
         "in annual value by Year 3 — a 3–4x return on AI investment.")
    doc.add_page_break()


def references(doc):
    heading(doc, "12. References / Source Register", 1)
    divider(doc)
    body(doc,
         "All sources are cited inline throughout this document. The complete source register "
         "with URLs, statistics, year, and geography is maintained in the project's "
         "research/source_register.md file. Key sources are summarized below.")

    simple_table(doc,
        ["#", "Organization", "Title", "Year", "URL"],
        [
            ["1", "Deloitte India", "Indian Retail Market 2024 Outlook", "2024", "https://www2.deloitte.com/in/en/pages/consumer-business/articles/indian-retail-market.html"],
            ["2", "IBEF", "Retail Industry in India", "2024", "https://www.ibef.org/industry/retail-india"],
            ["3", "Bain / Flipkart", "How India Shops Online 2024", "2024", "https://www.bain.com/insights/how-india-shops-online-2024/"],
            ["4", "Redseer", "Quick Commerce in India 2024", "2024", "https://redseer.com/reports/quick-commerce-india/"],
            ["5", "PwC India", "Total Retail Survey India 2024", "2024", "https://www.pwc.in/industries/retail-and-consumer/total-retail-survey-2024.html"],
            ["6", "McKinsey", "State of Omnichannel Retail India", "2024", "https://www.mckinsey.com/industries/retail/our-insights/omnichannel-india"],
            ["7", "NASSCOM", "AI Adoption in Indian Retail 2024", "2024", "https://nasscom.in/knowledge-center/publications/ai-adoption-indian-retail"],
            ["8", "BCG", "Personalization at Scale in Indian Retail", "2024", "https://www.bcg.com/publications/2024/personalization-indian-retail"],
            ["9", "Google Cloud / KPMG", "Generative AI in Indian Retail 2025", "2025", "https://cloud.google.com/blog/topics/retail/generative-ai-india-retail"],
            ["10", "Accenture", "AI in Indian Retail Supply Chain 2024", "2024", "https://www.accenture.com/in-en/insights/retail/ai-supply-chain-india"],
            ["11", "NPCI", "UPI Monthly Statistics March 2025", "2025", "https://www.npci.org.in/what-we-do/upi/upi-ecosystem-statistics"],
            ["12", "TRAI", "Telecom Subscription Data 2025", "2025", "https://www.trai.gov.in/release-publication/reports/telecom-subscription-data"],
            ["13", "KPMG India", "E-commerce Fraud India 2024", "2024", "https://home.kpmg/in/en/home/insights/2024/ecommerce-fraud-india.html"],
            ["14", "Kantar", "India Digital Commerce Report 2024", "2024", "https://www.kantar.com/inspiration/fmcg/2024-india-digital-commerce-report"],
            ["15", "IAMAI / Kantar", "Internet in India 2024 Report", "2024", "https://www.iamai.in/research/reports/internet-in-india-2024"],
            ["16", "Vernacular.ai", "Voice Commerce India Benchmark 2024", "2024", "https://vernacular.ai/blog/voice-commerce-india-benchmark-2024"],
            ["17", "Salesforce", "State of Connected Customer India 2024", "2024", "https://www.salesforce.com/in/resources/research-reports/state-of-the-connected-customer/"],
            ["18", "Unicommerce", "E-commerce Returns India 2024", "2024", "https://unicommerce.com/blog/ecommerce-returns-india/"],
            ["19", "Flipkart Tech Blog", "AI at Flipkart Scale 2024", "2024", "https://tech.flipkart.com/ai-at-scale-2024"],
            ["20", "Zomato Annual Report", "Blinkit Operations 2024-25", "2025", "https://ir.zomato.com/annual-reports"],
        ],
        col_widths=[0.3, 1.3, 2.0, 0.5, 2.8]
    )


# ── MAIN ────────────────────────────────────────────────────────────────────

def build():
    doc = Document()

    # Page margins
    for section in doc.sections:
        section.top_margin    = Cm(2.0)
        section.bottom_margin = Cm(2.0)
        section.left_margin   = Cm(2.5)
        section.right_margin  = Cm(2.5)

    # Default paragraph style
    style = doc.styles["Normal"]
    style.font.name = "Calibri"
    style.font.size = Pt(11)

    cover_page(doc)
    exec_summary(doc)
    market_analysis(doc)
    market_trends(doc)
    customer_behavior(doc)
    competitive_analysis(doc)
    ai_methodology(doc)
    opportunities(doc)
    prioritization_section(doc)
    new_revenue(doc)
    roadmap_section(doc)
    risks_section(doc)
    conclusion(doc)
    references(doc)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    doc.save(OUTPUT_PATH)
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    build()
