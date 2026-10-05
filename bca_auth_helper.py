"""
BCA Open Banking API - Security & Signature Helper
Implements BCA SNAP BI & API V3 HMAC-SHA256 Request Signing
"""

import hashlib
import hmac
import base64
import json
from datetime import datetime, timezone, timedelta


class BCAAuthHelper:
    def __init__(self, client_id="bca_client_corp_001", client_secret="bca_secret_corp_key_2026", api_key="bca_api_key_sandbox_9988"):
        self.client_id = client_id
        self.client_secret = client_secret
        self.api_key = api_key

    def get_basic_auth_header(self):
        """Generates Basic Auth string: Base64(client_id:client_secret) for OAuth 2.0 token endpoint."""
        token_str = f"{self.client_id}:{self.client_secret}"
        encoded = base64.b64encode(token_str.encode("utf-8")).decode("utf-8")
        return f"Basic {encoded}"

    def get_timestamp(self):
        """Generates ISO-8601 Timestamp in WIB (UTC+7) timezone format required by BCA."""
        wib = timezone(timedelta(hours=7))
        return datetime.now(wib).strftime("%Y-%m-%dT%H:%M:%S.000+07:00")

    def calculate_body_hash(self, body_data):
        """Calculates Lowercase(Hex(SHA256(Minify(RequestBody))))."""
        if not body_data:
            minified_body = ""
        elif isinstance(body_data, dict):
            minified_body = json.dumps(body_data, separators=(",", ":"))
        elif isinstance(body_data, str):
            minified_body = body_data.strip()
        else:
            minified_body = str(body_data)

        sha256_hash = hashlib.sha256(minified_body.encode("utf-8")).hexdigest()
        return sha256_hash.lower()

    def generate_hmac_signature(self, http_method, relative_path, access_token, timestamp, body_data=None):
        """
        Calculates official BCA HMAC-SHA256 Signature:
        StringToSign = HTTPMethod + ":" + RelativePath + ":" + AccessToken + ":" + BodyHash + ":" + Timestamp
        Signature = Base64(HMAC-SHA256(StringToSign, ClientSecret))
        """
        body_hash = self.calculate_body_hash(body_data)
        string_to_sign = f"{http_method.upper()}:{relative_path}:{access_token}:{body_hash}:{timestamp}"

        hmac_digest = hmac.new(
            self.client_secret.encode("utf-8"),
            string_to_sign.encode("utf-8"),
            hashlib.sha256
        ).digest()

        return base64.b64encode(hmac_digest).decode("utf-8")

    def build_bca_headers(self, http_method, relative_path, access_token, body_data=None, custom_timestamp=None):
        """Constructs complete dictionary of mandatory BCA SNAP BI security headers."""
        timestamp = custom_timestamp or self.get_timestamp()
        signature = self.generate_hmac_signature(http_method, relative_path, access_token, timestamp, body_data)

        return {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "X-BCA-Key": self.api_key,
            "X-BCA-Timestamp": timestamp,
            "X-BCA-Signature": signature
        }
