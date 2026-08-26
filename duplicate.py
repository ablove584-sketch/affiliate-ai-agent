import hashlib
import re
from collections import Counter

AR_STOP = {
    "من","في","على","إلى","عن","هذا","هذه","ذلك","تلك","هو","هي","هم","مع",
    "أن","إن","ما","لا","لم","لن","قد","كل","أو","و","ثم","حتى","كما","كان",
    "كانت","يكون","يمكن","هناك","بعد","قبل","لكن","لأن","أي","أكثر","أقل"
}

def normalize(text):
    text = text.lower()
    text = re.sub(r"https?://\S+", " ", text)
    text = re.sub(r"[^\w\s\u0600-\u06FF]", " ", text)
    text = re.sub(r"(.)\1{2,}", r"\1", text)
    return re.sub(r"\s+", " ", text).strip()

def tokens(text):
    return [x for x in normalize(text).split() if x not in AR_STOP and len(x) > 1]

def shingles(text, n=3):
    t = tokens(text)
    if len(t) <= n:
        return set(t)
    return {" ".join(t[i:i+n]) for i in range(len(t)-n+1)}

def jaccard(a, b):
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)

def cosine(a, b):
    ca, cb = Counter(tokens(a)), Counter(tokens(b))
    keys = set(ca) | set(cb)
    if not keys:
        return 0.0
    dot = sum(ca[k] * cb[k] for k in keys)
    na = sum(v*v for v in ca.values()) ** 0.5
    nb = sum(v*v for v in cb.values()) ** 0.5
    return dot / (na * nb) if na and nb else 0.0

def similarity(candidate, old):
    c_all = f'{candidate["title"]} {candidate["topic"]} {candidate["angle"]} {candidate["content"]}'
    o_all = f'{old["title"]} {old["topic"]} {old["angle"]} {old["content"]}'
    text_score = cosine(c_all, o_all)
    shingle_score = jaccard(shingles(c_all), shingles(o_all))
    title_score = cosine(candidate["title"], old["title"])
    topic_score = cosine(candidate["topic"], old["topic"])
    kw_score = jaccard(set(candidate["keywords"]), set(str(old["keywords"]).split(",")))
    return round(max(
        0.50 * text_score + 0.25 * shingle_score + 0.15 * title_score + 0.10 * topic_score,
        0.55 * text_score + 0.20 * shingle_score + 0.15 * topic_score + 0.10 * kw_score
    ), 4)

def fingerprint(post):
    base = normalize(f'{post["title"]}|{post["topic"]}|{post["angle"]}|{post["content"]}')
    return hashlib.sha256(base.encode("utf-8")).hexdigest()

def is_duplicate(candidate, old_posts, threshold):
    scores = [(similarity(candidate, old), old["id"]) for old in old_posts]
    best = max(scores, default=(0.0, None))
    return best[0] >= threshold, best
