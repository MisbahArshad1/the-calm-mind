# The Calm Mind Collection - PRD

## Original Problem Statement
Build a complete set of PDFs for journals and ebooks that sell in 2026. Must help one person solve one particular problem. User will sell on Payhip. Products should be colorful and presentable.

## Architecture
- **Frontend**: React 19 + Framer Motion + Phosphor Icons + Tailwind CSS
- **Backend**: FastAPI + ReportLab (PDF generation) + MongoDB (download tracking + email capture)
- **PDF Generation**: Server-side on startup using ReportLab canvas API
- **No payment integration**: User sells on Payhip externally

## User Persona
- People struggling with anxiety/stress seeking digital self-help tools
- Payhip sellers looking for ready-to-sell digital product bundles

## Core Requirements
- [x] 5 unique, colorful PDF products targeting anxiety relief
- [x] Beautiful landing page to showcase products
- [x] Download functionality for each PDF
- [x] Bundle pricing display
- [x] Mobile responsive design
- [x] Download tracking analytics
- [x] Lead magnet popup with free mini-PDF + email capture

## What's Been Implemented (March 2026)

### PDFs Generated (6 total):
1. **90-Day Anxiety Relief Journal** (94 pages) - Daily prompts, mood tracking, gratitude, self-care
2. **Morning & Evening Routine Planner** (36 pages) - 30 daily sheets + weekly habit trackers
3. **The Calm Mind Ebook** (14 pages) - 6 chapters on anxiety science & techniques
4. **Weekly Reflection Workbook** (13 pages) - 12 themed weekly reflection spreads
5. **Mindfulness & Breathing Exercise Cards** (11 pages) - 20 printable exercise cards
6. **5 Emergency Calm Techniques** (8 pages) - FREE lead magnet with 5 detailed techniques

### Web App Features:
- Hero section with "Reclaim Your Calm" headline + Framer Motion animations
- Bento grid product showcase with 5 colored product cards
- Bundle section ($29.99 for all 5, save 46%)
- Testimonials section (3 reviews)
- About section with stats
- Sticky navigation bar with blur effect
- Download buttons with tracking
- **Lead magnet popup** - appears at 40% scroll or after 12s, captures email + name, auto-downloads free PDF

### API Endpoints:
- GET /api/products - Product catalog
- GET /api/download/{id} - PDF download
- POST /api/track-download/{id} - Track downloads
- GET /api/stats - Download + subscriber statistics
- POST /api/subscribe - Email capture
- GET /api/lead-magnet - Free PDF download

## Testing Status
- Backend: 100% all endpoints working
- Frontend: 100% all components functional
- Lead magnet flow: Tested end-to-end (form → submit → success → PDF download)

## Backlog / Next Tasks
- P1: Upload PDFs to Payhip and link CTA buttons to Payhip product pages
- P1: Connect email capture to an email marketing service (e.g., ConvertKit, Mailchimp)
- P2: Add more ebook chapters with expanded content
- P2: Add product preview modal (show first 2-3 pages inline)
- P3: Add dark mode toggle
- P3: SEO meta tags and Open Graph images
