from chatbot import ask_question


print("=" * 60)
print("       NIT JALANDHAR ADMISSION CHATBOT")
print("=" * 60)

print("Ask questions about admission, fees, hostel, courses,")
print("documents, eligibility, counselling, etc.")
print("Type 'exit' to quit.")

while True:

    question = input("\nYou: ")

    if question.lower() in ["exit", "quit", "bye"]:
        print("Chatbot: Goodbye!")
        break

    if not question.strip():
        continue

    try:

        answer = ask_question(question)

        print("\nChatbot:")
        print(answer)

    except Exception as e:

        print("\nError:")
        print(e)