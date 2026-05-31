// src/lib/nodeSession.ts
// Shared utilities for multi-question sessions with difficulty tiers.

// ── Difficulty ─────────────────────────────────────────────────────────────

/** Node index prefixes map to difficulty tiers 1–5 */
function nodeNumFromId(nodeId: string): number {
  const parts = nodeId.split('_')
  const n = parseInt(parts[parts.length - 1], 10)
  return isNaN(n) ? 1 : n
}

export function nodeDifficulty(nodeId: string): number {
  const n = nodeNumFromId(nodeId)
  if (n % 3 === 1) return 1
  if (n % 3 === 2) return 2
  return 3
}

export const DIFFICULTY_LABELS: Record<number, string> = {
  1: 'Basics',
  2: 'Intermediate',
  3: 'Advanced',
}

export const DIFFICULTY_COLORS: Record<number, string> = {
  1: '#4ddd94',   // green
  2: '#5bc0f8',   // blue
  3: '#f5a623',   // amber
}

// ── Session queue ──────────────────────────────────────────────────────────

/** All node IDs per module, in order */
const MODULE_NODES: Record<string, string[]> = {
  fact_scanner: [
    'fac_node_01','fac_node_02','fac_node_03','fac_node_04','fac_node_05',
    'fac_node_06','fac_node_07','fac_node_08','fac_node_09','fac_node_10',
    'fac_node_11','fac_node_12','fac_node_13','fac_node_14','fac_node_15',
    'fac_node_16',
  ],
  logic_thread: [
    'log_node_01','log_node_02','log_node_03','log_node_04','log_node_05',
    'log_node_06','log_node_07','log_node_08','log_node_09','log_node_10',
    'log_node_11','log_node_12','log_node_13',
  ],
  snap_gap: [
    'snp_node_01','snp_node_02','snp_node_03','snp_node_04','snp_node_05',
    'snp_node_06','snp_node_07','snp_node_08','snp_node_09','snp_node_10',
    'snp_node_11','snp_node_12','snp_node_13',
  ],
  tap_clues: [
    'tap_node_01','tap_node_02','tap_node_03','tap_node_04','tap_node_05',
    'tap_node_06','tap_node_07','tap_node_08','tap_node_09','tap_node_10',
    'tap_node_11','tap_node_12','tap_node_13',
  ],
}

/** Nodes grouped by difficulty tier within a module */
function nodesByTier(module: string): Record<number, string[]> {
  const all = MODULE_NODES[module] ?? []
  const tiers: Record<number, string[]> = { 1: [], 2: [], 3: [] }
  for (const id of all) tiers[nodeDifficulty(id)].push(id)
  return tiers
}

/** Fisher-Yates shuffle */
function shuffle<T>(arr: T[]): T[] {
  const a = [...arr]
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]]
  }
  return a
}

/**
 * Build a 5-question session queue starting from startNodeId.
 * Questions come from the same module and get difficult only up to the difficulty of startNodeId.
 * Questions 2-5 are sorted by difficulty to increment in difficulty.
 */
export function buildSessionQueue(
  module:      string,
  startNodeId: string,
  unlockedIds: string[],
): string[] {
  const startD = nodeDifficulty(startNodeId)
  const allNodes = MODULE_NODES[module] ?? []
  const targetLength = 5

  // Candidate pools: only difficulties <= startD, excluding startNodeId
  const sameTier = shuffle(
    allNodes.filter(id => nodeDifficulty(id) === startD && id !== startNodeId)
  )
  const lowerTiers = allNodes.filter(id => nodeDifficulty(id) < startD)

  // Group and shuffle lower tiers to maintain randomness
  const lowerTiersByD: Record<number, string[]> = { 1: [], 2: [], 3: [] }
  for (const id of lowerTiers) {
    const d = nodeDifficulty(id)
    if (lowerTiersByD[d]) {
      lowerTiersByD[d].push(id)
    }
  }
  
  let sortedLower: string[] = []
  for (let d = 1; d < startD; d++) {
    sortedLower = sortedLower.concat(shuffle(lowerTiersByD[d] || []))
  }

  const queue: string[] = [startNodeId]
  const seen = new Set([startNodeId])

  // Fill with lower tiers first
  for (const id of sortedLower) {
    if (queue.length >= targetLength) break
    if (!seen.has(id)) {
      queue.push(id)
      seen.add(id)
    }
  }

  // Fill with same tier
  for (const id of sameTier) {
    if (queue.length >= targetLength) break
    if (!seen.has(id)) {
      queue.push(id)
      seen.add(id)
    }
  }

  // Sort questions 2 to queue.length by difficulty to increment difficulty
  const remaining = queue.slice(1)
  remaining.sort((a, b) => nodeDifficulty(a) - nodeDifficulty(b))

  return [startNodeId, ...remaining]
}

// ── localStorage persistence ───────────────────────────────────────────────

export interface SessionProgress {
  sessionQueue:  string[]
  questionIndex: number
  savedAt:       number   // epoch ms
  next_node?:    string
  streak?:       number
}

function storageKey(module: string, startNodeId: string): string {
  return `critica_session__${module}__${startNodeId}`
}

export function saveSession(
  module:       string,
  startNodeId:  string,
  progress:     Omit<SessionProgress, 'savedAt'>,
): void {
  try {
    localStorage.setItem(
      storageKey(module, startNodeId),
      JSON.stringify({ ...progress, savedAt: Date.now() }),
    )
  } catch { /* ignore quota errors */ }
}

export function loadSession(
  module:      string,
  startNodeId: string,
): SessionProgress | null {
  try {
    const raw = localStorage.getItem(storageKey(module, startNodeId))
    if (!raw) return null
    const data = JSON.parse(raw) as SessionProgress
    // Expire after 24 hours
    if (Date.now() - data.savedAt > 86_400_000) {
      localStorage.removeItem(storageKey(module, startNodeId))
      return null
    }
    return data
  } catch { return null }
}

export function clearSession(
  module:      string,
  startNodeId: string,
): void {
  try {
    localStorage.removeItem(storageKey(module, startNodeId))
  } catch { /* ignore */ }
}
