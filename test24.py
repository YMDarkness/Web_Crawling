import pandas as pd
import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration, BartForConditionalGeneration, BartTokenizer

# CSV 파일 불러오기
df = pd.read_csv("2025-02-18_news_report.csv")

# 뉴스 본문이 있으면 본문 사용, 없으면 제목 사용
df['keyword'] = df.get('category', df['title']).fillna(df['title'])
df = df[['title', 'keyword']].dropna()
#category(카테고리)가 있으면 사용하고, 없으면 title(제목)을 사용
#필요한 컬럼(title, keyword)만 남기고 결측값(NA) 제거

# 뉴스 본문을 하나의 텍스트로 변환
news_text = " ".join(df['keyword'].tolist())
#전체 뉴스의 keyword 값을 하나의 문자열로 결합

# 텍스트 분할 함수
def split_text(text, chunk_size=150):
    words = text.split()
    return [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

chunks = split_text(news_text)

print(f"뉴스 개수 : {len(df)}\n분할된 뉴스 개수 : {len(chunks)}\n")
print(f"첫 번째 뉴스\n{chunks[0] if chunks else '없음'}\n")

print(f"[합쳐진 전체 뉴스 텍스트(500자)]\n{news_text[:500]}\n")
print(f"[분할된 텍스트 개수] {len(chunks)}\n")
print(f"[첫 번째 분할 텍스트]\n{chunks[:3]}\n")

# 모델 로드 및 GPU 설정
device = "cuda" if torch.cuda.is_available() else "cpu"

t5_model = T5ForConditionalGeneration.from_pretrained("t5-base").to(device)
t5_tokenizer = T5Tokenizer.from_pretrained("t5-base", legacy=False)

bart_model = BartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn").to(device)
bart_tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")
#T5와 BART 요약 모델을 불러오고 GPU(cuda) 또는 CPU에서 실행할 수 있도록 설정

# 요약 함수
def summarize(text, model, tokenizer, max_length=100):
    input_ids = tokenizer.encode(text.strip(), return_tensors="pt", truncation=True, max_length=512).to(device)
    summary_ids = model.generate(input_ids, max_length=max_length, min_length=30, num_beams=5)
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True).strip()
#입력된 뉴스 텍스트를 요약하여 반환하는 함수
#max_length=100 → 요약된 텍스트의 최대 길이 설정
#num_beams=5 → 빔 서치 기법을 사용해 요약 품질을 향상

# 뉴스 요약 실행
t5_summaries = [summarize(chunk, t5_model, t5_tokenizer) for chunk in chunks]
bart_summaries = [summarize(chunk, bart_model, bart_tokenizer) for chunk in chunks]

print(f"뉴스 개수: {len(df)}\nT5 요약 개수: {len(t5_summaries)}\n")

if len(t5_summaries) < len(df):
    missing_count = len(df) - len(t5_summaries)
    t5_summaries.extend([""] * missing_count)  # 부족한 부분을 빈 문자열로 채움
df["T5_summary"] = t5_summaries

# T5 요약 결과 개수 맞추기
if len(t5_summaries) < len(df):
    missing_count = len(df) - len(t5_summaries)
    t5_summaries.extend([""] * missing_count)
df["T5_summary"] = t5_summaries

# BART 요약 결과 개수 맞추기
if len(bart_summaries) < len(df):
    missing_count = len(df) - len(bart_summaries)
    bart_summaries.extend([""] * missing_count)
df["BART_summary"] = bart_summaries

df["T5_summary"] = t5_summaries[:len(df)]
df["BART_summary"] = bart_summaries[:len(df)]
#뉴스 데이터 개수(len(df))와 요약 개수를 맞추기 위해 부족한 부분은 빈 문자열("")로 채움

# 요약 결과 저장
df.to_csv("2025-02-18_news_summary.csv", index=False, encoding='utf-8-sig')
print("요약 완료 결과가 저장되었습니다.")
import pandas as pd
import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration, BartForConditionalGeneration, BartTokenizer

