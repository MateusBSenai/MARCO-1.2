<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="/agenda-de-eventos/assets/css/login.css?v=1">
    <link rel="icon" href="/agenda-de-eventos/assets/icons/logo_temporaria.png">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Agenda de Eventos</title>
</head>
<body>
    <div class="login-container">
        <div class="magnus-logo">
            <img src="/agenda-de-eventos/assets/icons/logo_temporaria.png" alt="logo">
            <h3 class="magnus">Magnus</h3>
        </div>
        
        <h2>Login</h2>
        <form method="POST">
            <div class="inputs">
                <h4 class="marcador-inputs">Digite seu Email</h4>
                <input type="text" class="input-login" name="email" placeholder="email@email.com">
                <h4 class="marcador-inputs">Digite sua Senha</h4>
                <input type="password" class="senha-adm input-login" name="senha" placeholder="Senha">
            </div>
            <button class="entrar-login" type="submit" name="entrar">Entrar</button>
            <h5 class="alerta-login" value="erro" name="erro">
                <?php 
                    echo $_SESSION['erro_login'] ?? '';
                    unset($_SESSION['erro_login']);
                ?>
            </h5>
        </form>
    </div>
</body>
</html>