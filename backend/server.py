from fastapi import FastAPI, APIRouter
from fastapi.responses import FileResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
import uuid
from datetime import datetime, timezone

from generators.pdf_generator import generate_all_pdfs, OUTPUT_DIR
from generators.lead_magnet import generate_lead_magnet

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

app = FastAPI()
api_router = APIRouter(prefix="/api")

# Generate PDFs on startup
PDF_PATHS = {}

# Product catalog
PRODUCTS = [
    {
        "id": "journal",
        "title": "90-Day Anxiety Relief Journal",
        "subtitle": "Daily Prompts, Mood Tracking & Gratitude Practice",
        "description": "Transform your relationship with anxiety over 90 days. Each day includes morning intentions, mood tracking, guided journaling prompts, gratitude practice, and evening reflections. Written with compassion and backed by CBT principles.",
        "price": "$12.99",
        "pages": "95+ pages",
        "category": "Journal",
        "color": "green",
        "features": [
            "90 daily journal spreads with unique prompts",
            "Morning intention & evening reflection sections",
            "Mood tracking with 7-point scale",
            "Gratitude & self-care prompts",
            "Final reflection pages",
        ],
        "filename": "90_day_anxiety_relief_journal.pdf",
        "badge": "Best Seller",
    },
    {
        "id": "planner",
        "title": "Morning & Evening Routine Planner",
        "subtitle": "Build Calm Habits That Stick",
        "description": "Design your ideal morning and evening routines with this structured planner. Includes 30 daily routine sheets with checklists, weekly habit trackers, and reflection spaces. Perfect companion to the journal.",
        "price": "$9.99",
        "pages": "38 pages",
        "category": "Planner",
        "color": "gold",
        "features": [
            "30 daily routine planning sheets",
            "Morning & evening checklists",
            "4 weekly habit tracker grids",
            "Daily inspirational quotes",
            "Notes & reflection space",
        ],
        "filename": "morning_evening_routine_planner.pdf",
        "badge": "Popular",
    },
    {
        "id": "ebook",
        "title": "The Calm Mind",
        "subtitle": "A Complete Guide to Understanding & Managing Anxiety",
        "description": "Learn the science behind anxiety and master evidence-based techniques for lasting calm. Covers breathing methods, cognitive reframing, mindfulness, routine building, and when to seek help. Your comprehensive anxiety toolkit.",
        "price": "$14.99",
        "pages": "50+ pages",
        "category": "Ebook",
        "color": "teal",
        "features": [
            "9 in-depth chapters",
            "Evidence-based techniques",
            "Breathing method guides",
            "Cognitive reframing exercises",
            "30-day calm action plan",
        ],
        "filename": "the_calm_mind_ebook.pdf",
        "badge": "Comprehensive",
    },
    {
        "id": "workbook",
        "title": "Weekly Reflection Workbook",
        "subtitle": "12 Weeks of Guided Self-Discovery",
        "description": "Deep dive into your weekly patterns with themed reflection pages. Each week focuses on a different aspect of mental wellness: awareness, acceptance, gratitude, boundaries, self-compassion, and more.",
        "price": "$9.99",
        "pages": "14 pages",
        "category": "Workbook",
        "color": "indigo",
        "features": [
            "12 themed weekly spreads",
            "Weekly wins & challenges sections",
            "Mood overview tracking",
            "Guided reflection questions",
            "Next week intention setting",
        ],
        "filename": "weekly_reflection_workbook.pdf",
        "badge": "Deep Work",
    },
    {
        "id": "cards",
        "title": "Mindfulness & Breathing Exercise Cards",
        "subtitle": "20 Printable Cards for Instant Calm",
        "description": "Print, cut, and keep these 20 exercise cards anywhere you need them. Each card has step-by-step instructions for a different calming technique, from box breathing to body scans to grounding exercises.",
        "price": "$7.99",
        "pages": "12 pages (20 cards)",
        "category": "Cards",
        "color": "coral",
        "features": [
            "20 unique exercise cards",
            "Step-by-step instructions",
            "Duration & difficulty ratings",
            "Pro tips for each technique",
            "Print & cut format",
        ],
        "filename": "mindfulness_breathing_cards.pdf",
        "badge": "Quick Use",
    },
]

