$(document).ready(function () {
   $.ajax({url: '/word_cloud', success: function (data) {
       var words_data = $.parseJSON(data);
       $('#div1').jQCloud(words_data, {
           autoResize: true
       });
   }});
});


setInterval(function(){
    $.ajax({url: '/word_cloud', success: function(data) {
    console.log(data)
    var words_data = $.parseJSON(data);
    $('#div1').html("")
    $('#div1').jQCloud(words_data, {
               autoResize: true
       });
    }});
},5000);

setInterval(function(){
    $.ajax({url: '/tweets', success: function(data) {
    console.log(data)
    var tweets_data = $.parseJSON(data);
    $('#RawTweets').html("")
    $("#RawTweets").append("<h1>Raw Tweets</h1>")
    $.each(tweets_data, function(i, item) {
            $("#RawTweets").append("<p>" + item + "</p>");
    });
    }});
},5000);