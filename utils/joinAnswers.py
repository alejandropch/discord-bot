def joinAnswers(user):
  """ this function collects all questions' id with its answer """
  answers=[]

  for i in range(user.nQuestions):
      answers.append({
          "id": str(user.questions[i]["id"]),
          "answer": user.response[i]
  })
  return answers