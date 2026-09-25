# AI Methodology Analysis
## NovaMart Week 2: AI-Driven Market Analysis
### Research Date: September 2026

---

## Overview

This document explains each AI/ML methodology considered for NovaMart's implementation. For each method, the rationale for selection is explained — not just what the method does, but why it is appropriate for the specific business problem.

Format: Input Data → AI Technique → Output → Business Decision

---

## 1. Customer Segmentation — K-Means Clustering

**Why appropriate:** K-Means is computationally efficient for large customer datasets and produces interpretable, actionable segments. It is appropriate when the number of segments is known or can be determined via elbow method, and when segments are roughly spherical in feature space.

**Input Data:**
- Purchase frequency, recency, monetary value (RFM features)
- Category preferences (grocery, fashion, electronics)
- Channel preference (app, web, in-store)
- Geographic tier (Tier-1/2/3)
- Payment method preference

**AI Technique:** K-Means Clustering (k=4–8 segments, determined via elbow method and silhouette score)

**Output:**
- Customer segment labels (e.g., Value Hunter, Convenience Seeker, Discovery Shopper, Occasion Buyer)
- Segment centroids defining each group's behavioral profile
- Segment membership probability per customer

**Business Decision:**
- Tailor marketing campaigns, discount strategies, and product recommendations per segment
- Allocate marketing budget proportionally to segment CLV
- Design segment-specific loyalty program tiers

**Limitations & Mitigations:**
- K-Means assumes spherical clusters; use DBSCAN or Gaussian Mixture Models if segments are irregular
- Requires feature scaling (StandardScaler) before fitting
- Re-run monthly as customer behavior evolves

---

## 2. Churn Prediction — Logistic Regression + XGBoost

**Why appropriate:** Logistic Regression provides interpretable probability scores (important for business stakeholders). XGBoost captures non-linear interactions between features that Logistic Regression misses. Using both provides a baseline + high-performance model comparison.

**Input Data:**
- Days since last purchase (recency)
- Purchase frequency trend (last 30/60/90 days)
- Customer service interaction count
- App engagement metrics (sessions, time-in-app)
- Discount dependency ratio
- Category breadth (number of categories purchased)

**AI Technique:**
- Logistic Regression (baseline, interpretable)
- XGBoost (gradient boosted trees, high accuracy)
- SHAP values for feature importance explanation

**Output:**
- Churn probability score (0–1) per customer
- Top 3 churn risk factors per customer (via SHAP)
- High-risk customer list (probability > 0.7)

**Business Decision:**
- Trigger personalized retention offers for high-risk customers
- Assign customer success outreach for top-value churning customers
- Adjust loyalty program benefits for at-risk segments

**Expected Performance:** XGBoost typically achieves AUC 0.82–0.88 on retail churn datasets; Logistic Regression baseline ~0.74.

---

## 3. Demand Forecasting — Time-Series (ARIMA / Prophet / LSTM)

**Why appropriate:** Retail demand has strong temporal patterns (seasonality, trends, festive spikes). A layered approach is used: Prophet for interpretable baseline forecasting, LSTM for capturing complex non-linear temporal dependencies.

**Input Data:**
- Historical sales data (SKU-level, daily/weekly)
- Promotional calendar (discounts, festive events)
- Weather data (for grocery/FMCG categories)
- Local event data (IPL, festivals, school calendars)
- Competitor pricing signals
- Social media trend signals

**AI Technique:**
- Facebook Prophet: Handles seasonality, holidays, and trend changepoints; interpretable
- LSTM (Long Short-Term Memory): Captures long-range temporal dependencies; better for complex multi-variate forecasting
- Ensemble: Weighted average of Prophet + LSTM predictions

**Output:**
- 7-day, 14-day, 30-day demand forecast per SKU per store/dark-store
- Confidence intervals (80%, 95%)
- Anomaly flags for unexpected demand spikes

**Business Decision:**
- Automated purchase order generation to suppliers
- Dynamic safety stock calculation
- Promotional timing optimization (launch promotions when demand is naturally rising)

**Expected Accuracy:** MAPE (Mean Absolute Percentage Error) target: <12% for stable SKUs, <20% for seasonal SKUs.

