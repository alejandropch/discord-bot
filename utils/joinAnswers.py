def joinAnswers(form):
  """ this function collects all questions' id with its answer """
  answers=[]

  for i in range(form.nQuestions):
      answers.append({
          "id": str(form.questions[i]["id"]),
          "answer": form.response[i]
  })
  return answers