(function () {
    // IIFE: envolve todo o script para nao criar variaveis globais no navegador.

    // Mapa das classes Tailwind aplicadas ao select conforme o status operacional escolhido.
    const STATUS_BADGE_CLASSES = {
        pendente: "bg-amber-50 text-amber-800 ring-amber-600/20",
        em_separacao: "bg-sky-50 text-sky-800 ring-sky-600/20",
        conferida: "bg-indigo-50 text-indigo-800 ring-indigo-600/20",
        finalizada: "bg-emerald-50 text-emerald-800 ring-emerald-600/20"
    };
    // Lista plana de todas as classes possiveis; usada para limpar o estilo antigo antes de aplicar o novo.
    const STATUS_BADGE_CLASS_NAMES = Object.values(STATUS_BADGE_CLASSES).join(" ").split(" ");

    function getCookie(name) {
        // Le um cookie pelo nome. O Django grava o token CSRF no cookie csrftoken.
        const cookies = document.cookie ? document.cookie.split(";") : [];
        for (const cookie of cookies) {
            const trimmed = cookie.trim();
            if (trimmed.startsWith(`${name}=`)) {
                return decodeURIComponent(trimmed.slice(name.length + 1));
            }
        }
        return "";
    }

    function showFeedback(message, isError) {
        // Exibe uma pequena mensagem no canto da tela apos uma acao AJAX.
        const feedback = document.querySelector("[data-ajax-feedback]");
        if (!feedback) {
            return;
        }
        feedback.textContent = message;
        // Alterna a cor entre erro e sucesso/informacao.
        feedback.classList.toggle("bg-rose-700", isError);
        feedback.classList.toggle("bg-slate-950", !isError);
        feedback.classList.remove("hidden");
        window.setTimeout(() => feedback.classList.add("hidden"), 2400);
    }

    async function updateStatus(select) {
        // Guarda o valor anterior para reverter a UI se a API devolver erro.
        const previousValue = select.dataset.previousValue || select.value;
        select.disabled = true;

        try {
            // Envia POST JSON para a rota data-url criada no template.
            const response = await fetch(select.dataset.url, {
                method: "POST",
                headers: {
                    // Indica que o corpo da requisicao e JSON.
                    "Content-Type": "application/json",
                    // Token CSRF exigido pelo Django para aceitar POST autenticado.
                    "X-CSRFToken": getCookie("csrftoken"),
                    // Identificador comum para views reconhecerem chamada AJAX, se precisarem.
                    "X-Requested-With": "XMLHttpRequest"
                },
                body: JSON.stringify({
                    // data-field informa qual campo do model sera alterado.
                    field: select.dataset.field,
                    // select.value e o novo status escolhido pelo usuario.
                    value: select.value
                })
            });
            // Converte a resposta JSON da view atualizar_status_json em objeto JavaScript.
            const payload = await response.json();
            if (!response.ok || !payload.ok) {
                throw new Error(payload.error || "Nao foi possivel atualizar.");
            }
            select.dataset.previousValue = select.value;
            applyStatusBadge(select);
            showFeedback("Status atualizado.", false);
            // Recalcula os indicadores porque mudar status pode alterar os cards.
            loadIndicators();
        } catch (error) {
            // Em erro de rede, permissao ou validacao, voltamos o select para o valor antigo.
            select.value = previousValue;
            applyStatusBadge(select);
            showFeedback(error.message, true);
        } finally {
            select.disabled = false;
        }
    }

    function applyStatusBadge(select) {
        // Remove classes antigas de cor e aplica a cor correspondente ao valor atual.
        select.classList.remove(...STATUS_BADGE_CLASS_NAMES);
        select.classList.add(...(STATUS_BADGE_CLASSES[select.value] || STATUS_BADGE_CLASSES.pendente).split(" "));
    }

    async function loadIndicators() {
        // Busca os numeros dos cards superiores respeitando os filtros atuais da URL.
        const container = document.querySelector("[data-indicators-url]");
        if (!container) {
            return;
        }
        const query = new URLSearchParams(window.location.search);
        // Indicadores nao dependem da pagina atual da paginacao.
        query.delete("page");

        try {
            const response = await fetch(`${container.dataset.indicatorsUrl}?${query.toString()}`, {
                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                }
            });
            const payload = await response.json();
            if (!response.ok || !payload.ok) {
                return;
            }
            Object.entries(payload.indicadores).forEach(([key, value]) => {
                // Cada card possui data-indicator="nome"; aqui atualizamos o texto do card certo.
                const target = document.querySelector(`[data-indicator="${key}"]`);
                if (target) {
                    target.textContent = value;
                }
            });
        } catch (error) {
            showFeedback("Indicadores indisponiveis.", true);
        }
    }

    function normalizeText(value) {
        // Normaliza texto para pesquisa: minusculo e sem acentos.
        return value
            .toLowerCase()
            .normalize("NFD")
            .replace(/[\u0300-\u036f]/g, "");
    }

    function setupDynamicSearch() {
        // Configura a pesquisa instantanea da tabela exibida na pagina atual.
        const input = document.querySelector("[data-datatable-search]");
        const rows = Array.from(document.querySelectorAll("[data-datatable-row]"));
        const emptyRow = document.querySelector("[data-datatable-empty]");
        const visibleRows = document.querySelector("[data-visible-rows]");
        let timer = null;

        if (!input || rows.length === 0) {
            return;
        }

        // A busca local atende a listagem atual; data-search-url aponta para a evolucao AJAX.
        function applySearch() {
            // term e o texto digitado pelo usuario ja normalizado.
            const term = normalizeText(input.value.trim());
            let count = 0;

            rows.forEach((row) => {
                // data-search foi preenchido no template com campos importantes da separacao.
                const source = normalizeText(row.dataset.search || row.textContent);
                const visible = term === "" || source.includes(term);
                // hidden oculta a linha sem remover o elemento do DOM.
                row.classList.toggle("hidden", !visible);
                if (visible) {
                    count += 1;
                }
            });

            if (visibleRows) {
                // Atualiza o contador "visiveis / total".
                visibleRows.textContent = count;
            }
            if (emptyRow) {
                // Mostra uma linha de estado vazio quando nada bate com a pesquisa.
                emptyRow.classList.toggle("hidden", count > 0);
            }
        }

        input.addEventListener("input", () => {
            // Pequeno debounce para nao recalcular a tabela a cada tecla instantaneamente.
            window.clearTimeout(timer);
            timer = window.setTimeout(applySearch, 120);
        });
    }

    // Para cada select de status renderizado na tabela, guarda valor inicial e liga o evento change.
    document.querySelectorAll("[data-status-select]").forEach((select) => {
        select.dataset.previousValue = select.value;
        applyStatusBadge(select);
        select.addEventListener("change", () => updateStatus(select));
    });

    // Inicializa pesquisa e indicadores quando a pagina termina de carregar o script.
    setupDynamicSearch();
    loadIndicators();
})();
