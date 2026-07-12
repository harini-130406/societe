import re
import datetime
import json
import os

# Deprecated tech pattern mapping
DEPRECATED_TECH = {
    r"\btls\s+1\.0\b": "TLS 1.0 (superseded by TLS 1.2/1.3)",
    r"\btls\s+1\.1\b": "TLS 1.1 (superseded by TLS 1.2/1.3)",
    r"\bssl\s*v[23]\b": "SSLv2/SSLv3 (insecure, deprecated)",
    r"\bsha-?1\b": "SHA-1 (cryptographically broken)",
    r"\bmd5\b": "MD5 (cryptographically broken)",
    r"\bwindows\s+server\s+2012\b": "Windows Server 2012 (End of Life)",
    r"\bwindows\s+server\s+2008\b": "Windows Server 2008 (End of Life)",
    r"\bwindows\s+xp\b": "Windows XP (End of Life)",
    r"\bwindows\s+7\b": "Windows 7 (End of Life)",
    r"\bdes\b": "DES (insecure)",
    r"\b3des\b": "3DES (deprecated)"
}

# Deprecated standards pattern mapping
DEPRECATED_STANDARDS = {
    r"\bnist\s+800-53\s+rev\s*4\b": "NIST SP 800-53 Rev 4 (superseded by Rev 5)",
    r"\biso\s*(?:27001|27002):2013\b": "ISO/IEC 27001:2013 (superseded by ISO/IEC 27001:2022)",
    r"\bpci-?dss\s+v?3\.2(?:\.1)?\b": "PCI-DSS v3.2.1 (superseded by PCI-DSS v4.0)"
}

# Global cache for policy metadata
_policy_metadata_cache = None

def load_policy_metadata():
    """
    Loads policy_metadata.json from sample_data directory.
    Returns a dict mapping policy filenames to metadata.
    """
    global _policy_metadata_cache
    if _policy_metadata_cache is not None:
        return _policy_metadata_cache
    
    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sample_data_dir = os.path.join(base_dir, "sample_data")
        metadata_path = os.path.join(sample_data_dir, "policy_metadata.json")
        
        with open(metadata_path, "r", encoding="utf-8") as f:
            metadata_list = json.load(f)
        
        # Convert to dict keyed by filename
        _policy_metadata_cache = {item["file"]: item for item in metadata_list}
        return _policy_metadata_cache
    except Exception as e:
        print(f"Warning: Could not load policy_metadata.json: {e}")
        return {}

def get_policy_status(policy_filename: str) -> str:
    """
    Returns the status of a policy from metadata (active, retired, draft).
    Defaults to 'active' if not found.
    """
    metadata = load_policy_metadata()
    policy_data = metadata.get(policy_filename, {})
    return policy_data.get("status", "active").lower()

def check_staleness(raw_text: str, metadata: dict, policy_filename: str = None) -> dict:
    """
    Checks the raw text of an obligation and its document metadata for staleness.
    Checks:
    - Old review dates (> 18 months)
    - Deprecated technologies
    - Deprecated standards
    - Missing metadata fields (owner, version, review history)
    """
    reasons = []
    is_date_stale = False
    
    # 0. Policy Status Check (from metadata)
    if policy_filename:
        policy_status = get_policy_status(policy_filename)
        if policy_status == "retired":
            reasons.append("Policy status is 'retired' in metadata")
            is_date_stale = True
        elif policy_status == "draft":
            reasons.append("Policy status is 'draft' in metadata (not yet approved)")
    
    # 1. Date Check
    review_date = metadata.get("review_date") or metadata.get("last_reviewed")
    if review_date:
        try:
            # Handle string conversion
            rev_str = str(review_date).strip()
            rev_date = datetime.datetime.strptime(rev_str, "%Y-%m-%d")
            # Fixed target timestamp for SG hackathon context
            current_time = datetime.datetime(2026, 7, 11)
            age_months = (current_time - rev_date).days / 30.4
            if age_months > 18:
                is_date_stale = True
                reasons.append(f"Last reviewed date ({rev_str}) is older than 18 months")
        except Exception:
            reasons.append(f"Invalid date format in metadata: {review_date}")
    else:
        reasons.append("Missing review date")
        is_date_stale = True

    # 2. Deprecated Tech Check
    for regex, desc in DEPRECATED_TECH.items():
        if re.search(regex, raw_text, re.IGNORECASE):
            reasons.append(f"References superseded/deprecated technology: {desc}")
            
    # 3. Deprecated Standards Check
    for regex, desc in DEPRECATED_STANDARDS.items():
        if re.search(regex, raw_text, re.IGNORECASE):
            reasons.append(f"References superseded/deprecated compliance standard: {desc}")
            
    # 4. Metadata Integrity Checks
    owner = metadata.get("owner")
    if not owner or str(owner).lower().strip() in ["unknown", "unknown owner", ""]:
        reasons.append("Missing owner metadata")
        
    version = metadata.get("version")
    if not version or str(version).strip() == "":
        reasons.append("Missing version metadata")
        
    review_history = metadata.get("review_history")
    if not review_history or (isinstance(review_history, list) and len(review_history) == 0):
        reasons.append("Missing review history metadata")
        
    return {
        "is_stale": len(reasons) > 0,
        "is_date_stale": is_date_stale,
        "reasons": reasons
    }
