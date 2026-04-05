from twin_manager import simulate_snapshot


def sync_twins():
    twins = simulate_snapshot()
    print(f"SYNC COMPLETE: {len(twins)} twins updated")
    return twins


def start_sync():
    return sync_twins()
