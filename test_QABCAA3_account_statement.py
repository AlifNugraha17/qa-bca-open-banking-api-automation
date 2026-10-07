"""
TIKET JIRA: QABCAA-3
Summary: [Account Statement] Verify historical transaction history and statement retrieval by date range
Endpoint: GET /banking/v3/corporates/{CorporateID}/accounts/{AccountNo}/statements
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


def test_QABCAA3_account_statement():
    print("\n=======================================================================")
    print("🚀 MENJALANKAN TEST TIKET QABCAA-3: Account Statement (Mutasi Rekening BCA)")
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
    account_no = "0201245678"
    relative_path = f"/banking/v3/corporates/{corp_id}/accounts/{account_no}/statements?startDate=2026-10-01&endDate=2026-10-05"
    endpoint = f"http://127.0.0.1:8080{relative_path}"

    headers = auth_helper.build_bca_headers(
        http_method="GET",
        relative_path=relative_path,
        access_token=access_token,
        body_data=None
    )

    print(f"\n📡 Mengirim HTTP GET ke: {endpoint}")
    print(f"🔒 X-BCA-Key: {headers['X-BCA-Key']}")
    print(f"🛡️ X-BCA-Signature: {headers['X-BCA-Signature'][:30]}...")

    response = requests.get(endpoint, headers=headers, timeout=5)

    print(f"\n📥 HTTP Response Status: {response.status_code} {response.reason}")
    print("📄 Response JSON Payload:")
    print(json.dumps(response.json(), indent=2))

    assert response.status_code == 200, f"Expected 200 OK but got {response.status_code}"
    data = response.json()
    assert "TransactionData" in data, "Missing TransactionData array in response"
    assert isinstance(data["TransactionData"], list), "TransactionData must be a list"
    assert len(data["TransactionData"]) > 0, "TransactionData array should not be empty"

    trailer = data.get("Trailer", {})
    assert trailer.get("TotalRecords") == len(data["TransactionData"]), "Trailer TotalRecords mismatch with array length!"

    print(f"\n✅ TEST PASSED: Mutasi rekening berhasil diverifikasi ({len(data['TransactionData'])} catatan transaksi valid)!")


if __name__ == "__main__":
    test_QABCAA3_account_statement()
