const btn =document.getElementById("summarize");
btn.addEventListener("click", function() {
    btn.disabled = true;
    btn.innerHTML = "Summarizing....";
    chrome.tabs.query({currentWindow: true, active: true}, function(tabs){
        var video_url = tabs[0].url;
        var xhr = new XMLHttpRequest();
        xhr.open("GET", "http://localhost:5000/api/summarize?youtube_url=" + video_url, true);
        xhr.onload = function() {
            var text = xhr.responseText;
            const p = document.getElementById("output");
            p.innerHTML = text;
            btn.disabled = false;
            btn.innerHTML = "Summarize";
        }
        xhr.send();
    });

});