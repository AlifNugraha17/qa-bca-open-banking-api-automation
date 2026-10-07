# 📢 LinkedIn Post Template: BCA Open Banking API Automation & Security Testing

Dokumen ini berisi draft postingan LinkedIn yang siap di-*copy-paste* untuk mempublikasikan proyek portofolio QA Automation ini ke LinkedIn Anda. Tersedia versi Bahasa Indonesia dan Bahasa Inggris.

---

## 🇮🇩 Versi Bahasa Indonesia (Rekomendasi)

```text
🚀 [Project Showcase: Enterprise Backend API & Security Automation for BCA Open Banking (SNAP BI)]

Sebagai Quality Assurance Engineer, menguji integritas API di sektor perbankan dan finansial membutuhkan standar akurasi serta keamanan yang sangat ketat. 

Saya baru saja menyelesaikan proyek otomasi pengujian end-to-end untuk arsitektur API Bank Central Asia (BCA) Open Banking & Standar Nasional Open API Pembayaran (SNAP BI) menggunakan Python & Pytest.

Dalam proyek ini, seluruh test case dikelola dan ditelusuri secara terstruktur menggunakan Jira Scrum/Kanban Board dengan tracking Requirements Traceability Matrix (RTM):

📌 Modul & Skenario Pengujian (Jira Board: QABCAA):
✅ [QABCAA-1] OAuth 2.0 B2B Client Credentials Token Generation
✅ [QABCAA-2] Balance Inquiry (Cek Saldo Rekening Giro/Tabungan)
✅ [QABCAA-3] Account Statement (Mutasi Rekening Historis dengan Filter Tanggal)
✅ [QABCAA-4] Intra-bank Fund Transfer (Transfer Antar Rekening BCA)
✅ [QABCAA-5] Virtual Account Inquiry & Bill Payment Settlement

Selain fungsionalitas positif, fokus utama pengujian ini adalah Defect & Security Regression Testing:
🔴 [QABCAA-6 - Security Defect] Verifikasi penolakan request dengan Signature Manipulated / Tampered (HMAC-SHA256). Memastikan perlindungan terhadap Man-in-the-Middle (MitM) Attack (HTTP 401 Unauthorized).
🔴 [QABCAA-7 - Financial Idempotency Bug] Verifikasi pencegahan Replay Attack & Double Spending. Sistem wajib menolak transaksi duplikat dengan Transaction ID yang sama (HTTP 409 Conflict).

🛠️ Tech Stack & Key Highlights:
- Python 3.13, Pytest, Requests, hashlib & hmac
- Standar Kriptografi BCA: HMAC-SHA256 Request Signing, Hex SHA-256 Body Hash Minification, dan WIB ISO-8601 Timestamps
- Built-in Lightweight Core Banking Mock Server (zero external dependencies)
- 100% Test Pass Rate (7/7 Scenarios Passed)

🔗 Repository GitHub: https://github.com/AlifNugraha17/qa-bca-open-banking-api-automation

Terbuka untuk diskusi, masukan, dan peluang kolaborasi di bidang QA Automation & Software Testing! 💬

#QualityAssurance #QAEngineer #APITesting #TestAutomation #Python #Pytest #OpenBanking #BCA #SNAPBI #FintechSecurity #Jira #SoftwareTesting #Portfolio
```

---

## 🇬🇧 Versi Bahasa Inggris (International / Global Audience)

```text
🚀 [Portfolio Showcase: Enterprise Backend API & Security QA Automation — BCA Open Banking & SNAP BI]

Ensuring transaction integrity, cryptography standards, and idempotency in banking APIs is critical to financial security.

I recently engineered an automated API QA & Security test suite targeting Bank Central Asia (BCA) Open Banking and Indonesia's National Standard for Open API Payment (SNAP BI) using Python & Pytest.

All test scenarios were designed with strict Requirements Traceability Matrix (RTM) tracked on Jira:

📌 Jira Test Execution Matrix (Project Key: QABCAA):
✅ [QABCAA-1] OAuth 2.0 B2B Client Credentials Authorization & Bearer Token Generation
✅ [QABCAA-2] Customer Ledger & Available Balance Inquiry with HMAC Verification
✅ [QABCAA-3] Historical Account Statement Retrieval by Date Range
✅ [QABCAA-4] Intra-bank Fund Transfer with Unique Idempotency Keys
✅ [QABCAA-5] BCA Virtual Account Inquiry & Payment Settlement

🛡️ Negative Security & Financial Defect Audits:
🔴 [QABCAA-6 - Cryptographic Security] Validated gateway rejection against tampered HMAC-SHA256 signatures to prevent Man-in-the-Middle (MitM) tampering (HTTP 401).
🔴 [QABCAA-7 - Financial Idempotency] Validated prevention of Replay Attacks & duplicate transaction submissions to eliminate double-spending risks (HTTP 409 Conflict).

🛠️ Tech Stack:
- Python 3.13 | Requests | Pytest | pytest-html
- Cryptography: SHA-256 Body Minification + HMAC-SHA256 Request Signing + UTC+7 Timestamps
- Self-contained Banking Simulator Mock Server for zero-dependency CI runs
- 7/7 Test Cases Automated & Passed

🔗 GitHub Repository: https://github.com/AlifNugraha17/qa-bca-open-banking-api-automation

Would love to hear your thoughts, feedback, and connect with fellow QA and Fintech professionals! 🚀

#SoftwareTesting #QualityAssurance #QAAutomation #APITesting #Fintech #Cybersecurity #Python #Pytest #BCA #SNAPBI #Jira #TestAutomation
```

---

## 📸 Rekomendasi Media untuk Dilampirkan di LinkedIn Post:
1. **Screenshot Jira Board** (menampilkan status kolom To Do, In Progress, Done dengan tiket `QABCAA-1` hingga `QABCAA-7`).
2. **Screenshot Terminal / Pytest Execution** (menampilkan 7/7 PASSED: `test_QABCAA1` s/d `test_QABCAA7`).
