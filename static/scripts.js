// Theme management
const toastify = {
  show(message, type = 'success') {
      const toast = document.createElement('div');
      toast.className = `fixed top-4 right-4 p-4 rounded-lg shadow-lg ${
          type === 'success' ? 'bg-green-500' : 'bg-red-500'
      } text-white transform transition-all duration-300 translate-y-0 opacity-100`;
      toast.textContent = message;
      document.body.appendChild(toast);

      setTimeout(() => {
          toast.classList.add('translate-y-[-100%]', 'opacity-0');
          setTimeout(() => toast.remove(), 300);
      }, 3000);
  }
};

const themes = {
  light: {
      background: 'bg-gray-100',
      text: 'text-gray-900',
      card: 'bg-white'
  },
  dark: {
      background: 'bg-gray-900',
      text: 'text-gray-100',
      card: 'bg-gray-800'
  },
  blue: {
      background: 'bg-blue-100',
      text: 'text-blue-900',
      card: 'bg-white'
  }
};

function applyTheme(themeName) {
  const theme = themes[themeName];
  document.body.className = `${theme.background} ${theme.text}`;
  document.querySelectorAll('.theme-card').forEach(card => {
      card.className = `${theme.card} rounded-lg shadow-lg p-6`;
  });
}

document.addEventListener("DOMContentLoaded", () => {
  const themeToggle = document.getElementById("theme-toggle");
  const currentTheme = localStorage.getItem("theme") || "light";

  document.body.className = currentTheme;
  themeToggle.textContent = currentTheme === "light" ? "Modo Escuro" : "Modo Claro";

  themeToggle.addEventListener("click", () => {
      const newTheme = document.body.className === "light" ? "dark" : "light";
      document.body.className = newTheme;
      localStorage.setItem("theme", newTheme);
      themeToggle.textContent = newTheme === "light" ? "Modo Escuro" : "Modo Claro";
  });

  document.addEventListener("DOMContentLoaded", () => {
      // Add to cart functionality
      document.querySelectorAll(".add-to-cart").forEach((form) => {
          form.addEventListener("submit", (event) => {
              event.preventDefault();
              const formData = new FormData(form);

              fetch("/add_to_cart", {
                  method: "POST",
                  body: formData,
              })
                  .then((response) => response.json())
                  .then((data) => {
                      if (data.message) {
                          alert(data.message);
                          window.location.href = '/cart';
                      } else if (data.error) {
                          alert("Erro: " + data.error);
                      }
                  })
                  .catch((error) => {
                      console.error("Erro na requisição:", error);
                      alert("Ocorreu um erro ao adicionar ao carrinho.");
                  });
          });
      });

      // Remove from cart functionality
      document.querySelectorAll(".remove-item").forEach((form) => {
          form.addEventListener("submit", (event) => {
              event.preventDefault();
              const formData = new FormData(form);

              fetch("/remove_from_cart", {
                  method: "POST",
                  body: formData,
              })
                  .then((response) => response.json())
                  .then((data) => {
                      if (data.message) {
                          alert(data.message);
                          location.reload();
                      } else if (data.error) {
                          alert("Erro: " + data.error);
                      }
                  })
                  .catch((error) => {
                      console.error("Erro na requisição:", error);
                      alert("Ocorreu um erro ao remover do carrinho.");
                  });
          });
      });
  });});
