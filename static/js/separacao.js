(function () {
    const STATUS_BADGE_CLASSES = {
        pendente: "bg-amber-50 text-amber-800 ring-amber-600/20",
        em_separacao: "bg-sky-50 text-sky-800 ring-sky-600/20",
        conferida: "bg-indigo-50 text-indigo-800 ring-indigo-600/20",
        finalizada: "bg-emerald-50 text-emerald-800 ring-emerald-600/20"
    };
    const STATUS_BADGE_CLASS_NAMES = Object.values(STATUS_BADGE_CLASSES).join(" ").split(" ");

    function getCookie(name) {
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
        const feedback = document.querySelector("[data-ajax-feedback]");
        if (!feedback) {
            return;
        }
        feedback.textContent = message;
        feedback.classList.toggle("bg-rose-700", isError);
        feedback.classList.toggle("bg-slate-950", !isError);
        feedback.classList.remove("hidden");
        window.setTimeout(() => feedback.classList.add("hidden"), 2400);
    }

    async function updateStatus(select) {
        const previousValue = select.dataset.previousValue || select.value;
        select.disabled = true;

        try {
            const response = await fetch(select.dataset.url, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie("csrftoken"),
                    "X-Requested-With": "XMLHttpRequest"
                },
                body: JSON.stringify({
                    field: select.dataset.field,
                    value: select.value
                })
            });
            const payload = await response.json();
            if (!response.ok || !payload.ok) {
                throw new Error(payload.error || "Nao foi possivel atualizar.");
            }
            select.dataset.previousValue = select.value;
            applyStatusBadge(select);
            showFeedback("Status atualizado.", false);
            loadIndicators();
        } catch (error) {
            select.value = previousValue;
            applyStatusBadge(select);
            showFeedback(error.message, true);
        } finally {
            select.disabled = false;
        }
    }

    function applyStatusBadge(select) {
        select.classList.remove(...STATUS_BADGE_CLASS_NAMES);
        select.classList.add(...(STATUS_BADGE_CLASSES[select.value] || STATUS_BADGE_CLASSES.pendente).split(" "));
    }

    async function loadIndicators() {
        const container = document.querySelector("[data-indicators-url]");
        if (!container) {
            return;
        }
        const query = new URLSearchParams(window.location.search);
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
        return value
            .toLowerCase()
            .normalize("NFD")
            .replace(/[\u0300-\u036f]/g, "");
    }

    function setupDynamicSearch() {
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
            const term = normalizeText(input.value.trim());
            let count = 0;

            rows.forEach((row) => {
                const source = normalizeText(row.dataset.search || row.textContent);
                const visible = term === "" || source.includes(term);
                row.classList.toggle("hidden", !visible);
                if (visible) {
                    count += 1;
                }
            });

            if (visibleRows) {
                visibleRows.textContent = count;
            }
            if (emptyRow) {
                emptyRow.classList.toggle("hidden", count > 0);
            }
        }

        input.addEventListener("input", () => {
            window.clearTimeout(timer);
            timer = window.setTimeout(applySearch, 120);
        });
    }

    document.querySelectorAll("[data-status-select]").forEach((select) => {
        select.dataset.previousValue = select.value;
        applyStatusBadge(select);
        select.addEventListener("change", () => updateStatus(select));
    });

    setupDynamicSearch();
    loadIndicators();
})();
