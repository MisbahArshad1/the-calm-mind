import { useEffect, useState, useRef } from "react";
import "@/App.css";
import { motion, useInView } from "framer-motion";
import {
  Leaf,
  Download,
  Star,
  BookOpen,
  Sun,
  Moon,
  Brain,
  Heart,
  Wind,
  ArrowDown,
  Check,
  Package,
  Sparkle,
  Timer,
  FileText,
  ShieldCheck,
  ShoppingCart,
} from "@phosphor-icons/react";
import LeadMagnetPopup from "@/components/LeadMagnetPopup";

// ============================================================
// PAYHIP CONFIGURATION - UPDATE THESE WITH YOUR PAYHIP LINKS
// ============================================================
const PAYHIP_LINKS = {
  journal: "https://payhip.com/b/YOUR_JOURNAL_LINK",
  planner: "https://payhip.com/b/YOUR_PLANNER_LINK",
  ebook: "https://payhip.com/b/YOUR_EBOOK_LINK",
  workbook: "https://payhip.com/b/YOUR_WORKBOOK_LINK",
  cards: "https://payhip.com/b/YOUR_CARDS_LINK",
  bundle: "https://payhip.com/b/YOUR_BUNDLE_LINK",
  lead_magnet: "https://payhip.com/b/YOUR_FREE_LEAD_MAGNET_LINK",
};
// ============================================================

const PRODUCTS = [
  {
    id: "journal",
    title: "90-Day Anxiety Relief Journal",
    subtitle: "Daily Prompts, Mood Tracking & Gratitude Practice",
    description: "Transform your relationship with anxiety over 90 days. Each day includes morning intentions, mood tracking, guided journaling prompts, gratitude practice, and evening reflections. Written with compassion and backed by CBT principles.",
    price: "$12.99",
    pages: "95+ pages",
    category: "Journal",
    color: "green",
    features: [
      "90 daily journal spreads with unique prompts",
      "Morning intention & evening reflection sections",
      "Mood tracking with 7-point scale",
    ],
    badge: "Best Seller",
  },
  {
    id: "planner",
    title: "Morning & Evening Routine Planner",
    subtitle: "Build Calm Habits That Stick",
    description: "Design your ideal morning and evening routines with this structured planner. Includes 30 daily routine sheets with checklists, weekly habit trackers, and reflection spaces. Perfect companion to the journal.",
    price: "$9.99",
    pages: "38 pages",
    category: "Planner",
    color: "gold",
    features: [
      "30 daily routine planning sheets",
      "Morning & evening checklists",
      "4 weekly habit tracker grids",
    ],
    badge: "Popular",
  },
  {
    id: "ebook",
    title: "The Calm Mind",
    subtitle: "A Complete Guide to Understanding & Managing Anxiety",
    description: "Learn the science behind anxiety and master evidence-based techniques for lasting calm. Covers breathing methods, cognitive reframing, mindfulness, routine building, and when to seek help. Your comprehensive anxiety toolkit.",
    price: "$14.99",
    pages: "50+ pages",
    category: "Ebook",
    color: "teal",
    features: [
      "9 in-depth chapters",
      "Evidence-based techniques",
      "Breathing method guides",
    ],
    badge: "Comprehensive",
  },
  {
    id: "workbook",
    title: "Weekly Reflection Workbook",
    subtitle: "12 Weeks of Guided Self-Discovery",
    description: "Deep dive into your weekly patterns with themed reflection pages. Each week focuses on a different aspect of mental wellness: awareness, acceptance, gratitude, boundaries, self-compassion, and more.",
    price: "$9.99",
    pages: "14 pages",
    category: "Workbook",
    color: "indigo",
    features: [
      "12 themed weekly spreads",
      "Weekly wins & challenges sections",
      "Guided reflection questions",
    ],
    badge: "Deep Work",
  },
  {
    id: "cards",
    title: "Mindfulness & Breathing Exercise Cards",
    subtitle: "20 Printable Cards for Instant Calm",
    description: "Print, cut, and keep these 20 exercise cards anywhere you need them. Each card has step-by-step instructions for a different calming technique, from box breathing to body scans to grounding exercises.",
    price: "$7.99",
    pages: "12 pages (20 cards)",
    category: "Cards",
    color: "coral",
    features: [
      "20 unique exercise cards",
      "Step-by-step instructions",
      "Duration & difficulty ratings",
    ],
    badge: "Quick Use",
  },
];

