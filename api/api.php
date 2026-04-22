<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);

// Controllers
require_once "../controllers/EventoController.php";
require_once "../controllers/LoginController.php";
require_once "../controllers/IngressoController.php";

header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: GET, POST, OPTIONS");
header("Access-Control-Allow-Headers: Content-Type, Authorization, X-Requested-With");

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit;
}

header("Content-Type: application/json; charset=UTF-8");

// Instanciamento de Controllers
$eventoController = new EventoController();
$loginController = new LoginController();
$ingressoController = new IngressoController();

$acao = $_GET['acao'] ?? null;
$method = $_SERVER['REQUEST_METHOD'];
$data = json_decode(file_get_contents("php://input"), true);

if ($method === 'POST' && !$data && in_array($acao, ['cadastrar', 'login', 'comprar'])) {
    http_response_code(400);
    echo json_encode(["status" => "erro", "mensagem" => "Dados JSON inválidos"]);
    exit;
}

switch ($acao) {
    case 'eventos':
        if ($method !== 'GET') {
            http_response_code(405);
            echo json_encode(["status" => "erro", "mensagem" => "Método não permitido"]);
            exit;
        }
        $id = $_GET['id'] ?? null;
        $resultado = $eventoController->getEventos($id);

        if ($id && !$resultado) {
            http_response_code(404);
            echo json_encode(["status" => "erro", "mensagem" => "Evento não encontrado"]);
            exit;
        }

        // Formatação de imagem para Base64 (Mantido na API conforme pedido)
        $inputParaMap = ($id && $resultado) ? [$resultado] : ($resultado ?: []);
        $dadosFormatados = array_map(function ($item) {
            if (isset($item['foto_evento']) && !empty($item['foto_evento'])) {
                $item['foto_evento'] = 'data:' . ($item['tipo_imagem'] ?? 'image/jpeg') . ';base64,' . base64_encode($item['foto_evento']);
            }
            return $item;
        }, $inputParaMap);

        echo json_encode($id ? ($dadosFormatados[0] ?? null) : $dadosFormatados, JSON_UNESCAPED_UNICODE);
        break;

    case 'usuario':
        $email = $_GET['email'] ?? null;
        if (!$email) {
            http_response_code(400);
            echo json_encode(["status" => "erro", "mensagem" => "Email é obrigatório"]);
            exit;
        }
        $res = $loginController->getPerfil($email);
        if ($res['status'] === 'erro')
            http_response_code(404);
        echo json_encode($res, JSON_UNESCAPED_UNICODE);
        break;

    case 'cadastrar':
        $nome = $data['nome'] ?? null;
        $email = $data['email'] ?? null;
        $senha = $data['senha'] ?? null;
        if (!$nome || !$email || !$senha) {
            http_response_code(400);
            echo json_encode(["status" => "erro", "mensagem" => "Campos nome, email e senha são obrigatórios"]);
            exit;
        }
        $res = $loginController->registrarApi($nome, $email, $senha);
        if ($res['status'] === 'sucesso')
            http_response_code(201);
        else
            http_response_code(500);
        echo json_encode($res);
        break;

    case 'login':
        $email = $data['email'] ?? null;
        $senha = $data['senha'] ?? null;
        if (!$email || !$senha) {
            http_response_code(400);
            echo json_encode(["status" => "erro", "mensagem" => "Campos email e senha são obrigatórios"]);
            exit;
        }
        $res = $loginController->loginApi($email, $senha);
        if ($res['status'] === 'erro')
            http_response_code(401);
        echo json_encode($res, JSON_UNESCAPED_UNICODE);
        break;

    case 'comprar':
        $email = $data['email'] ?? null;
        $evento_id = $data['evento_id'] ?? null;
        if (!$email || !$evento_id) {
            http_response_code(400);
            echo json_encode(["status" => "erro", "mensagem" => "Campos email e evento_id são obrigatórios"]);
            exit;
        }
        $res = $ingressoController->comprar($email, $evento_id);
        if ($res['status'] === 'sucesso')
            http_response_code(201);
        else
            http_response_code(500);
        echo json_encode($res);
        break;

    case 'meus_ingressos':
        $email = $_GET['email'] ?? null;
        if (!$email) {
            http_response_code(400);
            echo json_encode(["status" => "erro", "mensagem" => "O email é obrigatório"]);
            exit;
        }
        $ingressos = $ingressoController->getMeusIngressos($email);

        // Formata imagens
        $ingressosFormatados = array_map(function ($item) {
            if (isset($item['foto_evento']) && !empty($item['foto_evento'])) {
                $item['foto_evento'] = 'data:' . ($item['tipo_imagem'] ?? 'image/jpeg') . ';base64,' . base64_encode($item['foto_evento']);
            }
            return $item;
        }, $ingressos);

        echo json_encode($ingressosFormatados, JSON_UNESCAPED_UNICODE);
        break;

    default:
        http_response_code(400);
        echo json_encode(["status" => "erro", "mensagem" => "Recurso inválido"]);
        break;
}