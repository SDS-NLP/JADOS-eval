# 文書レベルの日本語平易化の評価データセット
このリポジトリは、日本語文の平易化に関するデータセットを提供します。  
各データは、wikipediaの記事、言語モデルによって生成された平易化文章、および複数人のによる4つの評価観点アノテーションを含んでいます。

---

## 📁 データセット構造

データは `JSONL` 形式で提供され、各行が1つの元文×1モデルの平易化出力に対応します。


各行は次のような構造です：

```json
{
  "original_id": 1,
  "simplified_id": 6,
  "model_name": "JADOS_target",
  "original_text": "...",
  "simplified_text": "...",
  "annotations": [
    {
      "evaluator_id": 5,
      "data_source": "./data_1",
      "criterion_scores": {
        "necessity": 1,
        "sufficiency": 2,
        "sentence_simplicity": 1,
        "document_simplicity": 3
      }
    },
    ...
  ]
}
