ACCEPT_KEYWORDS = [
    "Autoriser tous les cookies",

    # Keep optional
    "stay opted-in",
    "stay opt-in",
    "stay opted in",
    "stay opt in",
    "stay opted",
    "stay opt",

    # Basic accept
    "accept",
    "accept all",
    "accept all cookie",
    "accept all cookies",
    "accept cookie",
    "accept cookies",
    "accept all and close",
    "accept all & close",
    "accept everything",
    "accept all terms",

    # Allow wording
    "allow",
    "allow all",
    "allow all cookie",
    "allow all cookies",
    "allow cookie",
    "allow cookies",
    "allow everything",

    # Agree wording
    "agree",
    "agree all",
    "agree to all",
    "i agree",
    "i accept",
    "agree and continue",
    "agree & close",

    # Consent wording
    "consent",
    "give consent",
    "provide consent",
    "grant consent",

    # Positive confirmation
    "yes",
    "yes, i agree",
    "yes, accept",
    "ok",
    "okay",
    "got it",
    "sounds good",
    "understand",
    "i understand",

    # Continue wording
    "continue",
    "continue to site",
    "continue browsing",
    "continue with all",
    "continue and accept",
    "proceed",
    "proceed to site",
    "accept and proceed",
    "accept and continue",

    # Enable wording
    "enable all",
    "enable cookie",
    "enable cookies",
    "enable all cookie",
    "enable all cookies",

    # Confirm wording
    "confirm",
    "confirm all",
    "confirm and continue",
]

REJECT_KEYWORDS = [
    # Basic reject
    "decline",
    "decline all",
    "decline cookie",
    "decline cookies",
    "decline all cookie",
    "decline all cookies",
    "reject",
    "reject all",
    "reject cookie",
    "reject cookies",
    "reject all cookie",
    "reject all cookies",

    # Deny wording
    "deny",
    "deny all",
    "deny cookie",
    "deny cookies",

    # Negative agreement
    "disagree",
    "refuse",

    # Opt-out wording
    "opt out",
    "opt-out",
    "opt out of all",
    "opt out of cookie",
    "opt out of cookies",

    # Explicit negative
    "do not accept",
    "do not agree",
    "do not allow",

    # Disable wording
    "disable",
    "disable all",
    "disable cookie",
    "disable cookies",
    "turn off cookie",
    "turn off cookies",
    "turn off all",

    # Hard rejection
    "reject non-essential",
    "deny non-essential",
]

SPECIAL_KEYWORDS = [
    "Accepter uniquement les cookies nécessaires",

    # Essential / Necessary only
    "essential only",
    "necessary only",
    "strictly necessary",
    "strictly necessary only",
    "use necessary cookie only",
    "use necessary cookies only",
    "only necessary",
    "only essential",
    "required only",
    "accept essential only",
    "allow essential only",
    "essential cookie only",
    "essential cookies only",
    "necessary cookie only",
    "necessary cookies only",

    # Optional related
    "accept optional",
    "allow optional",
    "optional only",
    "enable optional",
    "accept selected",
    "allow selected",

    # Partial / selective consent
    "accept selected cookie",
    "accept selected cookies",
    "allow selected cookie",
    "allow selected cookies",
    "selected cookie only",
    "selected cookies only",
    "save selected",
    "confirm selected",
    "confirm selection",
    "save selection",
    "apply selection",
    "apply selected",

    # Required related
    "required",
    "required only",
    "required cookies",
    "required cookie",
    "required cookies only",
    "use required cookies only",
    "accept required",
    "accept required only",
    "accept required cookies",
    "allow required",
    "allow required only",
    "allow required cookies",
    "required and functional only",

    # Preferences only
    "accept preference",
    "accept preferences",
    "allow preference",
    "allow preferences",
    "enable preference",
    "enable preferences",
    "consent to selected",
    "accept some",
    "allow some",

    # Reject optional / decline optional
    "reject optional",
    "reject optional cookie",
    "reject optional cookies",
    "reject nonessential",
    "reject non-essential",
    "reject nonessential cookies",
    "reject non-essential cookies",
    "reject unessential",
    "reject unessential cookies",
    "reject unnecessary",
    "reject unnecessary cookies",
    "decline optional",
    "decline optional cookies",
    "decline nonessential",
    "decline non-essential",
    "decline nonessential cookies",
    "decline non-essential cookies",
    "decline unnecessary",
    "decline unnecessary cookies",
    "disable optional",
    "disable optional cookies",
    "disable nonessential",
    "disable non-essential",
    "disable unnecessary",

    # Mixed wording
    "accept essential cookie",
    "accept essential cookies",
    "allow essential cookie",
    "allow essential cookies",
    "accept necessary cookie",
    "accept necessary cookies",
    "allow necessary cookie",
    "allow necessary cookies",
]

CUSTOMIZE_KEYWORDS = [
    # Settings
    "cookie setting",
    "cookie settings",
    "cookies setting",
    "cookies settings",
    "privacy setting",
    "privacy settings",
    "setting",
    "settings",
    "advanced setting",
    "advanced settings",
    "advanced option",
    "advanced options",

    # Manage
    "manage",
    "manage cookie",
    "manage cookies",
    "manage preference",
    "manage preferences",
    "manage option",
    "manage options",
    "manage setting",
    "manage settings",
    "manage consent",

    # Preferences
    "preference",
    "preferences",
    "cookie preference",
    "cookie preferences",
    "cookies preference",
    "cookies preferences",
    "privacy preference",
    "privacy preferences",

    # Customize
    "customize",
    "customise",
    "edit preference",
    "edit preferences",
    "edit setting",
    "edit settings",

    # More info
    "more option",
    "more options",
    "show purposes",
    "learn more",
    "view detail",
    "view details",
    "detail",
    "details",

    # Save actions
    "save choice",
    "save choices",
    "confirm choice",
    "confirm choices",
    "save setting",
    "save settings",
    "save preference",
    "save preferences",
    "apply setting",
    "apply settings",

    # Dismiss-like
    "close",
    "dismiss",
    "no thanks",
    "not now",
    "later",
    "skip",
]

ACTION_KEYWORDS = ACCEPT_KEYWORDS + REJECT_KEYWORDS + SPECIAL_KEYWORDS + CUSTOMIZE_KEYWORDS
