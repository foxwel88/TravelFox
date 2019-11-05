
chrome.extension.onMessage.addListener(
function(request, sender, sendMessage) {
    if (request.greeting == "hello") {
        var node1=document.querySelector('#authentication > tbody > tr:nth-child(5) > th:nth-child(1)').innerHTML;var node1_i=node1[1].charCodeAt()-65;var node1_j=node1[3].charCodeAt()-49;
        var node2=document.querySelector('#authentication > tbody > tr:nth-child(6) > th:nth-child(1)').innerHTML;var node2_i=node2[1].charCodeAt()-65;var node2_j=node2[3].charCodeAt()-49;
        var node3=document.querySelector('#authentication > tbody > tr:nth-child(7) > th:nth-child(1)').innerHTML;var node3_i=node3[1].charCodeAt()-65;var node3_j=node3[3].charCodeAt()-49;
        sendMessage([node1_i,node1_j,node2_i,node2_j,node3_i,node3_j]);
    }
});