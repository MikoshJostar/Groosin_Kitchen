document.addEventListener("DOMContentLoaded", function () {
  var assistant = document.getElementById("assistant");
  var bubble = document.getElementById("assistant-bubble");
  if (!assistant || !bubble) return;

  var dishes = [];
  try {
    dishes = JSON.parse(document.getElementById("dishes-data").textContent);
  } catch (e) {
    dishes = [];
  }

  var isDragging = false;
  var didDrag = false;
  var startX, startY, startLeft, startTop;
  var DRAG_THRESHOLD = 5; // px — щоб відрізнити клік від перетягування

  function setPosition(x, y) {
    var w = window.innerWidth;
    var h = window.innerHeight;
    var size = assistant.offsetWidth;
    x = Math.max(0, Math.min(x, w - size));
    y = Math.max(0, Math.min(y, h - size));
    assistant.style.left = x + "px";
    assistant.style.top = y + "px";
    assistant.style.right = "auto";
    assistant.style.bottom = "auto";
  }

  function getPointer(e) {
    if (e.touches && e.touches.length) {
      return { x: e.touches[0].clientX, y: e.touches[0].clientY };
    }
    return { x: e.clientX, y: e.clientY };
  }

  function onPointerDown(e) {
    isDragging = true;
    didDrag = false;
    assistant.classList.remove("bounce");
    var p = getPointer(e);
    var rect = assistant.getBoundingClientRect();
    startX = p.x;
    startY = p.y;
    startLeft = rect.left;
    startTop = rect.top;
    document.addEventListener("mousemove", onPointerMove);
    document.addEventListener("mouseup", onPointerUp);
    document.addEventListener("touchmove", onPointerMove, { passive: false });
    document.addEventListener("touchend", onPointerUp);
    e.preventDefault();
  }

  function onPointerMove(e) {
    if (!isDragging) return;
    var p = getPointer(e);
    var dx = p.x - startX;
    var dy = p.y - startY;
    if (Math.abs(dx) > DRAG_THRESHOLD || Math.abs(dy) > DRAG_THRESHOLD) {
      didDrag = true;
      hideBubble();
    }
    setPosition(startLeft + dx, startTop + dy);
    if (e.cancelable) e.preventDefault();
  }

  function onPointerUp() {
    isDragging = false;
    document.removeEventListener("mousemove", onPointerMove);
    document.removeEventListener("mouseup", onPointerUp);
    document.removeEventListener("touchmove", onPointerMove);
    document.removeEventListener("touchend", onPointerUp);

    if (!didDrag) {
      toggleBubble();
    }
  }

  function pickRandomDish() {
    if (!dishes.length) return null;
    return dishes[Math.floor(Math.random() * dishes.length)];
  }

  function showBubble() {
    var dish = pickRandomDish();
    if (!dish) {
      bubble.innerHTML =
        '<strong>Порада шеф-кухаря</strong>' +
        'Наразі меню порожнє — зазирніть трохи пізніше!';
    } else {
      bubble.innerHTML =
        '<strong>Раджу сьогодні скуштувати</strong>' +
        '<span class="dish-name">' + escapeHtml(dish.name) + '</span><br>' +
        (dish.description ? '<span>' + escapeHtml(dish.description) + '</span><br>' : '') +
        '<span class="dish-price">' + escapeHtml(dish.price) + ' грн</span>';
    }

    positionBubble();
    bubble.style.display = "block";
  }

  function hideBubble() {
    bubble.style.display = "none";
  }

  function toggleBubble() {
    if (bubble.style.display === "block") {
      hideBubble();
    } else {
      showBubble();
    }
  }

  function positionBubble() {
    var rect = assistant.getBoundingClientRect();
    bubble.style.display = "block"; // тимчасово, щоб дізнатись розміри
    var bubbleWidth = bubble.offsetWidth;
    var bubbleHeight = bubble.offsetHeight;

    var left = rect.left + rect.width / 2 - bubbleWidth / 2;
    var top = rect.top - bubbleHeight - 18;

    left = Math.max(8, Math.min(left, window.innerWidth - bubbleWidth - 8));
    if (top < 8) {
      // якщо над помічником не вистачає місця — показуємо збоку
      top = rect.top;
      left = rect.left - bubbleWidth - 18;
      if (left < 8) left = rect.right + 18;
    }

    bubble.style.left = left + "px";
    bubble.style.top = top + "px";
  }

  function escapeHtml(str) {
    var div = document.createElement("div");
    div.textContent = str;
    return div.innerHTML;
  }

  assistant.addEventListener("mousedown", onPointerDown);
  assistant.addEventListener("touchstart", onPointerDown, { passive: false });

  window.addEventListener("resize", function () {
    if (bubble.style.display === "block") positionBubble();
  });

  // легка анімація "дихання", щоб привернути увагу, поки з ним не взаємодіяли
  setTimeout(function () {
    assistant.classList.add("bounce");
  }, 1500);
});
