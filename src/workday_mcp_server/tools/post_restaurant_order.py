from datetime import datetime
import json

from workday_mcp_server.workday_client import WorkdayClient

client = WorkdayClient()


MONTHS = [
    "JAN", "FEB", "MAR", "APR", "MAY", "JUN",
    "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"
]


def parse_order_items(order_items_input: str):
    parsed_items = []

    try:
        if (
            order_items_input.strip().startswith("[")
            or order_items_input.strip().startswith("{")
        ):
            parsed = json.loads(order_items_input)
            parsed_items = parsed if isinstance(parsed, list) else [parsed]
        else:
            raise ValueError("Not JSON")
    except Exception:
        item_segments = order_items_input.split(",")

        for segment in item_segments:
            segment = segment.strip()

            if not segment:
                continue

            import re

            match = re.match(r"^(\d+)\s+(.+)$", segment)

            if match:
                parsed_items.append(
                    {
                        "itemName": match.group(2).strip(),
                        "quantity": int(match.group(1)),
                    }
                )
            else:
                parsed_items.append(
                    {
                        "itemName": segment,
                        "quantity": 1,
                    }
                )

    return parsed_items


async def post_restaurant_order(
    restaurant_id: str,
    worker_id: str,
    order_items_input: str,
    delivery_date: str,
    order_address: str,
):
    parsed_items = parse_order_items(order_items_input)

    if not parsed_items:
        return {
            "error": "No valid order items supplied."
        }

    bulk_items_result = await client.post(
        "/orderItems?bulk=true",
        {
            "data": parsed_items
        },
    )

    response_data = bulk_items_result.get("data", [])

    dynamic_order_items = [
        {
            "id": item["body"]["id"]
        }
        for item in response_data
        if item.get("status") == 201
        and item.get("body")
        and item["body"].get("id")
    ]

    if not dynamic_order_items:
        return {
            "error": "No order item IDs returned."
        }

    dt = datetime.strptime(delivery_date, "%Y-%m-%d")

    order_payload = {
        "restaurant": {
            "id": restaurant_id
        },
        "createdBy": {
            "id": worker_id
        },
        "orderItems": dynamic_order_items,
        "orderAddress": order_address,
        "deliveryDate": delivery_date,
        "orderMonth": MONTHS[dt.month - 1],
        "orderYear": str(dt.year),
    }

    return await client.post(
        "/restaurantOrders",
        order_payload,
    )