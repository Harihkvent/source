
# Practical Career Navigator — Project Document
**Beginner-friendly, layout-aware resume parser + explainable job recommender and roadmap generator**

---

## Overview (Executive Summary)
This project builds a reproducible, beginner-friendly system that:
- Robustly extracts structured profiles from heterogeneous resume files (PDF, DOCX, image) using OCR + layout grouping + spaCy NER and rules.
- Performs accurate job recommendations using a two-stage pipeline: fast recall (TF-IDF or SBERT) + a lightweight, explainable re-ranker (Logistic Regression / RandomForest).
- Generates prioritized, time-bound skill-gap roadmaps with resource links and simple, transparent scoring.
- Avoids graph databases and heavy ML; designed for undergraduates and small teams.

---

## Contents
1. Project conception & justification  
2. System design & minimal architecture  
3. Technology stack & implementation plan (step-by-step)  
4. Datasets (download links)  
5. Key recent research (2019–2024) — papers with links (Google Scholar / publisher pages)  
6. Experimental plan & evaluation metrics  
7. Deliverables, timeline, and reproducibility checklist  
8. Appendix: code snippets, annotation schema, labeling guide, sample resources

---

## 1. Project Conception & Justification

**Problem statement.** Early-career candidates and placement cells need accurate resume parsing and high-quality, explainable job recommendations. Existing SOTA often requires heavy compute, layout models, or specialized graph databases. This project demonstrates a practical, high-value pipeline that is beginner-friendly and reproducible.

**Primary objective.** Implement and evaluate a full pipeline (ingestion → parsing → matching → roadmap) that runs on modest hardware and uses simple, explainable ML.

**Novelty.** The contribution is practical: showing how robust performance and real user value can be achieved with an accessible stack (Tesseract + spaCy + TF-IDF/SBERT + scikit-learn reranker), plus a reproducible evaluation and a small user study.

---

## 2. System Design & Minimal Architecture

**Architecture:** Monolithic FastAPI backend + Streamlit frontend (optional React). No microservices. No graph DB. PostgreSQL (or SQLite) for storage. Optional vector/search index via Annoy/FAISS or scikit-learn NearestNeighbors.

**Components:**
- Frontend (Streamlit or React)
- API (FastAPI) + Auth (JWT)
- Resume ingestion (pdf2image + pytesseract)
- Layout grouping (simple y-axis clustering)
- Parsing (spaCy + PhraseMatcher + regex rules)
- Skill-normalizer (JSON taxonomy + RapidFuzz + embedding fallback)
- Job index (TF-IDF or SBERT)
- Re-ranker (scikit-learn LogisticRegression/RandomForest)
- Roadmap generator (impact score + curated resources)
- DB: PostgreSQL / SQLite for profiles, jobs, taxonomy, logs

**Data Flow (textual):**
Upload → OCR → Block grouping → spaCy parsing → normalize skills → store profile → retrieve jobs (TF-IDF/SBERT + NearestNeighbors) → feature extraction → re-rank → present results + roadmap → log feedback

---

## 3. Technology Stack & Why

- **FastAPI** (backend): quick, integrates with Python ML stack.
- **Streamlit** (demo frontend): extremely fast for prototypes; use React if you need production polish.
- **Tesseract (pytesseract)**: offline OCR, good baseline for scanned resumes.
- **pdf2image**: convert PDF pages to images for OCR.
- **spaCy**: fast, beginner-friendly NER and rule matchers.
- **SentenceTransformers** (optional): semantic embeddings for better recall (`all-mpnet-base-v2` recommended); fallback to TF-IDF for low-compute setups.
- **scikit-learn**: TF-IDF, NearestNeighbors, LogisticRegression/RandomForest for re-ranking.
- **RapidFuzz / fuzzywuzzy**: fuzzy string match for skill normalization.
- **PostgreSQL / SQLite**: store profiles, taxonomy, job corpus (JSON/JSONB).
- **Annoy / FAISS**: optional approximate nearest neighbors.
- **Docker**: optional containerization for reproducibility.

---

## 4. Implementation Plan (concise steps)

**Week 1: Data & setup**
- Collect/prepare resumes (anonymized, n≈500) and job postings (n≈2000). Prepare skill taxonomy (300 common skills).
- Repo: FastAPI + Streamlit skeleton, venv/requirements.

**Week 2: Ingestion & OCR**
- Implement pdf2image + pytesseract ingestion pipeline.
- Implement simple block grouping by vertical proximity.

**Week 3: Parsing**
- Build spaCy pipeline + custom PhraseMatcher patterns for skills & degrees.
- Add regex extractors for email/phone and date normalization.

**Week 4: Normalization & Index**
- Implement RapidFuzz/embedding fallback for skill canonicalization.
- Index job corpus with TF-IDF and NearestNeighbors.

**Week 5: Retrieval & Re-rank**
- Implement retrieval (TF-IDF or SBERT); label ~300 resume–job pairs and train LogisticRegression/RandomForest re-ranker.

