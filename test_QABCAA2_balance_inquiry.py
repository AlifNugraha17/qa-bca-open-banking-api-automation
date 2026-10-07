"""
TIKET JIRA: QABCAA-2
Summary: [Balance Inquiry] Verify customer ledger and available balance inquiry with valid HMAC signature
Endpoint: GET /banking/v3/corporates/{CorporateID}/accounts/{AccountNo}/balance
"""

import sys
import os
import json
import requests
from bca_auth_helper import BCAAuthHelper
from bca_mock_server import start_bca_mock_server

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def test_QABCAA2_balance_inquiry():
    print("\n=======================================================================")
    print("🚀 MENJALANKAN TEST TIKET QABCAA-2: Balance Inquiry (Cek Saldo BCA)")
    print("=======================================================================")

    start_bca_mock_server(port=8080)

    # 1. Baca Bearer Token dari QABCAA-1
    token_file = "bca_active_token.txt"
    if os.path.exists(token_file):
        with open(token_file, "r", encoding="utf-8") as f:
            access_token = f.read().strip()
    else:
        access_token = "bca_access_token_sec_99a8b7c65d4e3f2a1b"

    auth_helper = BCAAuthHelper()
    corp_id = "BCA_CORP_8877"
    account_no = "0201245678"
    relative_path = f"/banking/v3/corporates/{corp_id}/accounts/{account_no}/balance"
    endpoint = f"http://127.0.0.1:8080{relative_path}"

    # 2. Bangun Headers Keamanan Resmi BCA SNAP BI (HMAC-SHA256)
    headers = auth_helper.build_bca_headers(
        http_method="GET",
        relative_path=relative_path,
        access_token=access_token,
        body_data=None
    )

    print(f"\n📡 Mengirim HTTP GET ke: {endpoint}")
    print(f"🔒 X-BCA-Key: {headers['X-BCA-Key']}")
    print(f"⏰ X-BCA-Timestamp: {headers['X-BCA-Timestamp']}")
    print(f"🛡️ X-BCA-Signature (HMAC-SHA256): {headers['X-BCA-Signature'][:30]}...")

    # 3. Eksekusi Request
    response = requests.get(endpoint, headers=headers, timeout=5)

    print(f"\n📥 HTTP Response Status: {response.status_code} {response.reason}")
    print("📄 Response JSON Payload:")
    print(json.dumps(response.json(), indent=2))

    # 4. Validasi Assertions
    assert response.status_code == 200, f"Expected 200 OK but got {response.status_code}"
    data = response.json()
    assert data.get("AccountNo") == account_no, f"Account number mismatch! Got {data.get('AccountNo')}"
    assert data.get("Currency") == "IDR", "Currency must be IDR"
    assert "AvailableBalance" in data, "Missing AvailableBalance in response"
    assert data.get("AvailableBalance") > 0, "Available balance should be greater than zero"

    print(f"\n✅ TEST PASSED: Saldo rekening {account_no} terverifikasi aktif sebesar Rp {data['AvailableBalance']:,.2f} IDR!")


if __name__ == "__main__":
    test_QABCAA2_balance_inquiry()
