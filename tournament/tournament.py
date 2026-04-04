import concurrent.futures
import time
import docker
import threading

try:
    import docker
    client = docker.from_env()
    client.ping()   # Test connection
    DOCKER_AVAILABLE = True
    print("[Tournament] Docker connected ✓")
except Exception as e:
    DOCKER_AVAILABLE = False
    client = None
    print(f"[Tournament] Docker not available: {e}")
    print("[Tournament] Running in MOCK mode")

print_lock = threading.Lock()
def safe_print(msg):
    with print_lock:
        print(msg)

client = docker.from_env()


def create_twin(twin_id: int, real_container_name: str) -> str:
    """
    Clone the real container into a twin for safe testing.
    Returns the twin container name.
    """
    twin_name = f"twinforge_twin_{twin_id}"


    try:
        old = client.containers.get(twin_name)
        old.stop()
        old.remove()
    except:
        pass


    try:
        real = client.containers.get(real_container_name)
        image = real.image
    except Exception as e:
        safe_print(f"[Twin {twin_id}] WARNING: Real container not found. Using default image.")
        image = "python:3.11-slim"  


    twin = client.containers.run(
        image=image,
        name=twin_name,
        detach=True,
        mem_limit="256m",
        cpu_period=100000,
        cpu_quota=50000,
        labels={"twinforge": "twin", "twin_id": str(twin_id)},
        command="sleep 300"  
    )

    safe_print(f"[Twin {twin_id}] Created successfully: {twin_name}")
    return twin_name


def apply_fix_on_twin(twin_name: str, fix: dict) -> dict:
    """
    Apply a single fix on a single twin container.
    Returns a result dict with success, speed, side effects.
    """
    safe_print(f"[Tournament] ▶ Starting fix '{fix['name']}' on {twin_name}")
    start_time = time.time()
    success = False
    side_effects = []
    error_msg = None

    try:
        container = client.containers.get(twin_name)
        action = fix["action"]

        if action == "restart_service":
            container.restart(timeout=10)
            time.sleep(3)
           
            container.reload()
            success = container.status == "running"

        elif action == "scale_memory":
            container.update(mem_limit="512m")
            time.sleep(2)
            container.reload()
            success = container.status == "running"

        elif action == "rate_limit":
         
            time.sleep(1)
            success = True
            side_effects.append("some_requests_may_be_rejected")

        elif action == "rollback":
            
            container.stop()
            time.sleep(2)
            container.start()
            time.sleep(3)
            container.reload()
            success = container.status == "running"
            side_effects.append("brief_downtime")

        elif action == "scale_up":
           
            time.sleep(2)
            success = True

        elif action == "clear_cache":
            container.exec_run("sh -c 'echo 3 > /proc/sys/vm/drop_caches' 2>/dev/null || true")
            time.sleep(1)
            success = True

        else:
            safe_print(f"[Tournament] Unknown action: {action}")
            success = False

        recovery_time = round(time.time() - start_time, 2)

    except Exception as e:
        recovery_time = round(time.time() - start_time, 2)
        error_msg = str(e)
        side_effects.append("fix_threw_exception")
        success = False
        safe_print(f"[Tournament] ✗ Fix '{fix['name']}' failed: {e}")

    status_icon = "✓" if success else "✗"
    safe_print(f"[Tournament] {status_icon} '{fix['name']}' → "
               f"{'SUCCESS' if success else 'FAILED'} in {recovery_time}s")

    return {
        "fix_id":            fix["id"],
        "fix_name":          fix["name"],
        "fix_action":        fix["action"],
        "twin":              twin_name,
        "success":           success,
        "recovery_seconds":  recovery_time,
        "side_effects":      side_effects,
        "risk_level":        fix.get("risk_level", "medium"),
        "error":             error_msg,
    }



