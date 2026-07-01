import httpx

from workday_mcp_server.workday_auth import get_bearer_token


async def get_worker_by_name(worker_name: str):
    if not worker_name:
        return {
            "error": "Missing required parameter 'worker_name'."
        }

    token = await get_bearer_token()

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get(
            "https://api.workday.com/common/v1/workers",
            headers=headers,
            params={"search": worker_name},
        )

    response.raise_for_status()

    result = response.json()

    workers = result.get("data", [])

    if not workers:
        return {
            "error": f"No workers found matching '{worker_name}'."
        }

    matched_workers = [
        {
            "name": worker.get("descriptor"),
            "id": worker.get("id"),
        }
        for worker in workers
    ]

    exact_match = next(
        (
            worker
            for worker in matched_workers
            if worker.get("name")
            and worker["name"].lower().strip()
            == worker_name.lower().strip()
        ),
        None,
    )

    if len(matched_workers) > 1 and not exact_match:
        return {
            "status": "multiple_matches",
            "workers": matched_workers,
        }

    selected_worker = exact_match or matched_workers[0]

    return {
        "status": "success",
        "worker": selected_worker,
    }