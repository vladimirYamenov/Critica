'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function SignInForm() {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    if (!email || !password) { setError('EMAIL AND PASSWORD ARE REQUIRED.'); return; }
    setLoading(true);
    try {
      const res = await fetch('http://localhost:8000/api/auth/login/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });
      const data = await res.json();
      if (!res.ok) { setError(data.error || data.detail || 'LOGIN FAILED. PLEASE CHECK YOUR CREDENTIALS.'); return; }
      localStorage.setItem('accessToken', data.tokens.access);
      localStorage.setItem('refreshToken', data.tokens.refresh);
      localStorage.setItem('user', JSON.stringify(data.user));
      setSuccess('AUTHENTICATION SUCCESSFUL — REDIRECTING...');
      setTimeout(() => router.push('/dashboard'), 1200);
    } catch {
      setError('COULD NOT REACH THE SERVER. PLEASE CHECK YOUR CONNECTION.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={s.inner}>
      {/* Document header - scaled down to sit in upper-left area */}
      <div style={s.hdrWrap}>
        <div style={s.hdr}>
          <div style={s.logo}>
            <div style={s.oval1} />
            <div style={s.oval2} />
          </div>
          <div style={s.hdrTitle}>OFFICIAL STUDENT AUTHENTICATION DOCUMENT</div>
        </div>
      </div>

      {/* Rotated, ink-effect stamp */}
      <div style={s.stampWrap}>
        <span style={s.stamp}>AUTHENTICATION FORM</span>
      </div>

      {/* Main title section with separator line */}
      <div style={s.sec}>
        <div style={s.secDot} />
        <span>IDENTIFICATION</span>
        <div style={s.hrLine} />
      </div>

      {/* Messages */}
      {error && <div style={{ ...s.msg, ...s.msgErr }}>{error}</div>}
      {success && <div style={{ ...s.msg, ...s.msgOk }}>{success}</div>}

      <form onSubmit={handleSubmit} style={{ position: 'relative', zIndex: 1, marginTop: '24px' }}>
        <div style={s.fieldGroup}>
          <label style={s.lbl}>EMAIL ADDRESS</label>
          <input
            style={s.inp}
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Enter email address here..."
            required
            onFocus={(e) => (e.target.style.borderBottomColor = '#6A4CFF')}
            onBlur={(e) => (e.target.style.borderBottomColor = '#c4b48a')}
          />
        </div>

        <div style={s.fieldGroup}>
          <label style={{ ...s.lbl, marginTop: '12px' }}>PASSWORD</label>
          <input
            style={s.inp}
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Enter password here..."
            required
            onFocus={(e) => (e.target.style.borderBottomColor = '#6A4CFF')}
            onBlur={(e) => (e.target.style.borderBottomColor = '#c4b48a')}
          />
        </div>

        {/* Separator line before buttons */}
        <div style={s.hrLine} />

        {/* Consolidated action buttons at the bottom */}
        <div style={s.actionRow}>
          <button type="button" style={s.fgt} onClick={() => alert('Password recovery coming soon!')}>
            FORGOT PASSWORD?
          </button>

          <div style={s.subWrap}>
            <button
              type="submit"
              disabled={loading}
              style={{ ...s.btn, opacity: loading ? 0.55 : 1, cursor: loading ? 'not-allowed' : 'pointer' }}
              onMouseEnter={(e) => { if (!loading) { e.currentTarget.style.boxShadow = '1px 1px 0 #1a1209'; e.currentTarget.style.transform = 'translate(2px,2px)'; }}}
              onMouseLeave={(e) => { e.currentTarget.style.boxShadow = '3px 3px 0 #1a1209'; e.currentTarget.style.transform = 'none'; }}
            >
              {loading ? 'PROCEEDING...' : 'PROCEED TO ACCESS'}
            </button>
          </div>
        </div>
      </form>
    </div>
  );
}

const s: Record<string, React.CSSProperties> = {
  inner: { fontFamily: "'Courier Prime', monospace", position: 'relative', zIndex: 1, padding: '24px' },

  /* Header styling - aligned left */
  hdrWrap: { textAlign: 'left', marginBottom: '16px', display: 'flex', justifyContent: 'flex-start' },
  hdr: {
    background: '#1a1209',
    color: '#f0e6cc',
    padding: '9px 14px',
    display: 'flex',
    alignItems: 'center',
    gap: '12px',
    borderRadius: '1px',
    maxWidth: '400px', // Prevents it from taking full width
  },
  logo: { position: 'relative', width: '36px', height: '22px', flexShrink: 0 },
  oval1: { width: '24px', height: '15px', borderRadius: '50%', background: '#6A4CFF', position: 'absolute', left: 0, top: '3px' },
  oval2: { width: '24px', height: '15px', borderRadius: '50%', background: '#20C4B4', position: 'absolute', left: '12px', top: '3px', opacity: 0.85 },
  hdrTitle: { fontFamily: "'Courier Prime', monospace", fontSize: '10px', fontWeight: 700, letterSpacing: '0.16em', color: '#f0e6cc' },

  /* Title and separators */
  sec: {
    display: 'flex', alignItems: 'center', gap: '10px',
    margin: '14px 0 8px',
    fontSize: '9px', fontWeight: 700, letterSpacing: '0.2em', color: '#5c4a28',
    fontFamily: "'Courier Prime', monospace",
  },
  secDot: { width: '10px', height: '10px', borderRadius: '50%', background: '#c4b48a', flexShrink: 0 },
  hrLine: { flex: 1, height: '1.5px', background: '#c4b48a', opacity: 0.7 },

  /* Rotated ink-effect stamp */
  stampWrap: { textAlign: 'center', margin: '30px 0', display: 'flex', justifyContent: 'center' },
  stamp: {
    display: 'inline-block',
    border: '3px solid #6A4CFF',
    padding: '7px 20px',
    fontFamily: "'Courier Prime', monospace",
    fontSize: '11px',
    fontWeight: 700,
    letterSpacing: '0.2em',
    color: '#6A4CFF',
    background: 'rgba(106,76,255,0.08)',
    transform: 'rotate(-5deg)', // Apply rotation like ink
    opacity: 0.8, // Make it look slightly faded/less digitally sharp
  },

  /* Input group structure */
  fieldGroup: { marginBottom: '20px' },
  msg: { borderRadius: '2px', padding: '7px 10px', fontSize: '10px', margin: '10px 0 4px', fontFamily: "'Courier Prime', monospace", letterSpacing: '0.05em' },
  msgErr: { background: '#f5d4cc', border: '1.5px solid #c05040', color: '#7a2010' },
  msgOk:  { background: '#ccf0d8', border: '1.5px solid #3a8050', color: '#1a5030' },
  lbl: {
    display: 'block', fontSize: '9px', fontWeight: 700, letterSpacing: '0.18em',
    color: '#5c4a28', marginBottom: '6px',
    fontFamily: "'Courier Prime', monospace",
  },
  inp: {
    width: '100%', background: 'transparent', border: 'none',
    borderBottom: '2px solid #c4b48a',
    fontFamily: "'Courier Prime', monospace", fontSize: '13px', color: '#1a1209',
    padding: '7px 4px', outline: 'none', transition: 'border-color 0.15s',
    boxSizing: 'border-box',
  },

  /* Action area consolidation */
  actionRow: { display: 'flex', flexDirection: 'column', alignItems: 'center', marginTop: '24px', gap: '16px' },
  fgt: {
    textAlign: 'center', fontSize: '9px', fontWeight: 700,
    letterSpacing: '0.1em', color: '#6A4CFF', background: 'none', border: 'none',
    cursor: 'pointer', fontFamily: "'Courier Prime', monospace",
  },
  subWrap: { textAlign: 'center' },
  btn: {
    fontFamily: "'Courier Prime', monospace", fontSize: '10px', fontWeight: 700,
    letterSpacing: '0.18em', color: '#1a1209', background: '#d4c9a8',
    border: '2px solid #1a1209', padding: '10px 30px', cursor: 'pointer',
    boxShadow: '3px 3px 0 #1a1209', transition: 'box-shadow 0.1s, transform 0.1s',
  },
};