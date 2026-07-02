(function () {
    const dashboardRoot = document.querySelector("[data-dashboard]");
    if (!dashboardRoot) {
        return;
    }

    dashboardRoot.dataset.ready = "true";
})();