const BUNDLE = {
  title: "The Complete Calm Mind Collection",
  original_price: "$55.95",
  bundle_price: "$29.99",
  savings: "Save 46%",
  description: "Get all 5 products together and save. Everything you need to manage anxiety, build calm routines, and create lasting peace of mind.",
};

const colorMap = {
  green: { badge: "badge-green", card: "product-green", icon: "#3A5A40" },
  gold: { badge: "badge-gold", card: "product-gold", icon: "#E9C46A" },
  teal: { badge: "badge-teal", card: "product-teal", icon: "#2A9D8F" },
  indigo: { badge: "badge-indigo", card: "product-indigo", icon: "#6366F1" },
  coral: { badge: "badge-coral", card: "product-coral", icon: "#E76F51" },
};

const productIcons = {
  journal: BookOpen,
  planner: Sun,
  ebook: Brain,
  workbook: Moon,
  cards: Wind,
};

function FadeInSection({ children, delay = 0, className = "" }) {
  const ref = useRef(null);
  const isInView = useInView(ref, { once: true, margin: "-80px" });

  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0, y: 40 }}
      animate={isInView ? { opacity: 1, y: 0 } : {}}
      transition={{ duration: 0.7, delay, ease: [0.16, 1, 0.3, 1] }}
      className={className}
    >
      {children}
    </motion.div>
  );
}

function Navbar() {
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 50);
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  return (
    <nav
      className={`nav-bar ${scrolled ? "nav-scrolled" : ""}`}
      data-testid="navbar"
    >
      <div className="section-container" style={{ display: "flex", alignItems: "center", justifyContent: "space-between", height: 64 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
          <Leaf size={24} weight="fill" color="#3A5A40" />
          <span className="font-serif" style={{ fontSize: 18, fontWeight: 700, color: "var(--primary)" }}>
            The Calm Mind
          </span>
        </div>
        <div style={{ display: "flex", alignItems: "center", gap: 24 }}>
          <a href="#products" className="font-body" style={{ fontSize: 14, fontWeight: 500, color: "var(--muted-fg)", textDecoration: "none" }} data-testid="nav-products-link">Products</a>
          <a href="#bundle" className="font-body" style={{ fontSize: 14, fontWeight: 500, color: "var(--muted-fg)", textDecoration: "none" }} data-testid="nav-bundle-link">Bundle</a>
          <a href="#about" className="font-body" style={{ fontSize: 14, fontWeight: 500, color: "var(--muted-fg)", textDecoration: "none" }} data-testid="nav-about-link">About</a>
          <a href={PAYHIP_LINKS.bundle} target="_blank" rel="noopener noreferrer" className="btn-primary" style={{ padding: "10px 24px", fontSize: 13 }} data-testid="nav-cta-btn">Get the Bundle</a>
        </div>
      </div>
    </nav>
  );
}

function HeroSection() {
  return (
    <section className="hero-section" data-testid="hero-section">
      <div className="hero-glow" />
      <div className="hero-glow-2" />

      <div className="section-container" style={{ display: "flex", flexDirection: "column", alignItems: "center", textAlign: "center", position: "relative", zIndex: 1, paddingTop: 80 }}>
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.1 }}
        >
          <span className="badge badge-green" style={{ marginBottom: 24, display: "inline-flex" }}>
            <Sparkle size={14} weight="fill" style={{ marginRight: 4 }} /> 2026 Digital Collection
          </span>
        </motion.div>

        <motion.h1
          className="font-serif"
          style={{ fontSize: "clamp(40px, 6vw, 72px)", fontWeight: 700, lineHeight: 1.1, color: "var(--fg)", marginBottom: 24, maxWidth: 700, letterSpacing: "-0.02em" }}
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.2 }}
        >
          Reclaim Your{" "}
          <span style={{ fontStyle: "italic", color: "var(--primary)" }}>Calm</span>
        </motion.h1>

        <motion.p
          className="font-body"
          style={{ fontSize: "clamp(16px, 2vw, 20px)", lineHeight: 1.7, color: "var(--muted-fg)", maxWidth: 560, marginBottom: 40 }}
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.35 }}
        >
          A curated collection of journals, planners, and guides designed to help you understand anxiety and build lasting peace of mind.
        </motion.p>

        <motion.div
          style={{ display: "flex", gap: 16, flexWrap: "wrap", justifyContent: "center" }}
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.5 }}
        >
          <a href={PAYHIP_LINKS.bundle} target="_blank" rel="noopener noreferrer" className="btn-accent" data-testid="hero-bundle-btn">
            <Package size={18} weight="bold" /> Get the Full Bundle
          </a>
          <a href="#products" className="btn-secondary" data-testid="hero-explore-btn">
            Explore Products <ArrowDown size={16} />
          </a>
        </motion.div>

        <motion.div
          style={{ marginTop: 64, display: "flex", gap: 48, flexWrap: "wrap", justifyContent: "center" }}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.8, delay: 0.7 }}
        >
          {[
            { icon: FileText, label: "5 Products" },
            { icon: Timer, label: "200+ Pages" },
            { icon: ShieldCheck, label: "Printable PDFs" },
            { icon: Heart, label: "Evidence-Based" },
          ].map((item, i) => (
            <div key={i} style={{ display: "flex", alignItems: "center", gap: 8, opacity: 0.6 }}>
              <item.icon size={18} color="var(--primary)" weight="duotone" />
              <span style={{ fontSize: 13, fontWeight: 600, color: "var(--muted-fg)" }}>{item.label}</span>
            </div>
          ))}
        </motion.div>

        <motion.div
          style={{ marginTop: 80, width: "100%", maxWidth: 900 }}
          initial={{ opacity: 0, y: 60 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.9, delay: 0.8 }}
        >
          <div className="hero-image-container breathe-animation">
            <img
              src="https://images.unsplash.com/photo-1558086478-d632ccc5a833?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzl8MHwxfHNlYXJjaHwxfHxjb3p5JTIwd29tYW4lMjBqb3VybmFsaW5nJTIwbW9ybmluZyUyMHN1bmxpZ2h0fGVufDB8fHx8MTc3MzA5NDI2OHww&ixlib=rb-4.1.0&q=85"
              alt="Cozy journaling in morning sunlight"
              style={{ width: "100%", height: 400, objectFit: "cover", display: "block" }}
              data-testid="hero-image"
            />
          </div>
        </motion.div>
      </div>
    </section>
  );
}

