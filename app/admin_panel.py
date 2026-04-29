import flet as ft
import requests
from config import HEADERS, SUPABASE_URL
import cv2

def admin_panel(page):
    page.title = "Painel Administrativo - O Show"
    page.bgcolor = "#F5F5F5"
    page.scroll = ft.ScrollMode.ALWAYS

    # --- VARIÁVEIS DE INTERFACE PARA RECARREGAR ---
    txt_vendidos = ft.Text("0", size=30, color="white", weight="bold")
    txt_presentes = ft.Text("0", size=30, color="#0D004E", weight="bold")
    lista_ingressos = ft.Column(spacing=10)

    def validar_pelo_hash(hash_codigo):
        """
        Função centralizada para buscar o ingresso no banco e invalidar se necessário.
        Pode ser chamada tanto pelo leitor de câmera quanto pelo campo de texto.
        """
        try:
            url = f"{SUPABASE_URL}/ingressos?qr_code_hash=eq.{hash_codigo}&select=id,usado"
            res = requests.get(url, headers=HEADERS).json()

            if res:
                ing = res[0]
                if ing['usado']:
                    page.snack_bar = ft.SnackBar(
                        ft.Text(f"ERRO: O código {hash_codigo} já foi utilizado!"), 
                        bgcolor="red"
                    )
                    page.snack_bar.open = True
                else:
                    if dar_checkin(ing['id']):
                        page.snack_bar = ft.SnackBar(
                            ft.Text(f"SUCESSO: Ingresso {hash_codigo} Validado!"), 
                            bgcolor="green"
                        )
                        page.snack_bar.open = True
            else:
                page.snack_bar = ft.SnackBar(
                    ft.Text("Código não encontrado no sistema!"), 
                    bgcolor="orange"
                )
                page.snack_bar.open = True
            
        except Exception as e:
            print(f"Erro na validação: {e}")
            page.snack_bar = ft.SnackBar(ft.Text("Erro de conexão com o banco!"))
            page.snack_bar.open = True
    
        page.update()

    def sair(e):
        from components import set_storage
        set_storage(page, "logado", False)
        page.clean()
        from login import login
        login(page)

    def dar_checkin(id_ingresso):
        try:
            url = f"{SUPABASE_URL}/ingressos?id=eq.{id_ingresso}"
            r = requests.patch(url, json={"usado": True}, headers=HEADERS)
            if r.status_code in [200, 204]:
                atualizar_dados()
                return True
        except Exception as e:
            print(f"Erro ao invalidar: {e}")
        return False
    
    def abrir_leitor_manual(e):
        codigo_input = ft.TextField(label="Digite o Hash do QR Code", expand=True, autofocus=True)

        def processar_validacao(e):
            hash_digitado = codigo_input.value
            if not hash_digitado: return

            url = f"{SUPABASE_URL}/ingressos?qr_code_hash=eq.{hash_digitado}&select=id,usado"
            res = requests.get(url, headers=HEADERS).json()

            if res:
                ing = res[0]
                if ing['usado']:
                    page.snack_bar = ft.SnackBar(ft.Text("ERRO: Ingresso já utilizado!"), bgcolor="red")
                else:
                    dar_checkin(ing['id'])
                    page.snack_bar = ft.SnackBar(ft.Text("SUCESSO: Entrada Liberada!"), bgcolor="green")
                    modal_manual.open = False
            else:
                page.snack_bar = ft.SnackBar(ft.Text("Código Inválido!"), bgcolor="orange")

            page.snack_bar.open = True
            page.update()

        modal_manual = ft.AlertDialog(
            title=ft.Text("Validação Manual"),
            content=ft.Column([ft.Text("Use esta opção se estiver no site (Render)"), codigo_input], tight=True),
            actions=[ft.ElevatedButton("Validar", on_click=processar_validacao)]
        )

        page.overlay.append(modal_manual)
        modal_manual.open = True
        page.update()