**Week 6: Roadmap & Explainability**
- Implement impact-scoring & roadmap mapping; add explanation templates and compute simple feature importances.

**Week 7: Evaluation**
- Evaluate parser (F1), recommender (Precision@5, NDCG@10), and run small user study (n≥20).

**Week 8: Finalize**
- Write report, prepare demo video, produce reproducible artifacts (Dockerfile, README).

---

## 5. Datasets (links & short notes)

> These are beginner-friendly and publicly accessible datasets and corpora you can use. Use them with privacy and license awareness.

1. **Kaggle Resume Dataset (LiveCareer examples)** — general labeled resumes useful for classification/NER seeds.  
   Download: https://www.kaggle.com/datasets/snehaanbhawal/resume-dataset  (Kaggle). citeturn0search4

2. **Kaggle Resume Dataset (another variant)** — https://www.kaggle.com/datasets/gauravduttakiit/resume-dataset. Useful sample resumes and categories. citeturn0search11

3. **HuggingFace 'Resume-Dataset'** — resumes in text form (community dataset).  
   Reference: https://huggingface.co/datasets/InferencePrince555/Resume-Dataset. citeturn0search18

4. **Resume dataset (research) — 'Resume Information Extraction via Post-OCR Text' dataset (286 resumes)** — paper and data referenced on arXiv (useful for parsing experiments).  
   Paper: https://arxiv.org/abs/2306.13775. citeturn0search19

5. **Job posting datasets / scraping** — scrape job boards (LinkedIn, Indeed, Naukri) respecting ToS; for experiments you can use Kaggle job-posting datasets (search Kaggle for 'job postings' or use public datasets). Example: many Kaggle corpora of job postings; search directly on Kaggle. (I recommend scraping with care and observing legal/ethical constraints.)

6. **Document understanding datasets (for layout model transfer learning)**:  
   - **DocBank** — layout and token-level annotations for document understanding. Use for transfer learning if needed. (Search "DocBank dataset").  
   - **RVL-CDIP** — document classification dataset (useful for layout tasks).  
   These are standard in layout/document work.

---

## 6. Key Recent Research (2019–2024) — Papers & Links

Below are selected, relevant papers from the last 4–5 years. Prefer Scopus-indexed journals where available. I include quick notes and links to the publisher/host pages.

1. **LayoutLMv2 — Xu et al. (2021)** — *LayoutLMv2: Multi-modal pre-training for visually-rich document understanding.* (ArXiv / Microsoft research).  
   PDF/notes: https://arxiv.org/abs/2012.15669.  
   Why read: seminal layout-aware transformer—useful background for parsing complex resumes. citeturn0search14

2. **GraphLayoutLM — Li et al. (2023)** — *Enhancing Visually-Rich Document Understanding via GraphLayoutLM.* (ACM conference proceedings).  
   Link: https://dl.acm.org/doi/10.1145/3611380.3628554.  
   Why read: shows how layout graphs improve extraction; relevant for understanding layout methods (we adopt a simpler approach for this project). citeturn0search1turn0search8

3. **A Deep-Learning-Inspired Person–Job Matching Model — Wang et al. (2021)** — *Complexity (Hindawi).*  
   Link: https://www.hindawi.com/journals/complexity/2021/6206288/  
   Why read: demonstrates person–job semantic matching methods combining sentence vectors and graph-like structures; useful for matching design. citeturn0search2

4. **A Study of Reciprocal Job Recommendation for College Graduates — Yao et al. (2023)** — *Applied Sciences (MDPI).*  
   Link: https://www.mdpi.com/2076-3417/13/22/12305  
   Why read: practical methods for graduate job recommendation; MDPI Applied Sciences is Scopus-indexed. citeturn0search3

5. **A Bibliometric Perspective on AI Research for Job–Résumé Matching — Rojas-Galeano et al. (2022)** — *The Scientific World Journal / Hindawi (PMC).*  
   Link: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9550515/  
   Why read: overview of trends and identified gaps (reproducibility, data, layout attention). citeturn0search12

6. **Navigating career stages in the age of artificial intelligence — Bankins et al. (2024)** — *Journal of Vocational Behavior (Elsevier).*  
   Link preview / PDF: https://www.sciencedirect.com/science/article/pii/S0001879124000526  (or research author PDF).  
   Why read: examines ethics, explainability, and user study importance for career systems. citeturn0search6turn0search21

7. **Resume Information Extraction via Post-OCR Text — Helli et al. (2023, arXiv)**  
   Link: https://arxiv.org/abs/2306.13775  
   Why read: practical dataset and methods for resume IE post-OCR; useful for building a baseline parser. citeturn0search19

---

## 7. Experimental Plan & Evaluation Metrics

**Parsing evaluation**
- Entities: NAME, EMAIL, PHONE, DEGREE, UNIVERSITY, SKILL, EXPERIENCE, PROJECT.  
- Metrics: Precision, Recall, F1 (per-entity + micro/macro averages).