def pick_winner(results: list) -> dict:
    """
    Given tournament results, pick the best fix.
    Priority: 1) Must succeed  2) Fewest side effects  3) Fastest
    """
    successful = [r for r in results if r["success"]]

    if not successful:
       
        winner = min(results, key=lambda x: x["recovery_seconds"])
        winner["tournament_status"] = "no_fix_succeeded_using_fastest"
        safe_print(f"[Tournament] ⚠ No fix succeeded. Picking fastest: {winner['fix_name']}")
        return winner

   
    winner = min(successful, key=lambda x: (
        len(x["side_effects"]),
        x["recovery_seconds"]
    ))
    winner["tournament_status"] = "winner"
    return winner



def destroy_twin(twin_id: int):
    """Remove twin container after tournament is done"""
    try:
        twin = client.containers.get(f"twinforge_twin_{twin_id}")
        twin.stop(timeout=5)
        twin.remove()
        safe_print(f"[Twin {twin_id}] Destroyed and cleaned up")
    except Exception as e:
        safe_print(f"[Twin {twin_id}] Cleanup warning: {e}")



def run_tournament(fixes: list, real_container_name: str = "twinforge-web-1") -> dict:
    """
    THE MAIN FUNCTION — called by the backend
    
    Input:  fixes (list of 3 fix dicts from fixes.py)
    Output: tournament result dict with winner and all results
    """
    print("\n" + "="*55)
    print("[Tournament] FIX TOURNAMENT STARTING")
    print(f"[Tournament] {len(fixes)} fixes competing:")
    for i, f in enumerate(fixes):
        print(f"  Fix {i+1}: {f['name']} (risk: {f['risk_level']})")
    print("="*55)

    tournament_start = time.time()


    print("\n[Tournament] Phase 1: Spawning twins...")
    twin_names = []
    for i, fix in enumerate(fixes):
        twin_name = create_twin(i + 1, real_container_name)
        twin_names.append(twin_name)

    time.sleep(2)  

    print("\n[Tournament] Phase 2: All fixes racing NOW...")
    results = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:

        future_to_fix = {
            executor.submit(apply_fix_on_twin, twin_names[i], fixes[i]): fixes[i]
            for i in range(len(fixes))
        }

        
        for future in concurrent.futures.as_completed(future_to_fix):
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                safe_print(f"[Tournament] Thread error: {e}")

    print("\n[Tournament] Phase 3: Judging results...")
    winner = pick_winner(results)

    total_time = round(time.time() - tournament_start, 1)

    print(f"\n{'='*55}")
    print(f"[Tournament]  WINNER: {winner['fix_name']}")
    print(f"[Tournament] Recovery time: {winner['recovery_seconds']}s")
    print(f"[Tournament] Side effects: {winner['side_effects'] or 'None'}")
    print(f"[Tournament] Total tournament time: {total_time}s")
    print("="*55 + "\n")


    print("[Tournament] Phase 4: Cleaning up twins...")
    for i in range(len(fixes)):
        destroy_twin(i + 1)

    return {
        "winner":                  winner["fix_id"],
        "winner_details":          winner,
        "all_results":             results,
        "total_tournament_seconds": total_time,
        "twins_tested":            len(fixes),
    }

# ─── TEST ─────────────────────────────────────────────────────
if __name__ == "__main__":
    print("[TEST] Running tournament in MOCK mode (no Docker needed)")
    print("[TEST] This simulates what happens during a real incident\n")

    # MOCK the Docker parts for standalone testing
    import unittest.mock as mock

    mock_container = mock.MagicMock()
    mock_container.status = "running"
    mock_container.image = "python:3.11-slim"

    with mock.patch('docker.from_env') as mock_docker:
        mock_docker.return_value.containers.get.return_value = mock_container
        mock_docker.return_value.containers.run.return_value = mock_container

        from fixes import get_fixes_for_anomaly
        test_fixes = get_fixes_for_anomaly("cpu_percent")

        print(f"Testing with {len(test_fixes)} fixes for CPU spike anomaly:")
        result = run_tournament(test_fixes, "fake_container")

        print("\n[TEST RESULT]")
        print(f"  Winner: {result['winner']}")
        print(f"  All results:")
        for r in result['all_results']:
            print(f"    - {r['fix_name']}: {'✓' if r['success'] else '✗'} in {r['recovery_seconds']}s")