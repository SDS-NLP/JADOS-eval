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
    ネスト構造（original_textごとにsimplified_listを持つ形式）を、
    評価者ごとに展開したpandas DataFrameに変換する。
    """
    rows = []
    for entry in dataset:
        original_id = entry["original_id"]
        original_text = entry["original_text"]

        for sim in entry["simplified_list"]:
            simplified_id = sim["simplified_id"]
            model_name = sim["model_name"]
            simplified_text = sim["simplified_text"]

            # 評価者順で整列（保証されていない場合に備えて）
            sorted_annotations = sorted(sim.get("annotations", []), key=lambda x: x["evaluator_id"])

            for ann in sorted_annotations:
                scores = ann["scores"]
                row = {
                    "original_id": original_id,
                    "simplified_id": simplified_id,
                    "model_name": model_name,
                    "original_text": original_text,
                    "simplified_text": simplified_text,
                    "evaluator_id": ann["evaluator_id"],
                    "necessity": scores.get("necessity"),
                    "sufficiency": scores.get("sufficiency"),
                    "sentence_simplicity": scores.get("sentence_simplicity"),
                    "document_simplicity": scores.get("document_simplicity")
                }
                rows.append(row)

    return pd.DataFrame(rows)
