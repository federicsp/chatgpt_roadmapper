# Chatgpt Roadmapper

This FastAPI application serves as the backend for a web application designed to help users learn a new word or a concept. Users can input a word or phrase and receive a roadmap that outlines some keywords. The application utilizes the ChatGPT library to generate a list of related words and descriptions, which are then displayed to the user through a Jinja2 template. Additionally, the application supports multiple languages and can store user data in a MongoDB database.

##
![main_en](https://raw.githubusercontent.com/federicsp/chatgpt_roadmapper/master/screenshots/main_en.png)

##
![example_roadmap](https://raw.githubusercontent.com/federicsp/chatgpt_roadmapper/master/screenshots/example_roadmap.png)


# Table of Contents

- [Chatgpt Roadmapper](#chatgpt-roadmapper)
- [Table of Contents](#table-of-contents)
- [Requirements](#requirements)
- [Usage](#usage)

<!-- required -->
## Requirements

This project requires:

- Python 3.9+
- packages in `requirements.txt`


## Usage

Start the application:

1. Clone the repository
2. Install the requirements
3. Export the key into your local environment:

```bash
export OPENAI_API_KEY=<API_KEY>
```

Grab an API key from [https://platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys)

4. Run the script with `python -m main`

Then open the application in your browser at `http://localhost:8000/`.

