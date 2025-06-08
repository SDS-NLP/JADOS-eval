import json
from collections import defaultdict
import os

# 入力ファイルと出力ファイル
INPUT_PATH = "data/dataset.jsonl"
OUTPUT_PATH = "data/nested_dataset.jsonl"

# original_id ごとにまとめる辞書
grouped_data = defaultdict(lambda: {"original_text": "", "simplified_list": []})

# ファイル読み込み
with open(INPUT_PATH, "r", encoding="utf-8") as f:
    for line in f:
        entry = json.loads(line)

        original_id = entry["original_id"]
        simplified_item = {
            "simplified_id": entry["simplified_id"],
            "model_name": entry["model_name"],
            "simplified_text": entry["simplified_text"],
            "annotations": []
        }

        # evaluator_id 昇順で annotations を並び替え・整形
        annotations = entry.get("annotations", [])
        sorted_anns = sorted(annotations, key=lambda x: x["evaluator_id"])

        for ann in sorted_anns:
            simplified_item["annotations"].append({
                "evaluator_id": ann["evaluator_id"],
                "scores": ann["criterion_scores"]
            })

        # original_text は代表の一つでOK（全て同じと仮定）
        grouped = grouped_data[original_id]
        grouped["original_text"] = entry["original_text"]
        grouped["simplified_list"].append(simplified_item)

# 保存先ディレクトリの作成
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

# JSONLとして保存
with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    for original_id, data in grouped_data.items():
        json.dump({
            "original_id": original_id,
            "original_text": data["original_text"],
            "simplified_list": data["simplified_list"]
        }, f, ensure_ascii=False)
        f.write("\n")

print(f"✅ Converted to nested format and saved to {OUTPUT_PATH}")
