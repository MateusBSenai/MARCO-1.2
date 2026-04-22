const fileInput = document.querySelector("#input-file")
const pTexto = document.querySelector(".texto-escolher-file")

fileInput.addEventListener("change", () => {
    pTexto.textContent = fileInput.files[0].name;
})

const modalLateral = document.querySelector(".modal-lateral")
const fecharBotao = document.querySelector(".form-submit")
const openAddEvento = document.querySelector(".open-add-evento")
const formModal = document.querySelector(".modal-lateral form")

openAddEvento.addEventListener("click", () => {
    formModal.reset()
    document.querySelector("#modo").value = "cadastrar"
    document.querySelector("#evento-id").value = ""

    modalLateral.style.animation = "deslizarParaDentro 0.5s forwards"
})

fecharBotao.addEventListener("click", () => {
    modalLateral.style.animation = "deslizarParaFora 0.5s forwards";
})

const botoesEditar = document.querySelectorAll(".editar-elemento")

botoesEditar.forEach(botao => {
    botao.addEventListener("click", () => {
        console.log(`${botao.dataset.titulo}`)
        document.querySelector("#evento-id").value = botao.dataset.id
        document.querySelector("input[name='titulo']").value = botao.dataset.titulo
        document.querySelector("input[name='data']").value = botao.dataset.data
        document.querySelector("input[name='local']").value = botao.dataset.local
        document.querySelector("input[name='hora']").value = botao.dataset.hora
        document.querySelector("input[name='valor']").value = botao.dataset.valor

        document.querySelector("#modo").value = "editar"

        modalLateral.style.animation = "deslizarParaDentro 0.5s forwards"
    })
})