BUNDLE_INFO = {
    "title": "The Complete Calm Mind Collection",
    "original_price": "$55.95",
    "bundle_price": "$29.99",
    "savings": "Save 46%",
    "description": "Get all 5 products together and save. Everything you need to manage anxiety, build calm routines, and create lasting peace of mind.",
}


@api_router.get("/")
async def root():
    return {"message": "The Calm Mind Collection API"}


@api_router.get("/products")
async def get_products():
    return {
        "products": PRODUCTS,
        "bundle": BUNDLE_INFO,
    }


@api_router.get("/products/{product_id}")
async def get_product(product_id: str):
    for p in PRODUCTS:
        if p["id"] == product_id:
            return p
    return {"error": "Product not found"}


@api_router.get("/download/{product_id}")
async def download_pdf(product_id: str):
    for p in PRODUCTS:
        if p["id"] == product_id:
            filepath = OUTPUT_DIR / p["filename"]
            if filepath.exists():
                return FileResponse(
                    path=str(filepath),
                    filename=p["filename"],
                    media_type="application/pdf",
                )
    return {"error": "File not found"}


@api_router.get("/download-all")
async def download_all():
    """Return list of download links for all products."""
    links = []
    for p in PRODUCTS:
        filepath = OUTPUT_DIR / p["filename"]
        if filepath.exists():
            links.append({
                "id": p["id"],
                "title": p["title"],
                "download_url": f"/api/download/{p['id']}",
            })
    return {"downloads": links}


# Track downloads in MongoDB
class DownloadEvent(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    product_id: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class EmailSubscriber(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: str
    name: str = ""
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class EmailInput(BaseModel):
    email: str
    name: str = ""


@api_router.post("/track-download/{product_id}")
async def track_download(product_id: str):
    event = DownloadEvent(product_id=product_id)
    doc = event.model_dump()
    doc['timestamp'] = doc['timestamp'].isoformat()
    await db.downloads.insert_one(doc)
    count = await db.downloads.count_documents({"product_id": product_id})
    return {"product_id": product_id, "total_downloads": count}


@api_router.get("/stats")
async def get_stats():
    stats = {}
    for p in PRODUCTS:
        count = await db.downloads.count_documents({"product_id": p["id"]})
        stats[p["id"]] = count
    total = sum(stats.values())
    sub_count = await db.subscribers.count_documents({})
    return {"downloads_by_product": stats, "total_downloads": total, "total_subscribers": sub_count}


@api_router.post("/subscribe")
async def subscribe(input: EmailInput):
    existing = await db.subscribers.find_one({"email": input.email}, {"_id": 0})
    if existing:
        return {"status": "already_subscribed", "message": "You're already subscribed! Check your downloads."}
    subscriber = EmailSubscriber(email=input.email, name=input.name)
    doc = subscriber.model_dump()
    doc['timestamp'] = doc['timestamp'].isoformat()
    await db.subscribers.insert_one(doc)
    return {"status": "success", "message": "Welcome! Your free guide is ready to download."}


@api_router.get("/lead-magnet")
async def download_lead_magnet():
    filepath = OUTPUT_DIR / "5_emergency_calm_techniques.pdf"
    if filepath.exists():
        return FileResponse(
            path=str(filepath),
            filename="5_emergency_calm_techniques.pdf",
            media_type="application/pdf",
        )
    return {"error": "File not found"}


app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@app.on_event("startup")
async def startup_event():
    global PDF_PATHS
    logger.info("Generating PDFs...")
    PDF_PATHS = generate_all_pdfs()
    lead_magnet_path = generate_lead_magnet()
    logger.info(f"PDFs generated: {list(PDF_PATHS.keys())}")
    logger.info(f"Lead magnet generated: {lead_magnet_path}")


@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
