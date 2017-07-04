function renderStatus(statusText) {
  document.getElementById('status').textContent = statusText;
}

// If clicked, get's the current url, if linkedin url, add's to my text file

chrome.tabs.query({ currentWindow: true, active: true }, function (tabs) {
    var url = tabs[0].url
    if (url.search('linkedin') != -1) {    
        renderStatus(url);    
        }
    else {
        renderStatus('FIX THE CODE!')
    }
    });
  
   // Add asp.net filesystem code here to save the linkedin url's in file; 
        // then with python, I can do the rest.. 
        
        
//       xhttp = new XMLHttpRequest();
//         xhttp.onreadystatechange = function() {
//             if (this.readyState == 4 && this.status == 200) {
//            // Typical action to be performed when the document is ready:
//            document.getElementById("demo").innerHTML = xhttp.responseText;
//             }
//         };
//         xhttp.open("GET", "filename", true);
//         xhttp.send();
//      
//     });
        