import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { X, Gift, EnvelopeSimple, ArrowRight, Check, SpinnerGap } from "@phosphor-icons/react";

// ============================================================
// UPDATE THIS WITH YOUR FREE PAYHIP LEAD MAGNET LINK
// On Payhip, create a $0 (free) product with the lead magnet PDF
// and set it to "Pay What You Want" with minimum $0
// This way Payhip captures the email FOR you automatically!
// ============================================================
const LEAD_MAGNET_LINK = "https://payhip.com/b/YOUR_FREE_LEAD_MAGNET_LINK";

export default function LeadMagnetPopup() {
  const [show, setShow] = useState(false);
  const [clicked, setClicked] = useState(false);

  useEffect(() => {
    const dismissed = sessionStorage.getItem("lead_popup_dismissed");
    if (dismissed) return;

    const timer = setTimeout(() => {
      setShow(true);
    }, 12000);

    const handleScroll = () => {
      const scrollPercent = (window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100;
      if (scrollPercent > 40 && !sessionStorage.getItem("lead_popup_dismissed")) {
        setShow(true);
        window.removeEventListener("scroll", handleScroll);
      }
    };

    window.addEventListener("scroll", handleScroll);
    return () => {
      clearTimeout(timer);
      window.removeEventListener("scroll", handleScroll);
    };
  }, []);

  const handleClose = () => {
    setShow(false);
    sessionStorage.setItem("lead_popup_dismissed", "true");
  };

  const handleGetGuide = () => {
    setClicked(true);
    window.open(LEAD_MAGNET_LINK, "_blank");
    setTimeout(() => {
      handleClose();
    }, 2000);
  };

  return (
    <AnimatePresence>
      {show && (
        <>
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={handleClose}
            style={{
              position: "fixed",
              inset: 0,
              background: "rgba(0,0,0,0.4)",
              backdropFilter: "blur(4px)",
              zIndex: 10000,
            }}
            data-testid="lead-magnet-backdrop"
          />

          {/* Modal */}
          <motion.div
            initial={{ opacity: 0, scale: 0.9, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.9, y: 20 }}
            transition={{ type: "spring", damping: 25, stiffness: 300 }}
            style={{
              position: "fixed",
              top: "50%",
              left: "50%",
              transform: "translate(-50%, -50%)",
              zIndex: 10001,
              width: "90%",
              maxWidth: 460,
              maxHeight: "92vh",
            }}
            data-testid="lead-magnet-popup"
          >
            <div
              style={{
                background: "#FFFFFF",
                borderRadius: 24,
                overflow: "hidden",
                boxShadow: "0 25px 60px rgba(0,0,0,0.15)",
                maxHeight: "92vh",
                overflowY: "auto",
              }}
            >
              {/* Top colored bar */}
              <div
                style={{
                  background: "linear-gradient(135deg, #3A5A40 0%, #2A9D8F 100%)",
                  padding: "24px 32px 20px",
                  position: "relative",
                }}
              >
                <button
                  onClick={handleClose}
                  style={{
                    position: "absolute",
                    top: 16,
                    right: 16,
                    background: "rgba(255,255,255,0.15)",
                    border: "none",
                    borderRadius: "50%",
                    width: 32,
                    height: 32,
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    cursor: "pointer",
                  }}
                  data-testid="lead-magnet-close-btn"
                >
                  <X size={16} color="white" weight="bold" />
                </button>

                <div
                  style={{
                    width: 48,
                    height: 48,
                    borderRadius: 14,
                    background: "rgba(255,255,255,0.2)",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    marginBottom: 16,
                  }}
                >
                  <Gift size={24} weight="fill" color="white" />
                </div>

                <p
                  style={{
                    color: "rgba(255,255,255,0.7)",
                    fontSize: 12,
                    fontWeight: 700,
                    textTransform: "uppercase",
                    letterSpacing: 1,
                    marginBottom: 8,
                    fontFamily: "'Manrope', sans-serif",
                  }}
                >
                  Free Download
                </p>

                <h3
                  className="font-serif"
                  style={{
                    color: "white",
                    fontSize: 24,
                    fontWeight: 700,
                    lineHeight: 1.2,
                    marginBottom: 8,
                  }}
                >
                  5 Emergency Calm Techniques
                </h3>

                <p
                  style={{
                    color: "rgba(255,255,255,0.8)",
                    fontSize: 14,
                    lineHeight: 1.5,
                    fontFamily: "'Manrope', sans-serif",
                  }}
                >
                  Science-backed methods that work in under 2 minutes. Your instant toolkit for when anxiety hits.
                </p>
              </div>

              {/* CTA area */}
              <div style={{ padding: "24px 32px 28px" }}>
                {clicked ? (
                  <motion.div
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    style={{ textAlign: "center", padding: "16px 0" }}
                    data-testid="lead-magnet-success"
                  >
                    <div
                      style={{
                        width: 56,
                        height: 56,
                        borderRadius: "50%",
                        background: "#dcfce7",
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                        margin: "0 auto 16px",
                      }}
                    >
                      <Check size={28} weight="bold" color="#166534" />
                    </div>
                    <p style={{ fontSize: 16, fontWeight: 600, color: "#1A1A1A", marginBottom: 8 }}>
                      Opening your free guide!
                    </p>
                    <p style={{ fontSize: 13, color: "#5C5C5C" }}>
                      Complete the free checkout to get your PDF.
                    </p>
                  </motion.div>
                ) : (
                  <div data-testid="lead-magnet-cta-area">
                    <div style={{ marginBottom: 20 }}>
                      {[
                        "Physiological Sigh - calm in 30 seconds",
                        "5-4-3-2-1 Grounding technique",
                        "Box Breathing used by Navy SEALs",
                        "Butterfly Hug for emotional overwhelm",
                        "4-7-8 Sleep Breath for insomnia",
                      ].map((item, i) => (
                        <div key={i} style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 8 }}>
                          <Check size={14} weight="bold" color="#3A5A40" />
                          <span style={{ fontSize: 13, color: "#5C5C5C", fontFamily: "'Manrope', sans-serif" }}>{item}</span>
                        </div>
                      ))}
                    </div>

                    <button
                      onClick={handleGetGuide}
                      className="btn-accent"
                      style={{
                        width: "100%",
                        justifyContent: "center",
                      }}
                      data-testid="lead-magnet-submit-btn"
                    >
                      Get My Free Guide <ArrowRight size={18} weight="bold" />
                    </button>

                    <p
                      style={{
                        textAlign: "center",
                        fontSize: 11,
                        color: "#5C5C5C",
                        marginTop: 12,
                      }}
                    >
                      Free on Payhip - no credit card required
                    </p>
                  </div>
                )}
              </div>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}
