'use client'

import {
  useState, useEffect,
  useRef, useCallback,
} from 'react'
import { useRouter, useParams } from 'next/navigation'
import { apiFetch } from '@/lib/api'
import {
  buildSessionQueue, saveSession, loadSession, clearSession,
  nodeDifficulty, DIFFICULTY_LABELS, DIFFICULTY_COLORS,
} from '@/lib/nodeSession'

// ── Types ─────────────────────────────────────────
interface SentencePair {
  pair_id:    string
  sentence_a: string
  sentence_b: string
}

interface SnapNodeData {
  node_id:              string
  title:                string
  focus:                string
  difficulty:           number
  micro_lesson_text:    string
  reading_passage:      string
  deep_dive_required:   boolean
  sentence_pairs:       SentencePair[]
  transition_tile_dock: string[]
}

type Phase     = 'loading' | 'micro_lesson' | 'deep_dive' | 'task' | 'mastery' | 'error'
type TileState = 'idle' | 'correct' | 'incorrect'

const SNAP_GAP_TUTORIAL_KEY =
  'critica_tutorial_seen_snap_gap_first_node'

const TUTORIAL_STEPS = [
  {
    label: 'Read the passage',
    code: 'TUT-SIG-001',
    text: 'In Snap-in-Gap, you will see a passage with blank gaps missing transition words. A tile bank on the right holds word options.\n\nYour mission: drag or click the correct tile into each gap to restore the paragraph\'s logical flow.',
    board: 'passage',
    notes: [
      'Drag a tile to fill the gap',
      'Gap turns teal when filled',
      'Click gap to clear it',
    ],
  },
  {
    label: 'Pick a tile',
    code: 'TUT-SIG-002',
    text: 'Look at the word tile bank on the right. Read the context before and after each gap. Ask yourself: is this a contrast? A result? An addition? Then click a tile to select it, it will highlight gold.',
    board: 'tiles',
    notes: [
      'Gold outline = current selected',
      'Faded tiles are already used',
      'Drag or click to place in gap',
    ],
  },
  {
    label: 'Fill the gap',
    code: 'TUT-SIG-003',
    text: 'After selecting a tile, click a gap in the passage to place it or drag the tile directly onto the gap. The gap will snap closed and turn teal. Click a filled gap to clear it and try again.',
    board: 'beforeAfter',
    notes: [
      'Teal snap = tile placed',
      'Click filled gap to clear',
      'One tile per gap only',
    ],
  },
  {
    label: 'Submit',
    code: 'TUT-SIG-004',
    text: 'When all gaps are filled, the Submit button activates. Hit it to check your answers. Correct gaps stay teal, wrong gaps turn red and clear giving you a chance to retry only the incorrect ones.',
    board: 'submit',
    notes: [
      'Bar fills as gaps are placed',
      'Submit unlocks at 4/4 filled',
      'Partial retry on wrong answers',
    ],
  },
] as const

// ── Shared styles ──────────────────────────────────
const F = "'Courier New', Courier, monospace"

const S = {
  page: {
    minHeight: '100vh',
    background: '#686664',
    display: 'flex' as const,
    alignItems: 'center' as const,
    justifyContent: 'center' as const,
    fontFamily: F,
  },
  card: {
    maxWidth: 640,
    width: '100%',
    background: '#2b2b2b',
    border: '1px solid #444',
    borderRadius: 4,
    padding: 48,
    fontFamily: F,
  },
  stamp: {
    display: 'inline-block' as const,
    border: '2px solid #888',
    padding: '3px 14px',
    fontSize: 10,
    fontWeight: 700,
    letterSpacing: '0.15em',
    color: '#aaa',
    marginBottom: 12,
    fontFamily: F,
  } as React.CSSProperties,
  h2: {
    fontSize: 20,
    fontWeight: 700,
    color: '#f0ece4',
    margin: '0 0 6px',
    fontFamily: F,
  } as React.CSSProperties,
  sub: {
    fontSize: 12,
    color: '#aaa',
    margin: '0 0 16px',
    fontFamily: F,
  } as React.CSSProperties,
  body: {
    fontSize: 13,
    lineHeight: 1.85,
    color: '#ccc',
    margin: '0 0 32px',
    fontFamily: F,
  } as React.CSSProperties,
  hr: {
    border: 'none',
    borderTop: '1px solid #444',
    margin: '16px 0',
  } as React.CSSProperties,
  btnPrimary: {
    padding: '10px 24px',
    background: '#f0ece4',
    border: '2px solid #888',
    borderRadius: 2,
    color: '#111',
    fontFamily: F,
    fontSize: 11,
    fontWeight: 700,
    cursor: 'pointer',
    letterSpacing: '0.08em',
  } as React.CSSProperties,
  btnSm: {
    padding: '7px 16px',
    background: 'transparent',
    border: '1px solid #555',
    borderRadius: 2,
    color: '#aaa',
    fontFamily: F,
    fontSize: 10,
    fontWeight: 700,
    cursor: 'pointer',
  } as React.CSSProperties,
  tutorialBtn: {
    padding: '7px 14px',
    background: '#2b2b2b',
    border: '1px solid #555',
    borderRadius: 2,
    color: '#f0ece4',
    fontFamily: F,
    fontSize: 10,
    fontWeight: 700,
    letterSpacing: '0.08em',
    cursor: 'pointer',
  } as React.CSSProperties,
}

// ── Sub-screens ───────────────────────────────────
function LoadScreen() {
  return (
    <div style={{ minHeight: '100vh', background: '#6b6b6b', display: 'flex',
      alignItems: 'center', justifyContent: 'center',
      fontFamily: F, color: '#ddd', fontSize: 13, letterSpacing: '0.1em' }}>
      LOADING NODE...
    </div>
  )
}

