export async function grabArticle() {
 const response = await chrome.runtime.sendMessage("articles?");
 return response;
}
