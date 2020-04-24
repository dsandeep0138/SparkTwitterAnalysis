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
    $('#first').html("")
    $('#first').jQCloud(words_data, {
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
            $("#RawTweets").append("<div class=\"card\">" + item + "</div>");
    });
    }});
},5000);

setInterval(function(){
    $.ajax({url: '/word_counts', success: function(data) {
    console.log(data)
    var counts_data = $.parseJSON(data);
    var data = [
              {
                x: counts_data['words'],
                y: counts_data['counts'],
                type: 'bar'
              }
            ];

    $('#second').html("")
    $("#second").append("<h1>Bar chart will go here</h1>")
    $.each(counts_data, function(i, item) {
            $("#second").append(Plotly.newPlot('second', data));
    });
    }});
},5000);
