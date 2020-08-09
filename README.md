## Training the model

- To train the model, run the command: `cd inference && docker run  -v $(pwd):/app rasa/rasa:1.10.8-full train --domain domain.yml --data data --out models`

-
