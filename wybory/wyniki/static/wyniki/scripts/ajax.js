function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);

            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$.ajaxSetup({ 
     beforeSend: function(xhr, settings) {
         if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         }
     } 
});

function modal_window(url, type, header) {
    $(type).click(function () {
        var criteria1 = $(this).text().trim()
        var criteria2 = 0
        var dane = criteria1
        var head = header
        if (type == ".rozmiar" && criteria1 != 'statki i zagranicza') {
            var numbers = criteria1.match(/\d+/g)
            criteria1 = []
            if (numbers.length == 2)
                criteria1 = numbers[0] + "" + numbers[1]
            else if (numbers.length == 4) {
                criteria1 = numbers[0] + "" + numbers[1]
                criteria2 = numbers[2] + "" + numbers[3]
            }
            else 
                criteria1 = numbers[0]
        }

        $.ajax({
            url : url,
            type : "POST",
            data : { nazwa: criteria1,
                     nazwa2: criteria2},

            success : function(json) {
                //W3SCHOOLS//
                var modal = document.getElementById('myModal');
                var content = document.getElementsByClassName('modal-body')[0]
                var span = document.getElementsByClassName("close")[0];
                var header = document.getElementById("modal-header-text").innerHTML = head + dane

                modal.style.display = "block";
                span.onclick = function() {
                    modal.style.display = "none";
                    while (content.firstChild) {
                        content.removeChild(content.firstChild);
                    }
                }
                window.onclick = function(event) {
                    if (event.target == modal) {
                        modal.style.display = "none";
                        while (content.firstChild) {
                            content.removeChild(content.firstChild);
                        }
                    }
                }
                var data = JSON.parse(json)
                console.log(data)
                for (i = 0; i < data.length; i++) {
                    var line = document.createElement("p")
                    line.innerHTML = data[i][0]
                    content.appendChild(line)
                }
            }
        });
    })
}

$(document).ready(function(){
    modal_window("wojewodztwo", ".name", "Dane dla: ")
    modal_window("typ", ".typ", "Dane dla: ")
    modal_window("rozmiar", ".rozmiar", "Dane dla gmin z przedzialu ")
});