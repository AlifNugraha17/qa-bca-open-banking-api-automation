"""
TIKET JIRA: QABCAA-4
Summary: [Fund Transfer] Verify intra-bank transfer execution between BCA accounts with unique idempotency key
Endpoint: POST /banking/v3/corporates/{CorporateID}/transfers
"""

import sys
import os
import uuid
import json
import requests
from bca_auth_helper import BCAAuthHelper
from bca_mock_server import start_bca_mock_server

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def test_QABCAA4_fund_transfer_intra():
    print("\n=======================================================================")
    print("🚀 MENJALANKAN TEST TIKET QABCAA-4: Transfer Dana Antar Rekening BCA")
    print("=======================================================================")

    start_bca_mock_server(port=8080)

    token_file = "bca_active_token.txt"
    if os.path.exists(token_file):
        with open(token_file, "r", encoding="utf-8") as f:
            access_token = f.read().strip()
    else:
        access_token = "bca_access_token_sec_99a8b7c65d4e3f2a1b"

    auth_helper = BCAAuthHelper()
    corp_id = "BCA_CORP_8877"
    relative_path = f"/banking/v3/corporates/{corp_id}/transfers"
    endpoint = f"http://127.0.0.1:8080{relative_path}"

    # Generate unique transaction ID (Idempotency Key)
    transaction_id = f"TRX-BCA-{uuid.uuid4().hex[:8].upper()}"

    payload = {
        "TransactionID": transaction_id,
        "SourceAccountNumber": "0201245678",
        "BeneficiaryAccountNumber": "0209876543",
        "Amount": 150000.00,
        "Currency": "IDR",
        "Remark": "Pembayaran Invoice Layanan Cloud QA",
        "ReferenceID": "REF-INV-2026-001"
    }

    # Bangun headers dengan payload hash HMAC-SHA256
    headers = auth_helper.build_bca_headers(
        http_method="POST",
        relative_path=relative_path,
        access_token=access_token,
        body_data=payload
    )

    print(f"\n📡 Mengirim HTTP POST ke: {endpoint}")
    print(f"🆔 Unique TransactionID (Idempotency): {transaction_id}")
    print(f"💸 Nominal Transfer: Rp {payload['Amount']:,.2f} IDR")
    print(f"🛡️ X-BCA-Signature (Payload-Inclusive HMAC): {headers['X-BCA-Signature'][:30]}...")

    response = requests.post(endpoint, headers=headers, json=payload, timeout=5)

    print(f"\n📥 HTTP Response Status: {response.status_code} {response.reason}")
    print("📄 Response JSON Payload:")
    print(json.dumps(response.json(), indent=2))

    assert response.status_code == 200, f"Expected 200 OK but got {response.status_code}"
    data = response.json()
    assert data.get("TransactionStatus") == "Success", "Transaction status must be 'Success'"
    assert data.get("TransactionID") == transaction_id, "TransactionID returned must match request"
    assert "ReferenceNumber" in data, "Missing ReferenceNumber in response"

    print(f"\n✅ TEST PASSED: Transfer dana sukses diproses oleh Core Perbankan BCA!")
    print(f"🧾 No Referensi Bank: {data['ReferenceNumber']}")


if __name__ == "__main__":
    test_QABCAA4_fund_transfer_intra()
