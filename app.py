from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder="templets")


# Correct answers
correct_answers = {
    "1": "legitimate",
    "2": "phishing",
    "3": "report",
    "4": "verify",
    "5": "report",
    "6": "ignore",
    "7": "contact",
    "8": "official",
    "9": "ignore",
    "10": "verify"
}


# Question details and explanations
question_details = {
    "1": {
        "question": "Question 1: Normal Email",
        "options": {
            "legitimate": "Legitimate",
            "phishing": "Phishing"
        },
        "explanation": "The message contains normal appointment information and does not ask for sensitive personal details."
    },
    "2": {
        "question": "Question 2: Suspicious Email",
        "options": {
            "phishing": "Phishing",
            "legitimate": "Legitimate"
        },
        "explanation": "The email uses urgency and asks the user to verify a password through a link. These are common phishing warning signs."
    },
    "3": {
        "question": "Question 3: Suspicious Attachment",
        "options": {
            "open": "Open the attachment",
            "download": "Download it immediately",
            "report": "Avoid opening it and report the email"
        },
        "explanation": "Unknown executable attachments can contain malware. Do not open them; report the suspicious email."
    },
    "4": {
        "question": "Question 4: Fake Link",
        "options": {
            "click": "Click the link",
            "ignore": "Ignore the warning signs",
            "verify": "Visit the official bank website directly"
        },
        "explanation": "A misleading website address may lead to a fake page. Visit the bank using its official website address instead."
    },
    "5": {
        "question": "Question 5: Password Theft",
        "options": {
            "enter": "Enter my password",
            "share": "Share my password",
            "report": "Ignore and report the email"
        },
        "explanation": "Legitimate services should not ask you to share your password through suspicious emails. Ignore and report the message."
    },
    "6": {
        "question": "Question 6: Fake Prize",
        "options": {
            "pay": "Pay the fee",
            "click": "Click the provided link",
            "ignore": "Ignore and report the message"
        },
        "explanation": "Unexpected prizes that require payment may be scams. Do not pay or follow suspicious links."
    },
    "7": {
        "question": "Question 7: Fake Bank Alert",
        "options": {
            "click": "Click the link immediately",
            "reply": "Reply with my bank details",
            "contact": "Contact the bank through its official number"
        },
        "explanation": "Contact your bank using a trusted official phone number instead of following links or replying to unexpected messages."
    },
    "8": {
        "question": "Question 8: Fake Company Message",
        "options": {
            "click": "Click the offer link",
            "official": "Check the company's official website",
            "reply": "Reply with my personal details"
        },
        "explanation": "Checking the company's official website helps you verify whether the offer is real without trusting a suspicious sender."
    },
    "9": {
        "question": "Question 9: Personal Information Theft",
        "options": {
            "share": "Share my personal information",
            "ignore": "Ignore and report the message",
            "reply": "Reply and ask for more details"
        },
        "explanation": "Never share personal information with unknown senders. Ignore and report suspicious requests."
    },
    "10": {
        "question": "Question 10: Money Transfer Scam",
        "options": {
            "transfer": "Transfer the money immediately",
            "verify": "Verify the request through another trusted channel",
            "reply": "Reply to the email and send the money"
        },
        "explanation": "Urgent money transfer requests should always be verified through another trusted communication channel."
    }
}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit_quiz():

    data = request.get_json(silent=True)

    if not data or not isinstance(data.get("answers"), dict):
        return jsonify({"error": "Invalid quiz submission."}), 400

    answers = data["answers"]

    # Check that all questions are answered
    if any(str(number) not in answers for number in range(1, 11)):
        return jsonify({"error": "Please answer all questions."}), 400

    score = 0
    review = []

    for question_number, correct_answer in correct_answers.items():

        user_answer = answers.get(question_number)
        details = question_details[question_number]

        # Validate the submitted option
        if not isinstance(user_answer, str):
            return jsonify({"error": "Invalid answer for question " + question_number}), 400

        if user_answer not in details["options"]:
            return jsonify({"error": "Invalid answer for question " + question_number}), 400

        is_correct = user_answer == correct_answer

        if is_correct:
            score += 1

        review.append({
            "question": details["question"],
            "user_answer": details["options"][user_answer],
            "correct_answer": details["options"][correct_answer],
            "is_correct": is_correct,
            "explanation": details["explanation"]
        })

    percentage = int((score / 10) * 100)

    return jsonify({
        "score": score,
        "total": 10,
        "percentage": percentage,
        "review": review
    })


if __name__ == "__main__":
    app.run(debug=False)