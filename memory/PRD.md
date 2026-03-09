# The Calm Mind Collection - PRD

## Original Problem Statement
Build a complete set of PDFs for journals and ebooks that sell in 2026. Must help one person solve one particular problem. User will sell on Payhip. Products should be colorful and presentable.

## Architecture
- **Frontend**: React 19 (STATIC) + Framer Motion + Phosphor Icons + Tailwind CSS
- **No backend needed** - all data hardcoded, buttons link to Payhip
- **Deployable on Vercel for free** (static site)

## What's Been Implemented

### 6 PDFs Generated:
1. 90-Day Anxiety Relief Journal (94 pages, $12.99)
2. Morning & Evening Routine Planner (36 pages, $9.99)
3. The Calm Mind Ebook (14 pages, $14.99)
4. Weekly Reflection Workbook (13 pages, $9.99)
5. Mindfulness & Breathing Exercise Cards (11 pages, $7.99)
6. 5 Emergency Calm Techniques - FREE lead magnet (8 pages)

### Static Landing Page:
- Hero, Product Grid, Bundle ($29.99), Testimonials, About, Footer
- All Buy Now buttons → Payhip checkout links
- Lead magnet popup → Payhip free product link
- Zero backend dependency, deployable as static site on Vercel

### How to Deploy:
1. Save to GitHub via Emergent
2. Connect GitHub repo to Vercel
3. Deploy frontend folder as static React app
4. Update PAYHIP_LINKS in App.js with real Payhip URLs

## Next Tasks
- P0: Upload PDFs to Payhip, get product URLs, update PAYHIP_LINKS in App.js
- P1: Deploy on Vercel (free)
- P2: Connect custom domain
- P3: Add SEO meta tags
