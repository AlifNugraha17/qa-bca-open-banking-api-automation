"""
TIKET JIRA: QABCAA-5
Summary: [Virtual Account] Verify end-to-end inquiry and bill payment settlement for BCA Virtual Account
Endpoints: POST /va/v1/inquiry & POST /va/v1/payment
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


def test_QABCAA5_virtual_account_payment():
    print("\n=======================================================================")
    print("🚀 MENJALANKAN TEST TIKET QABCAA-5: BCA Virtual Account (Inquiry & Payment)")
    print("=======================================================================")

    start_bca_mock_server(port=8080)

    token_file = "bca_active_token.txt"
    if os.path.exists(token_file):
        with open(token_file, "r", encoding="utf-8") as f:
            access_token = f.read().strip()
    else:
        access_token = "bca_access_token_sec_99a8b7c65d4e3f2a1b"

    auth_helper = BCAAuthHelper()
    base_url = "http://127.0.0.1:8080"
    va_number = "12345888999"

    # --- LANGKAH 1: VA INQUIRY (Cek Tagihan) ---
    inquiry_path = "/va/v1/inquiry"
    inquiry_payload = {"VirtualAccountNo": va_number}
    inquiry_headers = auth_helper.build_bca_headers("POST", inquiry_path, access_token, inquiry_payload)

    print(f"\n📡 [Step 1] Mengirim VA Inquiry ke: {base_url}{inquiry_path}")
    res_inquiry = requests.post(f"{base_url}{inquiry_path}", headers=inquiry_headers, json=inquiry_payload, timeout=5)
    print(f"📥 Response Inquiry Status: {res_inquiry.status_code}")
    print("📄 Response Data:")
    print(json.dumps(res_inquiry.json(), indent=2))

    assert res_inquiry.status_code == 200
    inquiry_data = res_inquiry.json()
    assert inquiry_data.get("BillStatus") == "UNPAID"
    bill_amount = inquiry_data.get("BillAmount")
    customer_name = inquiry_data.get("CustomerName")

    # --- LANGKAH 2: VA PAYMENT (Pelunasan Tagihan) ---
    payment_path = "/va/v1/payment"
    payment_payload = {
        "VirtualAccountNo": va_number,
        "PaymentAmount": bill_amount,
        "ReferenceID": "VA-SETTLE-998811"
    }
    payment_headers = auth_helper.build_bca_headers("POST", payment_path, access_token, payment_payload)

    print(f"\n📡 [Step 2] Mengirim VA Payment Settlement ke: {base_url}{payment_path}")
    res_payment = requests.post(f"{base_url}{payment_path}", headers=payment_headers, json=payment_payload, timeout=5)
    print(f"📥 Response Payment Status: {res_payment.status_code}")
    print("📄 Response Data:")
    print(json.dumps(res_payment.json(), indent=2))

    assert res_payment.status_code == 200
    payment_data = res_payment.json()
    assert payment_data.get("PaymentStatus") == "PAID"
    assert payment_data.get("PaymentFlagStatus") == "00"

    print(f"\n✅ TEST PASSED: Virtual Account {va_number} a.n {customer_name} berhasil dilunasi!")
    print(f"🧾 Bukti Bayar Bank: {payment_data.get('ReferenceNo')}")


if __name__ == "__main__":
    test_QABCAA5_virtual_account_payment()
