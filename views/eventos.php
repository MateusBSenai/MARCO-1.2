<!DOCTYPE html>
<html lang="pt-br">
<head>
    <!--
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    -->
    <link rel="stylesheet" href="/agenda-de-eventos/assets/css/tabela.css?v=2.22"><!--?v=1-->
    <link rel="icon" href="/agenda-de-eventos/assets/icons/logo_temporaria.png">
    <script src="/agenda-de-eventos/assets/js/script.js?v=1" type="module" defer></script>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Agenda de Eventos</title>
</head>
<body>
    <div class="header">
        <div class="logo-header">
            <img src="/agenda-de-eventos/assets/icons/logo_temporaria.png" alt="">
            <p>Magnus</p>
        </div>
        
        <img src="/agenda-de-eventos/assets/icons/brasil.png" alt="" class="brasil">
        <a href="index.php?page=logout"><img src="/agenda-de-eventos/assets/icons/logout.png" alt="" class="logout"></a>    
    </div>
    <div class="container mt-4">
        <div class="row-titulo">
            <h1 class="titulo-agenda text-center mb-4">Agenda de Eventos</h1>
            <button class="open-add-evento">
                <img src="/agenda-de-eventos/assets/icons/add.png" alt="" class="add-icon">
                Add Evento
            </button>
        </div>
        
        <hr class="linha">
        <table class="table table-striped table-bordered">
            <thead class="table-dark">
                <tr class="linha-base-tabela">
                    <th class="col-inicial">Evento</th>
                    <th>Imagem</th>
                    <th>Data</th>
                    <th>Local</th>
                    <th>Horário</th>
                    <th>Preço</th>
                    <th class="col-final">
                        <img src="https://cdn-icons-png.flaticon.com/128/4662/4662651.png" alt="Apagar Evento" class="deletar-evento" title="Apagar">
                        <img src="/agenda-de-eventos/assets/icons/edit.png" alt="Editar" class="editar-evento" title="Editar">
                    </th>
                </tr>
            </thead>
            <tbody>
                <?php foreach ($listaEventos as $ev): ?>
                    <tr>
                        <td  class="eventos"><?= htmlspecialchars($ev['titulo']) ?></td>
                        <td class="eventos">
                            <div class="sem-imagem">
                                <img src="data:<?= $ev['tipo_imagem'] ?>;base64,<?= base64_encode($ev['foto_evento']) ?>" 
                                    class="imagem-tabela" alt="<?= htmlspecialchars($ev['titulo']) ?>">
                            </div>
                        </td>
                        <td  class="eventos"><?= date('d/m/Y', strtotime($ev['data_evento'])) ?></td>
                        <td  class="eventos"><?= htmlspecialchars($ev['local_evento']) ?></td>
                        <td  class="eventos"><?= date('H:i', strtotime($ev['hora_evento'])) ?>h</td>
                        <td  class="eventos">R$ <?= number_format($ev['valor_evento'], 2, ',', '.') ?></td>
                        <td  class="eventos col-final-conteudo">
                            <form method="POST">
                                <button type="submit" name="deletar" value="<?=$ev['id']?>" class="btn btn-primary w-100">
                                    <img src="https://cdn-icons-png.flaticon.com/128/4662/4662651.png" alt="Apagar Evento" class="deletar-evento" title="Apagar">
                                </button>
                                <button type="button"
                                        name="editar"
                                        value="<?=$ev['id']?>" 
                                        class="btn btn-primary w-100 editar-elemento"
                                        data-id="<?= $ev['id'] ?>"
                                        data-titulo="<?= htmlspecialchars($ev['titulo']) ?>"
                                        data-data="<?= $ev['data_evento'] ?>"
                                        data-local="<?= htmlspecialchars($ev['local_evento']) ?>"
                                        data-hora="<?= $ev['hora_evento'] ?>"
                                        data-valor="<?= $ev['valor_evento'] ?>">
                                    <img src="/agenda-de-eventos/assets/icons/edit.png" alt="Editar Evento" class="editar-evento" title="Editar">
                                </button>
                            </form>
                        </td>
                    </tr>
                <?php endforeach; ?>
                <tr class="final-tabela"></tr>
            </tbody>
        </table>
    </div> <!-- Container -->

    <footer>
        <p>&copy;Copyright to Marcos Gustavo</p>
    </footer>
    
    <div class="modal-lateral">
        <form method="POST" class="row g-3 mb-4" enctype="multipart/form-data">
            <div class="titulo-form">
                <h2 class="titulo-form">Registro de Evento</h2>
                <p class="descrição-form">Insira as informações necessárias para realizar o cadastro do Evento</p>
            </div>

            <input type="hidden" name="modo" id="modo" value="cadastrar">
            <input type="hidden" name="id" id="evento-id">

            <div class="col-md-5">
                <h4 class="titulo-input-form">Nome do evento</h4>
                <input type="text" name="titulo" class="form-control" placeholder="Nome do Evento" required>
            </div>
            <div class="col-md-5">
                <h4 class="titulo-input-form">Foto do Evento</h4>
                <label for="input-file" class="label-file">
                    <div class="escolher-arquivo">Escolher Arquivo</div>
                    <p class="escolher-arquivo texto-escolher-file">Nenhum Arquivo Selecionado</p>
                </label>
                <input type="file" name="foto" class="form-control" id="input-file" placeholder="Imagem do Evento">
            </div>
            <div class="col-md-3">
                <h4 class="titulo-input-form">Data</h4>
                <input type="date" name="data" class="form-control" required>
            </div>
            <div class="col-md-3">
                <h4 class="titulo-input-form">Local do Evento</h4>
                <input type="text" name="local" class="form-control" placeholder="Local" required>
            </div>
            <div class="col-md-3">
                <h4 class="titulo-input-form">Horario</h4>
                <input type="time" name="hora" class="form-control" required>
            </div>
            <div class="col-md-3">
                <h4 class="titulo-input-form">Valor(R$)</h4>
                <input type="number" name="valor" class="form-control" placeholder="0,00" step="0.01" min="0" required>
            </div>
            <div class="col-md-1 botoes-form">
                <button class="form-submit fechar-form" type="button">Fechar</button>
                <button type="submit" class="btn btn-primary w-100 form-submit salvar-form">Salvar</button>
            </div>
        </form>
    </div>
    <div class="fade"></div>
</body>
</html>