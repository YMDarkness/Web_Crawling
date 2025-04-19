import pandas as pd
import torch
from torch.utils.data import Dataset
from sklearn.model_selection import train_test_split
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from sklearn.metrics import accuracy_score, classification_report

# csv 파일 로드
df = pd.read_csv("2025-02-21_news_report.csv")

# csv 파일 칼럼 확인
print(f"csv 파일 칼럼 확인: ", df.columns.tolist())

print(f"총 데이터 개수: {len(df)}")
print(df['keyword'].value_counts())  # 각 카테고리별 데이터 개수 확인

# 라벨 변환
df['label'] = df['keyword'].astype("category").cat.codes
print(df[['keyword', 'label']].head())

# 입력 데이터와 출력 데이터 설정
x = df['title']
y = df['label']

# 데이터 분할 (train : test = 8 : 2)
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# BERT 토크나이저 로드
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

# 데이터셋 전처리
class NewsDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_len=128):
        self.texts = texts.tolist()
        self.labels = labels.tolist()
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.texts)
    
    def __getitem__(self, idx):
        encoding = self.tokenizer(
            self.texts[idx],
            max_length=self.max_len,
            padding="max_length",
            truncation=True,
            return_tensors="pt"  #오타 수정 (return_tensor → return_tensors)
        )
        return {
            "input_ids": encoding["input_ids"].squeeze(),
            "attention_mask": encoding["attention_mask"].squeeze(),
            "labels": torch.tensor(self.labels[idx], dtype=torch.long)
        }

# 훈련 및 테스트 데이터셋 생성
train_dataset = NewsDataset(x_train, y_train, tokenizer)
test_dataset = NewsDataset(x_test, y_test, tokenizer)

# BERT 모델 로드
model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=len(df['label'].unique()))

# 학습 설정
'''training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,  #불필요한 `per_gpu_eval_batch_size` 제거
    num_train_epochs=10,
    save_steps=10_000,
    save_total_limit=2,
    logging_dir="./logs"
)'''

#모델 성능 개선
training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    per_device_train_batch_size=16,  #batch size 증가
    per_device_eval_batch_size=16,
    num_train_epochs=10,  #학습 횟수 증가
    learning_rate=2e-5,  #적절한 learning rate 조정
    save_steps=10_000,
    save_total_limit=2,
    logging_dir="./logs"
)


# Trainer 설정
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset
)

# 학습 실행
trainer.train()

#테스트 데이터셋 예측
predictions = trainer.predict(test_dataset)
preds = torch.argmax(torch.tensor(predictions.predictions), dim=1)

#정확도 및 성능 출력
accuracy = accuracy_score(y_test, preds)
print(f"\n 모델 정확도 : {accuracy : .4f}")

#상세 성능 보고서
print(f"\n분류 보고서\n", classification_report(y_test, preds))
