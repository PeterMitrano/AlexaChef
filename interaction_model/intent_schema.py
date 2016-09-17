{
    "intents": [
        {
            "intent": "StartNewRecipeIntent",
            "slots": [
                {
                    "name": "RecipeName",
                    "type": "AMAZON.LITERAL"
                }
            ]
        },
        { "intent": "SaveIntent" },
        { "intent": "IngredientsIntent" },
        { "intent": "InstructionsIntent" },
        { "intent": "AMAZON.HelpIntent" },
        { "intent": "AMAZON.NextIntent" },
        { "intent": "AMAZON.PreviousIntent" },
        { "intent": "AMAZON.RepeatIntent" },
        { "intent": "AMAZON.StartOverIntent" },
        { "intent": "AMAZON.YesIntent" },
        { "intent": "AMAZON.NoIntent" },
        {
            "intent": "RecipeNameIntent",
            "slots": [
                {
                    "name": "RecipeName",
                    "type": "AMAZON.LITERAL"
                }
            ]
        }
    ]
}
