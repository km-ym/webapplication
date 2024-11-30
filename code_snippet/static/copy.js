function createCopyButton(highlightDiv) {
    const button = document.createElement("button");
    button.className = "copy-code-button";
    button.innerText = "Copy";
    button.addEventListener("click", () => copyCodeToClipboard(button, highlightDiv));
    highlightDiv.appendChild(button);
  }
  async function copyCodeToClipboard(button, highlightDiv) {
    const codeToCopy = highlightDiv.querySelector("pre.chroma > code[data-lang]").innerText.replace(/\n\n/g,"\n");
    await navigator.clipboard.writeText(codeToCopy).then (() => {
      button.blur();
      button.innerText = "Copied!";
      setTimeout(function() {
        button.innerText = "Copy";
      }, 2000); 
    });
  }
  document.querySelectorAll(".highlight")
    .forEach(highlightDiv => createCopyButton(highlightDiv));