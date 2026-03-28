function popup(msg) {
    const p = document.createElement("div");
    p.innerHTML = msg + "<br><br><button onclick='this.parentElement.remove()'>OK</button>";
    p.style = "position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);background:white;padding:15px;z-index:9999;";
    document.body.appendChild(p);
}