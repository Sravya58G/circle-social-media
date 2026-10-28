document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("textarea").forEach(area => {
    area.addEventListener("input", () => {
      area.style.height = "auto";
      if (area.scrollHeight < 300) area.style.height = area.scrollHeight + "px";
    });
  });
});