function ErrorScreen({ msg, onBack }: { msg: string; onBack: () => void }) {
  return (
    <div style={{ minHeight: '100vh', background: '#1e1e1e', display: 'flex',
      flexDirection: 'column', alignItems: 'center', justifyContent: 'center',
      fontFamily: F, gap: 16 }}>
      <p style={{ color: '#ff6b6b', fontSize: 13 }}>{msg}</p>
      <button onClick={onBack} style={S.btnSm}>← DASHBOARD</button>
    </div>
  )
}

function LessonScreen({ node, onContinue }: { node: SnapNodeData; onContinue: () => void }) {
  return (
    <div style={{ minHeight: '100vh', background: '#6b6b6b', display: 'flex',
      alignItems: 'center', justifyContent: 'center', padding: 40, fontFamily: F }}>
      <div style={{ maxWidth: 640, width: '100%', background: '#2b2b2b',
        border: '1px solid #444', borderRadius: 4, padding: 48 }}>
        <div style={S.stamp}>MICRO-LESSON</div>
        <h2 style={{ fontSize: 22, fontWeight: 700, color: '#f0ece4', margin: '0 0 6px' }}>
          {node.title}
        </h2>
        <p style={{ fontSize: 13, color: '#aaa', margin: '0 0 16px' }}>{node.focus}</p>
        <hr style={{ border: 'none', borderTop: '1px solid #444', margin: '16px 0' }} />
        <p style={{ fontSize: 14, lineHeight: 1.85, color: '#ccc', margin: '0 0 32px' }}>
          {node.micro_lesson_text}
        </p>
        <button onClick={onContinue} style={S.btnPrimary}>Continue →</button>
      </div>
    </div>
  )
}

function DeepDiveScreen({ node, onContinue }: { node: SnapNodeData; onContinue: () => void }) {
  return (
    <div style={{ minHeight: '100vh', background: '#6b6b6b', display: 'flex',
      alignItems: 'center', justifyContent: 'center', padding: 40, fontFamily: F }}>
      <div style={{ maxWidth: 700, width: '100%', background: '#2b2b2b',
        border: '1px solid #444', borderRadius: 4, padding: 48 }}>
        <div style={S.stamp}>DEEP DIVE READING</div>
        <p style={{ fontSize: 13, color: '#888', margin: '0 0 20px', lineHeight: 1.7 }}>
          Read the full passage carefully. Do not skip — cognitive endurance is part of the exercise.
        </p>
        <p style={{ fontSize: 14, lineHeight: 1.95, color: '#ddd', background: '#222',
          border: '1px solid #444', borderRadius: 4, padding: 28, margin: '0 0 32px' }}>
          {node.reading_passage}
        </p>
        <button onClick={onContinue} style={S.btnPrimary}>I have finished reading →</button>
      </div>
    </div>
  )
}

function MasteryScreen({ node, data, onDashboard, onNext }:
  { node: SnapNodeData; data: any; onDashboard: () => void; onNext: () => void }) {
  return (
    <div style={{ minHeight: '100vh', background: '#1e1e1e', display: 'flex',
      alignItems: 'center', justifyContent: 'center', fontFamily: F }}>
      <div style={{ maxWidth: 480, width: '100%', background: '#0e1e0e',
        border: '2px solid #4ddd94', borderRadius: 4, padding: 52, textAlign: 'center' }}>
        <div style={{ ...S.stamp, color: '#4ddd94', borderColor: '#4ddd94',
          fontSize: 16, padding: '8px 24px' }}>
          ✓ NODE MASTERED
        </div>
        <h2 style={{ fontSize: 20, color: '#4ddd94', margin: '8px 0 16px', fontFamily: F }}>
          {node.title}
        </h2>
        <p style={{ fontSize: 13, color: '#aaa', margin: '0 0 28px' }}>
          Streak: {data?.streak ?? 0} days
        </p>
        <div style={{ display: 'flex', gap: 12, justifyContent: 'center', flexWrap: 'wrap' }}>
          {data?.next_node && (
            <button onClick={onNext} style={S.btnPrimary}>NEXT NODE →</button>
          )}
          <button onClick={onDashboard} style={S.btnSm}>← DASHBOARD</button>
        </div>
      </div>
    </div>
  )
}

