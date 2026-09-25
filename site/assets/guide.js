document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".code .copy").forEach((button) => {
    button.addEventListener("click", async () => {
      const code = button.closest(".code").querySelector("pre code").innerText;
      try {
        await navigator.clipboard.writeText(code);
        button.textContent = "Скопировано";
      } catch {
        button.textContent = "Не вышло";
      }
      button.classList.add("is-done");
      setTimeout(() => {
        button.textContent = "Копировать";
        button.classList.remove("is-done");
      }, 1600);
    });
  });

  const drawer = document.getElementById("drawer");
  drawer?.querySelectorAll("a").forEach((a) => {
    a.addEventListener("click", () => drawer.hidePopover?.());
  });

  const links = new Map();
  document.querySelectorAll(".toc ol a").forEach((a) => {
    const id = decodeURIComponent(a.hash.slice(1));
    links.set(id, [...(links.get(id) ?? []), a]);
  });
  const headings = [...document.querySelectorAll("main h3[id]")];
  if (!headings.length || !("IntersectionObserver" in window)) return;

  const visible = new Set();
  const update = () => {
    const current = headings.filter((h) => visible.has(h)).at(0)
      ?? headings.filter((h) => h.getBoundingClientRect().top < 0).at(-1);
    links.forEach((list) => list.forEach((a) => a.classList.remove("is-active")));
    links.get(current?.id)?.forEach((a) => a.classList.add("is-active"));
  };
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((e) => (e.isIntersecting ? visible.add(e.target) : visible.delete(e.target)));
    update();
  }, { rootMargin: "0px 0px -60% 0px" });
  headings.forEach((h) => observer.observe(h));
});
