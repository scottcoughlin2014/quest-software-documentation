var html = '<div class="container-fluid">';
html += '<div class="row">';
html += '<div class="col-sm-1"></div>';
html += '<div class="col-sm-9">';
html += '<div class="accordion" id="accordionExample">';
html += '</div>';
html += '</div>';
html += '</div>';
html += '</div>';


$(document).ready(function(){   
    $.ajax({ 
    type: 'GET', 
    url: 'https://scottcoughlin2014.github.io/quest-software-documentation/module.json', 
    dataType: 'json',
    success: function (data) {    /* Here data length is 5*/


         $('#page-content').prepend(html);

         for(var i=0;i<data.length;i++){
            console.log(data[i].fields.name);
            var elem = document.createElement('button');
            elem.className = 'btn btn-link collapsed';
            elem.innerText = data[i].fields.name;
            $("#accordionExample").append(elem);
         }

    }
});
});
