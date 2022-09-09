def joinAnswers(form):
  answers=[]
  for i in range(form.nQuestions):
      answers.append({
          "id": str(form.questions[i]["id"]),
          "answer": form.response[i]
  })
  return answers