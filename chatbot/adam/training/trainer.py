import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer, Trainer, TrainingArguments
from typing import List, Dict


class ChatbotT5:
    def __init__(self, model_path: str = None):
        self.tokenizer = T5Tokenizer.from_pretrained('t5-base')
        if model_path is None:
            self.model = T5ForConditionalGeneration.from_pretrained('t5-base')
        else:
            self.model = T5ForConditionalGeneration.from_pretrained(model_path)

    def prepare_data(self, dataset: List[Dict[str, str]], max_length: int = 128):
        input_texts = [d['question'] for d in dataset]
        output_texts = [d['response'] for d in dataset]

        inputs = self.tokenizer.batch_encode_plus(
            input_texts,
            padding=True,
            max_length=max_length,
            truncation=True,
            return_tensors='pt'
        )

        outputs = self.tokenizer.batch_encode_plus(
            output_texts,
            padding=True,
            max_length=max_length,
            truncation=True,
            return_tensors='pt'
        )

        input_ids = inputs['input_ids']
        input_attention_mask = inputs['attention_mask']
        output_ids = outputs['input_ids']
        output_attention_mask = outputs['attention_mask']

        data = []
        for i in range(len(dataset)):
            data.append({
                'input_ids': input_ids[i],
                'attention_mask': input_attention_mask[i],
                'labels': output_ids[i],
                'decoder_attention_mask': output_attention_mask[i],
            })

        return data

    def fine_tune(self, train_dataset, eval_dataset, model_dir: str = 'model',
                  num_train_epochs: int = 30, batch_size: int = 8):
        training_args = TrainingArguments(
            output_dir=model_dir,
            num_train_epochs=num_train_epochs,
            per_device_train_batch_size=batch_size,
            per_device_eval_batch_size=batch_size,
            logging_dir=model_dir+'/logs',
            logging_steps=10,
            evaluation_strategy='epoch',
            save_strategy='epoch',
            save_total_limit=3,
            eval_steps=10,
            load_best_model_at_end=True,
        )

        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=eval_dataset
        )

        trainer.train()

        self.model.save_pretrained(model_dir)

    def generate_response(self, input_text: str, max_length: int = 4016):
        input_ids = self.tokenizer.encode(
            input_text,
            padding=True,
            max_length=max_length,
            truncation=True,
            return_tensors='pt'
        )

        output_ids = self.model.generate(
            input_ids=input_ids,
            max_length=max_length,
            num_beams=4,
            early_stopping=True,
            do_sample=True,
            top_k=50,
            top_p=0.95,
            temperature=0.7,
        )

        response = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)

        return response