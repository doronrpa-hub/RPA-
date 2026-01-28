# 🇮🇱 RPA-PORT Customs AI

**AI-powered Israeli Customs Classification System**

Website: https://www.rpa-port.com  
Contact: devrpa@rpa-port.co.il

---

## 🎯 Features

- **HS Code Classification** - Classify products using Israeli customs tariff (10-digit codes)
- **Declaration Analysis** - Analyze import/export declarations
- **Tax Calculation** - Calculate customs duty, VAT, and purchase tax
- **Trade Agreements** - Identify benefits from 16+ trade agreements
- **Bilingual Support** - Hebrew and English

---

## 🚀 Quick Start

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variable
export ANTHROPIC_API_KEY=sk-ant-xxx

# Run server
uvicorn main:app --reload

# Open browser
open http://localhost:8000/docs
```

### Docker

```bash
# Build
docker build -t rpa-port-customs .

# Run
docker run -p 8080:8080 -e ANTHROPIC_API_KEY=sk-ant-xxx rpa-port-customs
```

---

## 🌐 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API info |
| `/health` | GET | Health check |
| `/docs` | GET | Swagger UI |
| `/api/chat` | POST | Chat with AI |
| `/api/classify` | POST | Classify product |
| `/api/agreements` | GET | List trade agreements |

---

## 📝 Example Usage

### Chat (Hebrew)
```bash
curl -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "איך מסווגים טלפון נייד?"}'
```

### Classify Product
```bash
curl -X POST http://localhost:8080/api/classify \
  -H "Content-Type: application/json" \
  -d '{"description": "אוזניות אלחוטיות בלוטוס"}'
```

---

## ☁️ Deploy to DigitalOcean

1. Push code to GitHub
2. Create App in DigitalOcean App Platform
3. Connect GitHub repository
4. Add environment variable: `ANTHROPIC_API_KEY`
5. Deploy!

---

## 🔑 Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `ANTHROPIC_API_KEY` | ✅ | Anthropic API key |
| `PORT` | ❌ | Server port (default: 8080) |

---

## 📄 License

© 2025 RPA-PORT LTD. All rights reserved.