---

## 4. Product Recommendation — Collaborative Filtering + Hybrid

**Why appropriate:** Collaborative filtering leverages the "wisdom of crowds" — customers with similar purchase histories tend to like similar products. Content-based filtering handles the cold-start problem for new products. A hybrid approach combines both for maximum coverage and accuracy.

**Input Data:**
- User-item interaction matrix (purchases, views, add-to-cart, ratings)
- Product attributes (category, brand, price, attributes)
- User demographics and segment
- Contextual signals (time of day, device, location)

**AI Technique:**
- Matrix Factorization (ALS — Alternating Least Squares): Collaborative filtering for established users/products
- Content-Based Filtering: TF-IDF or embedding-based similarity for new products
- Hybrid: Weighted combination; content-based weight increases for new products/users
- Two-Tower Neural Network: For real-time retrieval at scale (similar to YouTube/Flipkart architecture)

**Output:**
- Top-N product recommendations per user per context
- "Frequently bought together" bundles
- "Customers like you also bought" suggestions
- Cross-category discovery recommendations

**Business Decision:**
- Homepage personalization
- Cart page cross-sell/upsell
- Email/push notification product suggestions
- In-store digital display personalization

**Expected Impact:** 15–25% increase in average basket size; 10–18% increase in session conversion rate.

---

## 5. Dynamic Pricing — Random Forest + Reinforcement Learning

**Why appropriate:** Random Forest provides a robust, interpretable price elasticity model. Reinforcement Learning (RL) optimizes pricing policy over time by learning from customer response signals — appropriate once sufficient data is available.

**Input Data:**
- Historical price-demand curves per SKU
- Competitor prices (scraped/API)
- Inventory levels and days-of-supply
- Customer segment price sensitivity
- Time-of-day, day-of-week patterns
- Promotional calendar

**AI Technique:**
- Random Forest Regressor: Predicts demand at different price points (price elasticity modeling)
- Contextual Bandit / RL: Optimizes price decisions over time using reward signals (revenue, margin, conversion)

**Output:**
- Optimal price recommendation per SKU per time window
- Price elasticity coefficient per SKU-segment combination
- Revenue impact simulation for proposed price changes

**Business Decision:**
- Automated price adjustments within guardrails (min/max price bounds)
- Flash sale timing and depth optimization
- Competitive price matching triggers

**Expected Impact:** 6–12% revenue uplift; 3–5% margin improvement through reduced unnecessary discounting.

---

## 6. Fraud Detection — XGBoost + Anomaly Detection

**Why appropriate:** XGBoost excels at classification on tabular transaction data. Isolation Forest handles unsupervised anomaly detection for novel fraud patterns not seen in training data. The combination provides both known-fraud detection and unknown-fraud discovery.

**Input Data:**
- Transaction features: amount, time, location, device, payment method
- User behavioral features: session duration, click patterns, typing speed
- Historical fraud labels (supervised component)
- Network features: shared devices, IPs, addresses

**AI Technique:**
- XGBoost Classifier: Supervised fraud classification on labeled historical data
- Isolation Forest: Unsupervised anomaly detection for novel fraud patterns
- Graph Neural Network (GNN): For detecting fraud rings and coordinated fraud networks

**Output:**
- Fraud probability score per transaction (0–1)
- Fraud type classification (account takeover, payment fraud, return fraud, promo abuse)
- Real-time block/flag/review decision

**Business Decision:**
- Automated transaction blocking for high-confidence fraud (score > 0.95)
- Manual review queue for medium-confidence (0.6–0.95)
- Friction addition (OTP, CAPTCHA) for suspicious sessions

**Expected Performance:** Precision > 92%, Recall > 85%, False Positive Rate < 0.5% (critical to avoid blocking legitimate customers).

---

## 7. Sentiment Analysis & Review Intelligence — NLP + Transformers

**Why appropriate:** Large volumes of unstructured customer reviews, social media mentions, and support tickets contain actionable product and service intelligence. Transformer-based models (BERT, IndicBERT for Indian languages) provide state-of-the-art accuracy on Indian multilingual text.

