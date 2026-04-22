import requests

# 1. A URL deve parar no /v1
SUPABASE_URL = "https://txhwelgildkscnspbdup.supabase.co/rest/v1"

# 2. Cole aqui a chave que começa com "ey" (anon public)
CHAVE_BRUTA = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InR4aHdlbGdpbGRrc2Nuc3BiZHVwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzYyNTU5NDEsImV4cCI6MjA5MTgzMTk0MX0.xj0V5qh9EpRJxSoz2K4frNHkuCmMqRRpM0SWi0RlPZg" 

SUPABASE_KEY = CHAVE_BRUTA.strip()

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}