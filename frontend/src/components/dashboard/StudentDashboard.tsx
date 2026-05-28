'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';

interface Tab {
  id: number;
  label: string;
}

interface Lesson {
  id: number;
  icon: string;
  title: string;
  status: 'active' | 'done';
  description: string;
  progress: number;
  exercises: { completed: number; total: number };
}

const tabs: Tab[] = [
  { id: 1, label: '[1] TEXT STRUCTURE\nMASTERY' },
  { id: 2, label: '[2] SNAP-IN-GAP' },
  { id: 3, label: '[3] TAP THE CLUES' },
  { id: 4, label: '[4] FACT SCANNER' },
];

const lessons: Lesson[] = [
  {
    id: 1,
    icon: '⊕',
    title: 'Logic Thread',
    status: 'active',
    description:
      'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.',
    progress: 85,
    exercises: { completed: 3, total: 4 },
  },
  {
    id: 2,
    icon: '⊞',
    title: 'Snap In Gap',
    status: 'done',
    description:
      'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.',
    progress: 100,
    exercises: { completed: 4, total: 4 },
  },
];

export default function StudentDashboard() {
  const [activeTab, setActiveTab] = useState<number>(1);
  const [scrollPosition, setScrollPosition] = useState<number>(0);
  const [showProfileMenu, setShowProfileMenu] = useState<boolean>(false);
  const router = useRouter();

  const handleLogout = () => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('user');
    router.push('/auth');
  };

  return (
    <div className="min-h-screen bg-[#1e1e1e] text-[#eee] font-serif">
      {/* TOPBAR */}
      <header className="h-[52px] bg-[#1e1e1e] flex items-center justify-end gap-9 px-9 border-b border-[#333]">
        <div className="flex items-center gap-2 font-mono text-xs text-[#ddd]">
          <span className="text-sm">🔥</span>
          <strong>Streak:</strong>&nbsp;5 Days
        </div>
        <div className="flex items-center gap-2 font-mono text-xs text-[#ddd]">
          <span className="text-sm">⭐</span>
          <strong>Total:</strong>&nbsp;2,450 XP
        </div>
        <div className="relative">
          <button
            onClick={() => setShowProfileMenu(!showProfileMenu)}
            className="flex items-center gap-2 font-mono text-xs text-[#ddd] hover:text-[#fff] cursor-pointer transition-colors"
          >
            <span className="text-sm">👤</span>Juan Dela Cruz
          </button>
          {showProfileMenu && (
            <div className="absolute top-full right-0 mt-2 bg-[#2b2b2b] border border-[#444] rounded-sm shadow-lg z-50 min-w-[150px]">
              <button
                onClick={handleLogout}
                className="w-full text-left px-4 py-2 text-xs font-mono text-[#ddd] hover:bg-[#3a3a3a] hover:text-[#fff] transition-colors border-t border-[#444] first:border-t-0"
              >
                Logout
              </button>
            </div>
          )}
        </div>
      </header>

      {/* DARK SPACER */}
      <div className="h-20 bg-[#2b2b2b]" />

      {/* BODY ROW */}
      <div className="flex h-[calc(100vh-52px-80px)] bg-[#2b2b2b]">
        {/* LEFT COLUMN */}
        <div className="flex-1 flex flex-col min-w-0">
          {/* TABS */}
          <div className="flex items-end flex-shrink-0 bg-[#2b2b2b]">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`px-7 h-[52px] flex items-center justify-center font-mono text-xs font-bold uppercase tracking-wider cursor-pointer border-none outline-none whitespace-pre-wrap text-center transition-all ${
                  activeTab === tab.id
                    ? 'bg-[#c8c4bc] text-[#111] h-[60px]'
                    : 'bg-[#444] text-[#aaa] hover:bg-[#505050] hover:text-[#ccc]'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>

          {/* CONTENT PANEL */}
          <div className="flex-1 bg-[#c8c4bc] overflow-hidden flex">
            <div
              className="flex-1 overflow-y-auto px-9 pt-[30px] pb-[30px]"
              onScroll={(e) =>
                setScrollPosition(
                  (e.currentTarget.scrollTop /
                    (e.currentTarget.scrollHeight -
                      e.currentTarget.clientHeight)) *
                    100
                )
              }
            >
              {/* Doc Header */}
              <div className="text-center mb-6">
                <div className="inline-block border-[1.5px] border-[#777] px-6 py-1 font-mono text-xs tracking-widest text-[#333] bg-white bg-opacity-20 mb-4">
                  OFFICIAL STUDENT DASHBOARD DOCUMENT
                </div>
                <div className="flex items-center gap-0">
                  <div className="flex-1 h-px bg-[#888]" />
                  <div className="border-2 border-[#555] px-4 py-[7px] font-mono text-sm font-bold uppercase tracking-wider text-[#111] bg-[#ddd9d0] whitespace-nowrap">
                    TEXT STRUCTURE MASTERY
                  </div>
                  <div className="flex-1 h-px bg-[#888]" />
                </div>
              </div>

              {/* Bullet above card 1 */}
              <div className="flex flex-col items-start gap-1.5 my-1.5 ml-0">
                <div className="w-3 h-3 rounded-full bg-[#888] border-2 border-[#aaa] flex-shrink-0" />
              </div>

              {/* CARDS */}
              {lessons.map((lesson, idx) => (
                <div key={lesson.id}>
                  {/* Card Row */}
                  <div className="flex items-start gap-2.5 mb-1.5">
                    <div className="w-[14px] h-[14px] rounded-full bg-[#888] border-2 border-[#aaa] flex-shrink-0 mt-[14px]" />

                    {/* Card */}
                    <div className="flex-1 bg-[#f0ece4] border border-[#bbb] rounded-sm p-4 text-[#111] relative min-w-0">
                      {/* Card Top */}
                      <div className="flex justify-between items-center mb-2">
                        <div className="flex items-center gap-2">
                          <div className="w-6 h-6 bg-[#111] rounded-sm flex items-center justify-center text-white text-xs flex-shrink-0">
                            {lesson.icon}
                          </div>
                          <div className="font-mono text-xs font-bold uppercase tracking-wider">
                            {lesson.title}
                          </div>
                        </div>
                        <div
                          className={`font-mono text-xs tracking-wider px-[7px] py-[3px] border uppercase flex-shrink-0 ${
                            lesson.status === 'active'
                              ? 'text-[#55aaff] border-[#55aaff] bg-blue-100 bg-opacity-10'
                              : 'text-[#4ddd94] border-[#4ddd94] bg-green-100 bg-opacity-10'
                          }`}
                        >
                          {lesson.status === 'active'
                            ? 'UNLOCKED / ACTIVE'
                            : 'COMPLETED / DONE'}
                        </div>
                      </div>

                      {/* Description */}
                      <p className="text-xs leading-relaxed text-[#555] mb-2.5">
                        {lesson.description}
                      </p>

                      {/* Inner Bullet */}
                      <div className="flex items-center gap-2 mb-1">
                        <div className="w-2.5 h-2.5 rounded-full bg-[#aaa] border-[1.5px] border-[#ccc] flex-shrink-0" />
                      </div>

                      {/* Progress Bar */}
                      <div className="h-[5px] bg-[#bbb] rounded-sm mb-3 overflow-hidden">
                        <div
                          className="h-full bg-[#222] rounded-sm transition-all"
                          style={{ width: `${lesson.progress}%` }}
                        />
                      </div>

                      {/* Card Footer */}
                      <div className="flex justify-between items-end">
                        <div className="font-mono text-[10px] text-[#555] leading-6">
                          PROGRESS — {lesson.progress}%
                          <br />
                          {lesson.exercises.completed}/{lesson.exercises.total}{' '}
                          EXERCISES
                        </div>
                        <button className="font-mono text-xs font-bold uppercase tracking-wider text-center px-4 py-[9px] bg-[#d8d4cc] border-[1.5px] border-[#888] text-[#111] cursor-pointer leading-snug transition-all hover:bg-[#111] hover:text-[#eee] flex-shrink-0 whitespace-nowrap">
                          PULL PAPER &<br />
                          START TRAINING
                        </button>
                      </div>

                      {/* Completed Stamp */}
                      {lesson.status === 'done' && (
                        <div className="absolute top-1/2 left-[44%] -translate-x-1/2 -translate-y-1/2 -rotate-12 pointer-events-none">
                          <div className="font-mono text-4xl text-[#4ddd94] border-4 border-[#4ddd94] px-3 opacity-[0.72] bg-green-100 bg-opacity-5 whitespace-nowrap tracking-wider">
                            COMPLETED
                          </div>
                        </div>
                      )}
                    </div>
                  </div>

                  {/* Bullets between cards */}
                  {idx < lessons.length - 1 && (
                    <div className="flex flex-col items-start gap-1.5 my-1.5 ml-0">
                      <div className="w-3 h-3 rounded-full bg-[#888] border-2 border-[#aaa] flex-shrink-0" />
                      <div className="w-3 h-3 rounded-full bg-[#888] border-2 border-[#aaa] flex-shrink-0" />
                    </div>
                  )}
                </div>
              ))}

              {/* Trailing bullets */}
              <div className="flex flex-col items-start gap-1.5 my-1.5 ml-0">
                <div className="w-3 h-3 rounded-full bg-[#888] border-2 border-[#aaa] flex-shrink-0" />
                <div className="w-3 h-3 rounded-full bg-[#888] border-2 border-[#aaa] flex-shrink-0" />
              </div>
            </div>

            {/* Scroll Dots Column */}
            <div className="w-8 flex flex-col items-center justify-between py-[30px] flex-shrink-0 pr-1">
              {[...Array(7)].map((_, i) => (
                <div
                  key={i}
                  className="w-3.5 h-3.5 rounded-full bg-[#999] border-2 border-[#bbb] cursor-pointer hover:bg-[#777] transition-all"
                  style={{
                    opacity: Math.abs(i / 7 * 100 - scrollPosition) < 20 ? 1 : 0.5,
                  }}
                />
              ))}
            </div>
          </div>
        </div>

        {/* SIDEBAR */}
        <aside className="w-[300px] flex-shrink-0 bg-[#2b2b2b] border-l border-[#333] flex flex-col gap-3 p-3.5 overflow-y-auto">
          {[
            { icon: '📋', label: 'LEXICAL\nCLIPBOARD' },
            { icon: '📄', label: 'QUICK\nREVIEW' },
            { icon: '📈', label: 'METRIC\nLOG' },
          ].map((item, idx) => (
            <div
              key={idx}
              className="flex-1 bg-[#d0ccc4] rounded-sm flex flex-row items-start justify-center gap-3 px-5.5 py-4.5 cursor-pointer transition-all hover:bg-[#dedad2] min-h-[90px]"
            >
              <div className="text-2xl text-[#222] flex-shrink-0 mt-0.5">
                {item.icon}
              </div>
              <div className="font-mono text-sm font-bold uppercase tracking-wider text-[#111] leading-relaxed text-left whitespace-pre-line">
                {item.label}
              </div>
            </div>
          ))}
        </aside>
      </div>
    </div>
  );
}