**Input Data:**
- Product reviews (text + star rating)
- Customer support chat transcripts
- Social media mentions (Twitter/X, Instagram, YouTube comments)
- App store reviews
- Post-purchase survey responses

**AI Technique:**
- IndicBERT / MuRIL: Multilingual BERT variants fine-tuned on Indian languages for sentiment classification
- Aspect-Based Sentiment Analysis (ABSA): Extracts sentiment at the attribute level (e.g., "delivery was fast but packaging was poor")
- Topic Modeling (LDA / BERTopic): Discovers emerging complaint/praise themes

**Output:**
- Sentiment score per review (positive/negative/neutral)
- Aspect-level sentiment (product quality, delivery, price, customer service)
- Trending topics and emerging issues dashboard
- Net Promoter Score (NPS) prediction from review text

**Business Decision:**
- Product quality improvement prioritization
- Supplier performance management
- Marketing message optimization (amplify what customers love)
- Early warning system for product defects or service failures

---

## 8. Visual Search & Computer Vision — CNN + CLIP

**Why appropriate:** Indian consumers increasingly use visual search (photographing products to find similar items). Computer vision in stores enables cashierless checkout and shelf analytics. CLIP (Contrastive Language-Image Pretraining) enables cross-modal search (text-to-image and image-to-image).

**Input Data:**
- Product catalog images (all SKUs)
- User-uploaded query images
- In-store camera feeds (for shelf analytics)
- Product attribute labels

**AI Technique:**
- ResNet / EfficientNet: Product image feature extraction and classification
- CLIP: Cross-modal embedding for visual search (image query → similar products)
- YOLO v8: Real-time object detection for shelf analytics and cashierless checkout

**Output:**
- Top-N visually similar products for a query image
- Shelf planogram compliance score
- Out-of-stock detection alerts
- Customer traffic heatmaps (in-store)

**Business Decision:**
- Visual search feature in NovaMart app
- Automated shelf replenishment alerts
- Store layout optimization based on traffic patterns

---

## 9. Generative AI — LLM + RAG

**Why appropriate:** Generative AI (LLMs) can automate high-volume, repetitive content tasks (product descriptions, marketing copy) and power conversational commerce. RAG (Retrieval-Augmented Generation) grounds LLM responses in NovaMart's actual product catalog and policies, preventing hallucinations.

**Input Data:**
- Product catalog (attributes, specifications, images)
- Customer query (natural language)
- NovaMart policy documents (return policy, shipping policy)
- Customer purchase history (for personalized responses)

**AI Technique:**
- LLM (GPT-4o / Gemini 1.5 / Llama 3): Base language model for generation
- RAG Pipeline: Vector database (FAISS / Pinecone) stores product embeddings; retrieves relevant context before generation
- Fine-tuning: Domain-specific fine-tuning on NovaMart's catalog and tone-of-voice guidelines

**Output:**
- Auto-generated product descriptions (SEO-optimized, multilingual)
- Personalized marketing email/SMS copy
- Conversational shopping assistant responses
- Automated customer service responses for common queries

**Business Decision:**
- Reduce catalog content production cost by 70–80%
- Scale personalized marketing without proportional headcount increase
- 24/7 AI customer service reducing support ticket volume by 40–60%

---

## 10. Embeddings for Personalization

**Why appropriate:** Dense vector embeddings capture semantic similarity between products and users in a continuous space, enabling more nuanced personalization than traditional collaborative filtering.

**Input Data:**
- User interaction sequences (browse, purchase, search history)
- Product attributes and descriptions
- Category hierarchies

**AI Technique:**
- Word2Vec / Item2Vec: Learn product embeddings from co-purchase sequences
- Transformer-based Sequential Models (BERT4Rec, SASRec): Capture sequential purchase patterns
- Two-Tower Model: Separate user and item towers; dot product for relevance scoring

**Output:**
- User embedding vector (captures taste/preference)
- Item embedding vector (captures product characteristics)
- Real-time similarity scores for recommendation retrieval

**Business Decision:**
- Real-time personalized homepage
- "Complete the look" / "Complete the recipe" cross-category recommendations
- Personalized search result ranking
