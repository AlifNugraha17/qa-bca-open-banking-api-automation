# 🏦 BCA Open Banking - API QA Automation & Security Testing Suite

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)
![Requests](https://img.shields.io/badge/Requests-HTTP_Client-red?logo=python)
![Pytest](https://img.shields.io/badge/Pytest-Test_Framework-yellow?logo=pytest)
![Jira](https://img.shields.io/badge/Jira-Atlassian-0052CC?logo=jira)
![BCA](https://img.shields.io/badge/Bank-BCA_Open_Banking-005BAA?logo=bank)
![SNAP BI](https://img.shields.io/badge/Standard-SNAP_BI_Open_API-00A86B?logo=bank)

An enterprise-grade Backend API Quality Assurance and automated test suite targeting **Bank Central Asia (BCA) Open Banking API Architecture** and **Standar Nasional Open API Pembayaran (SNAP BI)**.

---

## 📌 Jira Requirements Traceability Matrix (RTM)

| Jira ID | Banking Module | Test Scenario & Summary | Issue Type | Test Script |
| :--- | :--- | :--- | :--- | :--- |
| **QABCA-1** | OAuth 2.0 Security | Verify successful B2B client credentials authorization and bearer token generation | `Task` | `test_QABCA1_oauth_token.py` |
| **QABCA-2** | Balance Inquiry | Verify customer ledger and available balance inquiry with valid HMAC signature | `Task` | `test_QABCA2_balance_inquiry.py` |
| **QABCA-3** | Account Statement | Verify historical transaction history and statement retrieval by date range | `Task` | `test_QABCA3_account_statement.py` |
| **QABCA-4** | Fund Transfer | Verify intra-bank transfer execution between BCA accounts with unique idempotency key | `Task` | `test_QABCA4_fund_transfer_intra.py` |
| **QABCA-5** | Virtual Account | Verify end-to-end inquiry and bill payment settlement for BCA Virtual Account | `Task` | `test_QABCA5_virtual_account_payment.py` |
| **QABCA-6** | Cryptographic Security | API endpoint fails to reject request when HMAC-SHA256 signature is manipulated | `Bug` 🔴 | `test_QABCA6_bug_tampered_signature.py` |
| **QABCA-7** | Financial Idempotency | System processes duplicate transfer request with identical Transaction ID (Replay Attack) | `Bug` 🔴 | `test_QABCA7_bug_replay_duplicate_transfer.py` |

---

## 🚀 How to Run the Tests

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Individual API Tests
```bash
python test_QABCA1_oauth_token.py
python test_QABCA2_balance_inquiry.py
```

### 3. Run Entire Suite via Pytest with HTML Report
```bash
pytest test_*.py -v --html=report.html
```

---

## 👤 Author
- **Alif Nugraha**
- GitHub: [@AlifNugraha17](https://github.com/AlifNugraha17)
- Quality Assurance | Backend API Automation | Python | BCA Open Banking | SNAP BI
