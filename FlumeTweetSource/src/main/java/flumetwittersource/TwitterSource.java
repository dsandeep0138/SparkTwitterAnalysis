package flumetwittersource;

import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.Map;

import org.apache.flume.Context;
import org.apache.flume.Event;
import org.apache.flume.EventDrivenSource;
import org.apache.flume.channel.ChannelProcessor;
import org.apache.flume.conf.Configurable;
import org.apache.flume.event.EventBuilder;
import org.apache.flume.source.AbstractSource;

import twitter4j.FilterQuery;
import twitter4j.StallWarning;
import twitter4j.Status;
import twitter4j.StatusDeletionNotice;
import twitter4j.StatusListener;
import twitter4j.TwitterStream;
import twitter4j.TwitterStreamFactory;
import twitter4j.conf.ConfigurationBuilder;
import twitter4j.json.DataObjectFactory;
import java.util.Random;
public class TwitterSource extends AbstractSource implements EventDrivenSource, Configurable {

    private String consumerKey;
    private String consumerSecret;
    private String accessToken;
    private String accessTokenSecret;

    private String[] keywords;

    private TwitterStream twitterStream;
    private Random random = new Random();
    @Override
    public void configure(Context context) {
        consumerKey = context.getString("consumerKey");
        consumerSecret = context.getString("consumerSecret");
        accessToken = context.getString("accessToken");
        accessTokenSecret = context.getString("accessTokenSecret");

        String keywordString = context.getString("keyWords", "");
        keywords = keywordString.split(",");

        ConfigurationBuilder cb = new ConfigurationBuilder();
        cb.setDebugEnabled(true)
                .setOAuthConsumerKey(consumerKey)
                .setOAuthConsumerSecret(consumerSecret)
                .setOAuthAccessToken(accessToken)
                .setOAuthAccessTokenSecret(accessTokenSecret)
                .setJSONStoreEnabled(true);

        twitterStream = new TwitterStreamFactory(cb.build()).getInstance();
    }

    @Override
    public void start() {

        final ChannelProcessor channel = getChannelProcessor();
        final Map<String, String> headers = new HashMap<String, String>();

        StatusListener listener = new StatusListener() {

            public void onStatus(Status status) {
                headers.put("timestamp", String.valueOf(status.getCreatedAt().getTime()));
                try {
                    Event event = EventBuilder.withBody(
                            DataObjectFactory.getRawJSON(status).getBytes(StandardCharsets.UTF_8), headers);
                    channel.processEvent(event);
                    Thread.sleep(2000);
                } catch (Exception e) {
                    System.out.println("Couldn't sleep");
                    throw new RuntimeException("Got exception in thread sleep");
                }
            }

            public void onDeletionNotice(StatusDeletionNotice statusDeletionNotice) {
            }

            public void onTrackLimitationNotice(int numberOfLimitedStatuses) {
            }

            public void onScrubGeo(long arg0, long arg1) {
            }

            public void onStallWarning(StallWarning arg0) {
            }

            public void onException(Exception ex) {
                System.out.println("Error while listening to Twitter stream.");
            }
        };
        twitterStream.addListener(listener);
        System.out.println("Starting up Twitter filtering...");
        FilterQuery query = new FilterQuery();
        if (keywords.length > 0) query.track(keywords);
        query.language("en");
        twitterStream.filter(query);
        super.start();
    }

}
