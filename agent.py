import argparse
from .config import Settings
from .db import MemoryDB
from .generator import AIGenerator
from .duplicate import is_duplicate
from .publishers import build_publishers

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    s = Settings()
    dry_run = args.dry_run or s.dry_run
    db = MemoryDB()

    try:
        db.add_run("started", f"dry_run={dry_run}")
        generator = AIGenerator(s)
        old = db.recent_posts(s.memory_lookback)
        rejected = []
        selected = None

        for attempt in range(1, s.max_generation_attempts + 1):
            post = generator.generate(old, rejected)
            duplicate, best = is_duplicate(post, old, s.duplicate_threshold)

            if duplicate:
                rejected.append({
                    "title": post["title"],
                    "topic": post["topic"],
                    "reason": f"similarity={best[0]} old_id={best[1]}"
                })
                print(f"[REJECTED] attempt={attempt} similarity={best[0]}")
                continue

            selected = post
            print(f"[ACCEPTED] attempt={attempt} title={post['title']}")
            break

        if not selected:
            raise RuntimeError("لم يتم الوصول إلى فكرة جديدة بعد عدد المحاولات المحدد")

        if dry_run:
            print("\n=== DRY RUN ===")
            print(selected["title"])
            print(selected["content"])
            print(" ".join(selected["hashtags"]))
            db.add_run("dry_run", selected["title"])
            return

        publishers = build_publishers(s)
        for pub in publishers:
            pub.publish(selected)
            db.add_post(selected, pub.name)
            print(f"[PUBLISHED] {pub.name}")

        db.add_run("success", selected["title"])

    except Exception as exc:
        db.add_run("failed", repr(exc))
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main()
