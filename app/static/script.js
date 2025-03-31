document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("submitbtn").addEventListener("click", function () {
        // Получаем введенный пользователем код
        const secretValue = document.getElementById("secret").value;

        // Отправляем запрос на сервер для проверки кода
        fetch("/check_secret", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ secret: secretValue })
        })
        .then(response => response.json()) // Преобразуем ответ в JSON
        .then(data => {
            if (data.success) {
                // Если код верный, создаем ссылку для скачивания и эмулируем клик
                const downloadLink = document.createElement("a");
                downloadLink.href = data.download_url;
                downloadLink.style.display = "none";
                document.body.appendChild(downloadLink);
                downloadLink.click();
                document.body.removeChild(downloadLink);
            }
        })
        .catch(error => console.error("Ошибка:", error));
    });
});