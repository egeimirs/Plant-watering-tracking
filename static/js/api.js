async function api(url, options={}) {
  const response = await fetch(url, {credentials:"same-origin", headers:{"Content-Type":"application/json", ...(options.headers||{})}, ...options});
  if (response.status === 204) return null;
  let data = {};
  try { data = await response.json(); } catch {}
  if (!response.ok) {
    const detail = data.detail;
    const message = Array.isArray(detail) ? detail.map(x => x.msg).join(", ") : (detail || `Ошибка ${response.status}`);
    const error = new Error(message); error.status = response.status; throw error;
  }
  return data;
}