**Matching evaluation**
- Collect labeled resume–job pairs (3-level relevance: Good / Maybe / No).  
- Metrics: Precision@5, Recall@10, NDCG@10, MAP.

**Roadmap evaluation**
- User study (n≥20–30): Likert scores for usefulness, clarity, actionability; qualitative feedback.

**Baselines**
- Parser: spaCy only (no layout), vs spaCy+block grouping.  
- Recommender: TF-IDF retrieval (no re-rank) vs TF-IDF + re-ranker.

**Statistical tests**
- Paired t-test or Wilcoxon signed-rank for user study comparisons; significance at p<0.05.

---

## 8. Reproducibility Checklist & Deliverables

**Repo (required)**
- `README.md` (setup & run instructions)  
- `requirements.txt` / `environment.yml`  
- `docker/Dockerfile` (optional)  
- `data/` with sample resumes and job postings (anonymized)  
- `notebooks/` for experiments and evaluation scripts  
- `app/` (FastAPI backend + Streamlit frontend)

**Deliverables**
- Project report (PDF) — methods, experiments, user study.  
- Code repo (GitHub).  
- Demo video (3–5 min).  
- Dataset split and labeling schema (appendix).

---

## Appendix A — Annotation schema (brief)
- Entities (BIO): NAME, EMAIL, PHONE, ADDRESS, DEGREE, COLLEGE, START_DATE, END_DATE, COMPANY, ROLE, SKILL, PROJECT, DESCRIPTION.  
- Labeling guide: annotate exact spans for NAME, SKILL, DEGREE; for EXPERIENCE annotate role + company + dates; for EDUCATION annotate degree + institution + year.

---

## Appendix B — Useful code snippets

**Tesseract OCR + pdf2image**
```python
from pdf2image import convert_from_path
import pytesseract

pages = convert_from_path('resume.pdf', dpi=300)
for i,page in enumerate(pages):
    text = pytesseract.image_to_string(page)
    data = pytesseract.image_to_data(page, output_type=pytesseract.Output.DICT)
```

**spaCy skill matching**
```python
import spacy
from spacy.matcher import PhraseMatcher

nlp = spacy.load("en_core_web_sm")
skills = ["python", "sql", "docker"]
matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
patterns = [nlp.make_doc(s) for s in skills]
matcher.add("SKILLS", patterns)
doc = nlp("Experience with Python and Docker")
matches = matcher(doc)
```

**TF-IDF + NearestNeighbors**
```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

vectorizer = TfidfVectorizer(ngram_range=(1,2), max_features=5000)
job_vecs = vectorizer.fit_transform(job_texts)
nn = NearestNeighbors(n_neighbors=50, metric='cosine').fit(job_vecs)

profile_vec = vectorizer.transform([profile_text])
distances, indices = nn.kneighbors(profile_vec)
```

---

## Appendix C — Links in one place (papers and datasets)

### Papers
- LayoutLMv2 (Xu et al., 2021): https://arxiv.org/abs/2012.15669. citeturn0search14  
- GraphLayoutLM (ACM, 2023): https://dl.acm.org/doi/10.1145/3611380.3628554. citeturn0search1  
- Person-Job Matching (Wang et al., 2021): https://www.hindawi.com/journals/complexity/2021/6206288/. citeturn0search2  
- Reciprocal Job Recommendation (Yao et al., 2023): https://www.mdpi.com/2076-3417/13/22/12305. citeturn0search3  
- Bibliometric Perspective (Rojas-Galeano et al., 2022): https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9550515/. citeturn0search12  
- Career stages review (Bankins et al., 2024): https://www.sciencedirect.com/science/article/pii/S0001879124000526. citeturn0search6  
- Resume IE post-OCR (Helli et al., 2023): https://arxiv.org/abs/2306.13775. citeturn0search19

### Datasets
- Kaggle Resume Dataset (LiveCareer): https://www.kaggle.com/datasets/snehaanbhawal/resume-dataset. citeturn0search4  
- Kaggle Resume Dataset (variant): https://www.kaggle.com/datasets/gauravduttakiit/resume-dataset. citeturn0search11  
- HuggingFace Resume Dataset: https://huggingface.co/datasets/InferencePrince555/Resume-Dataset. citeturn0search18  
- Resume IE paper / dataset: https://arxiv.org/abs/2306.13775. citeturn0search19

---

## Final notes & next steps
- I prepared this document as a comprehensive, reproducible plan that a beginner can follow. If you want, I will:
  - Convert this into a downloadable PDF and provide the link.  
  - Create the GitHub repo skeleton and sample code.  
  - Generate the annotation schema file and 100 synthetic annotated resume examples to seed labeling.

Tell me which of the three (PDF, repo skeleton, synthetic annotations) you want **now** — I'll generate it immediately and provide the download link.
