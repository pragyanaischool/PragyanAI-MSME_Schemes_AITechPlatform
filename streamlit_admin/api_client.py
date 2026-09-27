import requests
from config import BACKEND_API_URL

class APIClient:
    def __init__(self, base_url: str = BACKEND_API_URL):
        self.base_url = base_url

    def _headers(self, token: str = None) -> dict:
        headers = {"Content-Type": "application/json"}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        return headers

    def login(self, email: str, password: str) -> dict:
        url = f"{self.base_url}/api/auth/login"
        res = requests.post(url, json={"email": email, "password": password}, timeout=10)
        return {"status_code": res.status_code, "data": res.json()}

    def register(self, payload: dict) -> dict:
        url = f"{self.base_url}/api/auth/register"
        res = requests.post(url, json=payload, timeout=10)
        return {"status_code": res.status_code, "data": res.json()}

    def sync_company_profile(self, profile: dict, token: str) -> dict:
        url = f"{self.base_url}/api/company/register"
        res = requests.post(url, json=profile, headers=self._headers(token), timeout=10)
        return {"status_code": res.status_code, "data": res.json()}

    def get_my_company(self, token: str) -> dict:
        url = f"{self.base_url}/api/company/me"
        res = requests.get(url, headers=self._headers(token), timeout=10)
        return {"status_code": res.status_code, "data": res.json()}

    def evaluate_schemes(self, company_id: str, token: str = None) -> dict:
        url = f"{self.base_url}/api/schemes/evaluate/{company_id}"
        res = requests.get(url, headers=self._headers(token), timeout=10)
        return {"status_code": res.status_code, "data": res.json()}

    def query_ai_advisor(self, query: str, company_id: str = None, language: str = "English") -> str:
        url = f"{self.base_url}/api/ai/advisor"
        payload = {"query": query, "company_id": company_id, "language": language}
        try:
            res = requests.post(url, json=payload, timeout=30)
            if res.status_code == 200:
                return res.json().get("response", "No response content received.")
            return f"Error {res.status_code}: {res.text}"
        except Exception as e:
            return f"Service Connection Failure: {str(e)}"

    def upload_document(self, company_id: str, doc_type: str, file_name: str, file_bytes: bytes, token: str) -> dict:
        url = f"{self.base_url}/api/documents/upload"
        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        data = {"company_id": company_id, "doc_type": doc_type}
        files = {"file": (file_name, file_bytes)}
        res = requests.post(url, data=data, files=files, headers=headers, timeout=20)
        return {"status_code": res.status_code, "data": res.json()}

    def get_admin_dashboard(self, token: str) -> dict:
        url = f"{self.base_url}/api/dashboard/admin"
        res = requests.get(url, headers=self._headers(token), timeout=10)
        return {"status_code": res.status_code, "data": res.json()}

    def verify_company(self, company_id: str, status: str, notes: str, token: str) -> dict:
        url = f"{self.base_url}/api/admin/verify-company"
        payload = {"company_id": company_id, "status": status, "notes": notes}
        res = requests.post(url, json=payload, headers=self._headers(token), timeout=10)
        return {"status_code": res.status_code, "data": res.json()}

    def get_entity_dashboard(self, token: str) -> dict:
        url = f"{self.base_url}/api/dashboard/entity"
        res = requests.get(url, headers=self._headers(token), timeout=10)
        return {"status_code": res.status_code, "data": res.json()}

    def publish_scheme(self, scheme_data: dict, token: str) -> dict:
        url = f"{self.base_url}/api/schemes/publish"
        res = requests.post(url, json=scheme_data, headers=self._headers(token), timeout=10)
        return {"status_code": res.status_code, "data": res.json()}

client = APIClient()