function ProductCard({ product, index }) {
  const colors = colorMap[product.color] || colorMap.green;
  const Icon = productIcons[product.id] || BookOpen;
  const payhipLink = PAYHIP_LINKS[product.id] || "#";

  return (
    <FadeInSection delay={index * 0.1}>
      <div
        className={`product-card ${colors.card}`}
        style={{ padding: 32, height: "100%", display: "flex", flexDirection: "column" }}
        data-testid={`product-card-${product.id}`}
      >
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 16 }}>
          <div style={{ width: 48, height: 48, borderRadius: 14, background: "rgba(255,255,255,0.8)", display: "flex", alignItems: "center", justifyContent: "center" }}>
            <Icon size={24} weight="duotone" color={colors.icon} />
          </div>
          {product.badge && (
            <span className={`badge ${colors.badge}`}>{product.badge}</span>
          )}
        </div>

        <span style={{ fontSize: 11, fontWeight: 700, textTransform: "uppercase", letterSpacing: 1, color: "var(--muted-fg)", marginBottom: 6 }}>
          {product.category}
        </span>

        <h3 className="font-serif" style={{ fontSize: 22, fontWeight: 700, color: "var(--fg)", marginBottom: 6, lineHeight: 1.2 }}>
          {product.title}
        </h3>

        <p className="font-handwriting" style={{ fontSize: 18, color: colors.icon, marginBottom: 12 }}>
          {product.subtitle}
        </p>

        <p className="font-body" style={{ fontSize: 14, lineHeight: 1.6, color: "var(--muted-fg)", marginBottom: 16, flex: 1 }}>
          {product.description}
        </p>

        <div style={{ marginBottom: 16 }}>
          {product.features.map((f, i) => (
            <div key={i} className="feature-check">
              <div className="check-icon" style={{ background: "rgba(58, 90, 64, 0.1)" }}>
                <Check size={12} weight="bold" color="var(--primary)" />
              </div>
              <span style={{ fontSize: 13, color: "var(--muted-fg)" }}>{f}</span>
            </div>
          ))}
        </div>

        <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginTop: "auto", paddingTop: 16, borderTop: "1px solid rgba(0,0,0,0.06)" }}>
          <div>
            <span style={{ fontSize: 24, fontWeight: 700, color: "var(--fg)" }}>{product.price}</span>
            <span style={{ fontSize: 12, color: "var(--muted-fg)", marginLeft: 6 }}>{product.pages}</span>
          </div>
          <a
            href={payhipLink}
            target="_blank"
            rel="noopener noreferrer"
            className="btn-primary"
            style={{ padding: "10px 20px", fontSize: 13, textDecoration: "none" }}
            data-testid={`buy-btn-${product.id}`}
          >
            <ShoppingCart size={16} weight="bold" /> Buy Now
          </a>
        </div>
      </div>
    </FadeInSection>
  );
}

