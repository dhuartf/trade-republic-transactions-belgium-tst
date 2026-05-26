# Trade Republic Transaction Parser

An AI-powered tool to parse PDF bank statements from Trade Republic and extract structured transaction data.

## Features

- **Smart PDF Processing**: Efficient text extraction + Claude analysis
- **AI-Powered Extraction**: Uses AWS Bedrock (Claude Haiku 4.5) for intelligent parsing
- **Prompt Caching**: 90% cost savings on repeated calls via cached system prompts
- **System Prompt Architecture**: Clean separation of instructions and data
- **Structured Output**: ISIN, product names, quantities, amounts, and transaction types
- **Web Interface**: Modern React UI for upload and viewing
- **Data Aggregation**: Optional grouping by ISIN and transaction type
- **Export**: Download as JSON or CSV
- **Production Ready**: DynamoDB persistence, S3 storage, CDK infrastructure

## Architecture

### Backend (Python)
- **FastAPI**: REST API framework
- **AWS Bedrock**: Claude LLM for intelligent PDF parsing
- **pdfplumber**: PDF text extraction
- **boto3**: AWS SDK for S3 and DynamoDB

### Frontend (React + TypeScript)
- PDF upload interface
- Transaction data table
- Export functionality

### Infrastructure (AWS CDK)
- Lambda functions for API endpoints
- API Gateway
- S3 for PDF storage
- DynamoDB for transaction data
- IAM roles and policies

## Project Structure

```
registration-tst/
├── backend/           # Python backend
│   ├── src/
│   │   ├── api/      # FastAPI routes
│   │   ├── parsers/  # PDF and LLM parsing logic
│   │   ├── models/   # Data models
│   │   └── utils/    # Helper functions
│   └── requirements.txt
├── frontend/          # React + TypeScript
│   ├── src/
│   └── package.json
├── infrastructure/    # AWS CDK
│   └── app.py
└── samples/          # Sample PDFs
```

## Quick Start

### Prerequisites
- Python 3.12+
- Node.js 18+
- Claude API key

### 1. Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate  #On Mac: source venv/bin/activate 
pip install -r requirements.txt

# Run the backend
uvicorn src.api.main:app --reload
```

Backend will be available at `http://localhost:8000`

### 2. Frontend Setup
Open a new terminal:
```bash
cd frontend
npm install
npm start
```

Frontend will open at `http://localhost:3000`


### 4. Test It!
1. Open `http://localhost:3000` in your browser
2. Upload a Trade Republic PDF statement
3. Click "Upload & Parse"
4. View structured transactions and export to JSON/CSV
5. Upload the same PDF again - it will be retrieved from cache!


See [Infrastructure README](infrastructure/README.md) for details.

## License

MIT
