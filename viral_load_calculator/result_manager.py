import csv
import datetime
from pathlib import Path
import uuid

from viral_load_calculator.config import get_user_data_dir_or_file


def _default_result_path(path: str | None = None) -> Path:
    if path is None:
        return Path(get_user_data_dir_or_file(f"{datetime.date.today().isoformat()}.csv"))

    result_path = Path(path)
    if result_path.is_dir():
        result_path = result_path / f"{datetime.date.today().isoformat()}.csv"
    return result_path

def record_result(value: float, iu_ml: float, log: float,
                  result_type: str,
                  results: list
                ) -> dict:
    result = {
        'id': uuid.uuid4(),
        'value': value,
        'iu/ml': iu_ml,
        'log': log,
        'result_type': result_type,
        'created_at': datetime.datetime.now().strftime('%d/%m/%Y, %H:%M:%S'),
    }
    results.append(result)
    return result

def fetch_result(id: str, results: list) -> dict:
    for result in results:
        if id == result['id']:
            return result

    return {'error': 'Result Not Found'}

def save_result_file(results: list[dict], path: str | None = None) -> None:
    output_path = _default_result_path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    columns = ['id', 'value', 'iu/ml', 'log', 'result_type', 'created_at']
    with output_path.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        for result in results:
            writer.writerow({
                'id': str(result['id']),
                'value': result['value'],
                'iu/ml': result['iu/ml'],
                'log': result['log'],
                'result_type': result['result_type'],
                'created_at': result['created_at'],
            })
        
def fetch_result_file(path: str | None = None) -> list[dict]:
    input_path = _default_result_path(path)
    result_list = []

    if not input_path.exists():
        return result_list

    with input_path.open('r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            result_list.append({
                'id': row.get('id', ''),
                'value': float(row.get('value', 0)) if row.get('value') else 0.0,
                'iu/ml': float(row.get('iu/ml', 0)) if row.get('iu/ml') else 0.0,
                'log': float(row.get('log', 0)) if row.get('log') else 0.0,
                'result_type': row.get('result_type', ''),
                'created_at': row.get('created_at', ''),
            })
    return result_list

def export_result_file():
    """This function is a utility function to export the stored file to other formats other than csv"""
    raise NotImplementedError('The Export function has not been implemented yet')