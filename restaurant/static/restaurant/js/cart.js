(function () {
  var KEY = "gk_cart";
  var cart = {}; // id -> {id,name,price,qty}
  try { cart = JSON.parse(localStorage.getItem(KEY)) || {}; } catch (e) { cart = {}; }

  var backdrop = document.getElementById("modal-backdrop");
  var body = document.getElementById("modal-body");
  var countEl = document.getElementById("cart-count");

  function save() { try { localStorage.setItem(KEY, JSON.stringify(cart)); } catch (e) {} updateCount(); }
  function count() { return Object.values(cart).reduce(function (s, i) { return s + i.qty; }, 0); }
  function total() { return Object.values(cart).reduce(function (s, i) { return s + i.qty * i.price; }, 0); }
  function updateCount() { countEl.textContent = count(); }
  function esc(s) { var d = document.createElement("div"); d.textContent = s; return d.innerHTML; }
  function money(n) { return (Math.round(n * 100) / 100).toString().replace(".", ",") + " ₴"; }
  function open(html) { body.innerHTML = html; backdrop.hidden = false; }
  function close() { backdrop.hidden = true; }

  function cardData(card) {
    return { id: card.dataset.id, name: card.dataset.name, price: parseFloat(card.dataset.price),
             desc: card.dataset.desc, image: card.dataset.image };
  }
  function add(d, qty) {
    if (!cart[d.id]) cart[d.id] = { id: d.id, name: d.name, price: d.price, qty: 0 };
    cart[d.id].qty = Math.min(50, cart[d.id].qty + qty);
    save();
  }

  function showDetail(card) {
    var d = cardData(card), q = 1;
    open((d.image ? '<img class="detail-img" src="' + esc(d.image) + '" alt="">' : '') +
      "<h3>" + esc(d.name) + "</h3><p>" + esc(d.desc) + "</p><p><b>" + money(d.price) + "</b></p>" +
      '<div class="qty"><button type="button" id="q-minus">−</button><span id="q-val">1</span><button type="button" id="q-plus">+</button></div>' +
      '<div><button type="button" class="btn" id="q-add">Додати в кошик</button></div>');
    document.getElementById("q-minus").onclick = function () { q = Math.max(1, q - 1); document.getElementById("q-val").textContent = q; };
    document.getElementById("q-plus").onclick = function () { q = Math.min(50, q + 1); document.getElementById("q-val").textContent = q; };
    document.getElementById("q-add").onclick = function () { add(d, q); showCart(); };
  }

  function showCart() {
    var items = Object.values(cart);
    if (!items.length) { open("<h3>Кошик</h3><p>Кошик порожній. Оберіть страви з меню 🍷</p>"); return; }
    var rows = items.map(function (i) {
      return '<div class="cart-row"><div>' + esc(i.name) + '<br><small>' + money(i.price) + '</small></div>' +
        '<div class="qty"><button type="button" data-dec="' + i.id + '">−</button><span>' + i.qty +
        '</span><button type="button" data-inc="' + i.id + '">+</button></div></div>';
    }).join("");
    open("<h3>Ваше замовлення</h3>" + rows + '<div class="cart-total">Разом: ' + money(total()) + "</div>" +
      '<button type="button" class="btn" id="to-checkout">Оформити замовлення</button> ' +
      '<button type="button" class="btn secondary" id="to-menu">Продовжити вибір</button>');
    document.getElementById("to-menu").onclick = close;
    document.getElementById("to-checkout").onclick = showCheckout;
  }

  function showCheckout() {
    open('<h3>Оформлення</h3><form id="order-form">' +
      '<label>Ім\'я<input name="name" required maxlength="100"></label>' +
      '<label>Телефон<input name="phone" type="tel" required minlength="6" maxlength="30"></label>' +
      '<label>Коментар (адреса, побажання)<textarea name="comment" rows="3" maxlength="1000"></textarea></label>' +
      '<div class="cart-total">Разом: ' + money(total()) + '</div>' +
      '<div class="form-error" id="form-error"></div>' +
      '<button type="submit" class="btn">Підтвердити замовлення</button> ' +
      '<button type="button" class="btn secondary" id="back-cart">Назад</button></form>');
    document.getElementById("back-cart").onclick = showCart;
    document.getElementById("order-form").onsubmit = function (e) {
      e.preventDefault();
      var f = e.target, err = document.getElementById("form-error");
      var btn = f.querySelector("button[type=submit]"); btn.disabled = true;
      fetch("/order/", {
        method: "POST",
        headers: { "Content-Type": "application/json",
                   "X-CSRFToken": document.querySelector('meta[name=csrf-token]').content },
        body: JSON.stringify({ name: f.name.value, phone: f.phone.value, comment: f.comment.value,
          items: Object.values(cart).map(function (i) { return { id: i.id, qty: i.qty }; }) })
      }).then(function (r) { return r.json().then(function (j) { return { ok: r.ok, j: j }; }); })
        .then(function (res) {
          if (!res.ok) { err.textContent = res.j.error || "Помилка"; btn.disabled = false; return; }
          cart = {}; save();
          open('<div class="toast-ok"><h3>Дякуємо! 🎉</h3><p>Замовлення №' + res.j.order_id +
               ' прийнято. Сума: ' + money(parseFloat(res.j.total)) + '.<br>Ми зв\'яжемося з вами за телефоном.</p></div>');
        })
        .catch(function () { err.textContent = "Помилка з'єднання, спробуйте ще раз"; btn.disabled = false; });
    };
  }

  document.addEventListener("click", function (e) {
    var t = e.target;
    if (t.closest("#cart-fab")) return showCart();
    if (t.closest(".modal-close") || t === backdrop) return close();
    var dec = t.closest("[data-dec]"), inc = t.closest("[data-inc]");
    if (dec) { var i = cart[dec.dataset.dec]; i.qty--; if (i.qty < 1) delete cart[i.id]; save(); return showCart(); }
    if (inc) { cart[inc.dataset.inc].qty = Math.min(50, cart[inc.dataset.inc].qty + 1); save(); return showCart(); }
    var addBtn = t.closest(".add-btn");
    if (addBtn) {
      e.stopPropagation();
      add(cardData(addBtn.closest(".food-card")), 1);
      addBtn.textContent = "✓ Додано";
      setTimeout(function () { addBtn.textContent = "+ Додати в кошик"; }, 1000);
      return;
    }
    var card = t.closest(".food-card.clickable");
    if (card) showDetail(card);
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") close();
    if (e.key === "Enter" && e.target.classList && e.target.classList.contains("food-card")) showDetail(e.target);
  });
  updateCount();
})();
