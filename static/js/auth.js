const form = document.querySelector("form");
const message = document.getElementById("message");
form.addEventListener("submit", async (event) => {
  event.preventDefault(); message.textContent = "Проверка данных...";
  const values = Object.fromEntries(new FormData(form).entries());
  const register = form.id === "registerForm";
  try {
    await api(register ? "/api/auth/register" : "/api/auth/login", {method:"POST", body:JSON.stringify(values)});
    if (register) await api("/api/auth/login", {method:"POST", body:JSON.stringify(values)});
    location.href = "/";
  } catch (error) { message.textContent = error.message; }
});
