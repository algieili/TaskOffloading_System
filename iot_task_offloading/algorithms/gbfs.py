def compute_gbfs_score(task_params):
    """
    Placeholder for Greedy Best-First Search algorithm score.
    In a real scenario, this would evaluate a heuristic based on task requirements.
    """
    # Simple heuristic: lower temperature and CPU load are better
    score = (task_params['cpu_load'] * 0.4) + (task_params['net_latency'] * 0.6)
    return round(score, 2)
