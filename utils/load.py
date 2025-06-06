import json
import pandas as pd
from typing import List, Dict

def load_jsonl(path: str) -> List[Dict]:
    """
    JSONLファイルを読み込み、各行を辞書として返す。
    """
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]

def flatten(dataset: List[Dict]) -> pd.DataFrame:
    """
    入れ子構造のデータセットを評価者ごとのDataFrameに変換する。
    """
    rows = []
    for entry in dataset:
        for ann in entry["annotations"]:
            row = {
                "original_id": entry["original_id"],
                "simplified_id": entry["simplified_id"],
                "model_name": entry["model_name"],
                "original_text": entry["original_text"],
                "simplified_text": entry["simplified_text"],
                "evaluator_id": ann["evaluator_id"],
                "data_source": ann["data_source"],
                "necessity": ann["criterion_scores"]["necessity"],
                "sufficiency": ann["criterion_scores"]["sufficiency"],
                "sentence_simplicity": ann["criterion_scores"]["sentence_simplicity"],
                "document_simplicity": ann["criterion_scores"]["document_simplicity"],
            }
            rows.append(row)
    return pd.DataFrame(rows)

