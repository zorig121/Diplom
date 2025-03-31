import { useEffect, useState } from "react";

export default function Toast({ message, type = "success", style = {} }) {
    const background = type === "success" ? "#00b894" : "#d63031";
    const icon = type === "success" ? "✅" : "❌";
  
    const [exiting, setExiting] = useState(false);
    const [visible, setVisible] = useState(true);
  
    useEffect(() => {
      const timeout = setTimeout(() => setExiting(true), 4000);
      return () => clearTimeout(timeout);
    }, []);
  
    const handleAnimationEnd = () => {
      if (exiting) setVisible(false);
    };
  
    if (!visible) return null;
  
    return (
      <>
        <style>{`
          @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
          }
          @keyframes fadeOut {
            from { opacity: 1; transform: translateY(0); }
            to { opacity: 0; transform: translateY(-20px); }
          }
          .fade-in {
            animation: fadeIn 0.4s ease forwards;
          }
          .fade-out {
            animation: fadeOut 0.4s ease forwards;
          }
        `}</style>
        <div
          className={exiting ? "fade-out" : "fade-in"}
          onAnimationEnd={handleAnimationEnd}
          style={{
            position: "fixed",
            background,
            color: "white",
            padding: "0.75rem 1.25rem",
            borderRadius: "0.5rem",
            boxShadow: "0 0 10px rgba(0,0,0,0.2)",
            zIndex: 9999,
            fontWeight: "500",
            fontSize: "0.95rem",
            ...style, // 👈 dynamic top/right injected
          }}
        >
          {icon} {message}
        </div>
      </>
    );
  }
  