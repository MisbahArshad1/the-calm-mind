import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { X, Gift, EnvelopeSimple, ArrowRight, Check, SpinnerGap } from "@phosphor-icons/react";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export default function LeadMagnetPopup() {
  const [show, setShow] = useState(false);
  const [email, setEmail] = useState("");
  const [name, setName] = useState("");
  const [status, setStatus] = useState("idle"); // idle | loading | success | error
  const [message, setMessage] = useState("");

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

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!email) return;

    setStatus("loading");
    try {
      const res = await axios.post(`${API}/subscribe`, { email, name });
      setStatus("success");
      setMessage(res.data.message);
      // Auto-download after short delay
      setTimeout(() => {
        window.open(`${API}/lead-magnet`, "_blank");
      }, 1000);
    } catch (err) {
      setStatus("error");
      setMessage("Something went wrong. Please try again.");
    }
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
                    transition: "background 0.2s",
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

              {/* Form area */}
              <div style={{ padding: "24px 32px 28px" }}>
                {status === "success" ? (
                  <motion.div
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    style={{ textAlign: "center" }}
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
                      {message}
                    </p>
                    <p style={{ fontSize: 13, color: "#5C5C5C" }}>
                      Your PDF is downloading now...
                    </p>
                  </motion.div>
                ) : (
                  <form onSubmit={handleSubmit} data-testid="lead-magnet-form">
                    <div style={{ marginBottom: 12 }}>
                      <label
                        style={{
                          display: "block",
                          fontSize: 13,
                          fontWeight: 600,
                          color: "#1A1A1A",
                          marginBottom: 6,
                          fontFamily: "'Manrope', sans-serif",
                        }}
                      >
                        First name (optional)
                      </label>
                      <input
                        type="text"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        placeholder="Your first name"
                        style={{
                          width: "100%",
                          padding: "12px 16px",
                          borderRadius: 12,
                          border: "1.5px solid #E6E2D8",
                          fontSize: 14,
                          fontFamily: "'Manrope', sans-serif",
                          outline: "none",
                          transition: "border-color 0.2s",
                          boxSizing: "border-box",
                        }}
                        data-testid="lead-magnet-name-input"
                      />
                    </div>

                    <div style={{ marginBottom: 16 }}>
                      <label
                        style={{
                          display: "block",
                          fontSize: 13,
                          fontWeight: 600,
                          color: "#1A1A1A",
                          marginBottom: 6,
                          fontFamily: "'Manrope', sans-serif",
                        }}
                      >
                        Email address *
                      </label>
                      <div style={{ position: "relative" }}>
                        <EnvelopeSimple
                          size={18}
                          color="#5C5C5C"
                          style={{ position: "absolute", left: 14, top: "50%", transform: "translateY(-50%)" }}
                        />
                        <input
                          type="email"
                          value={email}
                          onChange={(e) => setEmail(e.target.value)}
                          placeholder="you@example.com"
                          required
                          style={{
                            width: "100%",
                            padding: "12px 16px 12px 40px",
                            borderRadius: 12,
                            border: "1.5px solid #E6E2D8",
                            fontSize: 14,
                            fontFamily: "'Manrope', sans-serif",
                            outline: "none",
                            transition: "border-color 0.2s",
                            boxSizing: "border-box",
                          }}
                          data-testid="lead-magnet-email-input"
                        />
                      </div>
                    </div>

                    {status === "error" && (
                      <p style={{ color: "#E76F51", fontSize: 13, marginBottom: 12 }} data-testid="lead-magnet-error">
                        {message}
                      </p>
                    )}

                    <button
                      type="submit"
                      disabled={status === "loading"}
                      className="btn-accent"
                      style={{
                        width: "100%",
                        justifyContent: "center",
                        opacity: status === "loading" ? 0.7 : 1,
                      }}
                      data-testid="lead-magnet-submit-btn"
                    >
                      {status === "loading" ? (
                        <>
                          <SpinnerGap size={18} className="animate-spin" /> Sending...
                        </>
                      ) : (
                        <>
                          Get My Free Guide <ArrowRight size={18} weight="bold" />
                        </>
                      )}
                    </button>

                    <p
                      style={{
                        textAlign: "center",
                        fontSize: 11,
                        color: "#5C5C5C",
                        marginTop: 12,
                      }}
                    >
                      No spam, ever. Just calm vibes.
                    </p>
                  </form>
                )}
              </div>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}
