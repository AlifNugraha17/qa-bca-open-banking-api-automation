"""
BCA Open Banking API - Mock Server & Core Banking Simulator
Provides real-time HTTP simulation of BCA SNAP BI & API V3 endpoints.
Runs on http://127.0.0.1:8080
"""

import sys
import json
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from bca_auth_helper import BCAAuthHelper

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

auth_helper = BCAAuthHelper()
PROCESSED_TRANSACTIONS = set()
MOCK_SERVER_INSTANCE = None


class BCAMockHandler(BaseHTTPRequestHandler):
    def _send_json(self, status_code, data):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode("utf-8"))

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body_bytes = self.rfile.read(content_length) if content_length > 0 else b""
        body_text = body_bytes.decode("utf-8") if body_bytes else ""
        try:
            body_json = json.loads(body_text) if body_text else {}
        except Exception:
            body_json = {}

        parsed_url = urlparse(self.path)
        path = parsed_url.path

        # 1. Endpoint: /api/oauth/token (OAuth 2.0 Token Generation)
        if path == "/api/oauth/token":
            auth_header = self.headers.get("Authorization", "")
            if not auth_header.startswith("Basic "):
                return self._send_json(401, {"ErrorCode": "ERR-BCA-INVALID-CLIENT", "ErrorMessage": "Missing or invalid Basic authorization header."})

            return self._send_json(200, {
                "access_token": "bca_access_token_sec_99a8b7c65d4e3f2a1b",
                "token_type": "Bearer",
                "expires_in": 3600,
                "scope": "resource.READ resource.WRITE"
            })

        # Security Check for Protected Endpoints
        sig_header = self.headers.get("X-BCA-Signature", "")
        if "corrupted_hash" in sig_header or "tampered" in sig_header:
            return self._send_json(401, {
                "ErrorCode": "ERR-BCA-INVALID-SIGNATURE",
                "ErrorMessage": "Unauthorized Request Signature. Cryptographic HMAC-SHA256 signature mismatch."
            })

        # 2. Endpoint: /banking/v3/corporates/{CorpID}/transfers (Fund Transfer Intra-Bank)
        if "/transfers" in path:
            trx_id = body_json.get("TransactionID")
            if not trx_id:
                return self._send_json(400, {"ErrorCode": "ERR-BCA-MISSING-PARAM", "ErrorMessage": "TransactionID is mandatory."})

            # Check Idempotency / Duplicate Transaction (Replay Attack detection)
            if trx_id in PROCESSED_TRANSACTIONS:
                return self._send_json(409, {
                    "ErrorCode": "ERR-BCA-DUPLICATE-TRANSACTION",
                    "ErrorMessage": f"Duplicate TransactionID '{trx_id}' detected within idempotency window. Replay rejected."
                })

            PROCESSED_TRANSACTIONS.add(trx_id)
            return self._send_json(200, {
                "TransactionStatus": "Success",
                "TransactionID": trx_id,
                "ReferenceNumber": "BCA-REF-20261005-998811",
                "Amount": body_json.get("Amount", 100000.00),
                "Currency": "IDR",
                "SourceAccount": body_json.get("SourceAccountNumber", "0201245678"),
                "BeneficiaryAccount": body_json.get("BeneficiaryAccountNumber", "0209876543"),
                "Timestamp": auth_helper.get_timestamp()
            })

        # 3. Endpoint: /va/v1/inquiry (BCA Virtual Account Inquiry)
        if path == "/va/v1/inquiry":
            va_no = body_json.get("VirtualAccountNo", "12345888999")
            return self._send_json(200, {
                "VirtualAccountNo": va_no,
                "CustomerName": "ALIF NUGRAHA",
                "BillAmount": 250000.00,
                "BillStatus": "UNPAID",
                "Currency": "IDR",
                "Description": "PEMBAYARAN TAGIHAN INTERNET & LISTRIK"
            })

        # 4. Endpoint: /va/v1/payment (BCA Virtual Account Payment Settlement)
        if path == "/va/v1/payment":
            va_no = body_json.get("VirtualAccountNo", "12345888999")
            amount = body_json.get("PaymentAmount", 250000.00)
            return self._send_json(200, {
                "VirtualAccountNo": va_no,
                "CustomerName": "ALIF NUGRAHA",
                "PaymentAmount": amount,
                "PaymentFlagStatus": "00",
                "PaymentStatus": "PAID",
                "ReferenceNo": "VA-BCA-PAY-776655",
                "Timestamp": auth_helper.get_timestamp()
            })

        self._send_json(404, {"ErrorCode": "ERR-BCA-404", "ErrorMessage": "Endpoint not found."})

    def do_GET(self):
        parsed_url = urlparse(self.path)
        path = parsed_url.path

        # 1. Endpoint: /balance (Balance Inquiry)
        if "/balance" in path:
            return self._send_json(200, {
                "AccountNo": "0201245678",
                "Name": "PT SINAR MAKMUR TEKNOLOGI",
                "Currency": "IDR",
                "AvailableBalance": 50000000.00,
                "LedgerBalance": 50000000.00,
                "Status": "ACTIVE"
            })

        # 2. Endpoint: /statements (Account Statement)
        if "/statements" in path:
            return self._send_json(200, {
                "AccountNo": "0201245678",
                "StartDate": "2026-10-01",
                "EndDate": "2026-10-05",
                "Currency": "IDR",
                "TransactionData": [
                    {
                        "TransactionDate": "2026-10-01",
                        "TransactionType": "CR",
                        "Amount": 15000000.00,
                        "Description": "SETORAN AWAL PEMBUKAAN REKENING",
                        "ReferenceNo": "BCA-TRX-00102"
                    },
                    {
                        "TransactionDate": "2026-10-03",
                        "TransactionType": "DB",
                        "Amount": 2500000.00,
                        "Description": "TRANSFER DANA KE REKENING VENDOR",
                        "ReferenceNo": "BCA-TRX-00103"
                    }
                ],
                "Trailer": {
                    "TotalRecords": 2,
                    "TotalDebit": 2500000.00,
                    "TotalCredit": 15000000.00
                }
            })

        self._send_json(404, {"ErrorCode": "ERR-BCA-404", "ErrorMessage": "Endpoint not found."})

    def log_message(self, format, *args):
        # Suppress noisy standard server logging
        return


def start_bca_mock_server(port=8080):
    global MOCK_SERVER_INSTANCE
    try:
        MOCK_SERVER_INSTANCE = HTTPServer(("127.0.0.1", port), BCAMockHandler)
        server_thread = threading.Thread(target=MOCK_SERVER_INSTANCE.serve_forever, daemon=True)
        server_thread.start()
        return True
    except OSError:
        # Already running
        return True


if __name__ == "__main__":
    print("[SERVER] Menjalankan BCA Mock Server di http://127.0.0.1:8080 ...")
    server = HTTPServer(("127.0.0.1", 8080), BCAMockHandler)
    server.serve_forever()
