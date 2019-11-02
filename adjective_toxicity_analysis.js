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

    let adj_file = 'clinton_adjectives.json'
    let output_file = 'clinton_adjectives_w_toxicity.json'

    let sentences = fs.readFileSync(adj_file)
    let sentencesArray = JSON.parse(sentences).sentences

    let sentencesJSON = []
    for (let j = 0; j < sentencesArray.length; j++){
        sentencesJSON.push({text: sentencesArray[j]})
    }

    for (let i = 0; i < sentencesJSON.length; i++) {
        let remark = sentencesJSON[i]

        let remark_length = remark.text.length
        remark.text = remark.text.replace("\n","")
        remark.text = remark.text.replace("\\r","")
        remark.text = remark.text.replace("\r","")
        remark.text = remark.text.replace("\\n","")

        console.log(remark_length)


        try{
            const perspective_analysis = await perspective.analyze(remark.text, {attributes: ['TOXICITY', 'INSULT','PROFANITY']})
            console.log(perspective_analysis)

            const toxicityScore = perspective_analysis.attributeScores.TOXICITY.summaryScore.value
            const insultScore = perspective_analysis.attributeScores.INSULT.summaryScore.value
            const profanityScore = perspective_analysis.attributeScores.PROFANITY.summaryScore.value

            remark['toxicity_score'] = toxicityScore
            remark['insult_score'] = insultScore
            remark['profanity_score'] = profanityScore

            console.log(remark)

            console.log("Sleeping for 1 sec")
            await sleep(1000)
            console.log("Continue 1 sec")
        } catch(err){
            console.log(err)
        }
    }

    fs.writeFile(output_file, JSON.stringify(sentencesJSON, null, 4), function(err){
        if(err) {
            console.log(err);
        } else {
            console.log("JSON saved to trump_remarks_w_toxicity.json");
        }
    })


})();
