from client import A2AClient

def main():
    # ── Discovery ───────────────────────────────────────────────
    research = A2AClient("http://localhost:8001")
    writer   = A2AClient("http://localhost:8002")

    print("Agents discovered:")
    print(f"  [{research.card['name']}] {research.card['description']}")
    print(f"  [{writer.card['name']}]   {writer.card['description']}")

    # ── User input ──────────────────────────────────────────────
    query = input("\nEnter research query: ")

    # ── Step 1: Research Agent ──────────────────────────────────
    print("\n[1/2] Sending query to ResearchAgent...")
    research_task = research.send_task(query)
    findings = research.get_artifact_text(research_task)
    print(f"      State: {research_task['status']['state']}")
    print(f"      Preview: {findings[:60]}...")

    # ── Step 2: Writer Agent (receives research output) ─────────
    print("\n[2/2] Passing findings to WriterAgent...")
    writer_task = writer.send_task(findings)   # artifact becomes input
    report = writer.get_artifact_text(writer_task)
    print(f"      State: {writer_task['status']['state']}")

    # ── Final output ────────────────────────────────────────────
    print("\n" + "="*48)
    print(report)
    print("="*48)

if __name__ == "__main__":
    main()