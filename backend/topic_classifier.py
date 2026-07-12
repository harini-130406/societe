import spacy

# Lazy loading of spaCy model
_nlp = None

def get_nlp():
    global _nlp
    if _nlp is None:
        _nlp = spacy.load("en_core_web_sm")
    return _nlp

# Comprehensive topic keywords (lowercased, lemmatized equivalents where appropriate)
TOPIC_KEYWORDS = {
    "Password": [
        "password", "passphrase", "complexity", "rotation", "rotate", "length", 
        "character", "alphanumeric", "pin", "credential"
    ],
    "MFA": [
        "mfa", "multi-factor", "2fa", "two-factor", "otp", "one-time password", 
        "token", "authenticator", "verification", "second factor"
    ],
    "Authentication": [
        "authenticate", "authentication", "login", "sign-in", "auth", "passwordless",
        "credential", "identity verification"
    ],
    "Encryption": [
        "encrypt", "encryption", "cryptographic", "cipher", "tls", "ssl", "hash", 
        "sha", "md5", "aes", "pgp", "certificate", "keys", "decryption", "cryptography"
    ],
    "Logging": [
        "log", "logs", "logging", "audit", "event", "syslog", "trace", "monitor", 
        "record", "siem"
    ],
    "Cloud": [
        "cloud", "aws", "azure", "gcp", "s3", "bucket", "vm", "instance", "tenant", 
        "serverless", "saas", "paas", "iaas", "kubernetes", "docker"
    ],
    "Network": [
        "network", "lan", "wan", "router", "switch", "subnet", "ip address", 
        "routing", "dns", "dhcp", "bandwidth"
    ],
    "Firewall": [
        "firewall", "ports", "ingress", "egress", "traffic", "block", "allow", 
        "ruleset", "packet filter"
    ],
    "VPN": [
        "vpn", "virtual private network", "tunnel", "ipsec", "openvpn", "wireguard", 
        "remote access"
    ],
    "Backup": [
        "backup", "backups", "replication", "replica", "restore", "disaster recovery", 
        "snapshot", "recovery point"
    ],
    "Identity": [
        "identity", "iam", "active directory", "ldap", "saml", "oidc", "user account", 
        "group membership", "provision", "entitlement", "directory service"
    ],
    "Access Control": [
        "access", "authorization", "rbac", "abac", "privilege", "permission", 
        "lock", "timeout", "inactivity", "revoke", "least privilege"
    ],
    "Retention": [
        "retention", "retain", "archive", "purge", "delete", "destroy", "lifespan", 
        "retrieved", "disposal"
    ],
    "Data Retention": [
        "data retention", "retain data", "data archive", "data purge", "data delete", 
        "data destroy", "data lifespan", "data disposal", "data storage", "data backup"
    ],
    "Vendor": [
        "vendor", "third-party", "supplier", "contractor", "external", "outsourcing", 
        "sla", "nda", "procurement"
    ],
    "Incident Response": [
        "incident", "breach", "response", "notification", "alert", "disaster", 
        "escalate", "forensic", "recovery plan", "compromise", "incident report"
    ],
    "Asset": [
        "asset", "assets", "hardware", "device", "equipment", "inventory"
    ],
    "Privacy": [
        "privacy", "personal data", "gdpr", "pii", "personal information", "data protection"
    ],
    "Monitoring": [
        "monitor", "monitoring", "surveillance", "observe", "track", "watch"
    ],
    "API": [
        "api", "application programming interface", "rest", "graphql", "web service", "endpoint"
    ],
    "Mobile": [
        "mobile", "smartphone", "tablet", "ios", "android", "cell phone", "portable device"
    ],
    "Endpoint": [
        "endpoint", "endpoints", "workstation", "client", "terminal", "device"
    ],
    "Provisioning": [
        "provision", "provisioning", "setup", "configure", "deploy", "initialize"
    ],
    "Physical": [
        "physical", "building", "facility", "premise", "on-site", "office", "security guard"
    ],
    "Change": [
        "change", "change management", "modification", "update", "alteration"
    ],
    "Patch": [
        "patch", "patching", "update", "security update", "hotfix", "service pack"
    ],
    "HR": [
        "hr", "human resources", "personnel", "employee", "staff", "workforce"
    ]
}

def classify_topics(text: str, threshold: float = 0.1) -> list:
    """
    Classifies a sentence into one or more topics.
    Uses spaCy for lemmatization and noun/verb checking, matching against keyword dicts.
    """
    nlp = get_nlp()
    doc = nlp(text.lower())
    
    # Extract lemmas and plain lowercased tokens
    lemmas = [token.lemma_ for token in doc]
    tokens = [token.text for token in doc]
    
    scores = {}
    
    for topic, keywords in TOPIC_KEYWORDS.items():
        score = 0
        for kw in keywords:
            # Multi-word keyword checking
            if " " in kw:
                if kw in text.lower():
                    score += 2.0
            else:
                # Direct match in tokens or lemmas
                if kw in tokens or kw in lemmas:
                    score += 1.0
                # Substring match (e.g. "backups" -> matches "backup")
                elif any(kw in t for t in tokens):
                    score += 0.5
                    
        if score > 0:
            # Normalize score by keyword list length or length of sentence
            scores[topic] = score
            
    if not scores:
        return ["access control"] # Default
        
    # Get all topics that have positive score, sorted
    sorted_topics = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    max_score = sorted_topics[0][1]
    
    # Return all topics with score >= max_score * 0.5, converted to lowercase
    selected_topics = [t.lower() for t, s in sorted_topics if s >= max_score * 0.5]
    
    return selected_topics
