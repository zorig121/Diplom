// src/pages/AuthPage.jsx

import { useEffect, useState, useRef } from 'react';
import gpuIcon from '../assets/gpu.png';
import Toast from '../components/Toast';

const API_BASE = 'http://localhost:8000';

const styles = {
    container: {
      position: 'relative',
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      minHeight: '100vh',
      overflow: 'hidden',
      background: 'linear-gradient(145deg, #0f0c29, #302b63, #24243e)',
      padding: '1rem',
      fontFamily: 'Roboto, sans-serif',
    },
    card: {
      background: 'linear-gradient(135deg, rgba(58,0,80,0.6), rgba(0,210,255,0.3))',
      backdropFilter: 'blur(18px)',
      padding: '2.5rem',
      borderRadius: '1.25rem',
      width: '100%',
      maxWidth: '540px',
      boxShadow: '0 12px 45px rgba(0, 255, 255, 0.25)',
      transform: 'scale(0.95)',
      opacity: 0,
      animation: 'fadeInScale 0.6s ease forwards',
      zIndex: 1,
      transition: 'all 0.4s ease',
      textAlign: 'center',
      border: '1px solid rgba(255, 255, 255, 0.15)',
      fontFamily: 'Orbitron, sans-serif',
    },
    icon: {
      width: '64px',
      height: '64px',
      marginBottom: '1.5rem',
      animation: 'pulseGlow 3s ease-in-out infinite',
    },
    heading: {
      marginBottom: '1.25rem',
      color: '#fff',
      fontSize: '1.75rem',
      fontWeight: 'bold',
      letterSpacing: '0.5px',
    },
    inputWrapper: {
      position: 'relative',
      marginBottom: '1.25rem',
    },
    input: {
      display: 'block',
      width: '100%',
      padding: '0.75rem 1rem',
      background: 'rgba(255,255,255,0.1)',
      color: 'white',
      border: '1px solid #8884',
      borderRadius: '0.5rem',
      outline: 'none',
      fontSize: '1rem',
    },
    togglePassword: {
      position: 'absolute',
      right: '1rem',
      top: '50%',
      transform: 'translateY(-50%)',
      background: 'none',
      border: 'none',
      color: 'white',
      cursor: 'pointer',
      fontSize: '1.1rem',
      padding: '0 0.25rem',
    },
    button: {
      width: '100%',
      padding: '0.75rem',
      backgroundColor: '#6a00f4',
      color: 'white',
      border: 'none',
      borderRadius: '0.5rem',
      cursor: 'pointer',
      fontWeight: '600',
      letterSpacing: '0.5px',
      transition: 'background-color 0.3s ease',
    },
    toggle: {
      color: '#00eaff',
      cursor: 'pointer',
      textDecoration: 'underline',
      marginLeft: '4px',
    },
    error: {
      color: '#ff4d6d',
      fontSize: '0.9rem',
      marginBottom: '1rem',
    },
    loader: {
      color: 'white',
      fontSize: '1.2rem',
      animation: 'fadeInScale 0.4s ease',
      marginTop: '2rem',
    },
  };

const animationStyle = `
  @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500&family=Roboto&display=swap');
  @keyframes fadeInScale {
    from { transform: scale(0.95); opacity: 0; }
    to { transform: scale(1); opacity: 1; }
  }
  @keyframes pulseGlow {
    0% { transform: scale(1); filter: drop-shadow(0 0 2px #00ffff); }
    50% { transform: scale(1.1); filter: drop-shadow(0 0 12px #ff00ff); }
    100% { transform: scale(1); filter: drop-shadow(0 0 2px #00ffff); }
  }
`;

