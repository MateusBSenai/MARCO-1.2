import cv2
import requests
from config import SUPABASE_URL, HEADERS

def iniciar_leitor():
    cap = cv2.VideoCapture(0) # Abre a webcam
    detector = cv2.QRCodeDetector()

    print("Aguardando leitura de QR Code...")

    while True:
        _, img = cap.read()
        data, bbox, _ = detector.detectAndDecode(img)
        
        if data:
            validar_entrada(data)
            break # Para após ler um código
        
        cv2.imshow("Leitor de QR Code - AccessPass", img)
        if cv2.waitKey(1) == ord("q"):
            break
            
    cap.release()
    cv2.destroyAllWindows()

def validar_entrada(hash_recebido):
    # 1. Verifica se o ingresso existe e se já foi usado
    URL = f"{SUPABASE_URL}/ingressos?qr_code_hash=eq.{hash_recebido}&select=*"
    response = requests.get(URL, headers=HEADERS)
    ingresso = response.json()

    if not ingresso:
        print("ERRO: Ingresso Inválido!")
        return

    if ingresso[0]['usado']:
        print("ALERTA: Este ingresso JÁ FOI USADO!")
    else:
        # 2. Marca como usado no Supabase
        ingresso_id = ingresso[0]['id']
        update_url = f"{SUPABASE_URL}/ingressos?id=eq.{ingresso_id}"
        requests.patch(update_url, json={"usado": True}, headers=HEADERS)
        print("SUCESSO: Entrada liberada!")