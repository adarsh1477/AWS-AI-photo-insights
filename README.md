# 📸 AWS-AI-photo-insights

An AI-powered photo search & upload system built with AWS Lambda, S3, Lex, Rekognition, and OpenSearch.

## 🧠 Features

- 🔍 **Search photos by label** (e.g., "cat", "sunset")
- 🧾 **Custom labels** on upload, stored as S3 metadata
- 🧠 **AWS Rekognition** detects image content automatically
- 📦 **Indexing with OpenSearch** for fast querying
- 🎯 **Lex chatbot** extracts key search terms
- ⚡️ **Deployed using AWS Lambda & CodePipeline**

---

## 📁 Project Structure
AWS-AI-photo-insights/ │ ├── Lambda Functions/ │ ├── index-photos/ # Lambda: Indexes photo labels into OpenSearch │ └── search-photos/ # Lambda: Processes search queries using Lex & OpenSearch │ ├── Frontend/ │ └── index.html # Static UI for uploading and searching photos


---

## 🚀 Architecture

- S3 triggers Lambda `index-photos` on upload
- `index-photos`:
  - Uses Rekognition to detect labels
  - Adds custom labels (from metadata)
  - Sends data to OpenSearch
- `search-photos` Lambda (via API Gateway) uses:
  - Lex for keyword extraction
  - OpenSearch to retrieve matching photos
- Frontend interacts with API Gateway endpoints for uploading and searching

---

## ✅ Setup Checklist

- [x] S3 Bucket with public access
- [x] Rekognition permissions
- [x] Lex bot and alias for keyword extraction
- [x] OpenSearch domain and index
- [x] Lambda functions with appropriate IAM roles
- [x] Static frontend hosted on S3
- [x] CodePipeline setup for CI/CD

---

## 🔧 To Do

- [ ] Add CodePipeline configuration (Step 6)
- [ ] Include `buildspec.yml` for Lambda CI
- [ ] Include `pipeline.yml` for frontend deployment

---

## 👨‍💻 Contributors

- **Adarsh Rai** – Frontend, Lambda Integration, Deployment  
- **Divyansh Agrawal ** – Lex, OpenSearch, API Gateway

---

## 📜 License

This project is part of a university assignment for Cloud Computing & Big Data Systems.
