from fuzzywuzzy import fuzz
import os, json
from twilio_challenge_santosh.sendgrid_email_api import sendgrid_mail
from twilio_challenge_santosh.emails_list import email_list
import streamlit as st
from twilio_challenge_santosh.twilio_sms_api import send_whatsapp_sms


def fuzzy_search(word, sentence, threshold=85):
    """
    This function takes a word, a sentence, and an optional threshold as input.
    It returns True if the word is found in the sentence with a similarity score
    above the threshold (percentage).
    """
    # Split the sentence into words
    words = sentence.lower().split()
    for w in words:
        # Calculate fuzzy matching ratio (higher means more similar)
        ratio = fuzz.ratio(word.lower(), w)
        if ratio >= threshold:
            return True
    return False


def personalize(summary):

    if summary is not None or summary:
        summary = json.loads(summary)
        st.info(summary)
        try:
            keys_list = list(summary.keys())
            final_summary = ""
            if (len(keys_list)) >= 1:
                for item in summary[keys_list[0]]:
                    final_summary = final_summary + "\n" + item
                    status_code = sendgrid_mail(
                        os.environ.get("MASTER_EMAIL"),
                        f"""
                                <!DOCTYPE html>
                                <html>
                                    <head>TODAY'S MEETING SUMMARY</head>\n
                                    <body>
                                        <b>{final_summary}</b>
                                    </body>
                                </html>
                                """,
                    )
                    st.write(
                        f"""Sent mail to Srum Master: {os.environ.get("MASTER_EMAIL")}. Status:{status_code}"""
                    )

                    send_whatsapp_sms(final_summary, os.environ.get("TO_PHONE"))
            if len(keys_list) >= 2:

                for task in summary[keys_list[1]]:
                    for email in email_list:
                        isTrue = fuzzy_search(
                            list(task.values())[0].lower(), email.split("@")[0]
                        )

                        if isTrue:
                            status_code = sendgrid_mail(
                                email,
                                f"""
                                <!DOCTYPE html>
                                <html>
                                    <head>TODAY'S TASK(S) FOR YOU</head>\n
                                    <body>
                                        <b>{str(list(task.values())[1])}</b>
                                    </body>
                                </html>
                                """,
                            )
                            st.write(f"""Sent mail to:{email}. Status: {status_code}""")
                            send_whatsapp_sms(
                                str(list(task.values())[1]), os.environ.get("TO_PHONE")
                            )

            else:
                status_code = sendgrid_mail(
                    os.environ.get("MASTER_EMAIL"),
                    f"""
                            <!DOCTYPE html>
                            <html>
                                <head>TODAY'S MEETING SUMMARY</head>\n
                                <body>
                                    <b>{final_summary}</b>
                                </body>
                            </html>
                            """,
                )
                st.info(status_code)
                send_whatsapp_sms(final_summary, os.environ.get("TO_PHONE"))

        except Exception as e:
            st.info({"msg": str(e), "code": 501})
