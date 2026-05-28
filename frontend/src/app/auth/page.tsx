'use client';

import { useState } from 'react';
import SignUpForm from '@/components/auth/SignUpForm';
import SignInForm from '@/components/auth/SignInForm';

export default function AuthPage() {
  const [activeTab, setActiveTab] = useState<'signup' | 'signin'>('signup');

  return (
    <main className="auth-page">
      <div className="folder-unit">

        {/* Folder Tabs */}
        <div className="tab-row">
          <button
            onClick={() => setActiveTab('signup')}
            className={`tab-btn ${activeTab === 'signup' ? 'tab-active' : 'tab-inactive'}`}
          >
            Sign Up
          </button>
          <button
            onClick={() => setActiveTab('signin')}
            className={`tab-btn ${activeTab === 'signin' ? 'tab-active' : 'tab-inactive'}`}
          >
            Sign In
          </button>
        </div>

        {/* Folder Body */}
        <div className="folder-body">

          {/* Binder punch holes */}
          <div className="binder-holes">
            <div className="hole" />
            <div className="hole" />
            <div className="hole" />
            <div className="hole" />
          </div>

          {/* Paper Insert */}
          <div className="paper">
            {activeTab === 'signup' ? <SignUpForm /> : <SignInForm />}
          </div>

        </div>
      </div>

      <style>{`
        .auth-page {
          min-height: 100vh;
          background: #6b6b6b;
          display: flex;
          align-items: center;
          justify-content: center;
          padding: 2rem 1rem;
          font-family: 'Courier New', Courier, monospace;
        }

        .folder-unit {
          width: 560px;
          display: flex;
          flex-direction: column;
          gap: 0;
          radius: 10px;
        }

        /* ── Tabs ── */
        .tab-row {
          display: flex;
          flex-direction: row;
          align-items: flex-end;
          justify-content: flex-end;
          gap: 4px;
          padding-bottom: 0;
        }

        .tab-btn {
          padding: 9px 28px;
          font-family: 'Courier New', Courier, monospace;
          font-size: 13px;
          font-weight: 700;
          border: none;
          cursor: pointer;
          letter-spacing: 0.03em;
          border-radius: 8px 8px 0 0;
          transition: background 0.12s, color 0.12s;
          line-height: 1;
        }

        .tab-active {
          background: #8c8a84;
          color: #f0ede6;
          padding: 10px 28px 10px;
        }

        .tab-inactive {
          background: #6e6c68;
          color: #a8a6a0;
          padding: 8px 28px 10px;
        }

        .tab-inactive:hover {
          background: #7a7874;
          color: #c8c6c0;
        }

        /* ── Folder Body ── */
        .folder-body {
          background: #8c8a84;
          border-radius: 0 0 10px 10px;
          min-height: 500px; /* <--- Forces the folder to be at least this tall */
          padding: 16px 16px 20px 12px;
          position: relative;
          width: 100%;
          box-sizing: border-box;
        }

        /* ── Punch Holes ── */
        .binder-holes {
          position: absolute;
          left: 16px;
          top: 16px;
          bottom: 16px;
          display: flex;
          flex-direction: column;
          justify-content: space-around;
        }

        .hole {
          width: 14px;
          height: 14px;
          border-radius: 50%;
          background: #5a5a58;
          border: 2px solid #4a4a48;
          box-sizing: border-box;
        }

        /* ── Paper Insert ── */
        .paper {
          background: #c8c5bc;
          border-radius: 4px;
          padding: 22px 22px 22px 52px;
          border: 1px solid #b0ada4;
          box-sizing: border-box;
        }
      `}</style>
    </main>
  );
}