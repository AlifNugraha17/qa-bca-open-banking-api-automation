"""
TIKET JIRA: QABCA-7 (FINANCIAL IDEMPOTENCY BUG TEST)
Summary: [Transaction Idempotency Bug] System processes duplicate transfer request with identical Transaction ID
Endpoint: POST /banking/v3/corporates/{CorporateID}/transfers
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


def test_QABCA7_bug_replay_duplicate_transfer():
    print("\n=======================================================================")
    print("🚀 MENJALANKAN TEST TIKET QABCA-7: Replay Attack & Idempotency Duplicate")
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

    # Gunakan TransactionID tetap untuk menguji deteksi duplikasi (Replay Attack)
    fixed_trx_id = "TRX-REPLAY-ATTACK-007"

    payload = {
        "TransactionID": fixed_trx_id,
        "SourceAccountNumber": "0201245678",
        "BeneficiaryAccountNumber": "0209876543",
        "Amount": 500000.00,  # Rp 500.000
        "Currency": "IDR",
        "Remark": "Uji Coba Idempotency / Double Spending"
    }

    headers = auth_helper.build_bca_headers("POST", relative_path, access_token, payload)

    # --- REQUEST PERTAMA (Transaksi Sah) ---
    print(f"\n📡 [Step 1] Mengirim Request Transfer Pertama (TransactionID: {fixed_trx_id})")
    res1 = requests.post(endpoint, headers=headers, json=payload, timeout=5)
    print(f"📥 Response Pertama: {res1.status_code} {res1.reason}")
    print(json.dumps(res1.json(), indent=2))
    assert res1.status_code == 200, "Request pertama harus sukses 200 OK"

    # --- REQUEST KEDUA (Duplikasi / Serangan Replay Attack dengan ID yang sama persis) ---
    print(f"\n📡 [Step 2] Mengirim Ulang Request KEDUA dengan TransactionID SAMA ({fixed_trx_id})")
    res2 = requests.post(endpoint, headers=headers, json=payload, timeout=5)
    print(f"📥 Response Kedua: {res2.status_code} {res2.reason}")
    print(json.dumps(res2.json(), indent=2))

    # ATURAN IDEMPOTENCY FINANSIAL PERBANKAN:
    # Core banking HARUS menolak request kedua dengan HTTP 409 Conflict!
    # Jika server meloloskan (HTTP 200), nasabah akan terpotong uangnya 2 kali (Double Debit / Replay Bug)!
    assert res2.status_code == 409, (
        f"[CRITICAL FINANCIAL IDEMPOTENCY DEFECT DETECTED!] "
        f"Server perbankan menerima transaksi duplikat dengan status {res2.status_code}! "
        f"Saldo nasabah berisiko terdebit ganda (Double Spending)!"
    )

    data2 = res2.json()
    assert data2.get("ErrorCode") == "ERR-BCA-DUPLICATE-TRANSACTION"
    print(f"\n✅ IDEMPOTENCY GUARD PASSED: Core BCA berhasil mencegah transaksi ganda (HTTP 409 Conflict)!")
    print(f"🛡️ Error Message: {data2.get('ErrorMessage')}")


if __name__ == "__main__":
    test_QABCA7_bug_replay_duplicate_transfer()
