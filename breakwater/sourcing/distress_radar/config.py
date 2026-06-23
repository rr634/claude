"""
Breakwater Distress Radar — configuration.

Central, tunable parameters for the distress-detection engine. Everything a
non-engineer might reasonably want to change (the $100K trigger, the target
submarkets, the scoring weights) lives here.
"""

# ---------------------------------------------------------------------------
# Hard trigger (the founder's rule): a recorded lien / claim of lien at or
# above this amount is the primary distress trigger for a developer.
# ---------------------------------------------------------------------------
LIEN_MIN_AMOUNT = 100_000

# Acquisition box (mirrors the Screening Box, artifact 03).
EXIT_VALUE_BOX = (2_000_000, 15_000_000)   # finished value range we pursue

# ---------------------------------------------------------------------------
# Canonical document types. County portals use many labels; adapters normalize
# raw labels into these codes (see models.normalize_doc_type).
# ---------------------------------------------------------------------------
CLAIM_OF_LIEN          = "CLAIM_OF_LIEN"            # FL Ch. 713 construction lien
LIS_PENDENS            = "LIS_PENDENS"              # lawsuit pending (often foreclosure)
NOTICE_OF_COMMENCEMENT = "NOTICE_OF_COMMENCEMENT"   # FL Ch. 713 — construction started
FINAL_JUDGMENT         = "FINAL_JUDGMENT"
JUDGMENT_LIEN          = "JUDGMENT_LIEN"
TAX_LIEN               = "TAX_LIEN"                 # federal/state/county tax lien
NOTICE_OF_DEFAULT      = "NOTICE_OF_DEFAULT"
MORTGAGE               = "MORTGAGE"
RELEASE                = "RELEASE"                  # satisfaction/release (negative signal)
OTHER                  = "OTHER"

# Document types that represent a monetary lien for the amount test.
LIEN_DOC_TYPES = {CLAIM_OF_LIEN, JUDGMENT_LIEN, TAX_LIEN}

# ---------------------------------------------------------------------------
# Distress scoring weights. Higher = stronger distress signal.
# Tuned to favor the Breakwater thesis: an *active* luxury project whose
# construction has stalled into liens and/or foreclosure.
# ---------------------------------------------------------------------------
DOC_WEIGHTS = {
    LIS_PENDENS:       40,   # foreclosure/litigation in progress — strongest
    NOTICE_OF_DEFAULT: 28,
    CLAIM_OF_LIEN:     30,   # contractor unpaid — classic stall
    FINAL_JUDGMENT:    25,
    JUDGMENT_LIEN:     20,
    TAX_LIEN:          18,
}

# Premium: a Notice of Commencement (active construction) PLUS a lien means a
# live project in financial trouble — our exact target (50–90% complete stall).
PREMIUM_STALLED_CONSTRUCTION = 25

# Each additional stacked lien beyond the first adds this much (cumulative pain).
STACK_PER_EXTRA_LIEN = 8

# A recent RELEASE/SATISFACTION of the lien reduces the score (problem cured).
RELEASE_PENALTY = 35

# Fit boosts (not distress per se — they rank in-thesis deals higher).
FIT_SUBMARKET  = 12
FIT_VALUE_BOX  = 10

# Amount banding: larger liens, more points (max qualifying lien on the parcel).
AMOUNT_BANDS = [
    (3_000_000, 25),
    (1_000_000, 18),
    (  500_000, 12),
    (  250_000,  8),
    (  100_000,  4),   # at/above the hard trigger
]

# Classification thresholds (composite score).
SCORE_THRESHOLD_HOT   = 60   # + must be "triggered" (lien >= LIEN_MIN_AMOUNT)
SCORE_THRESHOLD_WATCH = 30

# ---------------------------------------------------------------------------
# Target submarkets by county (mirrors thesis geography). Used for fit scoring
# and for prioritizing scarce analyst attention. Matching is case-insensitive
# substring against the parcel's submarket/city.
# ---------------------------------------------------------------------------
TARGET_SUBMARKETS = {
    "broward": {
        "Fort Lauderdale", "Las Olas", "Rio Vista", "Harbor Beach",
        "Coral Ridge", "Lighthouse Point", "Hillsboro Beach", "Sea Ranch Lakes",
    },
    "miami_dade": {
        "Miami Beach", "Coconut Grove", "Coral Gables", "Bay Harbor Islands",
        "Golden Beach", "Sunset Islands", "Key Biscayne",
    },
    "palm_beach": {
        "Palm Beach", "Manalapan", "Boca Raton", "Delray Beach",
        "Highland Beach", "Jupiter", "Admirals Cove", "Singer Island",
    },
    "martin":    {"Stuart", "Sewall's Point", "Jupiter Island"},
    "st_lucie":  {"Vero Beach"},
    "monroe":    {"Islamorada", "Key Largo"},
}


def all_submarkets():
    out = set()
    for s in TARGET_SUBMARKETS.values():
        out |= s
    return out
