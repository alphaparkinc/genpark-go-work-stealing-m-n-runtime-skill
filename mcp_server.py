import sys
import json
from client import WorkStealingRuntime

runtime = WorkStealingRuntime(num_p=4)

def handle_call(name, arguments):
    if name == "spawn":
        p = arguments.get("p_id", 0)
        tid = arguments.get("task_id", "t0")
        val = arguments.get("val", 1)
        runtime.spawn(p, tid, lambda: val)
        return {"status": "spawned", "task_id": tid}
    elif name == "step":
        p = arguments.get("p_id", 0)
        tid = runtime.step(p)
        return {"executed_task": tid, "completed_count": len(runtime.completed_tasks)}
    return {"error": f"Unknown tool: {name}"}

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            res = handle_call(req.get("name"), req.get("arguments", {}))
            print(json.dumps({"id": req.get("id"), "result": res}))
            sys.stdout.flush()
        except Exception as e:
            print(json.dumps({"error": str(e)}))
            sys.stdout.flush()

if __name__ == "__main__":
    main()
