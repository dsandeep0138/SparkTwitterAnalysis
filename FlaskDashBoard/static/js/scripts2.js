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
    $("#RawTweets").append("<h3><center>Most Relevant Tweets</center></h3>")
    $.each(tweets_data, function(i, item) {
            $("#RawTweets").append("<div class=\"card\">" + item + "</div>");
    });
    }});
},5000);


setInterval(function(){
    $.ajax({url: '/word_counts', success: function(data) {
        var counts_data = $.parseJSON(data);
        var data = [{
		x: counts_data['words'],
		y: counts_data['counts'],
		type: 'bar'
        }];

        var layout = {
		title: 'Most used terms',
        };

        Plotly.newPlot('second', data, layout);
    }});
},5000);


setInterval(function(){
    $.ajax({url: '/graph', success: function(data) {
        var graphs = $.parseJSON(data);
        var layout = {
		title: 'Tweets from April 1 to April 3!',
		font: {size: 10},
		showlegend: false,
        };

        var config = {responsive: true};
        Plotly.newPlot('third', graphs, layout, config);
    }});
}, 5000);


setInterval(function(){
    $.ajax({
	url: '/sentiments',
	success: function(data) {
		$("#total_counter_value").html(data['total'])
		$("#positive_counter").html(data['positive'] + " %")
		$("#neutral_counter").html(data['neutral'] + " %")
		$("#negative_counter").html(data['negative'] + " %")
	}
    });
},5000);
