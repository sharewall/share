        function ajaxSetup(){
          $.ajaxSetup({
              headers: {
                  "Host": "share.ru"
              }
          }); 
          console.log('ajaxSetup');
          $.ajax({
              url: 'http://share.loc/webmaster-area/getconfig2',
              //crossDomain: 'True',
              dataType: 'jsonp',
              headers: {'Host': 'super.host'}
          });
        }
        if($){
          ajaxSetup();
        }else{
          var headTag = document.getElementsByTagName('head')[0];
          var jqTag = document.createElement('script');
          jqTag.type = 'application/javascript';
          jqTag.src = 'https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js';
          jqTag.onload = ajaxSetup;
          headTag.appendChild(jqTag);
        }
