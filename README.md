# 📸 AWS-AI-photo-insights

## 🎥 Demo

[![Watch the demo](https://img.youtube.com/vi/CtGnK63FB4s/maxresdefault.jpg)](https://youtu.be/CtGnK63FB4s)

An AI-powered photo search & upload system built with AWS Lambda, S3, Lex, Rekognition, and OpenSearch.

## 🧠 Features

- 🔍 **Search photos by label** (e.g., "cat", "sunset")
- 🧾 **Custom labels** on upload, stored as S3 metadata
- 🧠 **AWS Rekognition** detects image content automatically
- 📦 **Indexing with OpenSearch** for fast querying
- 🎯 **Lex chatbot** extracts key search terms
- ⚡️ **Deployed using AWS Lambda & CodePipeline**

---

AWS-AI-photo-insights/
│
├── Lambda Functions/
│   ├── index-photos/           # Lambda function: Indexes photo labels into OpenSearch
│   └── search-photos/          # Lambda function: Processes search queries using Lex & OpenSearch
│
├── Frontend/
│   └── index.html              # Static frontend (HTML) for uploading and searching photos
│
├── cloudformation/
│   └── ai-photo-search.yaml    # CloudFormation template for provisioning AWS resources
│
├── buildspec.yml               # Backend (Lambda) CodeBuild buildspec
├── frontend-buildspec.yml      # Frontend (S3) CodeBuild buildspec
├── README.md                   # Project documentation



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


## 👨‍💻 Contributors

- **Adarsh Rai** – API Gateway(PUT),Frontend, Lambda Integration, Deployment, AWS codePipeline, CloudFormation
- **Divyansh Agrawal** – Lambda Build, Lex, OpenSearch, API Gateway(GET)

---

## 📜 License

This project is part of a university assignment for Cloud Computing & Big Data Systems.
