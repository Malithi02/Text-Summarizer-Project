from pathlib import Path
import torch
import pandas as pd
from tqdm import tqdm
from datasets import load_from_disk
import evaluate
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from textSummarizer.entity import ModelEvaluationConfig

class ModelEvaluation:
    def __init__(self, config):
        self.config = config

    def generate_batch_sized_chunks(self, list_of_elements, batch_size):
        for i in range(0, len(list_of_elements), batch_size):
            yield list_of_elements[i:i + batch_size]

    def calculate_metric_on_test_ds(
        self,
        dataset,
        metric,
        model,
        tokenizer,
        batch_size=16,
        device=None,
        column_text="dialogue",
        column_summary="summary"
    ):
        if device is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"

        article_batches = list(
            self.generate_batch_sized_chunks(dataset[column_text], batch_size)
        )
        target_batches = list(
            self.generate_batch_sized_chunks(dataset[column_summary], batch_size)
        )

        for article_batch, target_batch in tqdm(
            zip(article_batches, target_batches),
            total=len(target_batches)
        ):
            inputs = tokenizer(
                article_batch,
                max_length=1024,
                truncation=True,
                padding="max_length",
                return_tensors="pt"
            )

            summaries = model.generate(
                input_ids=inputs["input_ids"].to(device),
                attention_mask=inputs["attention_mask"].to(device),
                max_length=128,
                num_beams=8,
                length_penalty=0.8
            )

            decoded_summaries = [
                tokenizer.decode(s, skip_special_tokens=True)
                for s in summaries
            ]

            metric.add_batch(
                predictions=decoded_summaries,
                references=target_batch
            )

        return metric.compute()

    def evaluate(self):
        device = "cuda" if torch.cuda.is_available() else "cpu"

        tokenizer = AutoTokenizer.from_pretrained(
            Path(self.config.tokenizer_path),
            local_files_only=True
        )

        model = AutoModelForSeq2SeqLM.from_pretrained(
            Path(self.config.model_path),
            local_files_only=True
        ).to(device)

        dataset = load_from_disk(Path(self.config.data_path))

        rouge_metric = evaluate.load("rouge")

        score = self.calculate_metric_on_test_ds(
            dataset["test"][:10],
            rouge_metric,
            model,
            tokenizer,
            batch_size=2
        )

        rouge_dict = {
            k: score[k] for k in ["rouge1", "rouge2", "rougeL", "rougeLsum"]
        }

        pd.DataFrame(rouge_dict, index=["pegasus"]).to_csv(
            self.config.metric_file_name,
            index=False
        )