export default function AuthPage() {
  const [isLogin, setIsLogin] = useState(true);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [email, setEmail] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);

  const [toasts, setToasts] = useState([]);
  const isMounted = useRef(false);

  useEffect(() => {
    isMounted.current = true;
    return () => {
      isMounted.current = false;
    };
  }, []);

  const showToast = (message, type = 'success') => {
    const id = Date.now();
    if (!isMounted.current) return;
    setToasts((prev) => [...prev, { id, message, type }]);
    setTimeout(() => {
      if (!isMounted.current) return;
      setToasts((prev) => prev.filter((t) => t.id !== id));
    }, 5000);
  };

  const validatePassword = (value) => {
    if (!value) return 'Нууц үг шаардлагатай';
    if (value.length < 6) return 'Нууц үг хамгийн багадаа 6 тэмдэгт байх ёстой';
    if (!/[!@#$%^&*]/.test(value)) return 'Нууц үг тусгай тэмдэгт агуулсан байх ёстой (!@#$%^&*)';
    return '';
  };

  const validateEmail = (value) => {
    if (!value) return 'Имэйл шаардлагатай';
    if (!/^\S+@\S+\.\S+$/.test(value)) return 'Имэйл формат буруу байна';
    return '';
  };

  const validateConfirmPassword = (pass, confirmPass) => {
    if (!confirmPass) return 'Нууц үг баталгаажуулалт шаардлагатай';
    if (pass !== confirmPass) return 'Нууц үг таарахгүй байна';
    return '';
  };

  const isFormValid = () => {
    const emailError = validateEmail(email);
    const passError = validatePassword(password);
    let confirmError = '', emptyFields = '';

    if (!isLogin) {
      if (!username || !confirmPassword) {
        emptyFields = 'Бүх талбарыг бөглөнө үү.';
      } else {
        confirmError = validateConfirmPassword(password, confirmPassword);
      }
    }

    if (emailError || passError || confirmError || emptyFields) {
      if (emptyFields) showToast(emptyFields, 'error');
      if (emailError) showToast(emailError, 'error');
      if (passError) showToast(passError, 'error');
      if (confirmError) showToast(confirmError, 'error');
      return false;
    }

    return true;
  };

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
      fetch(`${API_BASE}/api/me`, {
        headers: { Authorization: `Bearer ${token}` },
      })
        .then((res) => (res.ok ? res.json() : Promise.reject('Unauthorized')))
        .then(() => {
          window.location.href = '/dashboard';
        })
        .catch(() => {
          localStorage.removeItem('access_token');
        });
    }
  }, []);

  const toggleMode = () => {
    setIsLogin(!isLogin);
    setUsername('');
    setPassword('');
    setConfirmPassword('');
    setEmail('');
  };

  const handleSubmit = async () => {
    if (!isFormValid()) return;
    setLoading(true);

    const endpoint = isLogin ? `${API_BASE}/api/login` : `${API_BASE}/api/register`;
    try {
      const res = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(
          isLogin
            ? { email, password }
            : { username, password, email }
        ),
      });
      const data = await res.json();

      if (!res.ok) {
        showToast(data.detail || 'Алдаа гарлаа', 'error');
        setLoading(false);
      } else {
        if (isLogin) {
          localStorage.setItem('access_token', data.access_token || data.token);
          showToast('Амжилттай нэвтэрлээ', 'success');
          setTimeout(() => {
            window.location.href = '/dashboard';
          }, 300);
        } else {
          showToast('Амжилттай бүртгэгдлээ! Одоо нэвтэрнэ үү.', 'success');
          toggleMode();
        }
        setLoading(false);
      }
    } catch {
      showToast('Сервертэй холбогдож чадсангүй.', 'error');
      setLoading(false);
    }
  };

  return (
    <>
      <style>{animationStyle}</style>
      <div style={{ position: 'fixed', top: 0, right: 0, zIndex: 9999 }}>
        {toasts.map((t, i) => (
            <Toast
            key={t.id}
            message={t.message}
            type={t.type}
            style={{ top: `${1 + i * 4}rem`, right: '1rem' }}
            />
        ))}
      </div>
      <div style={styles.container}>
        {loading ? (
          <div style={styles.loader}>Нэвтэрч байна...</div>
        ) : (
          <div className="auth-card" style={styles.card}>
            <img src={gpuIcon} alt="GPU Icon" style={styles.icon} />
            <h2 style={styles.heading}>{isLogin ? 'Нэвтрэх' : 'Бүртгүүлэх'}</h2>
            <form onSubmit={(e) => {
              e.preventDefault();
              handleSubmit();
            }}>
              {!isLogin && (
                <>
                  <div style={styles.inputWrapper}>
                    <input type="text" placeholder="Хэрэглэгчийн нэр" value={username}
                      onChange={(e) => setUsername(e.target.value)} style={styles.input} />
                  </div>
                </>
              )}
              <div style={styles.inputWrapper}>
                <input type="email" placeholder="Имэйл" value={email}
                  onChange={(e) => setEmail(e.target.value)} style={styles.input} />
              </div>
              <div style={styles.inputWrapper}>
                <input type={showPassword ? 'text' : 'password'} placeholder="Нууц үг"
                  value={password} onChange={(e) => setPassword(e.target.value)} style={styles.input} />
                <button type="button" onClick={() => setShowPassword(!showPassword)} style={styles.togglePassword}>
                  {showPassword ? '🙈' : '👁️'}
                </button>
              </div>
              {!isLogin && (
                <div style={styles.inputWrapper}>
                  <input type={showPassword ? 'text' : 'password'} placeholder="Нууц үг давтах"
                    value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} style={styles.input} />
                </div>
              )}
              <button type="submit" style={styles.button}>
                {isLogin ? 'Нэвтрэх' : 'Бүртгүүлэх'}
              </button>
            </form>
            <p style={{ marginTop: 10, color: 'white' }}>
              {isLogin ? 'Шинэ хэрэглэгч үү?' : 'Бүртгэлтэй хэрэглэгч үү?'}{' '}
              <span onClick={toggleMode} style={styles.toggle}>
                {isLogin ? 'Бүртгүүлэх' : 'Нэвтрэх'}
              </span>
            </p>
          </div>
        )}
      </div>
    </>
  );
}
