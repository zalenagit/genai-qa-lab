// Shared helpers for the ZY Demo Store pages.
const Store = {
  token: () => sessionStorage.getItem("token"),
  cart: () => JSON.parse(sessionStorage.getItem("cart") || "{}"),
  saveCart: (cart) => sessionStorage.setItem("cart", JSON.stringify(cart)),
  cartCount() { return Object.values(this.cart()).reduce((a, b) => a + b, 0); },
  requireLogin() { if (!this.token()) location.href = "index.html"; },
  async api(path, options = {}) {
    const headers = { "Content-Type": "application/json" };
    if (this.token()) headers.Authorization = "Bearer " + this.token();
    const res = await fetch(path, { ...options, headers });
    const body = res.status === 204 ? null : await res.json();
    return { status: res.status, body };
  },
  renderBadge() {
    const el = document.querySelector("[data-testid=cart-count]");
    if (el) el.textContent = this.cartCount();
  },
};
const money = (n) => "$" + n.toFixed(2);
