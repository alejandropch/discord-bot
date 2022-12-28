def getQuestionsList(fields):
    """ this function creates a list with only 'id' and 'questions' attributes """
    
    questions = []
    for x in fields:
        questions.append({"id": x['id'], "question": x['question']})
    return questions