function ProductsSection() {
  return (
    <section id="products" className="section-gap" data-testid="products-section">
      <div className="section-container">
        <FadeInSection>
          <div style={{ textAlign: "center", marginBottom: 64 }}>
            <span className="badge badge-green" style={{ marginBottom: 16, display: "inline-flex" }}>
              <Leaf size={14} weight="fill" style={{ marginRight: 4 }} /> The Collection
            </span>
            <h2 className="font-serif" style={{ fontSize: "clamp(32px, 4vw, 48px)", fontWeight: 700, color: "var(--fg)", marginBottom: 16, letterSpacing: "-0.02em" }}>
              Tools for Your <span style={{ fontStyle: "italic" }}>Journey</span>
            </h2>
            <p className="font-body" style={{ fontSize: 17, color: "var(--muted-fg)", maxWidth: 500, margin: "0 auto" }}>
              Five carefully crafted products, each designed to address a different aspect of anxiety management.
            </p>
          </div>
        </FadeInSection>

        <div className="bento-grid">
          {PRODUCTS.map((product, i) => (
            <ProductCard key={product.id} product={product} index={i} />
          ))}
        </div>
      </div>
    </section>
  );
}

function BundleSection() {
  return (
    <section id="bundle" className="bundle-section section-gap" data-testid="bundle-section">
      <div className="section-container" style={{ position: "relative", zIndex: 1 }}>
        <FadeInSection>
          <div style={{ textAlign: "center", maxWidth: 700, margin: "0 auto" }}>
            <span style={{ display: "inline-flex", alignItems: "center", gap: 6, padding: "6px 16px", borderRadius: 50, background: "rgba(233, 196, 106, 0.2)", color: "#E9C46A", fontSize: 12, fontWeight: 700, textTransform: "uppercase", letterSpacing: 1, marginBottom: 24 }}>
              <Package size={14} weight="fill" /> Bundle & Save
            </span>

            <h2 className="font-serif" style={{ fontSize: "clamp(32px, 4vw, 48px)", fontWeight: 700, color: "white", marginBottom: 16, letterSpacing: "-0.02em" }}>
              {BUNDLE.title}
            </h2>

            <p className="font-body" style={{ fontSize: 17, color: "rgba(255,255,255,0.7)", marginBottom: 40, lineHeight: 1.7 }}>
              {BUNDLE.description}
            </p>

            <div style={{ display: "flex", alignItems: "center", justifyContent: "center", gap: 16, marginBottom: 32 }}>
              <span className="price-original" style={{ fontSize: 24, color: "rgba(255,255,255,0.4)" }}>{BUNDLE.original_price}</span>
              <span style={{ fontSize: 48, fontWeight: 800, color: "#E9C46A" }}>{BUNDLE.bundle_price}</span>
              <span style={{ background: "rgba(231, 111, 81, 0.9)", color: "white", padding: "6px 14px", borderRadius: 50, fontSize: 13, fontWeight: 700 }}>
                {BUNDLE.savings}
              </span>
            </div>

            <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 12, marginBottom: 40 }}>
              {[
                "All 5 digital products included",
                "Instant download after purchase",
                "Printable PDF format",
                "Lifetime access to updates",
              ].map((item, i) => (
                <div key={i} style={{ display: "flex", alignItems: "center", gap: 10 }}>
                  <Check size={16} weight="bold" color="#E9C46A" />
                  <span style={{ color: "rgba(255,255,255,0.8)", fontSize: 15 }}>{item}</span>
                </div>
              ))}
            </div>

            <a
              href={PAYHIP_LINKS.bundle}
              target="_blank"
              rel="noopener noreferrer"
              className="btn-accent"
              style={{ padding: "18px 48px", fontSize: 17, textDecoration: "none", display: "inline-flex" }}
              data-testid="bundle-cta-btn"
            >
              <Package size={20} weight="bold" /> Get the Complete Bundle
            </a>

            <p className="font-handwriting" style={{ fontSize: 20, color: "rgba(233, 196, 106, 0.6)", marginTop: 16 }}>
              Secure checkout on Payhip
            </p>
          </div>
        </FadeInSection>
      </div>
    </section>
  );
}

