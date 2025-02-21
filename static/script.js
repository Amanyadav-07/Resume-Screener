document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    const progressBar = document.getElementById("progress-bar");
    const progressContainer = document.querySelector(".progress-container");

    form.addEventListener("submit", function (event) {
        event.preventDefault(); // Prevent default form submission

        progressContainer.style.display = "block"; // Show progress bar
        progressBar.style.width = "0%"; // Reset progress bar

        let progress = 0;
        let interval = setInterval(() => {
            progress += 10;
            progressBar.style.width = progress + "%";

            if (progress >= 100) {
                clearInterval(interval);
                form.submit(); // Submit the form after progress completes
            }
        }, 300);
    });

    // Smooth Fade-in Effect
    document.querySelectorAll(".fade-in").forEach((element, index) => {
        setTimeout(() => {
            element.style.opacity = 1;
            element.style.transform = "translateY(0)";
        }, index * 200);
    });
});
