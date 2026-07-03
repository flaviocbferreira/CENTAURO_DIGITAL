(function () {
    // IIFE evita variaveis globais e permite inicializar scripts do dashboard com seguranca.

    // Procura o elemento raiz do dashboard marcado no template com data-dashboard.
    const dashboardRoot = document.querySelector("[data-dashboard]");
    if (!dashboardRoot) {
        // Se o script for carregado em outra pagina, ele sai sem executar nada.
        return;
    }

    // Marca no DOM que o JavaScript do dashboard foi carregado.
    // Hoje e simples, mas deixa um ponto de extensao para futuras interacoes.
    dashboardRoot.dataset.ready = "true";
})();
