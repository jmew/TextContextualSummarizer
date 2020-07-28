import win32com.client as win32

def create_draft_email(summary_text):
    outlook = win32.Dispatch('outlook.application')

    mail = outlook.CreateItem(0)

    mail.Subject = 'Kalmiya AI Summarization Mail - Review'

    mail.HtmlBody = summary_text

    mail.Save()

    return True

if __name__ == "__main__":
    create_draft_email("hello world")