# CSV 파일 불러오기
df = pd.read_csv("2025-02-18_news_report.csv")

# 뉴스 본문이 있으면 본문 사용, 없으면 제목 사용
df['keyword'] = df.get('category', df['title']).fillna(df['title'])
df = df[['title', 'keyword']].dropna()
#category(카테고리)가 있으면 사용하고, 없으면 title(제목)을 사용
#필요한 컬럼(title, keyword)만 남기고 결측값(NA) 제거

# 뉴스 본문을 하나의 텍스트로 변환
news_text = " ".join(df['keyword'].tolist())
#전체 뉴스의 keyword 값을 하나의 문자열로 결합

# 텍스트 분할 함수
def split_text(text, chunk_size=150):
    words = text.split()
    return [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

chunks = split_text(news_text)

print(f"뉴스 개수 : {len(df)}\n분할된 뉴스 개수 : {len(chunks)}\n")
print(f"첫 번째 뉴스\n{chunks[0] if chunks else '없음'}\n")

print(f"[합쳐진 전체 뉴스 텍스트(500자)]\n{news_text[:500]}\n")
print(f"[분할된 텍스트 개수] {len(chunks)}\n")
print(f"[첫 번째 분할 텍스트]\n{chunks[:3]}\n")

# 모델 로드 및 GPU 설정
device = "cuda" if torch.cuda.is_available() else "cpu"

t5_model = T5ForConditionalGeneration.from_pretrained("t5-base").to(device)
t5_tokenizer = T5Tokenizer.from_pretrained("t5-base", legacy=False)

bart_model = BartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn").to(device)
bart_tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")
#T5와 BART 요약 모델을 불러오고 GPU(cuda) 또는 CPU에서 실행할 수 있도록 설정

# 요약 함수
def summarize(text, model, tokenizer, max_length=100):
    input_ids = tokenizer.encode(text.strip(), return_tensors="pt", truncation=True, max_length=512).to(device)
    summary_ids = model.generate(input_ids, max_length=max_length, min_length=30, num_beams=5)
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True).strip()
#입력된 뉴스 텍스트를 요약하여 반환하는 함수
#max_length=100 → 요약된 텍스트의 최대 길이 설정
#num_beams=5 → 빔 서치 기법을 사용해 요약 품질을 향상

# 뉴스 요약 실행
t5_summaries = [summarize(chunk, t5_model, t5_tokenizer) for chunk in chunks]
bart_summaries = [summarize(chunk, bart_model, bart_tokenizer) for chunk in chunks]

print(f"뉴스 개수: {len(df)}\nT5 요약 개수: {len(t5_summaries)}\n")

if len(t5_summaries) < len(df):
    missing_count = len(df) - len(t5_summaries)
    t5_summaries.extend([""] * missing_count)  # 부족한 부분을 빈 문자열로 채움
df["T5_summary"] = t5_summaries

# T5 요약 결과 개수 맞추기
if len(t5_summaries) < len(df):
    missing_count = len(df) - len(t5_summaries)
    t5_summaries.extend([""] * missing_count)
df["T5_summary"] = t5_summaries

# BART 요약 결과 개수 맞추기
if len(bart_summaries) < len(df):
    missing_count = len(df) - len(bart_summaries)
    bart_summaries.extend([""] * missing_count)
df["BART_summary"] = bart_summaries

df["T5_summary"] = t5_summaries[:len(df)]
df["BART_summary"] = bart_summaries[:len(df)]
#뉴스 데이터 개수(len(df))와 요약 개수를 맞추기 위해 부족한 부분은 빈 문자열("")로 채움

# 요약 결과 저장
df.to_csv("2025-02-18_news_summary.csv", index=False, encoding='utf-8-sig')
print("요약 완료 결과가 저장되었습니다.")
