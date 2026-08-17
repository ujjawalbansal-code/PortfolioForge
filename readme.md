how  would this work:

steps:
1. user inputs resume.txt

===llm step====
2. llm figures out what info it contains and suggests a list of sections the portfolio should contain , to keep it in check we also tell what pre_built sections we have(only their name and descriptions) , so it may choose some of them and also suggest new sections and descriptions based on what the resume contains


3. the list of sections is shown to user as a collection of 
checkboxes, he can uncheck any checkboxes and that section gets dropped, he could also add a new section and describe what he wants there ==> the final list of sections is passed to the llm along with resume.txt and models.py(models defining each pre_built section and a custom section class which can have cards)

===llm steps====
4. llm checks if the resume has data for all those sections and  returns a portfolio.json , which has sections nested with the info they should contain according to the models defined

5. we validate the portfolio.json against defined schemas

6. we extract number of section , this is passed as an argument to the sections generating loop, which later on appends section to the document object, this loop internally reads the type of section to be constructed and hence has mechanism to construct it , so we have a full script.js code written which takes things as an argument (which a python function parses for it)==>this file(with placeholders replaced by arguments) is sent to frontend and the live preview element which is a basic html file confined in an i frame , runs this script.js and when user clicks on the download btn whatever be the value of the content of iframe(hence the desired index.html) is downloaded as a file

so we need schemas.py(to validate req response), models.py(to define how each section looks), script.js(which is sent as response), and a download function on frontend

=====structure================================================================
skillCredProj/
├── backend/
│   ├── models.py              # Pydantic models for all section types
│   ├── section_catalog.py     # Pre-built section registry (names + descriptions)
│   ├── prompts.py             # LLM prompt templates (step 2 & step 4)
│   ├── llm_service.py         # Grok API calls, retry logic, validation
│   ├── main.py                # FastAPI app — all endpoints
│   ├── config.py              # Settings (API key, model name, debug flags)
│   └── requirements.txt       # Python dependencies
│
├── frontend/
│   ├── index.html             # App shell: upload → section picker → preview
│   ├── app.js                 # App logic: API calls, checkbox UI, iframe mgmt
│   ├── app.css                # App shell styles
│   ├── preview.html           # Minimal HTML loaded inside the iframe
│   ├── script.js              # Static portfolio renderer (reads PORTFOLIO_DATA)
│   └── styles.css             # Portfolio styles (for the generated site)
│
└── .env                       # GROQ_API_KEY (gitignored)
