<?php

require_once __DIR__ . '/../config/database.php';
require_once __DIR__ . '/../models/Evento.php';

class EventoController
{
    public function index()
    {
        $database = new Database();
        $db = $database->getConnection();
        $eventoModel = new Evento($db);

        if ($_SERVER['REQUEST_METHOD'] === 'POST') {
            if (isset($_POST['deletar'])) {
                $eventoModel->apagar($_POST['deletar']);
                header('Location: index.php?page=eventos');

            } elseif (isset($_POST['modo']) && $_POST['modo'] === 'editar' && !empty($_POST['id'])) {
                if (!empty($_FILES['foto']['tmp_name'])) {
                    $fotoBinaria = file_get_contents($_FILES['foto']['tmp_name']);
                    $tipoImagem = $_FILES['foto']['type'];

                    $eventoModel->editarComFoto(
                        $_POST['id'],
                        $_POST['titulo'],
                        $fotoBinaria,
                        $tipoImagem,
                        $_POST['data'],
                        $_POST['hora'],
                        $_POST['local'],
                        $_POST['valor']
                    );
                } else {
                    $eventoModel->editar(
                        $_POST['id'],
                        $_POST['titulo'],
                        $_POST['data'],
                        $_POST['hora'],
                        $_POST['local'],
                        $_POST['valor']
                    );
                }

            } elseif (isset($_POST['titulo'])) {
                if (!empty($_FILES['foto']['tmp_name'])) {
                    $fotoBinaria = file_get_contents($_FILES['foto']['tmp_name']);
                    $tipoImagem = $_FILES['foto']['type'];

                    $eventoModel->criar(
                        $_POST['titulo'],
                        $fotoBinaria,
                        $tipoImagem,
                        $_POST['data'],
                        $_POST['hora'],
                        $_POST['local'],
                        $_POST['valor']
                    );

                } else {
                    $eventoModel->criarSimg(
                        $_POST['titulo'],
                        $_POST['data'],
                        $_POST['hora'],
                        $_POST['local'],
                        $_POST['valor']
                    );
                }
            }

            header("Location: index.php?page=eventos");
            exit;
        }

        $listaEventos = $eventoModel->lerTodos();
        include __DIR__ . '/../views/eventos.php';
    }

    public function getEventos($id = null)
    {
        $database = new Database();
        $db = $database->getConnection();
        $eventoModel = new Evento($db);

        if ($id) {
            return $eventoModel->buscarPorId($id);
        }
        return $eventoModel->lerTodos();
    }
}