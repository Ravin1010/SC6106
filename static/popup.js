function popup(msg) {
    const p = document.createElement("div");

    p.innerHTML = msg + "<br><br><button onclick='this.parentElement.remove()'>OK</button>";

    p.style.position = "fixed";
    p.style.top = "50%";
    p.style.left = "50%";
    p.style.transform = "translate(-50%, -50%)";
    p.style.background = "white";
    p.style.padding = "15px";
    p.style.zIndex = "9999";
    p.style.borderRadius = "8px";
    p.style.boxShadow = "0 4px 10px rgba(0,0,0,0.2)";
    p.style.textAlign = "center";

    // 🔥 MOBILE FIXES
    p.style.maxWidth = "90%";
    p.style.width = "300px"; // fallback size
    p.style.boxSizing = "border-box";
    p.style.wordWrap = "break-word";
    p.style.overflowWrap = "break-word";
    p.style.maxHeight = "80vh";
    p.style.overflowY = "auto";

    document.body.appendChild(p);
}