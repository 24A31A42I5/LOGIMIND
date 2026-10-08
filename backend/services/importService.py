from __future__ import annotations

import csv
import io
import re
from datetime import datetime, timezone
from typing import Any

from common.repository import write_domain_records


DATASETS = {
    'distributor': {'products': 'distributor_shipments', 'shipments': 'distributor_shipments'},
    'raw_material': {'consumers': 'supplier_orders', 'supplies': 'supplier_orders'},
    'retail': {'sales': 'retail_sales', 'consumers': 'retail_consumers'},
    'restaurant': {'orders': 'restaurant_orders', 'menu': 'restaurant_menu'},
}


ALIASES = {
    'product_name': 'product', 'item_name': 'item', 'customer_name': 'customer', 'consumer_name': 'consumer',
    'purchase_quantity': 'quantity', 'purchase_date': 'date', 'order_date': 'date', 'order_time': 'time',
    'lat': 'latitude', 'lng': 'longitude', 'long': 'longitude', 'amount_paid': 'amount', 'sale_amount': 'amount',
    'order_status': 'status', 'food_category': 'category',
}


def _key(value: str) -> str:
    key = re.sub(r'[^a-z0-9]+', '_', value.strip().lower()).strip('_')
    return ALIASES.get(key, key)


def _value(value: str) -> Any:
    value = value.strip()
    if not value:
        return None
    try:
        return float(value) if '.' in value else int(value)
    except ValueError:
        return value


def import_csv(content: bytes, business_type: str, dataset: str, user_id: str) -> dict[str, Any]:
    collection = DATASETS.get(business_type, {}).get(dataset)
    if not collection:
        raise ValueError('Dataset is not supported for this business domain')
    try:
        text = content.decode('utf-8-sig')
        rows = csv.DictReader(io.StringIO(text))
        if not rows.fieldnames:
            raise ValueError('CSV must include a header row')
        records = []
        for row in rows:
            record = {_key(key): _value(value or '') for key, value in row.items() if key}
            record = {key: value for key, value in record.items() if value is not None}
            if not record:
                continue
            record.update({'userId': user_id, 'businessType': business_type, 'createdAt': datetime.now(timezone.utc).isoformat(), 'imported': True})
            records.append(record)
    except UnicodeDecodeError as exc:
        raise ValueError('CSV must be UTF-8 encoded') from exc
    if not records:
        raise ValueError('CSV contains no data rows')
    write_domain_records(collection, records)
    return {'dataset': dataset, 'collection': collection, 'count': len(records), 'records': records[:10]}