// ── Tutorial Popup ────────────────────────────────
function SnapGapTutorialPopup({
  open,
  step,
  onBack,
  onNext,
  onClose,
  onStart,
}: {
  open: boolean
  step: number
  onBack: () => void
  onNext: () => void
  onClose: () => void
  onStart: () => void
}) {
  if (!open) return null

  const current = TUTORIAL_STEPS[step]
  const isFirst = step === 0
  const isLast = step === TUTORIAL_STEPS.length - 1

  const stepBox = (label: string, index: number) => {
    const complete = index < step
    const active = index === step
    return (
      <div key={label} style={{
        width: 156, height: 76,
        border: '1px solid #777',
        background: complete ? '#b9dfbf' : active ? '#f8f7f3' : '#c9c7c2',
        color: '#111',
        boxShadow: active ? '0 3px 0 rgba(0,0,0,0.45)' : 'none',
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        position: 'relative', textAlign: 'center',
        fontFamily: F, fontSize: 12, fontWeight: 700,
      }}>
        <div style={{ position: 'absolute', top: 7, left: '50%', transform: 'translateX(-50%)' }}>
          <div style={{
            width: 24, height: 24, borderRadius: '50%',
            background: complete ? '#36b24a' : active ? '#ece7dc' : '#dbd8d2',
            color: complete ? '#fff' : '#111', display: 'flex', alignItems: 'center', justifyContent: 'center',
            fontSize: 11, fontWeight: 700,
          }}>{complete ? '✓' : index + 1}</div>
        </div>
        <span style={{ marginTop: 20, lineHeight: 1.15 }}>{label}</span>
      </div>
    )
  }

  const renderBoard = () => {
    if (current.board === 'passage') {
      return (
        <div style={{ padding: '18px 16px 12px' }}>
          <div style={{ fontFamily: F, fontSize: 11, fontWeight: 700, color: '#333', marginBottom: 10 }}>EXAMPLE GAP</div>
          <div style={{ fontFamily: F, fontSize: 12, color: '#222', lineHeight: 1.4 }}>
            Reading is essential.
            <span style={{ display: 'inline-block', width: 96, height: 20, border: '1px dashed #9a9a9a', background: '#e9e9e9', verticalAlign: 'middle', margin: '0 6px' }} />
            it builds critical thinking.
          </div>
        </div>
      )
    }

    if (current.board === 'tiles') {
      return (
        <div style={{ padding: '16px 14px 12px' }}>
          <div style={{ fontFamily: F, fontSize: 11, fontWeight: 700, color: '#333', marginBottom: 12 }}>WORD TILE BANK</div>
          <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
            {['FURTHERMORE', 'HOWEVER', 'ALTHOUGH', 'HENCE'].map((tile, i) => (
              <div key={tile} style={{
                padding: '8px 12px', minWidth: 92, textAlign: 'center',
                border: `2px solid ${i === 0 ? '#f0c400' : '#888'}`,
                background: i === 3 ? '#efefef' : '#fff',
                color: i === 3 ? '#bdbdbd' : '#111',
                fontFamily: F, fontWeight: 700, fontSize: 11,
              }}>{tile}</div>
            ))}
          </div>
        </div>
      )
    }

    if (current.board === 'beforeAfter') {
      return (
        <div style={{ padding: '16px 14px 12px' }}>
          <div style={{ fontFamily: F, fontSize: 11, fontWeight: 700, color: '#333', marginBottom: 12 }}>BEFORE & AFTER</div>
          <div style={{ display: 'grid', gridTemplateColumns: '70px 1fr', rowGap: 12, alignItems: 'center' }}>
            <div style={{ fontFamily: F, fontSize: 12, fontWeight: 700, color: '#111' }}>BEFORE :</div>
            <div style={{ width: 88, height: 20, border: '1px dashed #9a9a9a', background: '#e9e9e9' }} />
            <div style={{ fontFamily: F, fontSize: 12, fontWeight: 700, color: '#111' }}>AFTER :</div>
            <div style={{ display: 'inline-flex', alignItems: 'center', padding: '4px 8px', border: '1px solid #59baf7', background: '#d8efff', color: '#0f5f9a', fontFamily: F, fontSize: 11, fontWeight: 700, width: 'fit-content' }}>FURTHERMORE</div>
          </div>
        </div>
      )
    }

    return (
      <div style={{ padding: '16px 14px 12px' }}>
        <div style={{ fontFamily: F, fontSize: 11, fontWeight: 700, color: '#333', marginBottom: 12 }}>PROGRESS BAR</div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 12 }}>
          <div style={{ flex: 1, height: 10, background: '#efefef', border: '1px solid #555', overflow: 'hidden' }}>
            <div style={{ width: '75%', height: '100%', background: '#111' }} />
          </div>
          <div style={{ fontFamily: F, fontSize: 11, fontWeight: 700, color: '#111', minWidth: 28, textAlign: 'right' }}>3 / 4</div>
        </div>
        <div style={{ display: 'inline-flex', alignItems: 'center', justifyContent: 'center', width: '100%', padding: '8px 12px', background: '#ddd', border: '1px solid #888', fontFamily: F, fontSize: 12, fontWeight: 700 }}>SUBMIT →</div>
      </div>
    )
  }

  const primaryLabel = isLast ? 'START TRAINING →' : 'NEXT →'
  const secondaryLabel = isFirst ? 'EXIT TUTORIAL' : 'BACK'

  return (
    <div style={{
      position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.48)',
      zIndex: 150, display: 'flex', alignItems: 'center', justifyContent: 'center',
      padding: 20, fontFamily: F,
    }}>
      <div style={{ width: '100%', maxWidth: 840, background: '#d4d1cb', border: '1px solid #5f5d58', boxShadow: '0 18px 44px rgba(0,0,0,0.4)', padding: '10px 14px 14px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 8 }}>
          <div style={{ fontSize: 17, fontWeight: 700, letterSpacing: '0.28em', color: '#111' }}>CRITICA - FIELD BRIEFING DOCUMENT</div>
          <div style={{ fontSize: 17, fontWeight: 700, letterSpacing: '0.18em', color: '#111' }}>{current.code}</div>
        </div>

        <div style={{ background: '#d7d7d5', border: '1px solid #65635d', borderRadius: '16px 16px 10px 10px', padding: '30px 24px 22px', position: 'relative' }}>
          <div style={{ position: 'absolute', top: -1, left: -1, width: 54, height: 24, borderRadius: '16px 0 14px 0', background: '#d7d7d5', borderLeft: '1px solid #65635d', borderTop: '1px solid #65635d' }} />

          <div style={{ display: 'flex', alignItems: 'center', gap: 42, marginBottom: 30 }}>
            <div style={{ width: 120, textAlign: 'center' }}>
              <div style={{ width: 56, height: 56, border: '2px solid #6c6a64', background: '#fff', margin: '0 auto 8px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <div style={{ width: 34, height: 34, background: '#333', borderRadius: 4, position: 'relative' }}>
                  <div style={{ position: 'absolute', top: 6, left: '50%', transform: 'translateX(-50%)', width: 14, height: 14, borderRadius: '50%', background: '#d8d8d8' }} />
                  <div style={{ position: 'absolute', bottom: 6, left: 5, right: 5, height: 10, borderRadius: '10px 10px 4px 4px', background: '#d8d8d8' }} />
                </div>
              </div>
              <div style={{ fontSize: 15, fontWeight: 700, letterSpacing: '0.08em', color: '#111' }}>AGENT CRIT</div>
              <div style={{ fontSize: 10, color: '#222', letterSpacing: '0.06em' }}>FIELD INSTRUCTOR</div>
            </div>

            <div style={{ position: 'relative', flex: 1, background: '#fff', border: '1px solid #7b776f', boxShadow: '0 3px 12px rgba(0,0,0,0.18)', padding: '12px 16px', minHeight: 96 }}>
              <div style={{ position: 'absolute', left: -9, top: 38, width: 18, height: 18, background: '#fff', borderLeft: '1px solid #7b776f', borderBottom: '1px solid #7b776f', transform: 'rotate(45deg)' }} />
              <div style={{ fontSize: 13, lineHeight: 1.35, color: '#222', whiteSpace: 'pre-line' }}>{current.text}</div>
            </div>
          </div>

          <div style={{ border: '1px solid #7b776f', background: '#e7e4de', padding: 10, marginBottom: 28 }}>
            <div style={{ display: 'flex', gap: 8, justifyContent: 'space-between' }}>
              {TUTORIAL_STEPS.map((stepItem, index) => stepBox(stepItem.label, index))}
            </div>
          </div>

          <div style={{ display: 'flex', gap: 12, alignItems: 'stretch', background: '#e7e4de', border: '1px solid #7b776f', padding: 14 }}>
            <div style={{ flex: 1, minHeight: 202, background: '#fff', border: '1px solid #9a968f', padding: 18, position: 'relative' }}>
              {renderBoard()}
            </div>

            <div style={{ width: 112, background: '#fff', border: '1px solid #9a968f', padding: '10px 10px 12px' }}>
              <div style={{ fontSize: 10, fontWeight: 700, letterSpacing: '0.08em', color: '#222', marginBottom: 10 }}>QUICK NOTES</div>
              {current.notes.map((note, index) => (
                <div key={note} style={{ fontSize: 9, lineHeight: 1.45, color: '#333' }}>
                  {note}
                  {index < current.notes.length - 1 && <div style={{ height: 10 }} />}
                </div>
              ))}
            </div>
          </div>

          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: 24 }}>
            <button onClick={isFirst ? onClose : onBack} style={{ ...S.btnSm, minWidth: 160, background: '#d8d4cc', color: '#111', border: '1px solid #7b776f', fontSize: 11, letterSpacing: '0.06em' }}>
              {secondaryLabel}
            </button>
            <button onClick={isLast ? onStart : onNext} style={{ ...S.btnSm, minWidth: 170, background: '#d8d4cc', color: '#111', border: '1px solid #7b776f', fontSize: 11, letterSpacing: '0.06em' }}>
              {primaryLabel}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

// ── Main component ─────────────────────────────────
export default function SnapInGapPage() {
  const router = useRouter()
  const params = useParams()
  const nodeId = params.nodeId as string

  const [phase,       setPhase]       = useState<Phase>('loading')
  const [snapNode,    setSnapNode]     = useState<SnapNodeData | null>(null)
  const [errorMsg,    setErrorMsg]    = useState('')

  const [pairIdx,     setPairIdx]     = useState(0)
  const [board,       setBoard]       = useState<Record<string, string>>({})
  const [locked,      setLocked]      = useState<string[]>([])
  const [tileState,   setTileState]   = useState<TileState>('idle')
  const [wrongs,      setWrongs]      = useState(0)
  const [masteryData, setMasteryData] = useState<any>(null)
  const [submitting,  setSubmitting]  = useState(false)

  // feedback state
  const [fbText,        setFbText]        = useState('')
  const [hintText,      setHintText]      = useState('')
  const [hintTier,      setHintTier]      = useState(0)
  const [drawer,        setDrawer]        = useState(false)
  const [tutorialOpen,  setTutorialOpen]  = useState(false)
  const [tutorialStep,  setTutorialStep]  = useState(0)

  // hint overlay state
  const [hintOverlay,     setHintOverlay]     = useState(false)
  const [hintOverlayText, setHintOverlayText] = useState('')
  const [hintOverlayTier, setHintOverlayTier] = useState(0)

  const timerRef    = useRef<ReturnType<typeof setInterval> | null>(null)
  const inactiveRef = useRef(0)

  // session state
  const [sessionQueue,   setSessionQueue]   = useState<string[]>([])
  const [questionIndex,  setQuestionIndex]  = useState(0)
  const [sessionStartId, setSessionStartId] = useState<string | null>(null)
  const [savedNextNode,  setSavedNextNode]  = useState<string | null>(null)
  const [savedStreak,    setSavedStreak]    = useState<number | null>(null)

  // ── Load a question inline ──────────────────
  const loadQuestion = useCallback(async (targetNodeId: string) => {
    setPhase('loading')
    try {
      const d = await apiFetch(`/nodes/snap-gap/${targetNodeId}/`)
      setSnapNode(d)
      setPairIdx(0)
      setBoard({})
      setLocked([])
      setTileState('idle')
      setWrongs(0)
      setFbText('')
      setHintText('')
      setHintTier(0)
      setDrawer(false)
      setHintOverlay(false)
      setHintOverlayText('')
      setHintOverlayTier(0)
      setPhase('task')
    } catch (e: any) {
      setErrorMsg(e?.error ?? 'Failed to load next question.')
      setPhase('error')
    }
  }, [])

  // ── load ─────────────────────────────────────────
  useEffect(() => {
    const start = nodeId
    setSessionStartId(start)
    const saved = loadSession('snap_gap', start)

    if (saved && saved.sessionQueue.length === 5) {
      setSessionQueue(saved.sessionQueue)
      setQuestionIndex(saved.questionIndex)
      if (saved.next_node) setSavedNextNode(saved.next_node)
      if (saved.streak !== undefined) setSavedStreak(saved.streak)

      const activeId = saved.sessionQueue[saved.questionIndex] ?? start
      apiFetch(`/nodes/snap-gap/${activeId}/`)
        .then((d: SnapNodeData) => {
          setSnapNode(d)
          setPhase('task')
        })
        .catch((e: any) => {
          if (e?.status === 401)              { router.push('/auth');      return }
          if (e?.error === 'Node is locked.') { router.push('/dashboard'); return }
          setErrorMsg(e?.error ?? 'Failed to load node.')
          setPhase('error')
        })
    } else {
      apiFetch(`/nodes/snap-gap/${start}/`)
        .then((d: SnapNodeData) => {
          setSnapNode(d)
          setPhase('micro_lesson')

          apiFetch('/progression/dashboard/')
            .then((prog: any) => {
              const unlocked: string[] = prog.unlocked_nodes ?? []
              const queue = buildSessionQueue('snap_gap', start, unlocked)
              setSessionQueue(queue)
              setQuestionIndex(0)
              saveSession('snap_gap', start, {
                sessionQueue: queue,
                questionIndex: 0,
              })
            })
            .catch(() => {
              setSessionQueue([start])
              setQuestionIndex(0)
            })
        })
        .catch((e: any) => {
          if (e?.status === 401)              { router.push('/auth');      return }
          if (e?.error === 'Node is locked.') { router.push('/dashboard'); return }
          setErrorMsg(e?.error ?? 'Failed to load node.')
          setPhase('error')
        })
    }
  }, [nodeId, router])

  useEffect(() => {
    if (phase !== 'task' || nodeId !== 'snp_node_01') return

    const seen = localStorage.getItem(SNAP_GAP_TUTORIAL_KEY)
    if (seen === '1') return

    localStorage.setItem(SNAP_GAP_TUTORIAL_KEY, '1')
    setTutorialStep(0)
    setTutorialOpen(true)
  }, [phase, nodeId])

  // ── feedback ──────────────────────────────────────
  const callFeedback = useCallback(async (pair_id: string, tile: string, inactivity: boolean) => {
    const activeNodeId = snapNode?.node_id ?? nodeId
    try {
      const res = await apiFetch(`/nodes/snap-gap/${activeNodeId}/feedback/`, {
        method: 'POST',
        body: JSON.stringify({
          pair_id,
          selected_tile: tile,
          inactivity_seconds: inactivity ? 60 : inactiveRef.current,
        }),
      })
      setFbText(res.explanation ?? '')
      setHintText(res.hint ?? '')
      setHintTier(res.hint_tier ?? 0)
      setDrawer(true)
    } catch {
      setFbText('That transition does not fit here. Re-read both sentences.')
      setHintText('')
      setDrawer(true)
    }
  }, [nodeId, snapNode])

  // ── timer ─────────────────────────────────────────
  const resetTimer = useCallback(() => {
    inactiveRef.current = 0
    if (timerRef.current) clearInterval(timerRef.current)
    timerRef.current = setInterval(() => {
      inactiveRef.current += 1
      if (inactiveRef.current >= 60) {
        clearInterval(timerRef.current!)
        callFeedback('', '', true)
      }
    }, 1000)
  }, [callFeedback])

  useEffect(() => {
    if (phase === 'task') resetTimer()
    return () => { if (timerRef.current) clearInterval(timerRef.current) }
  }, [phase, resetTimer])

  // ── fetch hint overlay ────────────────────────────
  const fetchHint = useCallback(async () => {
    const activeNodeId = snapNode?.node_id ?? nodeId
    try {
      const res = await apiFetch(`/nodes/snap-gap/${activeNodeId}/feedback/`, {
        method: 'POST',
        body: JSON.stringify({
          pair_id: '',
          selected_tile: '',
          inactivity_seconds: 61,
        }),
      })
      const text = res.hint || res.explanation || 'Re-read the two sentences and think about how they relate logically.'
      setHintOverlayText(text)
      setHintOverlayTier(res.hint_tier ?? 0)
      setHintOverlay(true)
    } catch {
      setHintOverlayText('Re-read the two sentences and think about how they relate logically.')
      setHintOverlay(true)
    }
  }, [nodeId, snapNode])

  // ── tile click ────────────────────────────────────
  const handleTile = async (tile: string) => {
    if (!snapNode || tileState !== 'idle' || drawer) return
    resetTimer()
    const pair = snapNode.sentence_pairs[pairIdx]
    if (!pair) return
    try {
      const res = await apiFetch(`/nodes/snap-gap/${snapNode.node_id}/evaluate-gap/`, {
        method: 'POST',
        body: JSON.stringify({ pair_id: pair.pair_id, selected_tile: tile }),
      })
      if (res.result === 'correct') {
        setTileState('correct')
        setBoard(prev => ({ ...prev, [pair.pair_id]: tile }))
        setLocked(prev => [...prev, pair.pair_id])
        setTimeout(() => {
          setTileState('idle')
          if (pairIdx < snapNode.sentence_pairs.length - 1) setPairIdx(i => i + 1)
        }, 900)
      } else {
        setTileState('incorrect')
        const nextWrongs = wrongs + 1
        setWrongs(nextWrongs)
        setTimeout(() => setTileState('idle'), 600)
        await callFeedback(pair.pair_id, tile, false)
        if (nextWrongs >= 3) fetchHint()
      }
    } catch { setErrorMsg('Evaluation failed.') }
  }

  // ── submit ────────────────────────────────────────
  const handleSubmit = async () => {
    if (!snapNode || submitting) return
    setSubmitting(true)
    try {
      const res = await apiFetch(`/nodes/snap-gap/${snapNode.node_id}/mastery/`, {
        method: 'POST',
        body: JSON.stringify({
          board_state: board,
          save_progression: false,
        }),
      })
      if (res.status === 'mastered') {
        const nextIdx = questionIndex + 1

        if (nextIdx < sessionQueue.length) {
          const newNextNode = savedNextNode
          const newStreak = savedStreak

          if (sessionStartId) {
            saveSession('snap_gap', sessionStartId, {
              sessionQueue,
              questionIndex: nextIdx,
              next_node: newNextNode || undefined,
              streak: newStreak !== null ? newStreak : undefined,
            })
          }
          setQuestionIndex(nextIdx)
          loadQuestion(sessionQueue[nextIdx])
        } else {
          let finalRes = res
          if (sessionStartId) {
            finalRes = await apiFetch(
              `/nodes/snap-gap/${sessionStartId}/mastery/`,
              {
                method: 'POST',
                body: JSON.stringify({
                  commit_only: true,
                }),
              },
            )
          }

          const newNextNode = savedNextNode || finalRes.next_node
          const newStreak = savedStreak !== null ? savedStreak : (finalRes.streak ?? null)

          if (sessionStartId) clearSession('snap_gap', sessionStartId)
          setMasteryData({
            next_node: newNextNode,
            streak: newStreak,
          })
          setPhase('mastery')
        }
      }
    } catch (e: any) {
      setFbText(e?.status === 'incomplete'
        ? 'Some pairs are incorrect. Check and retry.'
        : 'Submission failed. Please try again.')
      setHintText('')
      setDrawer(true)
    } finally { setSubmitting(false) }
  }

  // ── phase guards ──────────────────────────────────
  if (phase === 'loading')      return <LoadScreen />
  if (phase === 'error')        return <ErrorScreen msg={errorMsg} onBack={() => router.push('/dashboard')} />
  if (phase === 'micro_lesson') return <LessonScreen node={snapNode!} onContinue={() => setPhase(snapNode!.deep_dive_required ? 'deep_dive' : 'task')} />
  if (phase === 'deep_dive')    return <DeepDiveScreen node={snapNode!} onContinue={() => setPhase('task')} />
  if (phase === 'mastery')      return (
    <MasteryScreen
      node={snapNode!} data={masteryData}
      onDashboard={() => router.push('/dashboard')}
      onNext={() => masteryData?.next_node && router.push(`/nodes/snap-gap/${masteryData.next_node}`)}
    />
  )

  // ── TASK PHASE ────────────────────────────────────
  const currentPair = snapNode!.sentence_pairs[pairIdx]
  const allDone     = locked.length === snapNode!.sentence_pairs.length

  const openTutorial  = () => { setTutorialStep(0); setTutorialOpen(true) }
  const closeTutorial = () => setTutorialOpen(false)
  const nextTutorialStep = () => setTutorialStep(prev => Math.min(prev + 1, TUTORIAL_STEPS.length - 1))
  const prevTutorialStep = () => setTutorialStep(prev => Math.max(prev - 1, 0))

  return (
    <div style={{ minHeight: '100vh', background: '#686664',
      display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: F }}>
      <div style={{ display: 'flex', alignItems: 'stretch',
        boxShadow: '0 12px 48px rgba(0,0,0,0.55)', borderRadius: 6 }}>

        {/* ── SIDEBAR ── */}
        <div style={{
          width: 40, background: '#2b2b2b',
          display: 'flex', flexDirection: 'column',
          alignItems: 'center', justifyContent: 'space-between',
          padding: '14px 0', borderRadius: '6px 0 0 6px',
          borderRight: '1px solid #1a1a1a',
        }}>
          <button
            onClick={() => fetchHint()}
            style={{
              writingMode: 'vertical-rl', transform: 'rotate(180deg)',
              fontSize: 11, fontWeight: 700, letterSpacing: '0.14em',
              color: '#999', background: 'none', border: 'none',
              cursor: 'pointer', padding: '10px 4px', fontFamily: F,
            }}
            onMouseEnter={e => (e.currentTarget.style.color = '#eee')}
            onMouseLeave={e => (e.currentTarget.style.color = '#999')}
          >
            HINT
          </button>
          <button
            onClick={() => {
              if (sessionStartId && sessionQueue.length > 0) {
                saveSession('snap_gap', sessionStartId, {
                  sessionQueue,
                  questionIndex,
                  next_node: savedNextNode || undefined,
                  streak: savedStreak !== null ? savedStreak : undefined,
                })
              }
              router.push('/dashboard')
            }}
            style={{
              writingMode: 'vertical-rl', transform: 'rotate(180deg)',
              fontSize: 11, fontWeight: 700, letterSpacing: '0.14em',
              color: '#666', background: 'none', border: 'none',
              cursor: 'pointer', padding: '10px 4px', fontFamily: F,
            }}
            onMouseEnter={e => (e.currentTarget.style.color = '#aaa')}
            onMouseLeave={e => (e.currentTarget.style.color = '#666')}
          >
            END SESSION
          </button>
        </div>

        {/* ── BOARD ── */}
        <div style={{
          background: '#b8b3ab', borderRadius: '0 6px 6px 0',
          overflow: 'hidden', display: 'flex', flexDirection: 'column', width: 900,
        }}>

          {/* banner */}
          <div style={{ padding: '12px 20px 10px', textAlign: 'center', background: '#b8b3ab' }}>
            <div style={{
              display: 'inline-block', border: '1.5px solid #888',
              padding: '7px 24px', fontSize: 14, fontWeight: 700,
              letterSpacing: '0.1em', color: '#333',
              background: 'rgba(255,255,255,0.25)', fontFamily: F,
            }}>
              <span style={{ color: '#444' }}>OBJECTIVE: </span>
              <span style={{ color: '#b03030' }}>
                SELECT THE CORRECT TRANSITION TILE TO BRIDGE THE GAP
              </span>
            </div>
          </div>

          {/* difficulty badge + Q counter */}
          <div style={{ padding: '6px 24px 6px', display: 'flex', flexDirection: 'column', gap: 6 }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                <div style={{ width: 8, height: 8, borderRadius: '50%', background: DIFFICULTY_COLORS[snapNode!.difficulty ?? nodeDifficulty(nodeId)], flexShrink: 0 }} />
                <span style={{ fontSize: 9, fontWeight: 700, letterSpacing: '0.12em', color: DIFFICULTY_COLORS[snapNode!.difficulty ?? nodeDifficulty(nodeId)], fontFamily: F }}>
                  LVL {snapNode!.difficulty ?? nodeDifficulty(nodeId)} — {DIFFICULTY_LABELS[snapNode!.difficulty ?? nodeDifficulty(nodeId)]}
                </span>
              </div>
              {sessionQueue.length > 0 && (
                <span style={{ fontSize: 9, fontWeight: 700, letterSpacing: '0.1em', color: '#555', fontFamily: F }}>
                  Q {questionIndex + 1} / {sessionQueue.length}
                </span>
              )}
            </div>
            {sessionQueue.length > 0 && (
              <div style={{ height: 6, background: '#e0ddd8', borderRadius: 3, overflow: 'hidden', position: 'relative', border: '1px solid #aaa' }}>
                <div style={{
                  height: '100%',
                  width: `${(questionIndex / sessionQueue.length) * 100}%`,
                  background: '#2b2b2b',
                  transition: 'width 0.3s ease-in-out'
                }} />
              </div>
            )}
          </div>

          {/* progress dots */}
          <div style={{ padding: '4px 24px 4px', display: 'flex', gap: 8, justifyContent: 'center' }}>
            {snapNode!.sentence_pairs.map((p, i) => (
              <div key={p.pair_id} style={{
                width: 34, height: 8, borderRadius: 4,
                background: locked.includes(p.pair_id) ? '#4ddd94' : i === pairIdx ? '#55aaff' : '#888',
                transition: 'background 0.3s',
              }} />
            ))}
          </div>

          {/* sentence pair area */}
          <div style={{ padding: '28px 40px 20px', flex: 1 }}>
            {currentPair && (
              <div>
                {/* sentence A */}
                <div style={{
                  background: '#fff', border: '1.5px solid #ccc',
                  borderRadius: 5, padding: '16px 20px',
                  fontSize: 14, lineHeight: 1.75,
                  color: '#1a1a1a', fontFamily: F, marginBottom: 14,
                }}>
                  {currentPair.sentence_a}
                </div>

                {/* gap slot */}
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '10px 0', gap: 12 }}>
                  <div style={{ flex: 1, height: 1, background: '#888', opacity: 0.5 }} />
                  <div style={{
                    border: tileState === 'correct'   ? '2px solid #4ddd94' :
                            tileState === 'incorrect' ? '2px solid #cc3333' : '2px dashed #888',
                    borderRadius: 4, padding: '8px 24px',
                    fontSize: 13, fontWeight: 700, letterSpacing: '0.12em',
                    color: tileState === 'correct'   ? '#4ddd94' :
                           tileState === 'incorrect' ? '#cc3333' : '#888',
                    background: tileState === 'correct'   ? 'rgba(77,221,148,0.1)' :
                                tileState === 'incorrect' ? 'rgba(204,51,51,0.1)'  : 'rgba(255,255,255,0.3)',
                    fontFamily: F, minWidth: 180, textAlign: 'center', transition: 'all 0.25s',
                  }}>
                    {tileState === 'correct'   ? `✓ ${board[currentPair.pair_id] ?? ''}` :
                     tileState === 'incorrect' ? '✕ INCORRECT' : '[ SELECT A TILE ]'}
                  </div>
                  <div style={{ flex: 1, height: 1, background: '#888', opacity: 0.5 }} />
                </div>

                {/* sentence B */}
                <div style={{
                  background: '#fff', border: '1.5px solid #ccc',
                  borderRadius: 5, padding: '16px 20px',
                  fontSize: 14, lineHeight: 1.75,
                  color: '#1a1a1a', fontFamily: F, marginTop: 14,
                }}>
                  {currentPair.sentence_b}
                </div>
              </div>
            )}

            {allDone && (
              <div style={{
                textAlign: 'center', padding: '24px 0 8px',
                fontSize: 13, color: '#4ddd94',
                fontWeight: 700, letterSpacing: '0.1em', fontFamily: F,
              }}>
                ALL GAPS BRIDGED — SUBMIT WHEN READY
              </div>
            )}
          </div>

          {/* tile dock */}
          <div style={{ background: '#a8a39b', borderTop: '1px solid #888', padding: '16px 28px' }}>
            <div style={{
              fontSize: 11, fontWeight: 700, letterSpacing: '0.12em',
              color: '#555', marginBottom: 12, fontFamily: F,
            }}>
              TRANSITION TILE DOCK
            </div>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: 10 }}>
              {snapNode!.transition_tile_dock.map(tile => (
                <button
                  key={tile}
                  disabled={tileState !== 'idle' || allDone}
                  onClick={() => handleTile(tile)}
                  style={{
                    padding: '10px 20px',
                    background: '#f0ece4', border: '1.5px solid #888',
                    borderRadius: 3, fontSize: 13, fontWeight: 700,
                    fontFamily: F,
                    cursor: tileState !== 'idle' || allDone ? 'not-allowed' : 'pointer',
                    opacity: tileState !== 'idle' || allDone ? 0.5 : 1,
                    color: '#1a1a1a', transition: 'all 0.12s', letterSpacing: '0.04em',
                  }}
                  onMouseEnter={e => { if (tileState === 'idle' && !allDone) { e.currentTarget.style.background = '#1a1a1a'; e.currentTarget.style.color = '#f0ece4' } }}
                  onMouseLeave={e => { e.currentTarget.style.background = '#f0ece4'; e.currentTarget.style.color = '#1a1a1a' }}
                >
                  {tile}
                </button>
              ))}
            </div>
          </div>

          {/* submit bar */}
          <div style={{
            display: 'flex', justifyContent: 'space-between', alignItems: 'center',
            padding: '12px 24px 16px', background: '#b8b3ab',
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 12, flexWrap: 'wrap' }}>
              <button onClick={openTutorial} style={S.tutorialBtn}>
                Show tutorial
              </button>
              <span style={{
                fontSize: 10, color: '#666',
                fontWeight: 700, letterSpacing: '0.08em',
                fontFamily: F,
              }}>
                {locked.length} / {snapNode!.sentence_pairs.length} PAIRS BRIDGED
                {wrongs > 0 && (
                  <span style={{ marginLeft: 14, color: '#b03030' }}>
                    ATTEMPTS: {wrongs}
                  </span>
                )}
              </span>
            </div>
            <button
              disabled={!allDone || submitting}
              onClick={handleSubmit}
              style={{
                display: 'flex', alignItems: 'center', gap: 12,
                background: submitting ? '#555' : allDone ? '#2b2b2b' : '#888',
                color: '#f0ece4', border: 'none', borderRadius: 2,
                padding: '12px 30px', fontSize: 13, fontWeight: 700,
                letterSpacing: '0.14em',
                cursor: allDone && !submitting ? 'pointer' : 'not-allowed',
                fontFamily: F, transition: 'background 0.2s',
              }}
            >
              {submitting ? 'CHECKING...' : <>SUBMIT <span style={{ fontSize: 18, lineHeight: 1 }}>→</span></>}
            </button>
          </div>
        </div>
      </div>

      <SnapGapTutorialPopup
        open={tutorialOpen}
        step={tutorialStep}
        onClose={closeTutorial}
        onBack={prevTutorialStep}
        onNext={nextTutorialStep}
        onStart={() => setTutorialOpen(false)}
      />

      {/* hint overlay */}
      {hintOverlay && (
        <div style={{
          position: 'fixed', inset: 0,
          background: 'rgba(0,0,0,0.45)',
          zIndex: 100,
          display: 'flex',
          alignItems: 'flex-start',
          justifyContent: 'flex-start',
          padding: 24,
          pointerEvents: 'none',
        }}>
          <div style={{
            background: '#fff',
            border: '2px solid #ddd',
            borderRadius: 5,
            padding: '16px 18px 14px',
            maxWidth: 260,
            boxShadow: '0 6px 24px rgba(0,0,0,0.35)',
            pointerEvents: 'all',
          }}>
            <div style={{
              fontSize: 9, fontWeight: 700, letterSpacing: '0.14em',
              color: '#888', marginBottom: 8, fontFamily: F,
            }}>
              SCAFFOLD HINT{hintOverlayTier > 0 ? ` — TIER ${hintOverlayTier}` : ''}
            </div>
            <p style={{
              fontSize: 12, color: '#222', lineHeight: 1.65,
              margin: '0 0 14px', fontFamily: F,
            }}>
              {hintOverlayText}
            </p>
            <button
              onClick={() => setHintOverlay(false)}
              style={{
                fontSize: 10, fontWeight: 700, color: '#444',
                background: '#eee', border: '1px solid #ccc',
                padding: '5px 14px', cursor: 'pointer',
                fontFamily: F, letterSpacing: '0.06em', borderRadius: 2,
              }}
            >
              Close
            </button>
          </div>
        </div>
      )}

      {/* feedback drawer */}
      {drawer && (
        <div style={{
          position: 'fixed', bottom: 0, left: 0, right: 0,
          background: '#180a0a', border: '2px solid #cc3333', borderBottom: 'none',
          padding: '20px 36px 28px', zIndex: 200, maxHeight: 300,
          overflowY: 'auto', fontFamily: F,
        }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
            <div style={{ ...S.stamp, color: '#ff6b6b', borderColor: '#ff6b6b', marginBottom: 0 }}>
              FEEDBACK
            </div>
            <button
              onClick={() => { setDrawer(false); resetTimer() }}
              style={{ background: 'none', border: 'none', color: '#ff6b6b', fontSize: 20, cursor: 'pointer', fontFamily: F }}
            >
              ✕
            </button>
          </div>
          {fbText && (
            <p style={{ fontSize: 14, color: '#ddd', lineHeight: 1.7, marginBottom: 12, fontFamily: F }}>
              {fbText}
            </p>
          )}
          {hintText && (
            <div style={{ background: '#2b1010', border: '1px solid #663333', borderRadius: 3, padding: 14, marginBottom: 16 }}>
              <div style={{ fontSize: 11, fontWeight: 700, letterSpacing: '0.12em', color: '#aa5533', marginBottom: 6, fontFamily: F }}>
                SCAFFOLD HINT — TIER {hintTier}
              </div>
              <p style={{ fontSize: 13, color: '#ddd', lineHeight: 1.7, margin: 0, fontFamily: F }}>
                {hintText}
              </p>
            </div>
          )}
          <button style={S.btnSm} onClick={() => { setDrawer(false); resetTimer() }}>
            Close and reattempt
          </button>
        </div>
      )}
    </div>
  )
}