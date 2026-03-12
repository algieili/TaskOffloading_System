def compute_gbfs_score(task_params):
    """
    [10% Functionality Prototype]
    Demonstrates the heuristic scoring phase of GBFS.
    Returns a deterministic score based on basic inputs.
    """
    # Simple demo calculation
    temp = float(task_params.get("Temperature (°C)", 0))
    cpu = float(task_params.get("CPU Load (%)", 0))
    score = (temp * 0.3) + (cpu * 0.7)
    return round(score, 2)
