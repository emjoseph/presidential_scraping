function sleep(ms){
    return new Promise(resolve=>{
        setTimeout(resolve,ms)
    })
}


(async () => {
    console.log("$&$&$&$&$&$&$&$&$&&$")
    console.log("$&$&$&$&$&$&$&$&$&&$")
    const fs = require('fs')
    const Sentiment = require('sentiment')
    let sentiment = new Sentiment()

    let perspective_key = ""

    const Perspective = require('perspective-api-client');
    const perspective = new Perspective({apiKey: perspective_key});

    let sentences = [
        "endless partisan american honest bipartisan good great tougher dirty lousy crazy free worse better flexible real single competent radical few exempt many religious top tough own confident false highest tiny guilty strong previous crooked big able late pro - life last blatant black much deep fake presidential willing craven other african powerful illegal tremendous major massive different wonderful new more socialist private stronger socialized same corrupt total ranking fellow baseless bad broken outstanding right sad interesting interested whole angry concerned",
        "crooked american real past fake russian sure crazy unbelievable 2nd many other productive radical same slow exact next possible secretive free transparent fair best monumental false actual unauthorized @potus rich live secret misleading public happy formal surprised anti - trump pro extreme such horrible environmental new evangelical great republican closed unprecedented political only unclassified natural mainstream more due extra economic fantastic focused serious tiny legal third disappointing okay dishonest perfect ukrainian usual disastrous huge irrational constitutional fourth last important high open late blatant rogue soviet long major enough fraudulent tough silent former smart popular hard drunk willing serial safe big unfair partisan loud clear controversial minded negative short busy striking hot incorrect entire first nervous local guilty massive ruthless illegal lucky angry dirty enraged phony wrong ukraine criminal interested good stymie second much entitled successful unpardonable disgraceful embarrassed w/ true own solemn future full breaking unable",
        "partisan most top pro ranking substantial first much same other great strong national gauged young youngest small many difficult better common greater third last broad international global aware new old prominent congressional good 13th additional presidential american complete encouraging hard necessary largest single military bigger",
        "partisan republican dispositive electoral more last weigh dramatic significant new modern biggest general strong afraid complete few innovative positive american annual full vocational democratic right serious minimum particular first small single economic bipartisan balanced congressional willing juvenile major longer several local entrenched unwilling careful chief many likely next traditional able open environmental comprehensive responsible precious worst antienvironmental long global much third tough accountable focused 21st legal conservative other such troubling clear sexual disqualifier fair great public easier low enough federal sure realistic worried older vast natural wealthier reliable latest personal free fit trustworthy dead fiscal clearer interested international whole financial grand simple bad sixth historical unbelievable various african different extreme national acceptable racist bigger hardcore little better intense angry good huge vital political important hard greatest historic jittery embarrassing lurid salacious straight sorry honest compelling non - irrational smaller bare high unfinished fine poor difficult legislative hopeful quick worthy best northwest impossible appropriate obvious lucky post moderate conciliatory worse largest possible presidential overwhelming specific unconstitutional extra constitutional only happy silly own true excellent unredacted current unique confidential closed top pre financing former active key sincerest hollow aggressive short independent anecdotal senior same welcome grateful broader lame civil impeachable aware undecided negative downward liberal tall eager basic second concerned mad supportive prominent gratified real cynical final old brave enormous plain determined perfect unpopular alternative wise essential ended informal inclined least certain 105th broad proper iraqi sad courteous behaved critical domestic productive proud healthy social sound common controversial north korean nuclear unfortunate previous private most unanimous powerless further okay normal evident maximum consecutive grave conscious strongest far passionate interdependent interesting unusual ordinary wrong ultimate live ambitious structural fast progressive"
    ]

    for (let i = 0; i < sentences.length; i++) {
        let remark = sentences[i]
        console.log(remark)

        try{
            const perspective_analysis = await perspective.analyze(remark, {attributes: ['TOXICITY', 'INSULT','PROFANITY']})
            console.log(perspective_analysis)

            const toxicityScore = perspective_analysis.attributeScores.TOXICITY.summaryScore.value
            const insultScore = perspective_analysis.attributeScores.INSULT.summaryScore.value
            const profanityScore = perspective_analysis.attributeScores.PROFANITY.summaryScore.value

            console.log(toxicityScore)
            console.log(insultScore)
            console.log(profanityScore)
            console.log("--------------")

            console.log("Sleeping for 1 sec")
            await sleep(1000)
            console.log("Continue 1 sec")
        } catch(err){
            console.log(err)
        }
    }

})();
