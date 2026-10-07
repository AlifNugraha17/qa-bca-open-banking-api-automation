"""
TIKET JIRA: QABCAA-1
Summary: [OAuth 2.0] Verify successful B2B client credentials authorization and bearer token generation
Endpoint: POST /api/oauth/token
"""

import sys
import time
import json
import requests
from bca_auth_helper import BCAAuthHelper
from bca_mock_server import start_bca_mock_server

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def test_QABCAA1_oauth_token():
    print("\n=======================================================================")
    print("🚀 MENJALANKAN TEST TIKET QABCAA-1: OAuth 2.0 Token Generation (BCA API)")
    print("=======================================================================")

    # 1. Pastikan BCA Mock Core Server berjalan
    start_bca_mock_server(port=8080)
    time.sleep(0.5)

    base_url = "http://127.0.0.1:8080"
    endpoint = f"{base_url}/api/oauth/token"

    # 2. Inisialisasi Otentikasi B2B BCA
    auth_helper = BCAAuthHelper(
        client_id="bca_client_corp_001",
        client_secret="bca_secret_corp_key_2026",
        api_key="bca_api_key_sandbox_9988"
    )

    basic_auth_header = auth_helper.get_basic_auth_header()

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": basic_auth_header
    }
    payload = {
        "grant_type": "client_credentials"
    }

    print(f"\n📡 Mengirim HTTP Request ke: {endpoint}")
    print(f"🔑 Header Authorization: {basic_auth_header[:25]}... (Encoded Client ID & Secret)")
    print(f"📦 Request Payload Body: {payload}")

    # 3. Eksekusi Request API
    response = requests.post(endpoint, headers=headers, data=payload, timeout=5)

    print(f"\n📥 HTTP Response Status: {response.status_code} {response.reason}")
    print("📄 Response JSON Payload:")
    print(json.dumps(response.json(), indent=2))

    # 4. Validasi Assertions (Kriteria Kualitas Perbankan)
    assert response.status_code == 200, f"Expected 200 OK but got {response.status_code}"
    
    res_data = response.json()
    assert "access_token" in res_data, "Response missing 'access_token' parameter!"
    assert res_data.get("token_type") == "Bearer", "Token type must be 'Bearer'!"
    assert res_data.get("expires_in") == 3600, "Token TTL expires_in should be 3600 seconds!"

    access_token = res_data["access_token"]
    print(f"\n✅ TEST PASSED: B2B OAuth 2.0 Token berhasil diterbitkan oleh Core BCA!")
    print(f"🎟️ Active Bearer Token: {access_token[:20]}... (Valid)")

    # Simpan token ke file lokal agar bisa dipakai oleh tiket-tiket berikutnya (Cek Saldo, Mutasi, Transfer)
    with open("bca_active_token.txt", "w", encoding="utf-8") as f:
        f.write(access_token)

    print("💾 Token otomatis tersimpan di 'bca_active_token.txt'.")


if __name__ == "__main__":
    test_QABCAA1_oauth_token()