function TestimonialsSection() {
  const testimonials = [
    {
      name: "Sarah M.",
      role: "Teacher",
      text: "This journal completely changed my mornings. I went from waking up with dread to actually looking forward to my journaling routine. The prompts are thoughtful and never feel repetitive.",
      avatar: "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?ixlib=rb-4.0.3&auto=format&fit=crop&w=100&q=80",
      rating: 5,
    },
    {
      name: "James L.",
      role: "Software Engineer",
      text: "As someone who struggled with anxiety for years, the breathing exercise cards are a game changer. I keep them on my desk and use them during stressful meetings. Simple but incredibly effective.",
      avatar: "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?ixlib=rb-4.0.3&auto=format&fit=crop&w=100&q=80",
      rating: 5,
    },
    {
      name: "Priya K.",
      role: "Freelance Designer",
      text: "The Calm Mind ebook gave me actual tools instead of vague advice. The ABCDE method for reframing thoughts has been life-changing. I recommend the whole bundle to everyone.",
      avatar: "https://images.unsplash.com/photo-1494790108377-be9c29b29330?ixlib=rb-4.0.3&auto=format&fit=crop&w=100&q=80",
      rating: 5,
    },
  ];

  return (
    <section className="section-gap" style={{ background: "var(--muted)" }} data-testid="testimonials-section">
      <div className="section-container">
        <FadeInSection>
          <div style={{ textAlign: "center", marginBottom: 64 }}>
            <span className="badge badge-coral" style={{ marginBottom: 16, display: "inline-flex" }}>
              <Heart size={14} weight="fill" style={{ marginRight: 4 }} /> What People Say
            </span>
            <h2 className="font-serif" style={{ fontSize: "clamp(32px, 4vw, 48px)", fontWeight: 700, color: "var(--fg)", letterSpacing: "-0.02em" }}>
              Real Stories, Real <span style={{ fontStyle: "italic" }}>Calm</span>
            </h2>
          </div>
        </FadeInSection>

        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(300px, 1fr))", gap: 24 }}>
          {testimonials.map((t, i) => (
            <FadeInSection key={i} delay={i * 0.15}>
              <div className="testimonial-card" data-testid={`testimonial-${i}`}>
                <div className="star-rating" style={{ marginBottom: 16 }}>
                  {[...Array(t.rating)].map((_, j) => (
                    <Star key={j} size={16} weight="fill" color="#E9C46A" />
                  ))}
                </div>
                <p className="font-body" style={{ fontSize: 15, lineHeight: 1.7, color: "var(--muted-fg)", marginBottom: 20, fontStyle: "italic" }}>
                  "{t.text}"
                </p>
                <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
                  <img
                    src={t.avatar}
                    alt={t.name}
                    style={{ width: 40, height: 40, borderRadius: "50%", objectFit: "cover" }}
                  />
                  <div>
                    <p style={{ fontWeight: 600, fontSize: 14, color: "var(--fg)" }}>{t.name}</p>
                    <p style={{ fontSize: 12, color: "var(--muted-fg)" }}>{t.role}</p>
                  </div>
                </div>
              </div>
            </FadeInSection>
          ))}
        </div>
      </div>
    </section>
  );
}

