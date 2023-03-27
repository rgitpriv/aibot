IRC bot built almost entirely from gpt, that integrates with the 3.5-turbo api.

It's definitely not perfect and there is a bit of weirdness (it also has a habit of doing major code changes when you ask for simple things) but it took less than an hour.

One funny thing that is maybe a new pattern we'll see - IRC doesn't allow carriage returns or multiple paragraphs. Getting it to fix the bug was giving weird behavior like it would completely refactor the program. So as a total 'new style'hack:

    query = message[len("!ai "):].strip()

becomes

    query = "In a single paragraph" + message[len("!ai "):].strip()  # manually changed

It also constructed the dockerfile include in this repo.


Instructions:

    docker build -t openai-bot .

    podman run --env OPENAI_API_KEY="<your_api_key" openai-bot:latest --server your-servername.com --port port(int) --nickname yourbotname --channel \#your_channel