# --- FUNÇÃO DE CÂMERA (COM PROTEÇÃO PARA NÃO CRASHAR NO RENDER) ---
    def abrir_leitor_camera(e):
        try:
            import cv2
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                raise Exception("Câmera não encontrada")

            detector = cv2.QRCodeDetector()

            # Se chegar aqui, a câmera abriu (provavelmente rodando local no PC)
            while True:
                ret, img = cap.read()
                if not ret: break

                data, _, _ = detector.detectAndDecode(img)
                if data: # 'data' é o texto lido pelo QR
                    validar_pelo_hash(data)
                    break
                    
                cv2.imshow("Leitor Magnus (Pressione ESC)", img)
                if cv2.waitKey(1) == 27: break
            
            cap.release()
            cv2.destroyAllWindows()
        
        except Exception as ex:
            # Se der erro (como no Render), abre o manual automaticamente e avisa
            page.snack_bar = ft.SnackBar(ft.Text(f"Câmera indisponível no servidor: {ex}"), bgcolor="orange")
            page.snack_bar.open = True
            abrir_leitor_manual(None)

    # --- FUNÇÃO PARA BUSCAR E ATUALIZAR DADOS (O RECARREGAR) ---
    def atualizar_dados(e=None):
        try:
            r_stats = requests.get(f"{SUPABASE_URL}/ingressos?select=*", headers=HEADERS)
            if r_stats.status_code == 200:
                dados_total = r_stats.json()
                total = len(dados_total)
                presentes = len([i for i in dados_total if i.get("usado") == True])
                
                txt_vendidos.value = str(total)
                txt_presentes.value = str(presentes)

            url_detalhada = f"{SUPABASE_URL}/ingressos?select=*,users(nome),eventos_db(titulo,valor_evento)"
            r_detalhes = requests.get(url_detalhada, headers=HEADERS)
            
            if r_detalhes.status_code == 200:
                ingressos = r_detalhes.json()
                lista_ingressos.controls.clear()
                
                for ing in ingressos:
                    nome_usuario = ing.get("users", {}).get("nome", "N/A")
                    nome_evento = ing.get("eventos_db", {}).get("titulo", "N/A")
                    valor = ing.get("eventos_db", {}).get("valor_evento", 0.0)
                    usado = ing.get("usado", False)
                    id_ingresso = ing.get("id") # Precisamos do ID para o banco

                    botao_checkin = ft.IconButton(
                        icon=ft.Icons.CHECK_CIRCLE_OUTLINE,
                        icon_color="green",
                        tooltip="Validar Entrada",
                        on_click=lambda e, idx=id_ingresso: dar_checkin(idx)
                    ) if not usado else ft.Icon(ft.Icons.DONE_ALL, color="blue", size=20)

                    lista_ingressos.controls.append(
                        ft.Container(
                            content=ft.Row([
                                ft.Icon(ft.Icons.CONFIRMATION_NUMBER, color="#0D004E" if not usado else "grey"),
                                ft.Column([
                                    ft.Text(f"Dono: {nome_usuario}", weight="bold", size=14),
                                    ft.Text(f"Evento: {nome_evento} | R$ {valor:.2f}", size=12),
                                ], expand=True),
                
                                # O BOTÃO ENTRA AQUI
                                botao_checkin, 
                
                                ft.Container(
                                    content=ft.Text("USADO" if usado else "PENDENTE", size=10, color="white", weight="bold"),
                                    bgcolor="green" if usado else "orange",
                                    padding=ft.padding.symmetric(horizontal=8, vertical=4),
                                    border_radius=5,
                                )
                            ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
                            bgcolor="white",
                            padding=15,
                            border_radius=10,
                            border=ft.border.all(1, "black12")
                        )
                    )
            
            page.update()
            
        except Exception as ex:
            print(f"Erro ao recarregar: {ex}")

    # --- COMPONENTES VISUAIS ---

    header = ft.Row([
        ft.Text("Área Administrativa - Magnus", size=30, weight="bold", color="#0D004E"),
        ft.Row([
            ft.IconButton(ft.Icons.REFRESH, on_click=atualizar_dados, icon_color="blue", tooltip="Recarregar dados"),
            ft.IconButton(ft.Icons.LOGOUT, on_click=sair, icon_color="red"),
        ])
    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    stats_cards = ft.Row([
        ft.Container(
            content=ft.Column([ft.Text("Vendidos", color="white"), txt_vendidos]),
            bgcolor="#0D004E", padding=20, border_radius=10, expand=True
        ),
        ft.Container(
            content=ft.Column([ft.Text("Presentes (O Show)", color="#0D004E"), txt_presentes]),
            bgcolor="#FFD700", padding=20, border_radius=10, expand=True
        )
    ])

    # Botões de Ação
    # --- FUNÇÕES PARA ABRIR MODAIS ---
    
    def abrir_novo_evento(e):
        # Campos do formulário (Baseado no seu Evento.php)
        titulo_input = ft.TextField(label="Título do Evento")
        data_input = ft.TextField(label="Data (DD/MM/AAAA)")
        local_input = ft.TextField(label="Local")
        valor_input = ft.TextField(label="Valor (R$)", value="0.00")
        url_imagem = ft.TextField(label="URL da Imagem (Capa)")

        def salvar_evento(e):
            try:
                # Pegando os valores
                data_digitada = data_input.value.replace("/", "") 

                # Converte DDMMYYYY para YYYY-MM-DD
                if len(data_digitada) == 8:
                    data_formatada = f"{data_digitada[4:]}-{data_digitada[2:4]}-{data_digitada[:2]}"
                else:
                    print("Erro: Data deve ter o formato DDMMYYYY ou DD/MM/YYYY")
                    return

                novo_evento = {
                    "titulo": titulo_input.value,
                    "data_evento": data_formatada,
                    "local_evento": local_input.value,
                    "valor_evento": float(valor_input.value.replace(',', '.')),
                    "hora_evento": "20:00:00",
                    "foto_evento": url_imagem.value if url_imagem.value else None
                }

                print(f"Tentando salvar formatado: {novo_evento}")

                r = requests.post(f"{SUPABASE_URL}/eventos_db", json=novo_evento, headers=HEADERS)

                if r.status_code in [200, 201]:
                    modal_evento.open = False
                    atualizar_dados()
                    page.update()
                else:
                    print(f"Erro do Supabase: {r.status_code} - {r.text}")
            
            except Exception as ex:
                print(f"Erro de execução: {ex}")

        modal_evento = ft.AlertDialog(
            title=ft.Text("Cadastrar Novo Show"),
            content=ft.Column([titulo_input, data_input, local_input, valor_input, url_imagem], tight=True),
            actions=[ft.TextButton("Salvar", on_click=salvar_evento)]
        )
        page.overlay.append(modal_evento)
        modal_evento.open = True
        page.update()

    def abrir_usuarios(e):
        # Busca usuários e seus ingressos (count)
        r = requests.get(f"{SUPABASE_URL}/users?select=*,ingressos(count)", headers=HEADERS)
        users = r.json()
        
        lista_users_ui = ft.Column(spacing=10, scroll=ft.ScrollMode.ALWAYS, height=400)
        
        for u in users:
            qtd_ingressos = u.get("ingressos", [{}])[0].get("count", 0)
            lista_users_ui.controls.append(
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.PERSON_OUTLINE),
                    title=ft.Text(u['nome']),
                    subtitle=ft.Text(f"{u['email']} | Ingressos: {qtd_ingressos}"),
                    trailing=ft.Icon(ft.Icons.ADMIN_PANEL_SETTINGS if u.get('admin') else None, color="blue")
                )
            )

        modal_user = ft.AlertDialog(
            title=ft.Text("Gestão de Utilizadores"),
            content=lista_users_ui,
            actions=[ft.TextButton("Fechar", on_click=lambda _: setattr(modal_user, "open", False) or page.update())]
        )
        page.overlay.append(modal_user)
        modal_user.open = True
        page.update()

    # --- BOTÕES DE AÇÃO ATUALIZADOS ---
    acoes = ft.Row([
        ft.ElevatedButton("Novo Evento", icon=ft.Icons.ADD, on_click=abrir_novo_evento),

        # OPÇÃO 1: CÂMERA (Foca no uso local/desktop)
        ft.ElevatedButton("Escanear (Câmera)", icon=ft.Icons.CAMERA_ALT, on_click=abrir_leitor_camera),

        # OPÇÃO 2: CÓDIGO (Foca no uso Web/Render)
        ft.ElevatedButton("Validar (Código)", icon=ft.Icons.KEYBOARD, on_click=abrir_leitor_manual),

        # OPÇÃO 3: USUÁRIOS (Gerenciamento básico de usuários e visualização de ingressos)
        ft.ElevatedButton("Usuários", icon=ft.Icons.PERSON, on_click=abrir_usuarios),
    ], alignment=ft.MainAxisAlignment.CENTER)

    # Montagem da Página
    page.add(
        header,
        ft.Divider(height=20, color="transparent"),
        stats_cards,
        ft.Divider(height=20),
        ft.Text("Logs de Ingressos Comprados", size=20, weight="bold"),
        lista_ingressos,
        ft.Divider(height=20, color="transparent"),
        acoes
    )

    atualizar_dados()