function AboutSection() {
  return (
    <section id="about" className="section-gap" data-testid="about-section">
      <div className="section-container">
        <div style={{ display: "grid", gridTemplateColumns: "1fr", gap: 64, alignItems: "center" }}>
          <FadeInSection>
            <div style={{ maxWidth: 700, margin: "0 auto", textAlign: "center" }}>
              <span className="badge badge-teal" style={{ marginBottom: 16, display: "inline-flex" }}>
                <Leaf size={14} weight="fill" style={{ marginRight: 4 }} /> Why This Collection
              </span>
              <h2 className="font-serif" style={{ fontSize: "clamp(32px, 4vw, 48px)", fontWeight: 700, color: "var(--fg)", marginBottom: 24, letterSpacing: "-0.02em" }}>
                Built for People Who <span style={{ fontStyle: "italic" }}>Feel Too Much</span>
              </h2>
              <p className="font-body" style={{ fontSize: 17, lineHeight: 1.8, color: "var(--muted-fg)", marginBottom: 24 }}>
                Anxiety affects 1 in 4 people. Yet most resources are either too clinical or too vague. This collection bridges that gap with beautiful, practical tools backed by cognitive behavioral therapy and mindfulness research.
              </p>
              <p className="font-body" style={{ fontSize: 17, lineHeight: 1.8, color: "var(--muted-fg)", marginBottom: 32 }}>
                Each product is designed to be used daily, building habits that compound over time. No jargon, no judgment, just a gentle companion on your path to calm.
              </p>

              <div className="stats-grid" style={{ maxWidth: 600, margin: "0 auto" }}>
                {[
                  { number: "90", label: "Daily Prompts" },
                  { number: "20", label: "Exercise Cards" },
                  { number: "6", label: "Breathing Methods" },
                  { number: "12", label: "Weekly Themes" },
                ].map((stat, i) => (
                  <FadeInSection key={i} delay={i * 0.1}>
                    <div className="stat-card">
                      <p className="font-serif" style={{ fontSize: 36, fontWeight: 700, color: "var(--primary)", marginBottom: 4 }}>
                        {stat.number}
                      </p>
                      <p style={{ fontSize: 13, color: "var(--muted-fg)", fontWeight: 500 }}>
                        {stat.label}
                      </p>
                    </div>
                  </FadeInSection>
                ))}
              </div>
            </div>
          </FadeInSection>
        </div>
      </div>
    </section>
  );
}

function Footer() {
  return (
    <footer className="footer-section" style={{ padding: "64px 0 32px" }} data-testid="footer">
      <div className="section-container">
        <div style={{ display: "flex", flexDirection: "column", alignItems: "center", textAlign: "center" }}>
          <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 16 }}>
            <Leaf size={24} weight="fill" color="#A3B18A" />
            <span className="font-serif" style={{ fontSize: 20, fontWeight: 700, color: "white" }}>
              The Calm Mind Collection
            </span>
          </div>
          <p style={{ fontSize: 14, maxWidth: 400, marginBottom: 32, lineHeight: 1.7 }}>
            Helping you find peace, one page at a time. All products are digital downloads in PDF format.
          </p>

          <div style={{ display: "flex", gap: 32, marginBottom: 32, flexWrap: "wrap", justifyContent: "center" }}>
            <a href="#products" style={{ color: "rgba(255,255,255,0.6)", textDecoration: "none", fontSize: 14 }}>Products</a>
            <a href="#bundle" style={{ color: "rgba(255,255,255,0.6)", textDecoration: "none", fontSize: 14 }}>Bundle</a>
            <a href="#about" style={{ color: "rgba(255,255,255,0.6)", textDecoration: "none", fontSize: 14 }}>About</a>
          </div>

          <div style={{ width: "100%", height: 1, background: "rgba(255,255,255,0.1)", marginBottom: 24 }} />

          <p style={{ fontSize: 12, opacity: 0.4 }}>
            &copy; 2026 The Calm Mind Collection. All rights reserved. Not a substitute for professional medical advice.
          </p>
        </div>
      </div>
    </footer>
  );
}

function App() {
  return (
    <div data-testid="app-container">
      <Navbar />
      <HeroSection />
      <ProductsSection />
      <BundleSection />
      <TestimonialsSection />
      <AboutSection />
      <Footer />
      <LeadMagnetPopup />
    </div>
  );
}

export default App;
