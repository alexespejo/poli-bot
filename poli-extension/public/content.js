const article = document.querySelector("article");

if (article) {
 const text = article.textContent;
 console.log("found article react");
 chrome.runtime.sendMessage({ html: text });
} else {
 console.log("article not found");
}
