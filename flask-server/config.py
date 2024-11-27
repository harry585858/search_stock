class Config:
    NAVER_CLIENT_ID = "네이버 애플리케이션의 클라이언트 ID"
    NAVER_CLIENT_SECRET = "네이버 애플리케이션의 클라이언트 Secret"
    NAVER_REDIRECT_URI = "http://localhost:5000/naver/callback"  # 콜백 URL
    NAVER_AUTH_URL = "https://nid.naver.com/oauth2.0/authorize"
    NAVER_TOKEN_URL = "https://nid.naver.com/oauth2.0/token"
    NAVER_PROFILE_URL = "https://openapi.naver.com/v1/nid/me"