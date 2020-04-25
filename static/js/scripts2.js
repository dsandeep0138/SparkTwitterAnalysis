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
    var words_data = $.parseJSON(data);
    $('#first').html("")
    $('#first').jQCloud(words_data, {
               autoResize: true
       });
    }});
},5000);


setInterval(function(){
    $.ajax({url: '/tweets', success: function(data) {
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
    var counts_data = $.parseJSON(data);
    $('#second').html("")
    $("#second").append("<h1>Bar chart will go here</h1>")
    $.each(counts_data, function(i, item) {
            $("#second").append("<p>" + item + "</p>");
    });
    }});
},5000);


setInterval(function(){
    $.ajax({
	url: '/sentiments',
	success: function(data) {
		console.log(data)
		$("#total_counter_value").html(data['total'])
		$("#positive_counter").html(data['positive'] + " %")
		$("#neutral_counter").html(data['neutral'] + " %")
		$("#negative_counter").html(data['negative'] + " %")
	}
    });
},5000);
