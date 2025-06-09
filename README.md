# 文書レベルの日本語平易化の評価データセット
このリポジトリでは、文章レベルの日本語平易化の評価に関するデータセットを配布しています。既存の日本語平易化コーパスである[JADOS](https://github.com/tmu-nlp/JADOS)データセットのwikipediaドメインのデータの一部をモデルによる平易化文章によって拡張し、それらに人手によるアノテーションを行いました。

各データは、wikipediaの記事、言語モデルによって生成された平易化文章、および複数人のによる4つの評価観点アノテーションを含んでいます。
データセットの詳細については[JADOS](https://github.com/tmu-nlp/JADOS)データセットの構築に関する[論文](https://aclanthology.org/2024.lrec-main.41.pdf)とアノテーションに関する[資料](https://docs.google.com/presentation/d/1llsXZbOz4raAwOb3BtbNLVp3mVEKCB9Y887OHM2u5SA/edit#slide=id.p)を参照してください。

---

## データ構造

データは `JSONL` 形式で提供され、各行が1つのソース文章に対応しています。  
その中で、各ソース文章には複数の平易化文（simplified_text）が `simplified_list` に辞書のリストにまとめられており、  
各平易化文には複数のアノテーターによる評価スコアが `annotations` に辞書のリストとしてまとめられています。

各行は以下のような入れ子構造になっています（一部抜粋）：

```json
{
  "original_id": 1,
  "original_text": "北越急行ほくほく線...",
  "simplified_list": [
    {
      "simplified_id": 1,
      "model_name": "bart",
      "simplified_text": "新潟県南魚沼市の六日町駅から...",
      "annotations": [
        {
          "evaluator_id": 1,
          "scores": {
            "necessity": 1,
            "sufficiency": 2,
            "sentence_simplicity": 2,
            "document_simplicity": 3
          }
        },
        ...
      ]
    },
    {
      "simplified_id": 2,
      "model_name": "gemma",
      "simplified_text": "ほくほく線は、新潟県の六日町駅から犀潟駅までを結ぶ電車の路線です。...",
      "annotations": [
        {
          "evaluator_id": 1,
          "scores": {
            "necessity": 1,
            "sufficiency": 3,
            "sentence_simplicity": 3,
            "document_simplicity": 3
          }
        },
        ...
      ]
    }
  ]
}
```

### データの詳細

| フィールド名 | 階層 | 型 | 説明 |
|--------------|------|----|------|
| `original_id` | top-level | int | 元の複雑な文章のID |
| `original_text` | top-level | str | wikipediaから抽出した平易化の対象となる文章 |
| `simplified_list` | top-level | list | 平易化された文章のリスト。各要素が1つのモデルによる出力に対応 |

#### simplified_list の要素

| フィールド名 | 階層 | 型 | 説明 |
|--------------|------|----|------|
| `simplified_id` | simplified_list[i] | int | モデル別に一意に定められたid|
| `model_name` | simplified_list[i] | str | 生成元モデルの名称（例："gemma", "GPT-4o_0-shot"） |
| `simplified_text` | simplified_list[i] | str | 平易化された文章 |
| `annotations` | simplified_list[i] | list | 各アノテーターによる評価のリスト |

#### annotations の要素

| フィールド名 | 階層 | 型 | 説明 |
|--------------|------|----|------|
| `evaluator_id` | annotations[j] | int | 評価者のID |
| `scores` | annotations[j] | dict | 各評価観点のスコア（0〜3の整数） |

##### scores の要素

| フィールド名 | 階層 | 型 | 説明 |
|--------------|------|----|------|
| `necessity` | scores | bool | 物事を説明する文章として体裁を保っているかどうか |
| `sufficiency` | scores | int | (1-3)元の文章の趣旨を保持しているか|
| `sentence_simplicity` | scores | int | (1-3)文単位での読みやすさ・単純さ |
| `document_simplicity` | scores | int | (1-3)文章全体としての平易さ |


##### model_name が表すモデルの詳細
| モデル名 | リンク | 説明 |
|--------------|------|------|
| bart| [link](https://huggingface.co/ku-nlp/bart-large-japanese) | `ku-nlp/bart-large-japanese`をJADOSデータセットのtrainデータで訓練したモデル |
| gemma  | [link](https://huggingface.co/google/gemma-2-9b-it) | `google/gemma-2-9b-itを利用` |
| GPT-4o_0-shot| [link](https://platform.openai.com/docs/models/gpt-4o) | `gpt-4o-2024-11-20`を利用．平易化の例を1件与えた1-shotの設定における生成結果|
| GPT-4o_1-shot | [link](https://platform.openai.com/docs/models/gpt-4o) | `gpt-4o-2024-11-20`を利用 |
| Llama-swallow | [link](https://huggingface.co/tokyotech-llm/Llama-3.1-Swallow-8B-Instruct-v0.2) | `tokyotech-llm/Llama-3.1-Swallow-8B-Instruct-v0.2`を利用 |
| JADOS_target  | [link](https://github.com/tmu-nlp/JADOS) | 拡張元のデータセットであるJADOSにおける人手で作成した平易化文章 |



##### LLMによる平易化に用いたプロンプト

```
次の記事を小学生が理解しやすい記事に変換してください。150字程度の短い記事になるように要約し、難しい表現は簡単な表現に言い換えたり補足の説明をしたりしてください。\n{original_text}
```