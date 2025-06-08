// Backend/login.js
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('loginForm');
    const errorDiv = document.getElementById('errorMessage');

    form.addEventListener('submit', (event) => {
        event.preventDefault(); // Evita el envío por defecto del formulario

        const email = form.email.value.trim();
        const password = form.password.value;

        // Credenciales predeterminadas
        const validEmail = "juan.perez@example.com";
        const validPassword = "JuanPerez2024"; 

        if (email === validEmail && password === validPassword) {
            // Redirigir a la página de preferencias
            window.location.href = "../pages/Preferencias.html";
        } else {
            // Mostrar mensaje de error
            errorDiv.textContent = "Correo o contraseña incorrectos.";
            errorDiv.style.display = "block";
        }
    });
});
