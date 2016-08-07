schema = {
    "intents": [
        {
            "intent": "StartNewRecipeIntent",
            "slots": [
                {
                    "name": "RecipeName",
                    "type": "AMAZON.LITERAL"
                }
            ]
        }, {
            "intent": "IngredientsIntent"
        }, {
            "intent": "InstructionsIntent"
        }, {"intent": "AMAZON.HelpIntent"}, {"intent": "AMAZON.NextIntent"},
        {"intent": "AMAZON.PreviousIntent"}, {"intent": "AMAZON.RepeatIntent"},
        {"intent": "AMAZON.StartOverIntent"}, {"intent": "AMAZON.YesIntent"},
        {"intent": "AMAZON.NoIntent"}
    ]
}


def intents():
    return [intent['intent'] for intent in schema['intents']]
