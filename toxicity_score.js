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

    let trumpRemarks = fs.readFileSync('trump_remarks_w_text.json')
    let trumpRemarksJSON = JSON.parse(trumpRemarks)

    for (let i = 0; i < trumpRemarksJSON.length; i++) {
        let remark = trumpRemarksJSON[i]
			
				let remark_length = remark.text.length
				remark.text = remark.text.replace("\n","")
				remark.text = remark.text.replace("\\r","")
				remark.text = remark.text.replace("\r","")
				remark.text = remark.text.replace("\\n","")
			
				console.log(remark_length)
			
				if (remark_length > 20480) {
					console.log("LONG ONE")
		
					remark_pieces = remark.text.match(/(.|[\r\n]){1,18000}/g);
					
					remark_toxicities = []
					for (let i = 0; i < remark_pieces.length; i++) {
						console.log(remark_pieces[i].length)
		        try{
		            const perspective_analysis = await perspective.analyze(remark_pieces[i])
					console.log(perspective_analysis)
		            const toxicityScore = perspective_analysis.attributeScores.TOXICITY.summaryScore.value
								remark_toxicities.push(toxicityScore)
		            console.log("Sleeping for 1 sec")
		            await sleep(1000)
		            console.log("Continue 1 sec")
		        } catch(err){
		            console.log(err)
		        }
					}
					console.log("TOXICITIES")
					console.log(remark_toxicities)
					var total = 0.0;
					for(var u = 0; u < remark_toxicities.length; u++) {
					    total += remark_toxicities[u];
					}
					var avg = total / remark_toxicities.length;
	        remark['toxicity_score'] = avg

					
				}else{
	        try{
	            const perspective_analysis = await perspective.analyze(remark.text)
									console.log(perspective_analysis)

	            const toxicityScore = perspective_analysis.attributeScores.TOXICITY.summaryScore.value

	            remark['toxicity_score'] = toxicityScore


				console.log(remark)

	            console.log("Sleeping for 1 sec")
	            await sleep(1000)
	            console.log("Continue 1 sec")
	        } catch(err){
	            console.log(err)
	        }
				}
					

    }

    fs.writeFile('trump_remarks_w_toxicity_2.json', JSON.stringify(trumpRemarksJSON, null, 4), function(err){
        if(err) {
            console.log(err);
        } else {
            console.log("JSON saved to trump_remarks_w_toxicity.json");
        }
    })


})();
