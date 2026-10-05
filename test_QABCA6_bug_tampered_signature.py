"""
TIKET JIRA: QABCA-6 (SECURITY DEFECT TEST)
Summary: [Security Defect] API endpoint fails to reject request when HMAC-SHA256 signature is manipulated
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


def test_QABCA6_bug_tampered_signature():
    print("\n=======================================================================")
    print("🚀 MENJALANKAN TEST TIKET QABCA-6: Security Audit (Tampered HMAC Signature)")
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

    transaction_id = f"TRX-SEC-{uuid.uuid4().hex[:8].upper()}"

    payload = {
        "TransactionID": transaction_id,
        "SourceAccountNumber": "0201245678",
        "BeneficiaryAccountNumber": "0209876543",
        "Amount": 10000000.00,  # 10 Juta Rupiah
        "Currency": "IDR",
        "Remark": "Percobaan Manipulasi Signature Keamanan"
    }

    # Buat headers dengan signature ASLI, lalu SENGAJA KITA RUSAK / PALSUKAN!
    headers = auth_helper.build_bca_headers("POST", relative_path, access_token, payload)
    headers["X-BCA-Signature"] = "corrupted_hash_tampered_attacker_payload_signature_xyz"

    print(f"\n📡 Mengirim Manipulated Security Request ke: {endpoint}")
    print(f"💀 X-BCA-Signature (PALSU / RUSAK): {headers['X-BCA-Signature']}")
    print(f"💸 Percobaan Transfer Nominal Besar: Rp {payload['Amount']:,.2f} IDR")

    response = requests.post(endpoint, headers=headers, json=payload, timeout=5)

    print(f"\n📥 HTTP Response Status: {response.status_code} {response.reason}")
    print("📄 Response JSON Payload:")
    print(json.dumps(response.json(), indent=2))

    # ATURAN KEAMANAN PERBANKAN (OWASP API Top 10):
    # Jika signature dipalsukan, Gateway Bank WAJIB menolak dengan HTTP 401 Unauthorized!
    # Jika server meloloskan (HTTP 200), ini adalah CACAT KEAMANAN FATAL (MITM vulnerability)!
    assert response.status_code == 401, (
        f"[CRITICAL SECURITY BUG DETECTED!] "
        f"API perbankan meloloskan transaksi dengan HTTP {response.status_code} padahal signature HMAC-SHA256 telah dipalsukan!"
    )

    data = response.json()
    assert data.get("ErrorCode") == "ERR-BCA-INVALID-SIGNATURE"
    print(f"\n✅ SECURITY GATE PASSED: Gateway BCA sukses memblokir request palsu dengan kode 401 Unauthorized!")
    print(f"🛡️ Error Message: {data.get('ErrorMessage')}")


if __name__ == "__main__":
    test_QABCA6_bug_tampered_signature()
