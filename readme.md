version1

user uploads resume.pdf(not resume.txt)===>llm extracts info.json from it==>we validate the response using pydantic ==> user fills the rest of the form(add images, pick a theme) and finally the full thing is saved===>user gets to see live preview ==> user for now can download the portfolio.html
user still needs to create an account , sign in , so that we can maintain the rate limit on llm usage, we also can consider file size caps on the PDF upload, a max-pages check, and a token budget per extraction call, since resume length is unbounded and directly drives LLM cost.

version2
user can edit/delete his portfolio
user get a shareable link to his portfolio


so the models we need
- info
- projects
- certificates

in v2 
- section
- card
- specific section type sub class



