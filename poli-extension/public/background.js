console.log("react background do something");

function setupContextMenu() {
 chrome.contextMenus.create({
  id: "openSidePanel",
  title: "React Context Menue",
  contexts: ["selection"],
 });
}

chrome.runtime.onInstalled.addListener(() => {
 setupContextMenu();
 console.log("startup react");
});

chrome.sidePanel
 .setPanelBehavior({ openPanelOnActionClick: true })
 .catch((error) => console.error(error));

chrome.contextMenus.onClicked.addListener((info, tab) => {
 //  chrome.storage.session.set({ lastWord: info.selectionText });

 if (info.menuItemId === "openSidePanel") {
  chrome.sidePanel.open({ windowId: tab.windowId });
 }
});

let pageContent;
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
 console.log("chrome call made from react fend");

 if (message.html) {
  console.log(message.html);
  pageContent = message.html.substring(0, 500);
 }
 if (pageContent) {
  sendResponse(pageContent);
 } else {
  sendResponse("No article found");
 }
});
