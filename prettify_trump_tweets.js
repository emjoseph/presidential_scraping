function sleep(ms){
    return new Promise(resolve=>{
        setTimeout(resolve,ms)
    })
}

(async () => {


    const fs = require('fs')
    const Sentiment = require('sentiment')
    let sentiment = new Sentiment()

    let perspective_key = ""

    const Perspective = require('perspective-api-client');
    const perspective = new Perspective({apiKey: perspective_key});

    let trumpTweetsUgly = fs.readFileSync('trump_tweets.json')
    let trumpTweetsJSON = JSON.parse(trumpTweetsUgly)

    for (let i = 0; i < trumpTweetsJSON.length; i++) {
        let tweet = trumpTweetsJSON[i]
        let sentiment_analysis = sentiment.analyze(tweet.text)
        tweet['timestamp'] = Date.parse(tweet['created_at'])/1000
        tweet['afinn_score'] = sentiment_analysis['score']
        tweet['afinn_comparative'] = sentiment_analysis['comparative']

        try{
            const perspective_analysis = await perspective.analyze(tweet.text);
            const toxicityScore = perspective_analysis.attributeScores.TOXICITY.summaryScore.value
            tweet['toxicity_score'] = toxicityScore
            console.log("Sleeping for 1 sec")
            await sleep(1000)
            console.log("Continue 1 sec")
        }catch(err){
            tweet['toxicity_score'] = 0.0
            console.log(err)
        }



    }

    fs.writeFile('trump_tweets_pretty.json', JSON.stringify(trumpTweetsJSON, null, 4), function(err){
        if(err) {
            console.log(err);
        } else {
            console.log("JSON saved to trump_tweets_pretty.json");
        }
    })


})();



